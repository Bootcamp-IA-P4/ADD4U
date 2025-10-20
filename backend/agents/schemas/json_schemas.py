"""
JSON Schemas del Binder
-----------------------
Esquemas de validación para JSON_A y JSON_B basados en los documentos del binder.
Estos esquemas permiten validar estructuralmente las salidas de los generadores.
"""

from typing import Dict, Any, List
import json


class BinderSchemas:
    """
    Esquemas de validación del binder para Mini-CELIA.
    Basados en los ejemplos de docs/diagrams/ejemplos_json/
    """

    # === Esquema JSON_A (output estructurado) ===
    JSON_A_SCHEMA = {
        "type": "object",
        "required": ["expediente_id", "documento", "seccion", "nodo", "timestamp", "actor", "json"],
        "properties": {
            "expediente_id": {"type": "string", "pattern": "^EXP-"},
            "documento": {"type": "string", "enum": ["JN", "PPT", "PCAP", "DEUC"]},
            "seccion": {"type": "string", "pattern": "^[A-Z]+\\.\\d+"},
            "nodo": {"type": "string", "enum": ["A"]},
            "timestamp": {"type": "string", "format": "date-time"},
            "actor": {"type": "string", "enum": ["LLM", "Usuario", "Sistema"]},
            "json": {"type": "object"},  # Contenido variable por sección
            "citas_golden": {"type": "array", "items": {"type": "string"}},
            "citas_normativas": {"type": "array", "items": {"type": "string"}},
            "hash": {"type": "string"},
        },
        "additionalProperties": True  # Permite campos extras (metadata, etc.)
    }

    # === Esquema JSON_B (narrativa) ===
    JSON_B_SCHEMA = {
        "type": "object",
        "required": ["expediente_id", "documento", "seccion", "nodo", "timestamp", "actor", "narrativa", "refs"],
        "properties": {
            "expediente_id": {"type": "string", "pattern": "^EXP-"},
            "documento": {"type": "string", "enum": ["JN", "PPT", "PCAP", "DEUC"]},
            "seccion": {"type": "string", "pattern": "^[A-Z]+\\.\\d+"},
            "nodo": {"type": "string", "enum": ["B"]},
            "timestamp": {"type": "string", "format": "date-time"},
            "actor": {"type": "string", "enum": ["LLM", "Usuario", "Sistema"]},
            "narrativa": {"type": "string", "minLength": 50},
            "refs": {
                "type": "object",
                "required": ["hash_json_A"],
                "properties": {
                    "hash_json_A": {"type": "string"},
                    "citas_golden": {"type": "array", "items": {"type": "string"}},
                    "citas_normativas": {"type": "array", "items": {"type": "string"}},
                }
            },
            "hash": {"type": "string"},
        },
        "additionalProperties": True
    }

    # === Esquemas específicos por sección (JN.1 como ejemplo) ===
    JN1_DATA_SCHEMA = {
        "type": "object",
        "properties": {
            "secciones_JN": {
                "type": "object",
                "required": ["objeto", "alcance", "ambito"],
                "properties": {
                    "objeto": {"type": "string", "minLength": 1},
                    "alcance": {"type": "string"},
                    "ambito": {"type": "string"},
                }
            }
        },
        "required": ["secciones_JN"],
    }

    # Mapeo de secciones a esquemas de datos
    SECTION_SCHEMAS = {
        "JN.1": JN1_DATA_SCHEMA,
        # Aquí se agregarían JN.2, JN.3, etc. según el binder
    }

    @staticmethod
    def get_schema(schema_type: str, seccion: str = None) -> Dict[str, Any]:
        """
        Obtiene el esquema de validación apropiado.
        
        Args:
            schema_type: 'json_a' o 'json_b'
            seccion: Sección del documento (ej: 'JN.1')
            
        Returns:
            Dict: Esquema JSON Schema
        """
        if schema_type == "json_a":
            schema = BinderSchemas.JSON_A_SCHEMA.copy()
            
            # Si hay un esquema específico para la sección, lo añadimos
            if seccion and seccion in BinderSchemas.SECTION_SCHEMAS:
                schema["properties"]["json"] = BinderSchemas.SECTION_SCHEMAS[seccion]
            
            return schema
        
        elif schema_type == "json_b":
            return BinderSchemas.JSON_B_SCHEMA.copy()
        
        else:
            raise ValueError(f"Tipo de esquema desconocido: {schema_type}")

    @staticmethod
    def validate_basic_structure(data: Dict[str, Any], schema_type: str) -> tuple[bool, List[str]]:
        """
        Validación básica de estructura sin usar jsonschema (más ligera).
        
        Args:
            data: Datos a validar
            schema_type: 'json_a' o 'json_b'
            
        Returns:
            tuple[bool, List[str]]: (is_valid, errores)
        """
        schema = BinderSchemas.get_schema(schema_type)
        errors = []
        
        # Verificar campos requeridos
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                errors.append(f"Campo obligatorio faltante: '{field}'")
        
        # Verificar tipos básicos
        if schema_type == "json_a":
            if "json" in data and not isinstance(data["json"], dict):
                errors.append("El campo 'json' debe ser un objeto/diccionario")
            if "nodo" in data and data["nodo"] != "A":
                errors.append("El campo 'nodo' debe ser 'A' para JSON_A")
        
        elif schema_type == "json_b":
            if "narrativa" in data:
                if not isinstance(data["narrativa"], str):
                    errors.append("El campo 'narrativa' debe ser un string")
                elif len(data["narrativa"]) < 50:
                    errors.append("La narrativa debe tener al menos 50 caracteres")
            if "nodo" in data and data["nodo"] != "B":
                errors.append("El campo 'nodo' debe ser 'B' para JSON_B")
            if "refs" in data and not isinstance(data["refs"], dict):
                errors.append("El campo 'refs' debe ser un objeto")
        
        return len(errors) == 0, errors

    @staticmethod
    def get_section_required_fields(seccion: str) -> List[str]:
        """
        Obtiene los campos requeridos para una sección específica.
        
        Args:
            seccion: Código de sección (ej: 'JN.1')
            
        Returns:
            List[str]: Lista de campos obligatorios (incluye campos anidados con notación punto)
        """
        if seccion not in BinderSchemas.SECTION_SCHEMAS:
            return []
        
        schema = BinderSchemas.SECTION_SCHEMAS[seccion]
        required_fields = []
        
        # Función recursiva para extraer campos requeridos
        def extract_required(schema_dict: Dict, prefix: str = ""):
            # Campos requeridos en este nivel
            for field in schema_dict.get("required", []):
                full_field = f"{prefix}.{field}" if prefix else field
                required_fields.append(full_field)
                
                # Si el campo tiene propiedades anidadas, explorarlas
                if "properties" in schema_dict and field in schema_dict["properties"]:
                    nested_schema = schema_dict["properties"][field]
                    if isinstance(nested_schema, dict) and "properties" in nested_schema:
                        extract_required(nested_schema, full_field)
        
        extract_required(schema)
        return required_fields
