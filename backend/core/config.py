from pydantic_settings import BaseSettings
from dotenv import load_dotenv # Importar load_dotenv

load_dotenv() # Añadir esta línea para cargar las variables de entorno

class Settings(BaseSettings):
    app_name: str = "Pliegos Públicos API"
    openai_api_key: str
    groq_api_key: str
settings = Settings()