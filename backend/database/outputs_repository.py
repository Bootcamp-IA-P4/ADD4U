"""
Repositorio para gestionar la colección de salidas.
Esto garantiza que cada JSON_A y JSON_B generado se conserve con total trazabilidad.
"""

from backend.database.mongo import get_collection
from datetime import datetime
import uuid 

async def save_output(expediente_id: str, documento: str, seccion: str, nodo: str, content: dict) -> str:
    """
    Guarda un output (JSON_A o JSON_B) en la colección `outputs` con trazabilidad completa.
    """

    collection = get_collection("outputs")

    doc = {
        "output_id": str(uuid.uuid4()),  # ID único para trazabilidad
        "expediente_id": expediente_id,
        "documento": documento,
        "seccion": seccion,
        "nodo": nodo,  # "A" (estructurado) o "B" (narrativa)
        "version": content.get("version", 1),
        "hash": content.get("hash", ""),
        "hash_prev": content.get("hash_prev", ""),
        "data": content.get("data", {}),
        "narrativa": content.get("narrativa", {}),
        "citas_golden": content.get("citas_golden", []),
        "citas_normativas": content.get("citas_normativas", []),
        "dependencias": content.get("dependencias", []),
        "estado": "final",
        "timestamp": datetime.utcnow().isoformat(),
        "raw": content,
    }

    result = await collection.insert_one(doc)
    return str(result.inserted_id)
