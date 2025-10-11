"""
Generator A (instrumentado)
----------------------------
Genera el contenido estructurado (JSON_A) a partir del Prompt A.
Integra trazabilidad con LangFuse y devuelve la estructura canónica.
"""

import os
import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from backend.core.langfuse_client import observe

load_dotenv()


class GeneratorA:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.2
        )

    @observe()  # registra ejecución en LangFuse
    async def ainvoke(self, inputs: dict):
        """
        inputs esperados:
        {
          "prompt_a": "...",
          "user_text": "...",
          "documento": "JN",
          "seccion": "JN.1",
          "expediente_id": "EXP-001"
        }
        """
        prompt_text = inputs.get("prompt_a") or "No se ha proporcionado prompt A"
        user_text = inputs.get("user_text", "")
        expediente_id = inputs.get("expediente_id", "EXP-000")
        documento = inputs.get("documento", "JN")
        seccion = inputs.get("seccion", "JN.x")

        # Construcción del prompt final
        full_prompt = f"{prompt_text}\n\nTexto del usuario:\n{user_text}"

        try:
            response = await self.llm.ainvoke(full_prompt)
            structured_output = response.content

            # === Estructura JSON_A canónica ===
            json_a = {
                "schema_version": "1.0.0",
                "doc": documento,
                "seccion": seccion,
                "expediente_id": expediente_id,
                "nodo": "A",
                "version": 1,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "actor": "G",
                "proveniencia": "A(JSON) desde UI+Golden",
                "data": {"structured_output": structured_output},
                "citas_golden": [],
                "citas_normativas": [],
                "faltantes": [],
                "alertas": [],
                "dependencias": [],
                "score_local": {
                    "estructura": 0,
                    "cumplimiento": 0,
                    "narrativa": 0
                },
                "metadata": {
                    "model": self.llm.model_name,
                    "status": "success"
                }
            }

            return {"json_a": json_a}

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
