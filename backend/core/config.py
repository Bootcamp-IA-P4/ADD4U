from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Pliegos Públicos API"

settings = Settings()