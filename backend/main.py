from fastapi import FastAPI
from backend.api.jn_routes import router as jn_router
from backend.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jn_router)