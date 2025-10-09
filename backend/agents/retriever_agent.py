"""
RetrieverAgent (stub)
----------------------
Simula la recuperación de contexto normativo desde la base de datos o embeddings.
Será reemplazado por el agente RAG real (Dev4).
"""

class RetrieverAgent:
    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "documento": "JN",
          "seccion": "JN.1",
          "user_text": "Texto del usuario..."
        }
        """
        return {
            "context": (
                "Contexto normativo simulado: Ley 9/2017 de Contratos del Sector Público, "
                "Artículo 28 — Principios generales."
            ),
            "status": "ok"
        }
