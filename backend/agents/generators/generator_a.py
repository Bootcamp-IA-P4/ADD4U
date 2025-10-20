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
from backend.agents.generators.output_parser import OutputParser

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
            json_schema = state.get("json_schema", "")
            
            # === Construcción del prompt mejorado ===
            # Nota: El truncamiento se aplica solo si es necesario para evitar límites del modelo
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
- No incluyas ningún texto adicional, explicaciones o formato que no sea el JSON.
- No inventes datos; usa "faltantes" si la información no está presente.
- Sigue el esquema canónico del documento.
"""

            print("Full Prompt para Generator A:\n", full_prompt)
            try:
                # === Invocación al modelo ===
                response = await self.llm.ainvoke(full_prompt)
                raw_output = response.content

                # === Usar OutputParser para limpieza y parsing ===
                parsed_json, parse_error = OutputParser.parse_json(raw_output, strict=False)
                
                if parse_error:
                    print(f"⚠️ Advertencia de parsing: {parse_error}")
                    print(f"Raw output (primeros 500 chars): {raw_output[:500]}")

                # === Construcción del JSON_A según esquema del binder ===
                json_a = {
                    "expediente_id": expediente_id,
                    "documento": documento,
                    "seccion": seccion,
                    "nodo": "A",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "actor": "LLM",
                    "json": parsed_json,  # Datos específicos de la sección
                    "citas_golden": golden,
                    "citas_normativas": [],
                    "hash": f"hash_A_{seccion}_{expediente_id}",
                    # Metadatos adicionales (no del binder, pero útiles)
                    "metadata": {
                        "model": self.llm.model_name,
                        "status": "success" if not parse_error else "warning",
                        "schema_version": "1.0.0",
                    },
                    "parse_error": parse_error,
                    "dependencias": dependencias,
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
                    model_inputs={"user_text": user_text, "context": context[:500]},
                    model_output=json_a,
                )

                # === Actualización del estado ===
                state["json_a"] = json_a
                return state

            except Exception as e:
                # Manejo robusto de errores (no rompe el flujo del grafo)
                print(f"❌ Error crítico en GeneratorA: {e}")
                state["json_a"] = {
                    "expediente_id": expediente_id,
                    "documento": documento,
                    "seccion": seccion,
                    "nodo": "A",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "actor": "LLM",
                    "json": {},
                    "citas_golden": [],
                    "citas_normativas": [],
                    "metadata": {"error": str(e), "status": "failed"},
                    "parse_error": str(e),
                }
                return state
