from fastapi import APIRouter, Query
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/normativa", tags=["normativa"])

# Config embeddings (HuggingFace, gratis, local)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# VectorStore conectado a Mongo Atlas
vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=os.getenv("MONGO_URI"),
    namespace="Golden.embeddings",   # DB=Golden, collection=embeddings
    embedding=embeddings,
    index_name="default"             # nombre de tu índice vectorial en Atlas
)

@router.get("/search")
async def search_normativa(q: str = Query(..., description="Pregunta del usuario"), k: int = 3):
    """
    Busca en normativa_global usando embeddings y devuelve los fragmentos más relevantes
    """
    results = vectorstore.similarity_search(q, k=k)
    return {
        "query": q,
        "results": [
            {
                "texto": doc.page_content,
                "metadata": doc.metadata
            } for doc in results
        ]
    }
