from fastapi import FastAPI
from backend.api.jn_routes import router as jn_router
from backend.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes_expedientes import router as expedientes_router
from backend.api.routes_outputs import router as outputs_router
from backend.api.routes_normativa import router as normativa_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jn_router)
app.include_router(expedientes_router)
app.include_router(outputs_router)
app.include_router(normativa_router)