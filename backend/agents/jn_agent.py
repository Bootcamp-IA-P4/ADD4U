import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any

# Importar esquemas
from backend.models.schemas_jn import UserInputJN
# Importar prompts
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template
# Importar config
from backend.core.config import settings
# Importar lógica de construcción JSON_A
from backend.core.logic_jn import build_jn_output

load_dotenv()

async def generate_justificacion_necesidad(
    user_input: UserInputJN,
    structured_llm_choice: str = "openai",
    narrative_llm_choice: str = "openai"
) -> Dict[str, Any]:
    """
    Genera la Justificación de la Necesidad en dos pasos:
    - JSON_A (estructurado, validado)
    - JSON_B (narrativa final)
    """

    # Configuración de modelos
    llm_openai = ChatOpenAI(model="gpt-5", api_key=settings.openai_api_key)
    llm_groq = ChatGroq(model="gpt-oss-120b", temperature=0, api_key=settings.groq_api_key)

    # Selección de LLMs
    structured_llm = llm_groq if structured_llm_choice == "groq" else llm_openai
    narrative_llm = llm_groq if narrative_llm_choice == "groq" else llm_openai

    # Parser para estructurado
    parser = JsonOutputParser(pydantic_object=dict)

    # --- Paso 1: Prompt A → datos estructurados ---
    structured_chain = prompt_a_template | structured_llm
    structured_output = await structured_chain.ainvoke({
        "user_input": user_input.user_text,
        "format_instructions": parser.get_format_instructions()
    })

    # Validar/normalizar con lógica interna → JSON_A
    json_a = await build_jn_output({
        "expediente_id": user_input.expediente_id,
        "seccion": user_input.seccion,
        "data_schema_json": structured_output
    })

    # --- Paso 2: Prompt B → narrativa ---
    narrative_chain = prompt_b_template | narrative_llm
    narrative_output = await narrative_chain.ainvoke({"structured_data": json_a})

    # JSON_B básico
    json_b = {
        "doc": "JN",
        "seccion": user_input.seccion,
        "expediente_id": user_input.expediente_id,
        "nodo": "B",
        "narrativa": narrative_output.content
    }

    # Devolver ambos resultados
    return {
        "json_a": json_a,
        "json_b": json_b
    }
