"""
LLM Client
-----------
Cliente centralizado para inicializar modelos LLM en Mini-CELIA.
Permite reutilizar configuración y cambiar de proveedor fácilmente.
"""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def get_llm(model_name: str = None, temperature: float = 0.2, max_tokens: int = 1500):
    """
    Devuelve una instancia configurada del modelo LLM (por defecto GPT-5).
    Todos los agentes que interactúan con LLM deben usar esta función.
    """

    model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-5")
    api_key = os.getenv("OPENAI_API_KEY")

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens
    )
