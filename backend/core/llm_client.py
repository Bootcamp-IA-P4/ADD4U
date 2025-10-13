"""
LLM Client (versión extendida y segura)
---------------------------------------
Cliente centralizado para inicializar modelos LLM en Mini-CELIA.

✔️ Usa las variables del .env existente (OpenAI, Groq).
✔️ Permite fallback automático si un proveedor falla.
✔️ Configura límites de tokens por tipo de agente (A/B).
✔️ Evita dependencias innecesarias si no hay configuración para otros LLMs.
"""

import os
from dotenv import load_dotenv

# Modelos soportados (solo si hay configuración disponible)
from langchain_openai import ChatOpenAI

try:
    from langchain_groq import ChatGroq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

load_dotenv()


def get_llm(
    provider: str = None,
    model_name: str = None,
    temperature: float = 0.2,
    max_tokens: int = None,
    task_type: str = "generic",
):
    """
    Devuelve una instancia configurada de LLM según el proveedor disponible.

    Args:
        provider: "openai" (default), "groq"
        model_name: nombre del modelo (p.ej., gpt-5, mixtral-8x7b)
        temperature: creatividad del modelo
        max_tokens: límite de tokens (puede venir del .env)
        task_type: identifica el tipo de tarea (json_a, json_b, validator…)

    Ejemplo:
        llm = get_llm(task_type="json_a", temperature=0.2)
    """

    # --- Config general ---
    provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()
    model_name = model_name or os.getenv("OPENAI_MODEL", "gpt-5")

    # --- Límite de tokens configurable por tipo de tarea ---
    default_max = {
        "json_a": int(os.getenv("MAX_TOKENS_JSON_A", "1500")),
        "json_b": int(os.getenv("MAX_TOKENS_JSON_B", "2500")),
        "validator": int(os.getenv("MAX_TOKENS_VALIDATOR", "1800")),
        "generic": int(os.getenv("MAX_TOKENS_DEFAULT", "2000")),
    }
    max_tokens = max_tokens or default_max.get(task_type, 2000)

    # --- Inicialización segura ---
    try:
        if provider == "groq" and HAS_GROQ:
            api_key = os.getenv("GROQ_API_KEY")
            model_name = model_name or os.getenv("GROQ_MODEL", "mixtral-8x7b")
            if not api_key:
                raise ValueError("Falta GROQ_API_KEY en .env")
            print(f"[LLM Client] Usando Groq model={model_name}")
            return ChatGroq(model=model_name, api_key=api_key, temperature=temperature)

        # Fallback predeterminado: OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta OPENAI_API_KEY en .env")
        print(f"[LLM Client] Usando OpenAI model={model_name}")
        return ChatOpenAI(model=model_name, api_key=api_key, temperature=temperature, max_tokens=max_tokens)

    except Exception as e:
        # Fallback automático → OpenAI si algo falla
        print(f"[LLM Client] ⚠️ Error al cargar {provider}: {e}. Usando fallback OpenAI.")
        fallback_api = os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            api_key=fallback_api,
            temperature=temperature,
            max_tokens=max_tokens,
        )
