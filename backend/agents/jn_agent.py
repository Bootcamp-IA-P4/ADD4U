import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any

# Importar los esquemas Pydantic desde backend.models
from backend.models.schemas_jn import (
    JustificacionNecesidadStructured,
    ObjetoAlcance,
    ContextoProblema,
    Objetivos,
    AlternativasConsideradas,
    TipoContratoProcedimiento,
    PresupuestoFinanciacion,
    PlazoHitos,
    RiesgosMitigacion
)

# Importar los prompts desde backend.prompts
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template

# Cargar variables de entorno
load_dotenv()

# --- Configuración de los modelos de lenguaje ---
# Asegúrate de que OPENAI_API_KEY y GROQ_API_KEY estén en tu .env
llm_openai = ChatOpenAI(model="gpt-5", temperature=0) # Puedes cambiar el modelo si lo deseas
llm_groq = ChatGroq(model="gpt-oss-120b", temperature=0) # Puedes cambiar el modelo si lo deseas

# --- Prompt A: Generador de datos estructurados ---
# Este prompt toma la información de entrada y la estructura según el esquema Pydantic.
parser_structured_jn = JsonOutputParser(pydantic_object=JustificacionNecesidadStructured)

# Las cadenas ahora se definirán dentro de la función para permitir la selección dinámica del LLM
# chain_prompt_a = prompt_a_template | llm_openai | parser_structured_jn # Eliminado de aquí
# chain_prompt_b_openai = prompt_b_template | llm_openai # Eliminado de aquí
# chain_prompt_b_groq = prompt_b_template | llm_groq # Eliminado de aquí

async def generate_justificacion_necesidad(
    user_input: Dict[str, Any],
    structured_llm_choice: str = "openai", # 'openai' o 'groq' para la estructuración
    narrative_llm_choice: str = "groq" # 'openai' o 'groq' para la narrativa
) -> Dict[str, Any]:
    """
    Genera la Justificación de la Necesidad en dos pasos:
    1. Estructura los datos de entrada (Prompt A).
    2. Genera la narrativa a partir de los datos estructurados (Prompt B).

    Args:
        user_input: Un diccionario con la información proporcionada por el usuario.
        structured_llm_choice: Elige el LLM para la generación de datos estructurados ('openai' o 'groq').
        narrative_llm_choice: Elige el LLM para la generación de la narrativa ('openai' o 'groq').

    Returns:
        Un diccionario con los datos estructurados y la narrativa generada.
    """
    # Seleccionar LLM para la estructuración
    if structured_llm_choice == "groq":
        structured_llm = llm_groq
    else: # Por defecto o si no es 'groq', usa openai
        structured_llm = llm_openai

    chain_prompt_a = prompt_a_template | structured_llm | parser_structured_jn

    # Paso 1: Generar datos estructurados (Prompt A)
    structured_data = await chain_prompt_a.ainvoke(
        {"user_input": user_input, "format_instructions": parser_structured_jn.get_format_instructions()}
    )

    # Seleccionar LLM para la narrativa
    if narrative_llm_choice == "groq":
        narrative_llm = llm_groq
    else: # Por defecto o si no es 'groq', usa openai
        narrative_llm = llm_openai

    narrative_chain = prompt_b_template | narrative_llm

    # Paso 2: Generar narrativa (Prompt B)
    narrative_output = await narrative_chain.ainvoke({"structured_data": structured_data})

    return {
        "structured_data": structured_data,
        "narrative": narrative_output.content # Acceder al contenido de la respuesta del LLM
    }