"""
ValidatorAgent (Producción)
----------------------------
Validador real de salidas estructuradas y narrativas contra esquemas del binder.
- Valida estructura contra esquemas JSON Schema
- Valida coherencia semántica entre JSON_A y JSON_B
- Bloquea el flujo si hay errores críticos
- Genera reportes detallados de validación
"""

import json
import re
import unicodedata
from typing import Any, Dict, List, Tuple
from langfuse import Langfuse
from langfuse import observe
import os
from dotenv import load_dotenv
from backend.agents.schemas.json_schemas import BinderSchemas
from backend.agents.generators.output_parser import OutputParser

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)


class ValidationResult:
    """Resultado estructurado de una validación"""
    
    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None, details: Dict = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "details": self.details,
            "severity": "critical" if not self.is_valid else ("warning" if self.warnings else "ok")
        }


class ValidatorAgent:
    """
    Validador de salidas JSON_A y JSON_B.
    - Valida contra esquemas del binder
    - Verifica coherencia semántica
    - Controla calidad de los outputs
    """
    
    def __init__(self, mode: str, strict: bool = True):
        """
        Args:
            mode: 'estructurado' (JSON_A) o 'narrativa' (JSON_B)
            strict: Si True, bloquea el flujo en errores. Si False, solo advierte.
        """
        if mode not in ["estructurado", "narrativa"]:
            raise ValueError("ValidatorAgent: modo inválido, usa 'estructurado' o 'narrativa'")

        self.mode = mode
        self.strict = strict

    
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

    @observe(name="validate_json_a")
    def validate_json_a(self, json_a: Dict[str, Any], seccion: str = None) -> ValidationResult:
        """
        Valida JSON_A contra el esquema del binder.
        
        Args:
            json_a: Diccionario con la estructura JSON_A
            seccion: Sección del documento (ej: 'JN.1')
            
        Returns:
            ValidationResult con el resultado de la validación
        """
        errors = []
        warnings = []
        
        # === Validación 1: Estructura presente ===
        if not json_a:
            return ValidationResult(False, errors=["JSON_A está vacío"])
        
        # === Validación 2: Esquema básico del binder ===
        is_valid_structure, structure_errors = BinderSchemas.validate_basic_structure(json_a, "json_a")
        if not is_valid_structure:
            errors.extend(structure_errors)
        
        # === Validación 3: Campo 'json' (datos específicos) ===
        if "json" in json_a:
            json_data = json_a["json"]
            
            # Verificar que sea un diccionario
            if not isinstance(json_data, dict):
                errors.append("El campo 'json' debe ser un objeto/diccionario")
            else:
                # Validar campos requeridos de la sección
                if seccion:
                    required_fields = BinderSchemas.get_section_required_fields(seccion)
                    for field in required_fields:
                        if field not in json_data:
                            errors.append(f"Campo obligatorio faltante en 'json': '{field}'")
                        elif not json_data[field] or json_data[field] == "faltantes":
                            warnings.append(f"Campo '{field}' está vacío o marcado como 'faltantes'")
        else:
            errors.append("Falta el campo 'json' con los datos estructurados")
        
        # === Validación 4: Metadatos de calidad ===
        if "parse_error" in json_a and json_a["parse_error"]:
            warnings.append(f"Error de parsing detectado: {json_a['parse_error']}")
        
        if "alertas" in json_a and json_a["alertas"]:
            warnings.extend([f"Alerta: {alert}" for alert in json_a["alertas"]])
        
        # === Resultado final ===
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details={
                "schema_validated": True,
                "section": seccion,
                "total_errors": len(errors),
                "total_warnings": len(warnings)
            }
        )
    
    @observe(name="validate_json_b")
    def validate_json_b(self, json_b: Dict[str, Any], json_a: Dict[str, Any]) -> ValidationResult:
        """
        Valida JSON_B contra el esquema del binder y coherencia con JSON_A.
        
        Args:
            json_b: Diccionario con la estructura JSON_B
            json_a: Diccionario con JSON_A para verificar coherencia
            
        Returns:
            ValidationResult con el resultado de la validación
        """
        errors = []
        warnings = []
        
        # === Validación 1: Estructura presente ===
        if not json_b:
            return ValidationResult(False, errors=["JSON_B está vacío"])
        
        # === Validación 2: Esquema básico del binder ===
        is_valid_structure, structure_errors = BinderSchemas.validate_basic_structure(json_b, "json_b")
        if not is_valid_structure:
            errors.extend(structure_errors)
        
        # === Validación 3: Narrativa presente y con longitud mínima ===
        narrative = json_b.get("narrativa", "")
        if not narrative:
            # Intentar extraer de narrative_output (formato antiguo)
            narrative = json_b.get("narrative_output", "")
        
        if not narrative or len(narrative.strip()) < 50:
            errors.append("La narrativa debe tener al menos 50 caracteres")
        
        # === Validación 4: Coherencia semántica con JSON_A ===
        if json_a and narrative:
            coherence_result = self._validate_semantic_coherence(json_a, narrative)
            if coherence_result["missing_fields"]:
                missing_count = len(coherence_result["missing_fields"])
                if missing_count > 5:  # Si faltan más de 5 valores, es error crítico
                    errors.append(f"Falta coherencia semántica: {missing_count} valores de JSON_A no están en la narrativa")
                else:
                    warnings.append(f"Advertencia de coherencia: {missing_count} valores menores no encontrados")
                
                # Agregar detalles de campos faltantes
                for field in coherence_result["missing_fields"][:3]:  # Mostrar solo los primeros 3
                    warnings.append(f"  - Campo '{field['field']}' con valor '{field['value']}' no encontrado")
        
        # === Validación 5: Referencias a JSON_A ===
        if "refs" in json_b:
            refs = json_b["refs"]
            if not isinstance(refs, dict):
                errors.append("El campo 'refs' debe ser un objeto")
            elif "hash_json_A" not in refs:
                warnings.append("Falta la referencia 'hash_json_A' en 'refs'")
        
        # === Resultado final ===
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            details={
                "schema_validated": True,
                "narrative_length": len(narrative),
                "total_errors": len(errors),
                "total_warnings": len(warnings),
                "coherence_checked": bool(json_a)
            }
        )
    
    def _validate_semantic_coherence(self, json_a: Dict[str, Any], narrative: str) -> Dict[str, Any]:
        """
        Valida que los valores clave de JSON_A estén presentes en la narrativa.
        
        Args:
            json_a: Estructura JSON_A
            narrative: Texto narrativo del JSON_B
            
        Returns:
            Dict con campos faltantes y estadísticas
        """
        # Extraer datos estructurados
        json_data = json_a.get("json", {})
        if not json_data:
            # Intentar formato antiguo
            json_data = json_a.get("data", {})
        
        # Normalizar narrativa
        narrative_clean = self.normalize_text(narrative)
        
        # Extraer valores del JSON_A
        extracted = self.extract_values(json_data)
        
        missing = []
        for key, val in extracted:
            # Ignorar campos técnicos
            if key.lower().startswith(("user_text", "texto_original", "intencion", "expediente_id", "codigo", "uuid")):
                continue
            
            val_clean = self.normalize_text(val)
            if len(val_clean) < 3:
                continue  # Ignorar palabras muy cortas
            
            # Buscar valor en narrativa
            pattern = re.escape(val_clean)
            if not re.search(pattern, narrative_clean):
                missing.append({"field": key, "value": val})
        
        return {
            "missing_fields": missing,
            "total_checked": len(extracted),
            "coherence_score": 1.0 - (len(missing) / max(len(extracted), 1))
        }

    @observe(name="validator_ainvoke")
    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta la validación y actualiza el estado.
        
        Si strict=True y hay errores críticos, marca el estado con 'validation_failed'.
        El orquestador debe verificar este flag y detener el flujo si es necesario.
        """
        if self.mode == "estructurado":
            json_a = state.get("json_a", {})
            seccion = state.get("seccion")
            
            result = self.validate_json_a(json_a, seccion)
            result_dict = result.to_dict()
            
            # Actualizar estado con resultado detallado
            state["validation_a_result"] = result_dict
            state["validation_a_passed"] = result.is_valid
            
            # Si es strict y hay errores, marcar para bloquear flujo
            if self.strict and not result.is_valid:
                state["validation_failed"] = True
                state["validation_error_message"] = f"Validación JSON_A falló: {'; '.join(result.errors)}"
            
            print(f"\n{'✅' if result.is_valid else '❌'} Validación JSON_A: {'APROBADA' if result.is_valid else 'RECHAZADA'}")
            if result.errors:
                print(f"  🔴 Errores: {len(result.errors)}")
                for error in result.errors[:3]:
                    print(f"    - {error}")
            if result.warnings:
                print(f"  ⚠️  Advertencias: {len(result.warnings)}")
            
            return state

        elif self.mode == "narrativa":
            json_b = state.get("json_b", {})
            json_a = state.get("json_a", {})
            
            result = self.validate_json_b(json_b, json_a)
            result_dict = result.to_dict()
            
            # Actualizar estado con resultado detallado
            state["validation_b_result"] = result_dict
            state["validation_b_passed"] = result.is_valid
            
            # Si es strict y hay errores, marcar para bloquear flujo
            if self.strict and not result.is_valid:
                state["validation_failed"] = True
                state["validation_error_message"] = f"Validación JSON_B falló: {'; '.join(result.errors)}"
            
            print(f"\n{'✅' if result.is_valid else '❌'} Validación JSON_B: {'APROBADA' if result.is_valid else 'RECHAZADA'}")
            if result.errors:
                print(f"  🔴 Errores: {len(result.errors)}")
                for error in result.errors[:3]:
                    print(f"    - {error}")
            if result.warnings:
                print(f"  ⚠️  Advertencias: {len(result.warnings)}")
                for warning in result.warnings[:3]:
                    print(f"    - {warning}")
            
            return state  
