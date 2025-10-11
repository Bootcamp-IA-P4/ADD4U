"""
LangFuse Client
---------------
Cliente global para trazabilidad de ejecuciones y métricas.
Cada nodo del grafo podrá usar el decorador @observe() para registrar sus trazas.
"""

from dotenv import load_dotenv
import os
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

# Compatibilidad con versiones antiguas de LangFuse
try:
    from langfuse.decorators import observe
except ImportError:
    def observe(func=None, *_, **__):
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper

__all__ = ["langfuse", "observe"]
