"""
Generator B (instrumentado)
----------------------------
Genera la narrativa final (JSON_B) a partir del contenido estructurado (JSON_A).
Integra evaluación local con TruLens.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from backend.core.trulens_client import register_eval

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
          "user_text": "...",
          "expediente_id": "...",
          "documento": "JN",
          "seccion": "JN.1"
        }
        """
        structured_data = inputs.get("json_a", {})
        prompt_b = inputs.get("prompt_b") or "No se ha proporcionado prompt B"
        expediente_id = inputs.get("expediente_id", "EXP-000")
        documento = inputs.get("documento", "JN")
        seccion = inputs.get("seccion", "JN.x")

        full_prompt = (
            f"{prompt_b}\n\n"
            f"Datos estructurados previos:\n{structured_data}\n\n"
            f"Genera una narrativa formal y coherente basada en estos datos."
        )

        try:
            response = await self.llm.ainvoke(full_prompt)
            narrative = response.content

            # === Evaluación básica con TruLens local ===
            metrics = {
                "coherencia": 0.9,  # placeholder (más adelante se calculará real)
                "completitud": 0.85,
                "tono": "neutral"
            }
            register_eval(
                app_name=f"{documento}-{seccion}",
                result={"expediente_id": expediente_id, "section": seccion},
                metrics=metrics
            )

            return {
                "json_b": {
                    "narrative_output": narrative,
                    "metrics": metrics,
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
