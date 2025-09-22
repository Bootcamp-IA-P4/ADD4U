from fastapi import APIRouter
from backend.models.schemas_jn import ContextIn
from backend.core.logic_jn import build_jn_output

router = APIRouter(prefix="/justificacion", tags=["justificacion"])

@router.post("/de_la_necesidad")
async def justificacion_de_la_necesidad(ctx: ContextIn):
    return await build_jn_output(ctx.dict())