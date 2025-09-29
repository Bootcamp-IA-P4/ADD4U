from pydantic import BaseModel

# Modelo simplificado para la entrada de usuario
# Sirve solo para validar lo mínimo necesario desde el frontend
class UserInputJN(BaseModel):
    expediente_id: str      # Identificador del expediente
    seccion: str            # Ejemplo: "JN.1", "JN.2", etc.
    user_text: str          # Texto libre proporcionado por el usuario
