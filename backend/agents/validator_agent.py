"""
ValidatorAgent (stub)
----------------------
Simula el proceso de validación de salidas (estructuradas o narrativas).
Será reemplazado por el validador real (Dev3).
"""

class ValidatorAgent:
    def __init__(self, mode: str = "estructurado"):
        self.mode = mode

    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "json_a" o "json_b": datos generados previamente
        }
        """
        return {
            "validation_result": f"Validación simulada exitosa en modo {self.mode}",
            "status": "ok"
        }
