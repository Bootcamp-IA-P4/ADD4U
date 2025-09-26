import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar las variables del .env
load_dotenv()

# Leer la URI
uri = os.getenv("MONGO_URI")

# Crear cliente global
client = MongoClient(uri)

def get_collection(name: str):
    db = client["Golden"] 
    return db[name]
