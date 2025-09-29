from fastapi import APIRouter, HTTPException
from backend.models.schemas_jn import UserInputJN
from backend.core.logic_jn import build_jn_output
from backend.agents.jn_agent import generate_justificacion_necesidad

router = APIRouter(prefix="/justificacion", tags=["justificacion"])

# Endpoint simple para probar JSON_A directamente
@router.post("/de_la_necesidad")
async def justificacion_de_la_necesidad(ctx: UserInputJN):
    """
    Genera solo el JSON_A (estructura validada) a partir de los datos del usuario.
    """
    return await build_jn_output(ctx.dict())

# Endpoint completo: JSON_A + JSON_B
@router.post("/generar_jn")
async def generar_justificacion_de_la_necesidad(request: UserInputJN):
    """
    Genera la Justificación de la Necesidad en dos fases:
    - JSON_A (estructurado, validado)
    - JSON_B (narrativa final)
    """
    try:
        result = await generate_justificacion_necesidad(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar la JN: {str(e)}")
