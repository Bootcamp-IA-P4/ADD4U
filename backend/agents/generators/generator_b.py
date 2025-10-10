"""
Generator B
-----------
Genera la narrativa final (JSON_B) a partir de la salida del Generator A.
Este agente convierte el contenido estructurado en un texto redactado.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class GeneratorB:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.4
        )

    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "json_a": {...},
          "prompt_b": "...",
          "user_text": "..."
        }
        """
        structured_data = inputs.get("json_a", {})
        prompt_b = inputs.get("prompt_b") or "No se ha proporcionado prompt B"

        full_prompt = (
            f"{prompt_b}\n\n"
            f"Datos estructurados previos:\n{structured_data}\n\n"
            f"Genera una narrativa formal y coherente basada en estos datos."
        )

        try:
            response = await self.llm.ainvoke(full_prompt)
            return {
                "json_b": {
                    "narrative_output": response.content,
                    "metadata": {
                        "model": self.llm.model_name,
                        "status": "success"
                    }
                }
            }
        except Exception as e:
            return {
                "json_b": {
                    "narrative_output": None,
                    "metadata": {
                        "error": str(e),
                        "status": "failed"
                    }
                }
            }
