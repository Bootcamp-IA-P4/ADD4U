import asyncio
from backend.database.mongo import get_collection

async def create_indexes():
    collection = get_collection("normativa_global")

    # Índices básicos para trazabilidad e integridad
    await collection.create_index("id", unique=True)       
    await collection.create_index("hash", unique=True)     
    await collection.create_index("titulo")                

    print("✅ Índices creados para normativa_global.")

if __name__ == "__main__":
    asyncio.run(create_indexes())
