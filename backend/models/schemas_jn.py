from pydantic import BaseModel
from typing import Any, Optional

class ContextIn(BaseModel):
    expediente_id: str
    seccion: str
    slots_confirmados_json: Optional[Any] = None
    ideas_aceptadas_json: Optional[Any] = None
    bloques_golden_json: Optional[Any] = None
    citas_normativas_json: Optional[Any] = None
    locale_meta_json: Optional[Any] = None
    data_schema_json: Optional[Any] = None
    hash_prev: Optional[str] = None