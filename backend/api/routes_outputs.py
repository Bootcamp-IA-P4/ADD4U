from fastapi import APIRouter, HTTPException, Query, Body
from backend.database.mongo import get_collection
from backend.database.outputs_repository import (
    save_output,
    list_outputs,
    get_latest_output,
    update_output_state
)
from datetime import datetime

router = APIRouter(prefix="/outputs", tags=["outputs"])


@router.get("/{expediente_id}")
async def get_outputs(expediente_id: str):
    """
    Devuelve todos los outputs asociados a un expediente.
    Ledger completo: incluye todas las secciones, nodos (A/B) y versiones.
    """
    try:
        collection = get_collection("outputs")
        cursor = collection.find({"expediente_id": expediente_id}, {"_id": 0}).sort([
            ("seccion", 1),
            ("nodo", 1),
            ("timestamp", 1)
        ])
        docs = [doc async for doc in cursor]
        return {"ledger": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recuperando outputs: {str(e)}")


@router.get("/{expediente_id}/{seccion}/{nodo}")
async def get_output_by_section(expediente_id: str, seccion: str, nodo: str):
    """
    Devuelve un output específico de un expediente:
    - expediente_id: ID del expediente
    - seccion: sección del documento (ej. JN.1, JN.2, …)
    - nodo: "A" (estructurado) o "B" (narrativa)
    """
    try:
        collection = get_collection("outputs")
        doc = await collection.find_one(
            {"expediente_id": expediente_id, "seccion": seccion, "nodo": nodo},
            {"_id": 0}
        )
        if not doc:
            raise HTTPException(status_code=404, detail="Output no encontrado")
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recuperando output: {str(e)}")


@router.get("/{expediente_id}/latest")
async def get_latest_outputs(expediente_id: str):
    """
    Devuelve la última narrativa (nodo B) de cada sección de un expediente.
    Pensado para frontend: vista resumida y lista para revisión/exportación.
    """
    try:
        collection = get_collection("outputs")

        # Traer solo nodo B, ordenado por timestamp descendente
        cursor = collection.find(
            {"expediente_id": expediente_id, "nodo": "B"},
            {"_id": 0}
        ).sort("timestamp", -1)

        latest_by_section = {}
        async for doc in cursor:
            seccion = doc["seccion"]
            if seccion not in latest_by_section:
                latest_by_section[seccion] = doc["narrativa"]

        return {
            "expediente_id": expediente_id,
            "documento": "JN",
            "secciones": latest_by_section
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recuperando últimas narrativas: {str(e)}")


@router.get("/{expediente_id}/jn/assembled")
async def get_assembled_jn(expediente_id: str):
    """
    Devuelve el documento JN ensamblado a partir de las últimas narrativas (nodo B)
    de cada sección (JN.1, JN.2, ...). Es un documento vivo y se actualiza a medida
    que se van generando nuevas secciones.
    """
    try:
        collection = get_collection("outputs")

        cursor = collection.find(
            {"expediente_id": expediente_id, "documento": "JN", "nodo": "B"},
            {"_id": 0}
        ).sort("timestamp", -1)

        latest_by_section = {}
        async for doc in cursor:
            seccion = doc.get("seccion")
            if seccion not in latest_by_section:
                latest_by_section[seccion] = doc.get("narrativa")

        assembled_sections = [
            {"seccion": s, "narrativa": latest_by_section[s]}
            for s in sorted(latest_by_section.keys())
        ]

        return {
            "expediente_id": expediente_id,
            "documento": "JN",
            "assembled": assembled_sections
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ensamblando JN: {str(e)}")


@router.get("/{expediente_id}/jn/validated")
async def get_validated_jn(expediente_id: str):
    """
    Devuelve el documento JN ensamblado y validado por un agente global.
    Por ahora es un stub: se limita a devolver el ensamblado y lo guarda como nodo VALIDATED.
    En el futuro, aquí se integrará el agente revisor (coherencia, estilo, normativa).
    """
    try:
        # 1. Recuperar ensamblado
        assembled = await get_assembled_jn(expediente_id)
        text = "\n\n".join([s["narrativa"] for s in assembled["assembled"]])

        # 2. Aquí en el futuro: llamar al agente validador global
        validated_text = f"[VALIDATED STUB] {text}"

        # 3. Guardar como nodo VALIDATED
        await save_output(
            expediente_id,
            "JN",
            "VALIDATED",  # usamos esta pseudo-sección para identificar
            "VALIDATED",  # nodo especial
            {
                "narrativa": validated_text,
                "version": 1,
                "estado": "validado",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

        return {
            "expediente_id": expediente_id,
            "documento": "JN",
            "nodo": "VALIDATED",
            "narrativa": validated_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validando JN: {str(e)}")


# ============================================================
# 🚀 NUEVOS ENDPOINTS CON FUNCIONES DEL REPOSITORIO
# ============================================================

@router.get("/list")
async def listar_outputs(
    expediente_id: str | None = Query(default=None),
    documento: str | None = Query(default=None),
    seccion: str | None = Query(default=None),
    nodo: str | None = Query(default=None),
    limit: int = Query(default=100, le=500)
):
    """
    📋 Lista outputs con filtros opcionales y paginación.
    
    Parámetros:
    - expediente_id: Filtrar por expediente
    - documento: Filtrar por tipo (JN, PPT, CEC, CR)
    - seccion: Filtrar por sección (JN.1, JN.2, etc.)
    - nodo: Filtrar por nodo (A, B, VL, CN, VALIDATED)
    - limit: Máximo de resultados (default: 100, max: 500)
    """
    try:
        docs = await list_outputs(expediente_id, documento, seccion, nodo, limit)
        return {
            "count": len(docs),
            "outputs": docs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando outputs: {str(e)}")


@router.get("/latest/{expediente_id}/{documento}/{seccion}/{nodo}")
async def obtener_output_mas_reciente(
    expediente_id: str,
    documento: str,
    seccion: str,
    nodo: str
):
    """
    🔍 Obtiene el output más reciente para una combinación específica.
    
    Útil para:
    - Recuperar última versión de JSON_A o JSON_B
    - Verificar si una sección ya fue generada
    - Obtener outputs previos para dependencias
    """
    try:
        doc = await get_latest_output(expediente_id, documento, seccion, nodo)
        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró output para {expediente_id}/{documento}/{seccion}/{nodo}"
            )
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo output: {str(e)}")


@router.patch("/{output_id}/estado")
async def actualizar_estado_output(
    output_id: str,
    estado: str = Body(..., embed=True)
):
    """
    ✏️ Actualiza el estado de un output.
    
    Estados válidos:
    - draft: Borrador inicial
    - validated: Validado por agente
    - approved: Aprobado por humano
    - rejected: Rechazado
    - final: Versión final
    
    Body:
    {
        "estado": "validated"
    }
    """
    valid_states = ["draft", "validated", "approved", "rejected", "final"]
    if estado not in valid_states:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Debe ser uno de: {', '.join(valid_states)}"
        )
    
    try:
        doc = await update_output_state(output_id, estado)
        if not doc:
            raise HTTPException(status_code=404, detail="Output no encontrado")
        return {
            "success": True,
            "output_id": output_id,
            "estado": estado,
            "updated_at": doc.get("updated_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando estado: {str(e)}")
