"""
ValidatorAgent (stub)
----------------------
Simula el proceso de validación de salidas (estructuradas o narrativas).
Será reemplazado por el validador real (Dev3).
"""

import json
import re
import unicodedata
from typing import Any, Dict, List, Tuple

class ValidatorAgent:
    def __init__(self, mode: str):
        if mode not in ["estructurado", "narrativa"]:
            raise ValueError("ValidatorAgent: modo inválido, usa 'estructurado' o 'narrativa'")

        self.mode = mode

    
    def normalize_text(self, text: str) -> str:
        """Limpia texto: sin tildes, minúsculas, sin signos."""
        if not isinstance(text, str):
            text = str(text)
        text = text.lower().strip()
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        return re.sub(r"[^\w\s]", "", text)

    def extract_values(self, data: Any, prefix: str = "") -> List[Tuple[str, str]]:
        """Recorre el JSON y devuelve lista [(clave_compuesta, valor_str)]."""
        values = []
        if isinstance(data, dict):
            for k, v in data.items():
                new_prefix = f"{prefix}.{k}" if prefix else k
                values.extend(self.extract_values(v, new_prefix))
        elif isinstance(data, list):
            for i, v in enumerate(data):
                new_prefix = f"{prefix}[{i}]"
                values.extend(self.extract_values(v, new_prefix))
        elif isinstance(data, (str, int, float, bool)):
            values.append((prefix, str(data)))
        return values

    
    def validate_json_a(self, json_a: Dict[str, Any]) -> Dict[str, Any]:
        if not json_a or "structured_output" not in json_a:
            return {"json_a_valid": False, "error": "json_a vacío o sin campo 'structured_output'"}

        try:
            parsed = json.loads(json_a["structured_output"])
            if not isinstance(parsed, dict):
                raise ValueError("El contenido no es un diccionario válido.")
        except Exception as e:
            return {"json_a_valid": False, "error": f"Error leyendo structured_output: {e}"}

        return {"json_a_valid": True, "message": "JSON_A validado correctamente."}

    def validate_json_b(self, json_b: Dict[str, Any], json_a: Dict[str, Any]) -> Dict[str, Any]:
        if not json_b or "narrative_output" not in json_b:
            return {"json_b_valid": False, "error": "json_b vacío o sin campo 'narrative_output'."}

        narrative = (json_b.get("narrative_output") or "").strip()
        if len(narrative) < 50:
            return {"json_b_valid": False, "error": "Narrativa demasiado corta."}

        raw = json_a.get("structured_output", "")
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            structured_str = match.group()
            try:
                structured = json.loads(structured_str)
            except Exception:
                return {"json_b_valid": False, "error": "No se pudo leer JSON_A para comparación."}
        else:
            return {"json_b_valid": False, "error": "No se pudo leer JSON_A para comparación."}

        # Normalizamos narrativa
        narrative_clean = self.normalize_text(narrative)

        # Extraer todos los valores del structured_output
        extracted = self.extract_values(structured)

        missing = []
        for key, val in extracted:
            
            if key.lower().startswith(("user_text", "texto_original", "intencion", "expediente_id", "codigo", "uuid")):
                continue

            val_clean = self.normalize_text(val)
            if len(val_clean) < 3:
                continue  # ignorar palabras muy cortas

            # Buscar valor en narrativa (sin límites de palabra)
            pattern = re.escape(val_clean)
            if not re.search(pattern, narrative_clean):
                missing.append({"field": key, "value": val})

        if missing:
            print("🔍 Valores faltantes detectados:")
            for m in missing:
                print(f"  → {m}")
            return {
                "json_b_valid": False,
                "error": f"Narrativa no coincide con {len(missing)} valores de JSON_A.",
                "missing_fields": missing,
            }

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
            if not result.get("json_b_valid"):
                state["validation_missing"] = result.get("missing_fields", [])
            return state  
