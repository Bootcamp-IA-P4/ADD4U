from pydantic import BaseModel
from typing import Any, Optional

class ContextIn(BaseModel):
    #expediente_id: str
    #seccion: str
    #slots_confirmados_json: Optional[Any] = None
    #ideas_aceptadas_json: Optional[Any] = None
    #bloques_golden_json: Optional[Any] = None
    #citas_normativas_json: Optional[Any] = None
    #locale_meta_json: Optional[Any] = None
    #data_schema_json: Optional[Any] = None
    #hash_prev: Optional[str] = None
    prompt: str

class JustificacionNecesidadStructured(BaseModel):
    justificacion: str
    narrativa: str

class ObjetoAlcance(BaseModel):
    nombre: str

class ContextoProblema(BaseModel):
    descripcion: str

class Objetivos(BaseModel):
    descripcion: str

class AlternativasConsideradas(BaseModel):
    descripcion: str

class TipoContratoProcedimiento(BaseModel):
    descripcion: str

class PresupuestoFinanciacion(BaseModel):
    descripcion: str

class PlazoHitos(BaseModel):
    descripcion: str

class RiesgosMitigacion(BaseModel):
    descripcion: str