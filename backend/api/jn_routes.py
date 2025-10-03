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
    if request.rag_query:
        results = vectorstore.similarity_search(request.rag_query, k=3)
        rag_context_str = "\n\nContexto de Normativa Relevante:\n" + "\n---\n".join([doc.page_content for doc in results])

    request.user_input.rag_context = rag_context_str

    try:
        jn_output = await generate_justificacion_necesidad(
            user_input=request.user_input,
            structured_llm_choice=request.structured_llm_choice,
            narrative_llm_choice=request.narrative_llm_choice,
        )

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
