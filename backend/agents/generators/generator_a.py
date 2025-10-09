# backend/agents/generators/generator_a.py
"""
Generator A
-----------
Genera el contenido estructurado (JSON_A) a partir del prompt A.
Este agente representa la primera fase del flujo de generación.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class GeneratorA:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.2
        )

    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "prompt_a": "...",
          "user_text": "...",
          "documento": "JN",
          "seccion": "JN.1"
        }
        """
        prompt_text = inputs.get("prompt_a") or "No se ha proporcionado prompt A"
        user_text = inputs.get("user_text", "")

        # Construcción del mensaje final
        full_prompt = f"{prompt_text}\n\nTexto del usuario:\n{user_text}"

        try:
            response = await self.llm.ainvoke(full_prompt)
            return {
                "json_a": {
                    "structured_output": response.content,
                    "metadata": {
                        "model": self.llm.model_name,
                        "section": inputs.get("seccion", ""),
                        "status": "success"
                    }
                }
            }
        except Exception as e:
            return {
                "json_a": {
                    "structured_output": None,
                    "metadata": {
                        "error": str(e),
                        "status": "failed"
                    }
                }
            }
