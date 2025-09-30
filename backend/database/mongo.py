# backend/database/mongo.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "Golden")

# Cliente global asíncrono
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

def get_collection(name: str):
    return db[name]
