import asyncio
from backend.database.mongo import get_collection

async def create_indexes():
    collection = get_collection("normativa_global")

    # hash: único → evita duplicados exactos
    await collection.create_index("hash", unique=True)

    # metadata.title: para búsquedas por título
    await collection.create_index("metadata.title")

    # id: índice normal (no único), por trazabilidad
    await collection.create_index("id")

    print("✅ Índices coherentes creados para normativa_global.")

if __name__ == "__main__":
    asyncio.run(create_indexes())
