import os
import json # Importar el módulo json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from typing import Dict, Any, Optional

# Importar los esquemas Pydantic desde backend.models
from backend.models.schemas_jn import UserRequest, ChatResponse, JustificacionNecesidadStructured

# Importar los prompts desde backend.prompts
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template
from backend.core.config import settings

# --- Configuración de los modelos de lenguaje ---
# Asegúrate de que OPENAI_API_KEY y GROQ_API_KEY estén en tu .env

# --- Prompt A: Generador de datos estructurados ---
# Este prompt toma la información de entrada y la estructura según el esquema Pydantic.
parser_structured_jn = JsonOutputParser(pydantic_object=JustificacionNecesidadStructured)

load_dotenv()

async def generate_justificacion_necesidad(
    user_input: UserRequest,
    structured_llm_choice: str = "groq", # Añadimos el selector para el LLM estructurado
    narrative_llm_choice: str = "openai", # Añadimos el selector para el LLM narrativo
) -> JustificacionNecesidadStructured:
    """
    Genera la Justificación de la Necesidad usando LLMs seleccionados por el usuario.
    Permite especificar el modelo concreto por etapa.
    """
    # Configuración de los modelos de lenguaje
    llm_openai = ChatOpenAI(model="gpt-5", api_key=settings.openai_api_key) # Usar settings.openai_api_key
    llm_groq = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=settings.groq_api_key) # Usar settings.groq_api_key

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
    structured_chain = prompt_a_template | structured_llm | parser_structured_jn
    narrative_chain = prompt_b_template | narrative_llm

    # Ejecutar las cadenas
    
    structured_output = await structured_chain.ainvoke({"user_input": user_input.user_text, "format_instructions": parser_structured_jn.get_format_instructions()})
    
    #Normalizar Pydantic
    if isinstance(structured_output, JustificacionNecesidadStructured):
        final_output = structured_output
    elif isinstance(structured_output, dict):
        final_output = JustificacionNecesidadStructured(**structured_output)
    else:
        final_output = JustificacionNecesidadStructured(justificacion=str(structured_output), narrativa="")
    
    # Ejecutar narrativa con JSON válido del estructurado
    narrative_payload = json.dumps(final_output.model_dump())
    narrative_output = await narrative_chain.ainvoke({"structured_data": narrative_payload, "user_input": user_input.user_text})

    # Asignar la narrativa al campo correspondiente
    try:
        maybe_json = json.loads (narrative_output.content)
        if isinstance(maybe_json, dict):
            final_output.narrativa = maybe_json.get("texto") or "\n\n".join(str(v) for v in maybe_json.values())
        else:
            final_output.narrativa = str (narrative_output.content)
    except Exception:
        final_output.narrativa = str (narrative_output.content)
    
    return final_output