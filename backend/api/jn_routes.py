from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
from backend.models.schemas_jn import UserRequest
from backend.core.logic_jn import build_jn_output
from backend.agents.jn_agent import generate_justificacion_necesidad

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
    structured_llm_choice: str = Field("openai", description="Elige el LLM para la generación de datos estructurados ('openai' o 'groq').")
    narrative_llm_choice: str = Field("groq", description="Elige el LLM para la generación de la narrativa ('openai' o 'groq').")
    rag_query: Optional[str] = Field(None, description="Consulta para buscar información relevante en la base de datos vectorial (RAG).")

@router.post("/de_la_necesidad")
async def justificacion_de_la_necesidad(ctx: UserRequest):
    return await build_jn_output(ctx.dict())

@router.post("/generar_jn")
async def generar_justificacion_de_la_necesidad(request: GenerateJNRequest):
    """
    Genera la Justificación de la Necesidad (JN) en formato estructurado y narrativo.
    Permite seleccionar el LLM a utilizar para cada etapa y opcionalmente usar RAG.
    """
    if request.structured_llm_choice not in ["openai", "groq"]:
        raise HTTPException(status_code=400, detail="structured_llm_choice debe ser 'openai' o 'groq'")
    if request.narrative_llm_choice not in ["openai", "groq"]:
        raise HTTPException(status_code=400, detail="narrative_llm_choice debe ser 'openai' o 'groq'")

    rag_context = ""
    if request.rag_query:
        results = vectorstore.similarity_search(request.rag_query, k=3)
        rag_context = "\n\nContexto de Normativa Relevante:\n" + "\n---\n".join([doc.page_content for doc in results])

    try:
        jn_output = await generate_justificacion_necesidad(
            user_input=request.user_input,
            structured_llm_choice=request.structured_llm_choice,
            narrative_llm_choice=request.narrative_llm_choice,
            rag_context=rag_context
        )
        return jn_output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la JN: {str(e)}")
