from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Pliegos Públicos API"
    openai_api_key: str
    groq_api_key: str
settings = Settings()