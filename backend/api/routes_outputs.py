from fastapi import APIRouter, HTTPException
from backend.database.mongo import get_collection

router = APIRouter(prefix="/outputs", tags=["outputs"])

@router.get("/{expediente_id}")
async def get_outputs(expediente_id: str):
    """
    Devuelve todos los outputs asociados a un expediente.
    Sirve como ledger completo del expediente.
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
    Devuelve un output específico (ej. JSON_A o JSON_B) de un expediente.
    - expediente_id: ID del expediente
    - seccion: sección del documento (ej. JN.1, JN.2)
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
