from pydantic import BaseModel, RootModel
from typing import Dict, Any

class UserInputJN(BaseModel):
    """
    Modelo de entrada del usuario.
    Se valida lo mínimo: expediente, sección y texto libre.
    """
    expediente_id: str
    seccion: str
    user_text: str


class StructuredJNOutput(RootModel[Dict[str, Any]]):
    """
    Modelo genérico para capturar el JSON estructurado
    devuelto por el Prompt A.
    """
    pass
