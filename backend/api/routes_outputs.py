from fastapi import APIRouter, HTTPException
from backend.database.mongo import get_collection

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

@router.get("/{expediente_id}/jn/final")
async def get_final_jn(expediente_id: str):
    """
    Devuelve el documento JN ensamblado a partir de las últimas narrativas (nodo B)
    de cada sección (JN.1, JN.2, ...). Es un documento vivo: devuelve tantas secciones
    como haya ya generadas para el expediente.
    """
    try:
        collection = get_collection("outputs")

        # Buscamos todas las narrativas (nodo B) del expediente
        cursor = collection.find(
            {"expediente_id": expediente_id, "documento": "JN", "nodo": "B"},
            {"_id": 0}
        ).sort("timestamp", -1)

        # Guardamos solo la última versión por sección
        latest_by_section = {}
        async for doc in cursor:
            seccion = doc.get("seccion")
            if seccion not in latest_by_section:  # solo la última
                latest_by_section[seccion] = doc.get("narrativa")

        # Ordenamos secciones al estilo JN.1, JN.2...
        final_sections = [
            {"seccion": s, "narrativa": latest_by_section[s]}
            for s in sorted(latest_by_section.keys())
        ]

        return {
            "expediente_id": expediente_id,
            "documento": "JN",
            "final": final_sections
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ensamblando JN final: {str(e)}")