import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any

# Importar esquemas
from backend.models.schemas_jn import UserInputJN, StructuredJNOutput
# Importar prompts
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template
# Importar config
from backend.core.config import settings
# Importar lógica de construcción JSON_A
from backend.core.logic_jn import build_jn_output

load_dotenv()

def get_llm(provider: str):
    """
    Devuelve el modelo LLM según el proveedor.
    Tiene fallback: si no hay credenciales para el elegido, usa el otro.
    """
    provider = provider.lower()

    if provider == "openai":
        if settings.openai_api_key:
            return ChatOpenAI(model="gpt-5", api_key=settings.openai_api_key)
        elif settings.groq_api_key:  # fallback
            return ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=settings.groq_api_key)

    if provider == "groq":
        if settings.groq_api_key:
            return ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=settings.groq_api_key)
        elif settings.openai_api_key:  # fallback
            return ChatOpenAI(model="gpt-5", api_key=settings.openai_api_key)

    # fallback absoluto (por si no hay ninguno configurado)
    raise ValueError("❌ No hay credenciales configuradas para OpenAI ni Groq.")


async def generate_justificacion_necesidad(
    user_input: UserInputJN,
    structured_llm_choice: str = "groq",
    narrative_llm_choice: str = "groq"
) -> Dict[str, Any]:
    """
    Genera la Justificación de la Necesidad en dos pasos:
    - JSON_A (estructurado, validado)
    - JSON_B (narrativa final)
    """

    # Seleccionar LLMs con fallback automático
    structured_llm = get_llm(structured_llm_choice)
    narrative_llm = get_llm(narrative_llm_choice)

    # Parser para estructurado (usa modelo Pydantic)
    parser = JsonOutputParser(pydantic_object=StructuredJNOutput)

    # --- Paso 1: Prompt A → datos estructurados ---
    structured_chain = prompt_a_template | structured_llm
    structured_output = await structured_chain.ainvoke({
        "user_input": user_input.user_text,
        "format_instructions": parser.get_format_instructions()
    })

    # Normalizar salida (AIMessage → str → dict)
    if hasattr(structured_output, "content"):
        structured_output = structured_output.content

    if isinstance(structured_output, str):
        try:
            structured_output = json.loads(structured_output)
        except Exception:
            structured_output = {"JN.1": {"objeto": user_input.user_text}}

    # Validar/normalizar con lógica interna → JSON_A
    json_a = await build_jn_output({
        "expediente_id": user_input.expediente_id,
        "seccion": user_input.seccion,
        "data_schema_json": structured_output
    })

    # --- Paso 2: Prompt B → narrativa ---
    narrative_chain = prompt_b_template | narrative_llm
    narrative_output = await narrative_chain.ainvoke({"structured_data": json_a})

    # Normalizar narrativa
    narrativa_texto = narrative_output.content if hasattr(narrative_output, "content") else str(narrative_output)

    # JSON_B básico
    json_b = {
        "doc": "JN",
        "seccion": user_input.seccion,
        "expediente_id": user_input.expediente_id,
        "nodo": "B",
        "narrativa": narrativa_texto
    }

    # Devolver ambos resultados
    return {
        "json_a": json_a,
        "json_b": json_b
    }
