from datetime import datetime
import hashlib
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
from backend.models.schemas_jn import UserRequest, OutputJsonA, OutputJsonB, OutputJsonBRefs
from backend.models.schemas_jn import UserRequest
from backend.core.logic_jn import build_jn_output
from backend.agents.jn_agent import generate_justificacion_necesidad
from backend.database.outputs_repository import save_output
from backend.utils.dict_utils import to_dict_safe

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
    citas_golden = []
    citas_normativas = []
    all_rag_metadata = []

    if request.rag_query:
        results = vectorstore.similarity_search(request.rag_query, k=3)
        rag_context_str = "\n\nContexto de Normativa Relevante:\n" + "\n---\n".join([doc.page_content for doc in results])

        for doc in results:
            citas_golden.append(doc.metadata.get("golden_citation", ""))
            citas_normativas.append(doc.metadata.get("normative_citation", ""))
            all_rag_metadata.append(doc.metadata)

    # Filtrar entradas vacías
    citas_golden = [c for c in citas_golden if c]
    citas_normativas = [c for c in citas_normativas if c]

    request.user_input.rag_context = rag_context_str

    try:
        jn_output = await generate_justificacion_necesidad(
            user_input=request.user_input,
            structured_llm_choice=request.structured_llm_choice,
            narrative_llm_choice=request.narrative_llm_choice,
        )

        expediente_id = request.user_input.expediente_id
        documento = "JN"

        # --- Guardado de outputs ---
        # Extraer json_a (objeto_alcance estructurado)
        json_a_dict = to_dict_safe(jn_output.objeto_alcance)
        json_a_dict.update({
            "citas_golden": citas_golden,
            "citas_normativas": citas_normativas,
            "rag_metadata": all_rag_metadata # Añadimos todos los metadatos para depuración
        })
        await save_output(
            expediente_id,
            documento,
            json_a_dict.get("seccion", request.user_input.seccion),
            "A",
            json_a_dict
        )

        # Extraer json_b (narrativa)
        json_b_dict = {
            "narrativa": jn_output.narrativa
        }
        await save_output(
            expediente_id,
            documento,
            request.user_input.seccion,
            "B",
            json_b_dict
        )

        return {
            "json_a": json_a_dict,
            "json_b": json_b_dict
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la JN: {str(e)}")
