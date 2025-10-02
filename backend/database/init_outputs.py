import asyncio
from backend.database.mongo import get_collection

async def create_indexes():
    collection = get_collection("outputs")

    await collection.create_index("output_id", unique=True)
    await collection.create_index("expediente_id")
    await collection.create_index([
        ("expediente_id", 1),
        ("documento", 1),
        ("seccion", 1),
        ("nodo", 1),
        ("version", 1)
    ])
    await collection.create_index("estado")
    await collection.create_index("timestamp")

    print("✅ Índices creados para outputs.")

if __name__ == "__main__":
    asyncio.run(create_indexes())
