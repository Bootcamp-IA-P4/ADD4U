import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables .env
load_dotenv()
uri = os.getenv("MONGO_URI")

# Crear cliente global asíncrono
client = AsyncIOMotorClient(uri)

def get_collection(name: str):
    db = client["Golden"]
    return db[name]
