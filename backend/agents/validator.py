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
    
    def __init__(self, mode: str, strict: bool = True, max_retries: int = 1):
        """
        Args:
            mode: 'estructurado' (JSON_A) o 'narrativa' (JSON_B)
            strict: Si True, bloquea el flujo en errores. Si False, solo advierte.
            max_retries: Número máximo de reintentos para reparar errores
        """
        if mode not in ["estructurado", "narrativa"]:
            raise ValueError("ValidatorAgent: modo inválido, usa 'estructurado' o 'narrativa'")

        self.mode = mode
        self.strict = strict
        self.max_retries = max_retries

    
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

    def sanitize_faltantes(self, data: Any) -> Tuple[Any, List[str]]:
        """
        Sanitiza valores 'faltantes' convirtiéndolos a cadenas vacías.
        Devuelve (data_sanitizada, lista_advertencias)
        """
        warnings = []
        
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if isinstance(value, str) and value.strip().lower() == "faltantes":
                    sanitized[key] = ""
                    warnings.append(f"Campo '{key}' tenía valor 'faltantes', convertido a cadena vacía")
                elif isinstance(value, (dict, list)):
                    sanitized[key], sub_warnings = self.sanitize_faltantes(value)
                    warnings.extend(sub_warnings)
                else:
                    sanitized[key] = value
            return sanitized, warnings
        elif isinstance(data, list):
            sanitized = []
            for item in data:
                if isinstance(item, str) and item.strip().lower() == "faltantes":
                    sanitized.append("")
                    warnings.append(f"Elemento de lista tenía valor 'faltantes', convertido a cadena vacía")
                elif isinstance(item, (dict, list)):
                    san_item, sub_warnings = self.sanitize_faltantes(item)
                    sanitized.append(san_item)
                    warnings.extend(sub_warnings)
                else:
                    sanitized.append(item)
            return sanitized, warnings
        else:
            return data, warnings
    
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
        
        # === Sanitización 0: Limpiar valores 'faltantes' ===
        if "json" in json_a:
            json_a["json"], sanitize_warnings = self.sanitize_faltantes(json_a["json"])
            if sanitize_warnings:
                warnings.extend([f"⚠️ Sanitización: {w}" for w in sanitize_warnings])
        
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
                        # Manejar campos anidados con notación punto (ej: "secciones_JN.objeto")
                        if '.' in field:
                            parts = field.split('.')
                            current = json_data
                            missing = False
                            
                            for i, part in enumerate(parts):
                                if isinstance(current, dict) and part in current:
                                    current = current[part]
                                else:
                                    field_path = '.'.join(parts[:i+1])
                                    errors.append(f"Campo obligatorio faltante: '{field_path}'")
                                    missing = True
                                    break
                            
                            # Verificar si el valor final está vacío o es "faltantes"
                            if not missing and (not current or current == "faltantes"):
                                warnings.append(f"Campo '{field}' está vacío o marcado como 'faltantes'")
                        else:
                            # Campo de primer nivel
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
    
    def generate_repair_prompt(self, json_data: Dict[str, Any], errors: List[str], seccion: str) -> str:
        """
        Genera un prompt de reparación para corregir errores en JSON_A.
        
        Args:
            json_data: JSON original con errores
            errors: Lista de errores detectados
            seccion: Sección del documento (ej: 'JN.1')
            
        Returns:
            Prompt de reparación para el LLM
        """
        import json
        
        # Obtener campos requeridos de la sección
        required_fields = BinderSchemas.get_section_required_fields(seccion) if seccion else []
        
        prompt = f"""Se ha generado un JSON con errores de estructura. Tu tarea es REPARARLO y devolver el JSON CORREGIDO.

JSON ORIGINAL (CON ERRORES):
```json
{json.dumps(json_data, ensure_ascii=False, indent=2)}
```

ERRORES DETECTADOS:
{chr(10).join(f"- {error}" for error in errors)}

CAMPOS REQUERIDOS PARA {seccion}:
{', '.join(required_fields)}

INSTRUCCIONES DE REPARACIÓN:
1. Mantén TODOS los datos existentes que sean válidos
2. Añade los campos faltantes con valores apropiados basados en el contexto existente
3. Para campos sin información, usa cadenas vacías "" o "Por determinar"
4. NUNCA uses "faltantes" como valor
5. Asegúrate de que la estructura sea válida según el esquema
6. Devuelve SOLO el JSON corregido, sin explicaciones adicionales

JSON CORREGIDO:"""
        
        return prompt
    
    async def auto_repair_json_a(self, json_a: Dict[str, Any], errors: List[str], seccion: str) -> Dict[str, Any]:
        """
        Intenta reparar automáticamente un JSON_A con errores usando el LLM.
        
        Args:
            json_a: JSON_A original con errores
            errors: Lista de errores detectados
            seccion: Sección del documento
            
        Returns:
            JSON_A reparado o el original si falla la reparación
        """
        try:
            from backend.core.llm_client import get_llm
            
            llm = get_llm(task_type="json_repair", temperature=0.1)
            
            # Extraer solo el campo 'json' para reparación
            json_data = json_a.get("json", {})
            
            # Generar prompt de reparación
            repair_prompt = self.generate_repair_prompt(json_data, errors, seccion)
            
            print(f"\n🔧 Intentando reparación automática de JSON_A...")
            
            # Invocar LLM para reparar
            response = await llm.ainvoke(repair_prompt)
            repaired_output = response.content
            
            # Parsear JSON reparado
            repaired_json, parse_error = OutputParser.parse_json(repaired_output, strict=False)
            
            if parse_error:
                print(f"⚠️ Error parseando JSON reparado: {parse_error}")
                return json_a  # Devolver original si falla el parsing
            
            # Actualizar el JSON_A con los datos reparados
            json_a["json"] = repaired_json
            json_a["metadata"]["repaired"] = True
            json_a["metadata"]["repair_attempt"] = True
            
            print(f"✅ JSON reparado exitosamente")
            return json_a
            
        except Exception as e:
            print(f"❌ Error durante reparación automática: {e}")
            return json_a  # Devolver original si falla la reparación
    
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
        
        Si strict=True y hay errores críticos, intenta reparación automática (si max_retries > 0).
        Si falla o no hay retries, marca el estado con 'validation_failed'.
        """
        if self.mode == "estructurado":
            json_a = state.get("json_a", {})
            seccion = state.get("seccion")
            
            # Intento inicial de validación
            result = self.validate_json_a(json_a, seccion)
            result_dict = result.to_dict()
            
            # Si hay errores y tenemos retries disponibles, intentar reparación
            if not result.is_valid and self.max_retries > 0:
                print(f"\n🔄 Validación falló, iniciando reparación automática (max_retries={self.max_retries})...")
                
                retry_count = 0
                while not result.is_valid and retry_count < self.max_retries:
                    retry_count += 1
                    print(f"\n🔧 Intento de reparación {retry_count}/{self.max_retries}...")
                    
                    # Reparar JSON_A
                    json_a = await self.auto_repair_json_a(json_a, result.errors, seccion)
                    state["json_a"] = json_a  # Actualizar estado con versión reparada
                    
                    # Re-validar
                    result = self.validate_json_a(json_a, seccion)
                    result_dict = result.to_dict()
                    
                    if result.is_valid:
                        print(f"✅ Reparación exitosa en intento {retry_count}")
                        result_dict["repaired"] = True
                        result_dict["repair_attempts"] = retry_count
                        break
                    else:
                        print(f"❌ Reparación intento {retry_count} falló, errores: {len(result.errors)}")
            
            # Actualizar estado con resultado detallado
            state["validation_a_result"] = result_dict
            state["validation_a_passed"] = result.is_valid
            
            # Si es strict y hay errores (después de todos los retries), marcar para bloquear flujo
            if self.strict and not result.is_valid:
                state["validation_failed"] = True
                state["validation_error_message"] = f"Validación JSON_A falló después de {self.max_retries} intentos: {'; '.join(result.errors)}"
            
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
