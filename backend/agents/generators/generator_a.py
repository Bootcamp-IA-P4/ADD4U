"""
Generator A 
----------------------------
Genera el contenido estructurado (JSON_A) a partir del Prompt A.
Integra trazabilidad LangFuse y evaluación TruLens.
Listo para uso directo o como nodo LangGraph (.as_node()).
"""

import os
import json
import datetime
from dotenv import load_dotenv
from backend.core.llm_client import get_llm
from backend.core.trulens_client import register_eval
from backend.core.langfuse_client import langfuse

load_dotenv()


class GeneratorA:
    """
    Generador del JSON_A (estructura de datos canónica)
    Entrada: prompt_a + user_text (+ contexto Golden y dependencias)
    Salida: state actualizado con json_a
    """

    def __init__(self):
        # El modelo se carga desde llm_client con configuración global
        self.llm = get_llm(task_type="json_a", temperature=0.2)

    async def ainvoke(self, state: dict):
        """
        Espera:
        {
          "prompt_a": "...",
          "user_text": "...",
          "documento": "JN",
          "seccion": "JN.1",
          "expediente_id": "EXP-001",
          "context": "...",              # opcional
          "citas_golden": [...],         # opcional
          "dependencias_previas": [...]  # opcional
        }
        """

        with langfuse.start_as_current_span(name="generator_a"):
            prompt_a = state.get("prompt_a", "")
            user_text = state.get("user_text", "")
            context = state.get("context", "")
            golden = state.get("citas_golden", [])
            dependencias = state.get("dependencias_previas", [])
            expediente_id = state.get("expediente_id", "EXP-000")
            documento = state.get("documento", "JN")
            seccion = state.get("seccion", "JN.x")

            # === Construcción del prompt mejorado ===
            full_prompt = f"""
{prompt_a}

[DATOS DEL USUARIO]
{user_text}

[CONTEXTO NORMATIVO]
{context or "Sin contexto disponible."}

[REFERENCIAS GOLDEN]
{json.dumps(golden, ensure_ascii=False, indent=2)}

[DEPENDENCIAS PREVIAS]
{json.dumps(dependencias, ensure_ascii=False, indent=2)}

[INSTRUCCIONES]
- Devuelve SOLO un objeto JSON válido UTF-8.
- No inventes datos; usa "faltantes" si la información no está presente.
- Sigue el esquema canónico del documento.
"""

            try:
                # === Invocación al modelo ===
                response = await self.llm.ainvoke(full_prompt)
                structured_output = response.content

                # === Intento de parsear el JSON ===
                try:
                    parsed_json = json.loads(structured_output)
                    parse_error = None
                except json.JSONDecodeError as e:
                    parsed_json = {"structured_output": structured_output}
                    parse_error = str(e)

                # === Construcción del JSON_A canónico ===
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
                    "data": parsed_json,
                    "faltantes": [],
                    "alertas": [parse_error] if parse_error else [],
                    "citas_golden": golden,
                    "dependencias": dependencias,
                    "score_local": {"estructura": 0, "cumplimiento": 0, "narrativa": 0},
                    "metadata": {
                        "model": self.llm.model_name,
                        "status": "success" if not parse_error else "warning"
                    },
                }

                # === Registro de la evaluación (TruLens) ===
                register_eval(
                    app_name=f"{documento}-{seccion}",
                    result={
                        "expediente_id": expediente_id,
                        "documento": documento,
                        "seccion": seccion,
                        "modo": "json_a",
                        "model": self.llm.model_name,
                    },
                    metrics=None,
                    app_version="json_a",
                    prompt=full_prompt,
                    model_inputs={"user_text": user_text},
                    model_output=structured_output,
                )

                # === Actualización del estado ===
                state["json_a"] = json_a
                return state

            except Exception as e:
                # Manejo robusto de errores (no rompe el flujo del grafo)
                state["json_a"] = {
                    "data": None,
                    "metadata": {"error": str(e), "status": "failed"}
                }
                return state
