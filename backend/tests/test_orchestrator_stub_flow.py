"""
Test funcional del orquestador con agentes stub.
Permite verificar el flujo completo: Retriever → Prompt → GeneratorA → ValidatorA → GeneratorB → ValidatorB.
"""

import asyncio
from backend.agents.orchestrator import build_orchestrator

async def main():
    workflow = build_orchestrator()

    input_data = {
        "expediente_id": "EXP-001",
        "documento": "JN",
        "seccion": "JN.1",
        "user_text": "Queremos montar un mercadillo con 15 puestos en la plaza del pueblo."
    }

    print("\n🔹 Ejecutando orquestador con stubs...\n")
    result = await workflow.ainvoke(input_data)
    print("Resultado final del grafo:\n")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
