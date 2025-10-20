from fastapi import FastAPI
from backend.api.jn_routes import router as jn_router
from backend.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes_expedientes import router as expedientes_router
from backend.api.routes_outputs import router as outputs_router
from backend.api.routes_normativa import router as normativa_router
# from backend.api.routes_metrics import router as metrics_router  # Ojito: Implementar routes_metrics.py

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de salud
@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servidor está activo"""
    return {
        "status": "ok",
        "service": settings.app_name,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }

app.include_router(jn_router)
app.include_router(expedientes_router)
app.include_router(outputs_router)
app.include_router(normativa_router)
# app.include_router(metrics_router)  # Ojito: Descomentar cuando se implemente routes_metrics.py