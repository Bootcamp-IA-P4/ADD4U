"""
OutputParser
------------
Responsable de la limpieza, parsing y validación de formato de las salidas de los LLMs.
Separación clara de responsabilidades: los generadores generan, el parser limpia y parsea.
"""

import json
import re
from typing import Any, Dict, Optional, Tuple


class OutputParser:
    """
    Parser centralizado para procesar respuestas de modelos LLM.
    - Limpia respuestas contaminadas (markdown, comentarios, prefijos)
    - Parsea JSON de forma robusta
    - Trunca textos largos de manera inteligente
    - Valida formato básico de JSON
    """

    @staticmethod
    def clean_json_response(raw_output: str) -> str:
        """
        Limpia la salida del LLM eliminando:
        - Bloques de código markdown (```json, ```)
        - Comentarios y explicaciones antes/después del JSON
        - Espacios en blanco innecesarios
        
        Args:
            raw_output: Respuesta cruda del modelo
            
        Returns:
            str: JSON limpio listo para parsear
        """
        if not raw_output:
            return "{}"
        
        # Eliminar bloques de markdown
        cleaned = raw_output.replace("```json", "").replace("```", "").strip()
        
        # Buscar el primer { y el último } para extraer solo el JSON
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            cleaned = match.group()
        
        return cleaned.strip()

    @staticmethod
    def parse_json(raw_output: str, strict: bool = False) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Parsea JSON de forma robusta con limpieza automática.
        
        Args:
            raw_output: Respuesta del modelo (puede estar contaminada)
            strict: Si True, falla en errores de parsing. Si False, retorna estructura mínima.
            
        Returns:
            Tuple[Optional[Dict], Optional[str]]: (parsed_json, error_message)
        """
        try:
            cleaned = OutputParser.clean_json_response(raw_output)
            parsed = json.loads(cleaned)
            
            if not isinstance(parsed, dict):
                if strict:
                    return None, "El JSON parseado no es un objeto/diccionario"
                return {"raw_content": parsed}, None
            
            return parsed, None
            
        except json.JSONDecodeError as e:
            error_msg = f"Error parseando JSON: {str(e)}"
            
            if strict:
                return None, error_msg
            
            # En modo no-estricto, devolvemos el contenido crudo
            return {
                "raw_content": raw_output[:1000],
                "parse_error": error_msg
            }, error_msg

    @staticmethod
    def truncate_text(text: str, max_length: int = 2000, suffix: str = "\n...[truncado]") -> str:
        """
        Trunca texto de manera inteligente manteniendo coherencia.
        
        Args:
            text: Texto a truncar
            max_length: Longitud máxima en caracteres
            suffix: Sufijo para indicar truncamiento
            
        Returns:
            str: Texto truncado o completo si es menor a max_length
        """
        if not text or len(text) <= max_length:
            return text
        
        # Truncar en el último espacio antes del límite para no cortar palabras
        truncated = text[:max_length].rsplit(' ', 1)[0]
        return truncated + suffix

    @staticmethod
    def validate_json_structure(data: Dict[str, Any], required_fields: list) -> Tuple[bool, list]:
        """
        Valida que un JSON tenga los campos requeridos.
        
        Args:
            data: Diccionario a validar
            required_fields: Lista de campos obligatorios
            
        Returns:
            Tuple[bool, list]: (is_valid, missing_fields)
        """
        if not isinstance(data, dict):
            return False, required_fields
        
        missing = [field for field in required_fields if field not in data]
        return len(missing) == 0, missing

    @staticmethod
    def extract_narrative_text(json_output: Dict[str, Any]) -> str:
        """
        Extrae el texto narrativo de un JSON_B de forma robusta.
        Busca en los campos comunes: 'narrativa', 'narrative_output', 'text', etc.
        
        Args:
            json_output: JSON de salida del GeneratorB
            
        Returns:
            str: Texto narrativo extraído
        """
        possible_keys = ['narrativa', 'narrative_output', 'text', 'content', 'redaccion']
        
        for key in possible_keys:
            if key in json_output and isinstance(json_output[key], str):
                return json_output[key].strip()
        
        # Si no encuentra ningún campo conocido, devuelve todo como string
        return json.dumps(json_output, ensure_ascii=False, indent=2)

    @staticmethod
    def normalize_json_output(
        raw_output: str,
        schema_type: str,
        expediente_id: str,
        documento: str,
        seccion: str
    ) -> Dict[str, Any]:
        """
        Normaliza la salida del modelo al formato canónico del binder.
        
        Args:
            raw_output: Salida cruda del modelo
            schema_type: 'json_a' o 'json_b'
            expediente_id: ID del expediente
            documento: Tipo de documento (JN, PPT, etc.)
            seccion: Sección del documento (JN.1, etc.)
            
        Returns:
            Dict: JSON normalizado al esquema del binder
        """
        import datetime
        
        parsed, error = OutputParser.parse_json(raw_output, strict=False)
        
        # Estructura base común
        base_structure = {
            "expediente_id": expediente_id,
            "documento": documento,
            "seccion": seccion,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "actor": "LLM",
        }
        
        if schema_type == "json_a":
            return {
                **base_structure,
                "nodo": "A",
                "json": parsed if not error else {},
                "citas_golden": [],
                "citas_normativas": [],
                "parse_error": error,
            }
        
        elif schema_type == "json_b":
            narrative = OutputParser.extract_narrative_text(parsed) if not error else ""
            return {
                **base_structure,
                "nodo": "B",
                "narrativa": narrative,
                "refs": {
                    "hash_json_A": "",
                    "citas_golden": [],
                    "citas_normativas": [],
                },
                "parse_error": error,
            }
        
        return base_structure
