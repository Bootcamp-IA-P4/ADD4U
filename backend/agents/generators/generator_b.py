"""
Generator B (versión final)
----------------------------
Genera la narrativa final (JSON_B) a partir del contenido estructurado (JSON_A).
Integra evaluación TruLens y trazabilidad LangFuse.
Listo para uso directo o como nodo LangGraph (.as_node()).
"""

import os
import json
import re
from dotenv import load_dotenv
from backend.core.llm_client import get_llm
from backend.core.trulens_client import register_eval
from backend.core.trulens_metrics import compute_basic_metrics
from backend.core.langfuse_client import langfuse

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

    def _clean_json_response(self, raw_text: str) -> str:
        """
        Limpia respuestas LLM que contengan JSON con markdown o texto adicional
        """
        # Quitar bloques markdown
        text = re.sub(r'```json\s*', '', raw_text)
        text = re.sub(r'```\s*', '', text)
        
        # Buscar primer { hasta último }
        start = text.find('{')
        end = text.rfind('}')
        
        if start == -1 or end == -1:
            # Si no encuentra JSON, devolver el texto original
            return raw_text
        
        return text[start:end+1].strip()

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
            
            # Limitar tamaño de structured_data a 2000 caracteres para evitar prompts excesivos
            structured_data_str = json.dumps(structured_data, ensure_ascii=False, indent=2)
            if len(structured_data_str) > 2000:
                structured_data_str = structured_data_str[:2000] + "\n...[datos truncados por longitud]"

            # === Construcción avanzada del prompt narrativo ===
            full_prompt = f"""
{prompt_b}

[DATOS ESTRUCTURADOS VALIDADOS]
{structured_data_str}

[OBJETIVO]
Redacta una narrativa formal y coherente basada en los datos estructurados.
Mantén tono administrativo neutro, evitando repeticiones y sin añadir información no presente.

[ESTILO]
- Usa párrafos breves y oraciones claras.
- No repitas texto literal del JSON_A.
- No incluyas explicaciones externas ni comentarios.
- Devuelve SOLO el objeto JSON final (JSON_B) con la clave narrativa.
"""

            try:
                # === Invocar al modelo ===
                response = await self.llm.ainvoke(full_prompt)
                narrative_output = response.content

                # === Limpiar respuesta antes de parsear ===
                cleaned_output = self._clean_json_response(narrative_output)

                # === Calcular métricas de evaluación ===
                metrics = compute_basic_metrics(structured_data, cleaned_output)

                # === Construcción del JSON_B final ===
                json_b = {
                    "schema_version": "1.0.0",
                    "doc": documento,
                    "seccion": seccion,
                    "expediente_id": expediente_id,
                    "nodo": "B",
                    "version": 1,
                    "actor": "G",
                    "proveniencia": "B(narrativa) desde JSON_A validado",
                    "narrative_output": narrative_output,
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
                    model_output={"narrative_output": narrative_output},
                )

                # === Actualizar estado global ===
                state["json_b"] = json_b
                return state

            except Exception as e:
                state["json_b"] = {
                    "narrativa": None,
                    "metadata": {"error": str(e), "status": "failed"}
                }
                return state
