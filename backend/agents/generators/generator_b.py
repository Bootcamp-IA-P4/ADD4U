"""
Generator B (versión final)
----------------------------
Genera la narrativa final (JSON_B) a partir del contenido estructurado (JSON_A).
Integra evaluación TruLens y trazabilidad LangFuse.
Listo para uso directo o como nodo LangGraph (.as_node()).
"""

import os
import json
import datetime
from dotenv import load_dotenv
from backend.core.llm_client import get_llm
from backend.core.trulens_client import register_eval
from backend.core.trulens_metrics import compute_basic_metrics
from backend.core.langfuse_client import langfuse
from backend.agents.generators.output_parser import OutputParser

load_dotenv()


class GeneratorB:
    """
    Generador de la narrativa (JSON_B)
    Entrada: prompt_b + json_a + user_text
    Salida: state actualizado con json_b
    """

    def __init__(self):
        # Configuramos el modelo para tareas narrativas (mayor longitud)
        self.llm = get_llm(task_type="json_b", temperature=0.3)

    async def ainvoke(self, state: dict):
        """
        Espera:
        {
          "json_a": {...},
          "prompt_b": "...",
          "user_text": "...",
          "expediente_id": "...",
          "documento": "JN",
          "seccion": "JN.1"
        }
        """

        with langfuse.start_as_current_span(name="generator_b"):
            structured_data = state.get("json_a", {})
            prompt_b = state.get("prompt_b", "")
            user_text = state.get("user_text", "")
            expediente_id = state.get("expediente_id", "EXP-000")
            documento = state.get("documento", "JN")
            seccion = state.get("seccion", "JN.x")
            
            # Convertir structured_data a string para el prompt
            structured_data_str = json.dumps(structured_data, ensure_ascii=False, indent=2)
            
            # Advertir si es muy largo (pero no truncar automáticamente)
            if len(structured_data_str) > 3000:
                print(f"⚠️ Advertencia: JSON_A tiene {len(structured_data_str)} caracteres (puede afectar calidad)")

            # === Construcción del prompt narrativo ===
            full_prompt = f"""
{prompt_b}

[DATOS ESTRUCTURADOS VALIDADOS]
{structured_data_str}

[INSTRUCCIONES]
Redacta una narrativa formal, coherente y completa basada en los datos estructurados.
- Usa párrafos breves y oraciones claras.
- Mantén un tono administrativo neutro.
- No inventes información no presente en los datos.
- Devuelve SOLO el texto narrativo, sin formato JSON ni explicaciones adicionales.
"""

            try:
                # === Invocar al modelo ===
                response = await self.llm.ainvoke(full_prompt)
                raw_output = response.content

                # === Extraer narrativa usando OutputParser ===
                # El modelo puede devolver JSON o texto plano
                parsed_output, parse_error = OutputParser.parse_json(raw_output, strict=False)
                
                if parse_error:
                    # Si no es JSON válido, asumir que es texto narrativo directo
                    narrative_output = raw_output.strip()
                else:
                    # Si es JSON, extraer el campo narrativo
                    narrative_output = OutputParser.extract_narrative_text(parsed_output)

                # === Calcular métricas de evaluación ===
                metrics = compute_basic_metrics(structured_data, narrative_output)

                # === Construcción del JSON_B según esquema del binder ===
                json_a_hash = structured_data.get("hash", f"hash_A_{seccion}_{expediente_id}")
                
                json_b = {
                    "expediente_id": expediente_id,
                    "documento": documento,
                    "seccion": seccion,
                    "nodo": "B",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "actor": "LLM",
                    "narrativa": narrative_output,
                    "refs": {
                        "hash_json_A": json_a_hash,
                        "citas_golden": structured_data.get("citas_golden", []),
                        "citas_normativas": structured_data.get("citas_normativas", []),
                    },
                    "hash": f"hash_B_{seccion}_{expediente_id}",
                    # Metadatos adicionales
                    "metadata": {
                        "model": self.llm.model_name,
                        "status": "success",
                        "narrative_length": len(narrative_output),
                        "metrics": metrics,
                    },
                }

                # === Registro de evaluación en TruLens ===
                register_eval(
                    app_name=f"{documento}-{seccion}",
                    result={
                        "expediente_id": expediente_id,
                        "documento": documento,
                        "seccion": seccion,
                        "modo": "json_b",
                        "model": self.llm.model_name,
                    },
                    metrics=metrics,
                    app_version="json_b",
                    prompt=full_prompt,
                    model_inputs={"json_a": structured_data, "user_text": user_text},
                    model_output={"narrativa": narrative_output},
                )

                # === Actualizar estado global ===
                state["json_b"] = json_b
                return state

            except Exception as e:
                print(f"❌ Error crítico en GeneratorB: {e}")
                state["json_b"] = {
                    "expediente_id": expediente_id,
                    "documento": documento,
                    "seccion": seccion,
                    "nodo": "B",
                    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                    "actor": "LLM",
                    "narrativa": "",
                    "refs": {"hash_json_A": "", "citas_golden": [], "citas_normativas": []},
                    "metadata": {"error": str(e), "status": "failed"}
                }
                return state
