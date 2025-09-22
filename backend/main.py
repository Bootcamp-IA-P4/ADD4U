from fastapi import FastAPI
from backend.api.routes_jn import router as jn_router
from backend.core.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(jn_router)