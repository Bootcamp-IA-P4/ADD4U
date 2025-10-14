import asyncio
from backend.agents.retriever_agent import RetrieverAgent

async def test_retriever_agent_connection():
    """
    Test funcional para comprobar que el RetrieverAgent:
    1. Se conecta correctamente a MongoDB Atlas.
    2. Genera embeddings del texto.
    3. Devuelve resultados del índice vectorial.
    """

    agent = RetrieverAgent()

    # Texto de prueba (puedes cambiarlo según el contenido de tu colección)
    query = {
        "documento": "JN",
        "seccion": "JN.1",
        "user_text": "Necesito saber qué normativa regula la presentación electrónica de ofertas",
    }

    print("🔍 Ejecutando consulta de prueba...")
    result = await agent.ainvoke(query)

    assert result["status"] in ["ok", "no_results"], "El agente no devolvió un estado válido"

    if result["status"] == "ok":
        print(f"✅ Recuperadas {len(result['matches'])} coincidencias")
        for match in result["matches"]:
            print(f"- {match.get('title', 'Sin título')} (score: {match.get('score'):.4f})")
        print("\nContexto (resumen):")
        print(result["context"][:400], "...")
    else:
        print("⚠️ No se encontraron resultados relevantes. Revisa el índice o los embeddings.")

    print("🧩 Test completado.")

if __name__ == "__main__":
    asyncio.run(test_retriever_agent_connection())
