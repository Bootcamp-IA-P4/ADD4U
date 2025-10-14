from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
doc = client["Golden"]["embeddings"].find_one({}, {"_id": 0})
print(doc)
