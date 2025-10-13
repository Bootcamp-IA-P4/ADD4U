"""
ValidatorAgent (stub)
----------------------
Simula el proceso de validación de salidas (estructuradas o narrativas).
Será reemplazado por el validador real (Dev3).
"""

import json
from typing import Dict, Any
# import os
# from dotenv import load_dotenv
import re

from trulens_eval import Tru, Feedback

# load_dotenv()

# open_api_key = os.environ.get("OPENAI_API_KEY")

class JNValidatorAgent:
    """
    Validador para la Justificación de la Necesidad.
    Dos modos:
      - "estructurado": valida json_a
      - "narrativa": valida json_b en coherencia con json_a + evalúa calidad con TruLens
    """

    def __init__(self, mode: str):
        if mode not in ["estructurado", "narrativa"]:
            raise ValueError("JNValidatorAgent: modo inválido, usa 'estructurado' o 'narrativa'")

        self.mode = mode

        # try:
        #     self.tru = Tru()
        #     self.f_relevance = Feedback(self.provider.relevance).on_input_output()
        #     self.f_conciseness = Feedback(self.provider.conciseness).on_output()
        #     self.f_coherence = Feedback(self.provider.coherence).on_output()
        # except Exception as e:
        #     # Fallback si TruLens no puede inicializarse
        #     self.tru = None
        #     self.provider = None
        #     self.f_relevance = None
        #     self.f_conciseness = None
        #     self.f_coherence = None
        #     print(f"⚠️ TruLens no pudo inicializarse correctamente: {e}")

    def validate_json_a(self, json_a: Dict[str, Any]) -> Dict[str, Any]:
        if not json_a or "structured_output" not in json_a:
            return {"json_a_valid": False, "error": "json_a vacío o sin campo 'structured_output'"}

        structured_str = json_a.get("structured_output")
        try:
            parsed_inner = json.loads(structured_str)
            if not isinstance(parsed_inner, dict):
                raise ValueError("El contenido interno no es un diccionario válido.")
            fields = parsed_inner.keys()
            if "resumen" not in fields or "actividad" not in fields:
                return {"json_a_valid": False, "error": "Faltan campos clave ('resumen' o 'actividad')."}
        except Exception:
            if len(structured_str) < 50:
                return {"json_a_valid": False, "error": "Texto demasiado corto para un json estructurado."}

        return {"json_a_valid": True, "message": "JSON_A validado correctamente."}

    def validate_json_b(self, json_b: Dict[str, Any], json_a: Dict[str, Any]) -> Dict[str, Any]:
        if not json_b or "narrative_output" not in json_b:
            return {"json_b_valid": False, "error": "json_b vacío o sin campo 'narrative_output'."}

        narrative = json_b.get("narrative_output", "").strip()
        if len(narrative) < 50:
            return {"json_b_valid": False, "error": "Narrativa demasiado corta."}

        # Extraer valores importantes
        try:
            structured_inner = json.loads(json_a.get("structured_output", "{}"))
            required_values = []
            for key in ["resumen", "actividad", "ubicacion", "capacidad"]:
                value = structured_inner.get(key)
                if isinstance(value, dict):
                    required_values.extend([str(v).lower() for v in value.values()])
                elif value:
                    required_values.append(str(value).lower())
        except Exception:
            return {"json_b_valid": False, "error": "No se pudo leer JSON_A para comparación."}

        # Comprobación semántica simple (ignora mayúsculas y puntuación)
        missing_values = []
        for v in required_values:
            v_clean = re.sub(r"[^\w\s]", "", v)
            if not re.search(re.escape(v_clean), re.sub(r"[^\w\s]", "", narrative)):
                missing_values.append(v)

        if missing_values:
            return {"json_b_valid": False,
                    "error": f"Narrativa no coincide con JSON_A, faltan valores: {missing_values}"}

        return {"json_b_valid": True, "message": "JSON_B validado correctamente."}

        resumen = ""
        try:
            structured_inner = json.loads(json_a.get("structured_output", "{}"))
            resumen = structured_inner.get("resumen", "")
        except Exception:
            pass

        if resumen and resumen.split()[0].lower() not in narrative.lower():
            return {"json_b_valid": False, "error": "Narrativa parece no corresponder con el resumen del JSON_A."}

        return {"json_b_valid": True, "message": "JSON_B validado correctamente."}

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if self.mode == "estructurado":
            json_a = state.get("json_a")
            result = self.validate_json_a(json_a)
            state["validation_result"] = result.get("message") if result.get("json_a_valid") else result.get("error")
            return state

        elif self.mode == "narrativa":
            json_b = state.get("json_b")
            json_a = state.get("json_a")
            result = self.validate_json_b(json_b, json_a)
            state["validation_result"] = result.get("message") if result.get("json_b_valid") else result.get("error")

            # Evaluación con TruLens (opcional)
            # try:
            #     if self.tru:  # Solo si TruLens se inicializó correctamente
            #         prompt = json_a.get("structured_output", "")
            #         response = json_b.get("narrative_output", "")
            #         self.tru.evaluate_run(
            #             input=prompt,
            #             output=response,
            #             feedbacks=[]
            #         )
            # except Exception as e:
            #     state["validation_trulens_error"] = str(e)

            return state  
