"""
PromptManager (stub)
---------------------
Simula la construcción de prompts dinámicos para los generadores A y B.
Será reemplazado por la versión real (Dev2).
"""

class PromptManager:
    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "documento": "JN",
          "seccion": "JN.1",
          "user_text": "Texto del usuario..."
        }
        """
        seccion = inputs.get("seccion", "JN.x")

        prompt_a = (
            f"Genera una representación estructurada (JSON) del texto del usuario "
            f"para la sección {seccion}, siguiendo el esquema predefinido."
        )

        prompt_b = (
            f"Redacta una versión narrativa formal y coherente para la sección {seccion}, "
            f"basada en los datos estructurados previos."
        )

        return {"prompt_a": prompt_a, "prompt_b": prompt_b}
