"""
RetrieverAgent (RAG)
----------------------
Recupera contexto normativo y fragmentos relacionados desde MongoDB Atlas
utilizando búsqueda vectorial (embeddings).
"""

import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "Golden")
COLLECTION_NAME = os.getenv("EMBEDDINGS_COLLECTION", "embeddings")

# Modelo de embeddings (mismo usado para indexar)
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

class RetrieverAgent:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.collection = self.client[DB_NAME][COLLECTION_NAME]

    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "documento": "JN",
          "seccion": "JN.1",
          "user_text": "Texto del usuario..."
        }
        """
        query_text = inputs.get("user_text", "")
        if not query_text:
            return {"context": "", "status": "error", "msg": "No user_text provided"}

        # Generar embedding del texto del usuario
        query_embedding = self.model.encode(query_text).tolist()

        # Búsqueda vectorial en MongoDB Atlas
        INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "default")

        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "numCandidates": 150,
                    "limit": 5,
                    "index": INDEX_NAME
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "title": 1,
                    "source": 1,
                    "page": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }


            }
        ]


        results = await self.collection.aggregate(pipeline).to_list(length=5)
        if not results:
            return {"context": "", "status": "no_results"}

        # Construir el contexto concatenado
        context = "\n\n".join([r.get("text", "") for r in results])
        return {
            "context": context,
            "matches": results,
            "status": "ok"
        }

# Prueba manual (opcional)
if __name__ == "__main__":
    async def test():
        agent = RetrieverAgent()
        res = await agent.ainvoke({
            "documento": "JN",
            "seccion": "JN.1",
            "user_text": "principios de contratación pública"
        })
        print(res["status"], len(res["context"].split()))
        for r in res["matches"]:
            print(r["titulo"], r["score"])

    asyncio.run(test())
