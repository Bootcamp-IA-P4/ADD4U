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


async def list_outputs(
    expediente_id: str | None = None,
    documento: str | None = None,
    seccion: str | None = None,
    nodo: str | None = None,
    limit: int = 100
):
    """
    Lista outputs con filtros opcionales.
    
    Args:
        expediente_id: Filtro por expediente
        documento: Filtro por tipo de documento (JN, PPT, etc.)
        seccion: Filtro por sección (JN.1, JN.2, etc.)
        nodo: Filtro por nodo (A, B, VL, CN)
        limit: Máximo de resultados
        
    Returns:
        Lista de outputs ordenados por timestamp descendente
    """
    collection = get_collection("outputs")
    query: dict[str, object] = {}
    
    if expediente_id:
        query["expediente_id"] = expediente_id
    if documento:
        query["documento"] = documento
    if seccion:
        query["seccion"] = seccion
    if nodo:
        query["nodo"] = nodo
    
    cursor = collection.find(query).sort("timestamp", -1).limit(limit)
    return [doc async for doc in cursor]


async def get_latest_output(
    expediente_id: str,
    documento: str,
    seccion: str,
    nodo: str
):
    """
    Obtiene el output más reciente para una combinación específica.
    
    Args:
        expediente_id: ID del expediente
        documento: Tipo de documento
        seccion: Sección
        nodo: Nodo (A o B)
        
    Returns:
        Documento más reciente o None
    """
    collection = get_collection("outputs")
    doc = await collection.find_one(
        {
            "expediente_id": expediente_id,
            "documento": documento,
            "seccion": seccion,
            "nodo": nodo,
        },
        sort=[("timestamp", -1)],
    )
    return doc


async def update_output_state(output_id: str, estado: str):
    """
    Actualiza el estado de un output.
    
    Args:
        output_id: ID único del output
        estado: Nuevo estado (draft, validated, approved, rejected)
        
    Returns:
        Documento actualizado
    """
    collection = get_collection("outputs")
    await collection.update_one(
        {"output_id": output_id},
        {"$set": {"estado": estado, "updated_at": datetime.utcnow().isoformat()}}
    )
    return await collection.find_one({"output_id": output_id})
