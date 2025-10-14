import asyncio
from backend.agents.validator import ValidatorAgent


async def test_validator_flow():
    json_a = {
        "structured_output": """{
            "seccion": "JN.1",
            "user_text": "Montaje de mercadillo con 15 puestos en la plaza del pueblo",
            "objeto": {"tipo": "mercadillo"},
            "alcance": {"lugar": "plaza del pueblo"},
            "ambito": {"puestos": 15}
        }""",
        "metadata": {"status": "success"}
    }

    json_b = {
        "narrative_output": "En el marco de la sección JN.1 se propone la instalación de un juego en la plaza del pueblo, compuesto por un total de 15 puestos. La actuación contempla el montaje de la infraestructura necesaria en dicho espacio público.",
        "metadata": {"status": "success"}
    }

    validator_a = ValidatorAgent(mode="estructurado")
    validator_b = ValidatorAgent(mode="narrativa")

    state = {"json_a": json_a, "json_b": json_b}

    result_a = await validator_a.ainvoke(state)
    print("🔹 Resultado Validator A:", result_a["validation_result"])

    result_b = await validator_b.ainvoke(result_a)
    print("🔹 Resultado Validator B:", result_b["validation_result"])


if __name__ == "__main__":
    asyncio.run(test_validator_flow())