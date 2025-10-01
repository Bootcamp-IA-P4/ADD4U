from fastapi import APIRouter
from backend.database.mongo import get_collection

router = APIRouter(prefix="/outputs", tags=["outputs"])

@router.post("/")
async def create_output(doc: dict):
    collection = get_collection("outputs")
    result = await collection.insert_one(doc)
    return {"inserted_id": str(result.inserted_id)}

@router.get("/{expediente_id}")
async def get_outputs(expediente_id: str):
    collection = get_collection("outputs")
    docs_cursor = collection.find({"expediente_id": expediente_id}, {"_id": 0})
    docs = [doc async for doc in docs_cursor]
    return {"data": docs}
