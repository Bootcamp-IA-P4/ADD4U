import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any

# Importar los esquemas Pydantic desde backend.models
from backend.models.schemas_jn import (
    ContextIn,
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
from backend.core.config import settings

# --- Configuración de los modelos de lenguaje ---
# Asegúrate de que OPENAI_API_KEY y GROQ_API_KEY estén en tu .env

# --- Prompt A: Generador de datos estructurados ---
# Este prompt toma la información de entrada y la estructura según el esquema Pydantic.
parser_structured_jn = JsonOutputParser(pydantic_object=JustificacionNecesidadStructured)

async def generate_justificacion_necesidad(
    user_input: ContextIn,
    structured_llm_choice: str = "openai", # Añadimos el selector para el LLM estructurado
    narrative_llm_choice: str = "openai"  # Añadimos el selector para el LLM narrativo
) -> JustificacionNecesidadStructured:
    # Configuración de los modelos de lenguaje
    llm_openai = ChatOpenAI(model="gpt-5", api_key=settings.openai_api_key) # Usar settings.openai_api_key
    llm_groq = ChatGroq(model="gpt-oss-120b", temperature=0, api_key=settings.groq_api_key) # Usar settings.groq_api_key

    # Seleccionar el LLM para la generación estructurada
    if structured_llm_choice == "groq":
        structured_llm = llm_groq
    else:
        structured_llm = llm_openai

    # Seleccionar el LLM para la generación narrativa
    if narrative_llm_choice == "groq":
        narrative_llm = llm_groq
    else:
        narrative_llm = llm_openai

    # Definir las cadenas con los LLMs seleccionados
    structured_chain = structured_data_prompt | structured_llm.with_structured_output(JustificacionNecesidadStructured)
    narrative_chain = narrative_prompt | narrative_llm

    # Ejecutar las cadenas
    structured_output = await structured_chain.ainvoke({"context": user_input.context})
    narrative_output = await narrative_chain.ainvoke({"structured_data": structured_output.json(), "context": user_input.context})

    # Asignar la narrativa al campo correspondiente
    structured_output.narrativa = narrative_output.content

    return structured_output