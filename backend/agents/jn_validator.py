"""
ValidatorAgent (stub)
----------------------
Simula el proceso de validación de salidas (estructuradas o narrativas).
Será reemplazado por el validador real (Dev3).
"""

# backend/agents/jn_validator.py

import json
from typing import Dict, Any


class JNValidatorAgent:
    """
    Validador para la Justificación de la Necesidad.
    Dos modos:
      - "estructurado": valida json_a
      - "narrativa": valida json_b en coherencia con json_a
    """

    def __init__(self, mode: str):
        if mode not in ["estructurado", "narrativa"]:
            raise ValueError("JNValidatorAgent: modo inválido, usa 'estructurado' o 'narrativa'")
        self.mode = mode

    def validate_json_a(self, json_a: Dict[str, Any]) -> Dict[str, Any]:
        if not json_a or "structured_output" not in json_a:
            return {"json_a_valid": False, "error": "json_a vacío o sin campo 'structured_output'"}

        structured_str = json_a.get("structured_output")
        try:
            # Intentar interpretar como JSON interno (si el generador lo produce como texto JSON)
            parsed_inner = json.loads(structured_str)
            if not isinstance(parsed_inner, dict):
                raise ValueError("El contenido interno no es un diccionario válido.")
            fields = parsed_inner.keys()
            if "resumen" not in fields or "actividad" not in fields:
                return {"json_a_valid": False, "error": "Faltan campos clave ('resumen' o 'actividad')."}
        except Exception:
            # No es JSON interno, pero aceptamos texto libre
            if len(structured_str) < 50:
                return {"json_a_valid": False, "error": "Texto demasiado corto para un json estructurado."}

        return {"json_a_valid": True, "message": "JSON_A validado correctamente."}


    def validate_json_b(self, json_b: Dict[str, Any], json_a: Dict[str, Any]) -> Dict[str, Any]:
        if not json_b or "narrative_output" not in json_b:
            return {"json_b_valid": False, "error": "json_b vacío o sin campo 'narrative_output'."}

        narrative = json_b.get("narrative_output", "").strip()
        if len(narrative) < 50:
            return {"json_b_valid": False, "error": "Narrativa demasiado corta."}

        # Validar coherencia básica con JSON_A
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
        """
        Método compatible con LangGraph (.ainvoke)
        """
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
            return state

