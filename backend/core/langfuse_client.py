"""
LangFuse Client
---------------
Cliente global para trazabilidad de ejecuciones y métricas.
Cada nodo del grafo podrá usar el decorador @observe() para registrar sus trazas.
"""

from langfuse import Langfuse
import os

from dotenv import load_dotenv
load_dotenv()

# Inicializa cliente global
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

# Decorador rápido para registrar funciones asíncronas
from langfuse.decorators import observe

__all__ = ["langfuse", "observe"]
