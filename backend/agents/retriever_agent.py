"""
RetrieverAgent (RAG)
----------------------
Recupera contexto normativo desde MongoDB Atlas usando búsqueda vectorial.
Devuelve contexto listo para prompts + metadatos (título, fuente, página, score).
Config vía .env
"""

import os
import asyncio
from typing import Dict, Any, List

from motor.motor_asyncio import AsyncIOMotorClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# --- Entorno / Config ---
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "Golden")
COLLECTION_NAME = os.getenv("EMBEDDINGS_COLLECTION", "embeddings")
INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "default")
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# límites (tuneables sin tocar código)
VSEARCH_NUM_CANDIDATES = int(os.getenv("VSEARCH_NUM_CANDIDATES", "150"))
VSEARCH_LIMIT = int(os.getenv("VSEARCH_LIMIT", "5"))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "4000"))  # recorta payload

class RetrieverAgent:
    def __init__(self):
        if not MONGO_URI:
            raise RuntimeError("MONGO_URI no está definido en .env")
        self.model = SentenceTransformer(MODEL_NAME)
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.collection = self.client[DB_NAME][COLLECTION_NAME]

    async def ainvoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
            query_text = (inputs or {}).get("user_text", "").strip()
            if not query_text:
                return {"status": "error", "msg": "user_text vacío", "context": ""}

            def build_pipeline(limit, num_candidates):
                return [
                    {
                        "$vectorSearch": {
                            "queryVector": query_embedding,
                            "path": "embedding",
                            "numCandidates": num_candidates,
                            "limit": limit,
                            "index": INDEX_NAME,
                        }
                    },
                    {
                        "$project": {
                                "_id": 0,
                                "text": 1,
                                "title": {
                                    "$ifNull": [
                                        "$title",
                                        "$metadata.title"
                                    ]
                                },
                                "source": {
                                    "$ifNull": [
                                        "$source",
                                        "$metadata.source"
                                    ]
                                },
                                "page": {
                                    "$ifNull": [
                                        "$page",
                                        "$metadata.page"
                                    ]
                                },
                                "score": {"$meta": "vectorSearchScore"},
                            }

                    },
                ]

            try:
                # --- Paso 1: embedding de la consulta ---
                query_embedding = self.model.encode(query_text).tolist()

                # --- Paso 2: primer intento ---
                limit = VSEARCH_LIMIT
                num_candidates = VSEARCH_NUM_CANDIDATES
                results = await self.collection.aggregate(
                    build_pipeline(limit, num_candidates)
                ).to_list(length=limit)

                # --- Paso 3: calibración automática ---
                # Si no hay resultados o todos los textos son muy cortos, ampliamos el rango
                if not results or sum(len(r.get("text", "")) for r in results) < 500:
                    num_candidates = int(num_candidates * 1.5)
                    limit = min(limit + 2, 10)
                    results = await self.collection.aggregate(
                        build_pipeline(limit, num_candidates)
                    ).to_list(length=limit)

                if not results:
                    return {"status": "no_results", "context": "", "matches": [], "query": query_text}

                # --- Paso 4: construir contexto legible ---
                chunks = []
                acc = 0
                for r in results:
                    t = (r.get("text") or "").strip()
                    if not t:
                        continue
                    if acc + len(t) + 2 > MAX_CONTEXT_CHARS:
                        remaining = max(0, MAX_CONTEXT_CHARS - acc - 3)
                        if remaining > 0:
                            chunks.append(t[:remaining] + "…")
                        break
                    chunks.append(t)
                    acc += len(t) + 2

                context = "\n\n".join(chunks)

                # --- Paso 5: metadatos / citas ---
                citations = [
                    {
                        "title": r.get("title") or "Sin título",
                        "source": r.get("source"),
                        "page": r.get("page"),
                        "score": r.get("score"),
                    }
                    for r in results
                ]

                # --- Paso 6: logging amigable ---
                print(f"[Retriever] {len(results)} resultados — promedio de score: "
                    f"{sum(c['score'] for c in citations)/len(citations):.3f} "
                    f"| numCandidates={num_candidates} limit={limit}")

                return {
                    "status": "ok",
                    "query": query_text,
                    "context": context,
                    "matches": citations,
                    "debug": {
                        "num_candidates": num_candidates,
                        "limit": limit,
                        "max_context_chars": MAX_CONTEXT_CHARS,
                        "index": INDEX_NAME,
                        "model": MODEL_NAME,
                    },
                }

            except Exception as e:
                return {
                    "status": "error",
                    "msg": f"Retriever falló: {type(e).__name__}: {e}",
                    "context": "",
                }


# Prueba manual local (opcional)
if __name__ == "__main__":
    async def _test():
        agent = RetrieverAgent()
        res = await agent.ainvoke({
            "documento": "JN",
            "seccion": "JN.1",
            "user_text": "Queremos montar un mercadillo con 15 puestos en la plaza del pueblo."
        })
        print(res["status"])
        if res["status"] == "ok":
            print(len(res["context"]))
            for m in res["matches"]:
                print(m)
        else:
            print(res.get("msg"))
    asyncio.run(_test())
