import asyncio
from backend.database.mongo import get_collection

async def create_indexes():
    collection = get_collection("expedientes")

    # Índices básicos
    await collection.create_index("expediente_id")
    await collection.create_index([
        ("expediente_id", 1),
        ("documento", 1),
        ("seccion", 1),
        ("nodo", 1)
    ])
    await collection.create_index("hash", unique=True)
    await collection.create_index("timestamp")

    # Índices (control de versiones + texto)
    await collection.create_index("documento")
    await collection.create_index("estado")
    await collection.create_index([
        ("expediente_id", 1),
        ("documento", 1),
        ("seccion", 1),
        ("version", 1)
    ])
    await collection.create_index([("texto_completo", "text")])

    print("✅ Índices creados para expedientes")

if __name__ == "__main__":
    asyncio.run(create_indexes())
