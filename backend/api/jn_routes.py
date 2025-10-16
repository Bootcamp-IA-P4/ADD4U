from datetime import datetime
import hashlib
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
from backend.models.schemas_jn import UserRequest, OutputJsonA, OutputJsonB, OutputJsonBRefs
from backend.models.schemas_jn import UserRequest
from backend.core.logic_jn import build_jn_output
from backend.agents.orchestrator import build_orchestrator, OrchestratorState
from backend.database.outputs_repository import save_output
from backend.utils.dict_utils import to_dict_safe
from backend.core.llm_client import get_llm

# Importaciones para RAG
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
import os

load_dotenv()

# Config embeddings (HuggingFace, gratis, local)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# VectorStore conectado a Mongo Atlas
vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=os.getenv("MONGO_URI"),
    namespace="Golden.embeddings",   # DB=Golden, collection=embeddings
    embedding=embeddings,
    index_name="default"             # nombre de tu índice vectorial en Atlas
)

router = APIRouter(prefix="/justificacion", tags=["justificacion"])

# Modelo de entrada para la API
class GenerateJNRequest(BaseModel):
    user_input: UserRequest = Field(..., description="Datos de entrada proporcionados por el usuario para generar la JN.")
    structured_llm_choice: str = Field("groq", description="Elige el LLM para la generación de datos estructurados ('openai' o 'groq').")
    narrative_llm_choice: str = Field("openai", description="Elige el LLM para la generación de la narrativa ('openai' o 'groq').")
    rag_query: Optional[str] = Field(None, description="Consulta para buscar información relevante en la base de datos vectorial (RAG).")

@router.post("/de_la_necesidad")
async def justificacion_de_la_necesidad(ctx: UserRequest):
    return await build_jn_output(ctx.dict())


@router.post("/generar_jn")
async def generar_justificacion_de_la_necesidad(request: GenerateJNRequest):
    """
    Genera la Justificación de la Necesidad (JN) en formato estructurado y narrativo.
    Permite seleccionar el LLM a utilizar para cada etapa y opcionalmente usar RAG.
    Genera la Justificación de la Necesidad (JN).
    Guarda siempre el resultado en la colección outputs,
    aunque no venga separado en json_a / json_b todavía.
    """
    if request.structured_llm_choice not in ["openai", "groq"]:
        raise HTTPException(status_code=400, detail="structured_llm_choice debe ser 'openai' o 'groq'")
    if request.narrative_llm_choice not in ["openai", "groq"]:
        raise HTTPException(status_code=400, detail="narrative_llm_choice debe ser 'openai' o 'groq'")

    rag_context_str = ""
    if request.rag_query:
        results = vectorstore.similarity_search(request.rag_query, k=3)
        rag_context_str = "\n\nContexto de Normativa Relevante:\n" + "\n---\n".join([doc.page_content for doc in results])

    # Inicializar el orquestador
    orchestrator_graph = build_orchestrator()

    # Preparar el estado inicial para el orquestador
    initial_state = OrchestratorState(
        expediente_id=request.user_input.expediente_id,
        documento="JN", # Asumimos que siempre es JN para este endpoint
        seccion=request.user_input.seccion,
        user_text=request.user_input.user_text,
        rag_results=[{"content": rag_context_str, "type": "rag"}] if rag_context_str else [],
        # Otros campos se irán rellenando a medida que el grafo avance
    )

    try:
        # Ejecutar el orquestador
        final_state = await orchestrator_graph.ainvoke(initial_state)

        jn_output = {}
        if "json_a" in final_state:
            jn_output["json_a"] = final_state["json_a"]
        if "json_b" in final_state:
            jn_output["json_b"] = final_state["json_b"]

        expediente_id = request.user_input.expediente_id
        documento = "JN"

        # --- Guardado flexible ---
        if "json_a" in jn_output:
            json_a_dict = to_dict_safe(jn_output["json_a"])
            await save_output(
                expediente_id,
                documento,
                json_a_dict.get("seccion", request.user_input.seccion),
                "A",
                json_a_dict
            )

        if "json_b" in jn_output:
            json_b_dict = to_dict_safe(jn_output["json_b"])
            await save_output(
                expediente_id,
                documento,
                json_b_dict.get("seccion", request.user_input.seccion),
                "B",
                json_b_dict
            )

        # fallback → si no está dividido
        if "json_a" not in jn_output and "json_b" not in jn_output:
            jn_output_dict = to_dict_safe(jn_output)
            await save_output(
                expediente_id,
                documento,
                request.user_input.seccion,
                "B",
                jn_output_dict
            )

        return jn_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la JN: {str(e)}")


# ============================================================
# 🚀 NUEVO ENDPOINT CON ORQUESTADOR LANGGRAPH
# ============================================================

class GenerateJNOrchestratedRequest(BaseModel):
    """Request para generar sección JN con orquestador LangGraph"""
    expediente_id: str = Field(..., description="ID del expediente")
    documento: str = Field(default="JN", description="Tipo de documento (JN, PPT, CEC, CR)")
    seccion: str = Field(..., description="Sección a generar (JN.1, JN.2, JN.3, etc.)")
    user_text: str = Field(..., description="Texto de entrada del usuario")


@router.post("/generar_jn_orquestado")
async def generar_jn_con_orquestador(request: GenerateJNOrchestratedRequest):
    """
    🎯 Genera una sección JN usando el orquestador LangGraph completo.
    
    Flujo:
    1. Retriever → Busca contexto RAG (normativa + golden)
    2. PromptRefiner → Refina instrucciones de la sección
    3. PromptManager → Construye prompts A y B dinámicamente
    4. GeneratorA → Genera JSON estructurado (JSON_A)
    5. ValidatorA → Valida estructura y reglas
    6. GeneratorB → Genera narrativa administrativa (JSON_B)
    7. ValidatorB → Valida coherencia narrativa
    8. Save → Guarda en MongoDB con trazabilidad
    
    Todo el flujo está instrumentado con LangFuse para observabilidad.
    """
    try:
        # Construir orquestador
        orchestrator = build_orchestrator(debug_mode=False)
        
        # Estado inicial
        initial_state = {
            "expediente_id": request.expediente_id,
            "documento": request.documento,
            "seccion": request.seccion,
            "user_text": request.user_text
        }
        
        # Ejecutar grafo
        final_state = await orchestrator.ainvoke(initial_state)
        
        # Respuesta
        return {
            "success": True,
            "expediente_id": request.expediente_id,
            "seccion": request.seccion,
            "json_a": final_state.get("json_a"),
            "json_b": final_state.get("json_b"),
            "validation_result": final_state.get("validation_result"),
            "rag_results_count": len(final_state.get("rag_results", [])),
            "message": f"Sección {request.seccion} generada exitosamente con orquestador LangGraph"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en orquestador: {str(e)}"
        )
