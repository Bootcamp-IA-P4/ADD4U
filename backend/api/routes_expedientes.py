# backend/api/routes_expedientes.py
from fastapi import APIRouter, Query
from backend.database.mongo import get_collection

router = APIRouter(prefix="/expedientes", tags=["expedientes"])

# Insertar documento de prueba
@router.post("/")
async def create_expediente(doc: dict):
    collection = get_collection("expedientes")
    result = await collection.insert_one(doc)
    total = await collection.count_documents({})
    return {
        "inserted_id": str(result.inserted_id),
        "total_docs_in_collection": total
    }

# Obtener todos los documentos de un expediente
@router.get("/{expediente_id}")
async def get_expediente(expediente_id: str):
    collection = get_collection("expedientes")
    cursor = collection.find({"expediente_id": expediente_id}, {"_id": 0})
    docs = await cursor.to_list(length=1000)  
    return {"data": docs}

# 🔍 Buscar texto libre en campo texto_completo
@router.get("/search/")
async def search_expedientes(q: str = Query(..., description="Palabra a buscar en texto_completo")):
    collection = get_collection("expedientes")
    cursor = collection.find(
        {"$text": {"$search": q}},
        {"_id": 0, "expediente_id": 1, "documento": 1, "seccion": 1, "texto_completo": 1}
    )
    docs = await cursor.to_list(length=100)
    return {"results": docs}
