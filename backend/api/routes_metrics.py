"""
Routes para métricas de observabilidad (LangFuse + TruLens)
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
from backend.core.langfuse_client import langfuse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/")
async def get_metrics(
    expediente_id: Optional[str] = Query(default=None, description="Filtrar por expediente"),
    days: int = Query(default=7, description="Días hacia atrás", le=90)
):
    """
    📊 Obtiene métricas de observabilidad desde LangFuse.
    
    Métricas incluidas:
    - Coste total y promedio por trace
    - Tiempo de ejecución promedio
    - Tasa de errores
    - Agentes que fallaron
    - Número de ejecuciones
    
    Parámetros:
    - expediente_id: Filtrar métricas por expediente específico
    - days: Rango de días a consultar (default: 7, max: 90)
    """
    try:
        # Calcular rango de fechas
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Construir filtros
        filters = {
            "from_timestamp": start_date.isoformat(),
            "to_timestamp": end_date.isoformat()
        }
        
        if expediente_id:
            filters["tags"] = [f"expediente:{expediente_id}"]
        
        # Consultar traces de LangFuse
        traces = langfuse.get_traces(**filters)
        
        # Calcular métricas
        total_traces = len(traces.data) if hasattr(traces, 'data') else 0
        total_cost = 0
        total_duration = 0
        error_count = 0
        failed_agents = []
        
        if hasattr(traces, 'data') and traces.data:
            for trace in traces.data:
                # Coste
                if hasattr(trace, 'cost') and trace.cost:
                    total_cost += trace.cost
                
                # Duración (en segundos)
                if hasattr(trace, 'duration') and trace.duration:
                    total_duration += trace.duration / 1000  # convertir ms a segundos
                
                # Errores
                if hasattr(trace, 'status') and trace.status == 'ERROR':
                    error_count += 1
                    
                    # Identificar agente que falló
                    if hasattr(trace, 'name'):
                        failed_agents.append({
                            "agent": trace.name,
                            "trace_id": trace.id,
                            "timestamp": trace.timestamp.isoformat() if hasattr(trace, 'timestamp') else None
                        })
        
        # Calcular promedios
        avg_cost = total_cost / total_traces if total_traces > 0 else 0
        avg_duration = total_duration / total_traces if total_traces > 0 else 0
        error_rate = (error_count / total_traces * 100) if total_traces > 0 else 0
        
        return {
            "periodo": {
                "desde": start_date.isoformat(),
                "hasta": end_date.isoformat(),
                "dias": days
            },
            "filtros": {
                "expediente_id": expediente_id
            },
            "metricas": {
                "total_ejecuciones": total_traces,
                "coste": {
                    "total_usd": round(total_cost, 4),
                    "promedio_usd": round(avg_cost, 4),
                    "moneda": "USD"
                },
                "tiempo": {
                    "promedio_segundos": round(avg_duration, 2),
                    "total_segundos": round(total_duration, 2)
                },
                "errores": {
                    "total": error_count,
                    "tasa_porcentaje": round(error_rate, 2)
                },
                "agentes_fallidos": failed_agents[:10]  # Primeros 10
            },
            "langfuse_dashboard_url": f"https://cloud.langfuse.com/project/{langfuse.project_id}/traces" if hasattr(langfuse, 'project_id') else None
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo métricas de LangFuse: {str(e)}"
        )


@router.get("/trace/{trace_id}")
async def get_trace_details(trace_id: str):
    """
    🔍 Obtiene detalles de un trace específico de LangFuse.
    
    Útil para:
    - Debugging de errores
    - Ver flujo completo de un expediente
    - Analizar costes por nodo
    """
    try:
        trace = langfuse.get_trace(trace_id)
        
        if not trace:
            raise HTTPException(status_code=404, detail="Trace no encontrado")
        
        return {
            "trace_id": trace.id,
            "name": trace.name if hasattr(trace, 'name') else None,
            "timestamp": trace.timestamp.isoformat() if hasattr(trace, 'timestamp') else None,
            "duration_ms": trace.duration if hasattr(trace, 'duration') else None,
            "cost_usd": trace.cost if hasattr(trace, 'cost') else None,
            "status": trace.status if hasattr(trace, 'status') else None,
            "metadata": trace.metadata if hasattr(trace, 'metadata') else {},
            "tags": trace.tags if hasattr(trace, 'tags') else [],
            "langfuse_url": f"https://cloud.langfuse.com/trace/{trace_id}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo detalles del trace: {str(e)}"
        )


@router.get("/quality")
async def get_quality_metrics(
    expediente_id: Optional[str] = Query(default=None)
):
    """
    📈 Obtiene métricas de calidad (TruLens - Opcional).
    
    Métricas de calidad semántica:
    - Relevancia de respuestas
    - Coherencia narrativa
    - Groundedness (basado en fuentes)
    - Toxicidad / bias
    
    ⚠️ Requiere integración TruLens (opcional para Sprint 1)
    """
    return {
        "status": "not_implemented",
        "message": "Métricas de calidad TruLens pendientes de implementación",
        "expediente_id": expediente_id,
        "nota": "Esta funcionalidad es opcional y se implementará en Sprints futuros"
    }
