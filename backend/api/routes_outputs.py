from fastapi import APIRouter, HTTPException
from backend.database.mongo import get_collection
from backend.database.outputs_repository import save_output
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
