from pydantic import BaseModel, RootModel, Field
from typing import Dict, Any, Optional, List

class UserRequest(BaseModel):
    expediente_id: str
    seccion: str
    user_text: str

class ObjetoAlcance(BaseModel):
    objeto: str = Field(description="Descripción del objeto o servicio a contratar.")
    alcance: str = Field(description="Alcance del objeto o servicio, incluyendo cantidades, plazos, etc.")
    ambito: str = Field(description="Ámbito geográfico o funcional de la contratación.")
"""
class ContextoProblema(BaseModel):
    problema_actual: str = Field(description="Descripción del problema o necesidad actual que se busca resolver.")
    impacto_problema: str = Field(description="Impacto del problema en la organización o en los usuarios.")

class Objetivos(BaseModel):
    objetivo_general: str = Field(description="Objetivo general que se busca lograr con la contratación.")
    objetivos_especificos: List[str] = Field(description="Lista de objetivos específicos que contribuyen al objetivo general.")

class AlternativasConsideradas(BaseModel):
    alternativas: List[str] = Field(description="Descripción de las alternativas consideradas para resolver el problema.")
    justificacion_seleccion: str = Field(description="Justificación de por qué la alternativa seleccionada es la más adecuada.")
"""
class JustificacionNecesidadStructured(BaseModel):
    objeto_alcance: ObjetoAlcance
    """
    contexto_problema: ContextoProblema
    objetivos: Objetivos
    alternativas_consideradas: AlternativasConsideradas
    """
    narrativa: Optional[str] = Field(None, description="Narrativa generada de la justificación de necesidad.")

class ChatResponse(RootModel[Dict[str, Any]]):
    """
    Respuesta en JSON del modelo con la Justificación de Necesidad.
    """
    pass

class OutputJsonA(BaseModel):
    expediente_id: str
    documento: str = "JN"
    seccion: str
    nodo: str = "A"
    timestamp: str
    actor: str = "LLM"
    secciones_JN: ObjetoAlcance
    citas_golden: List[str] = []
    citas_normativas: List[str] = []
    hash: str

class OutputJsonBRefs(BaseModel):
    hash_json_A: str
    citas_golden: List[str] = []
    citas_normativas: List[str] = []

class OutputJsonB(BaseModel):
    expediente_id: str
    documento: str = "JN"
    seccion: str
    nodo: str = "B"
    timestamp: str
    actor: str = "LLM"
    narrativa: str
    refs: OutputJsonBRefs
    hash: str
