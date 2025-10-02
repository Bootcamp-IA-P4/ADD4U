from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
from backend.models.schemas_jn import UserRequest, OutputJsonA, OutputJsonB, OutputJsonBRefs
from backend.core.logic_jn import build_jn_output
from backend.agents.jn_agent import generate_justificacion_necesidad
from datetime import datetime
import hashlib

router = APIRouter(prefix="/justificacion", tags=["justificacion"])

# Modelo de entrada para la API
class GenerateJNRequest(BaseModel):
    user_input: UserRequest = Field(..., description="Datos de entrada proporcionados por el usuario para generar la JN.")
    structured_llm_choice: str = Field("openai", description="Elige el LLM para la generación de datos estructurados ('openai' o 'groq').")
    narrative_llm_choice: str = Field("groq", description="Elige el LLM para la generación de la narrativa ('openai' o 'groq').")

@router.post("/de_la_necesidad")
async def justificacion_de_la_necesidad(ctx: UserRequest):
    return await build_jn_output(ctx.dict())

@router.post("/generar_jn", response_model=Dict[str, Any])
async def generar_justificacion_de_la_necesidad(request: GenerateJNRequest):
    """
    Genera la Justificación de la Necesidad (JN) en formato estructurado y narrativo.
    Permite seleccionar el LLM a utilizar para cada etapa.
    """
    if request.structured_llm_choice not in ["openai", "groq"]:
        raise HTTPException(status_code=400, detail="structured_llm_choice debe ser 'openai' o 'groq'")
    if request.narrative_llm_choice not in ["openai", "groq"]:
        raise HTTPException(status_code=400, detail="narrative_llm_choice debe ser 'openai' o 'groq'")

    try:
        jn_output = await generate_justificacion_necesidad(
            user_input=request.user_input,
            structured_llm_choice=request.structured_llm_choice,
            narrative_llm_choice=request.narrative_llm_choice,
        )

        # Generar timestamp y hash
        current_timestamp = datetime.now().isoformat(timespec='seconds') + 'Z'
        hash_a = hashlib.sha256(jn_output.model_dump_json().encode('utf-8')).hexdigest()
        hash_b = hashlib.sha256(jn_output.narrativa.encode('utf-8')).hexdigest()

        # Crear OutputJsonA
        output_a = OutputJsonA(
            expediente_id=request.user_input.expediente_id,
            seccion=request.user_input.seccion,
            timestamp=current_timestamp,
            secciones_JN=jn_output.objeto_alcance,
            hash=hash_a
        )

        # Crear OutputJsonB
        output_b_refs = OutputJsonBRefs(
            hash_json_A=hash_a,
            citas_golden=[], # Aquí puedes añadir lógica para citas golden si las tienes
            citas_normativas=[] # Aquí puedes añadir lógica para citas normativas si las tienes
        )
        output_b = OutputJsonB(
            expediente_id=request.user_input.expediente_id,
            seccion=request.user_input.seccion,
            timestamp=current_timestamp,
            narrativa=jn_output.narrativa,
            refs=output_b_refs,
            hash=hash_b
        )

        return {"output_jsonA": output_a.model_dump(), "output_jsonB": output_b.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la JN: {str(e)}")
