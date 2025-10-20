"""
Test Simplificado de OutputParser y Schemas
--------------------------------------------
Prueba solo OutputParser y BinderSchemas sin dependencias externas.
"""

import json
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from backend.agents.generators.output_parser import OutputParser
from backend.agents.schemas.json_schemas import BinderSchemas


def test_output_parser():
    """Prueba el OutputParser"""
    print("\n" + "="*70)
    print("TEST 1: OutputParser - Limpieza y Parsing")
    print("="*70)
    
    # Test 1: Limpieza de JSON con markdown
    print("\n📝 Test 1.1: Limpieza de JSON con markdown")
    raw_json = """
    Aquí está el JSON solicitado:
    ```json
    {
        "objeto": "Contratación de servicios informáticos",
        "alcance": "Nacional"
    }
    ```
    Espero que sea útil.
    """
    
    cleaned = OutputParser.clean_json_response(raw_json)
    print(f"  Input: {raw_json[:50]}...")
    print(f"  Output: {cleaned}")
    assert '{' in cleaned and '}' in cleaned, "Debería contener JSON válido"
    print("  ✅ Limpieza exitosa")
    
    # Test 2: Parsing robusto
    print("\n📝 Test 1.2: Parsing robusto")
    parsed, error = OutputParser.parse_json(raw_json, strict=False)
    assert parsed is not None, "El parsing debería devolver un resultado"
    assert "objeto" in parsed, "Debería parsear correctamente el campo 'objeto'"
    print(f"  Campos encontrados: {list(parsed.keys())}")
    print(f"  Error: {error if error else 'None'}")
    print(f"  ✅ Parsing exitoso: {len(parsed)} campos")
    
    # Test 3: Parsing de JSON inválido (modo no-estricto)
    print("\n📝 Test 1.3: Parsing de JSON inválido (non-strict)")
    invalid_json = "Esto no es un JSON válido { malformado }"
    parsed_invalid, error_invalid = OutputParser.parse_json(invalid_json, strict=False)
    assert parsed_invalid is not None, "En modo no-estricto debería devolver algo"
    assert error_invalid is not None, "Debería reportar error"
    print(f"  Input inválido procesado: {parsed_invalid}")
    print(f"  ✅ Manejo de errores correcto")
    
    # Test 4: Truncamiento inteligente
    print("\n📝 Test 1.4: Truncamiento inteligente")
    long_text = "Lorem ipsum dolor sit amet " * 100  # ~2700 chars
    truncated = OutputParser.truncate_text(long_text, max_length=200)
    print(f"  Longitud original: {len(long_text)} chars")
    print(f"  Longitud truncada: {len(truncated)} chars")
    assert len(truncated) <= 220, "El texto debería truncarse"
    assert truncated.endswith("[truncado]"), "Debería incluir sufijo"
    print(f"  ✅ Truncamiento exitoso")
    
    # Test 5: Validación de estructura JSON
    print("\n📝 Test 1.5: Validación de estructura")
    data = {"campo1": "valor1", "campo2": "valor2", "campo3": "valor3"}
    required = ["campo1", "campo2"]
    is_valid, missing = OutputParser.validate_json_structure(data, required)
    assert is_valid, "Debería ser válido"
    assert len(missing) == 0, "No debería faltar ningún campo"
    print(f"  ✅ Validación de estructura correcta")
    
    # Test 6: Extracción de narrativa
    print("\n📝 Test 1.6: Extracción de narrativa")
    json_b = {
        "narrativa": "Este es el texto narrativo del documento.",
        "otros_campos": "..."
    }
    narrative = OutputParser.extract_narrative_text(json_b)
    assert narrative == "Este es el texto narrativo del documento."
    print(f"  Narrativa extraída: '{narrative[:50]}...'")
    print(f"  ✅ Extracción exitosa")


def test_binder_schemas():
    """Prueba los esquemas del binder"""
    print("\n" + "="*70)
    print("TEST 2: Binder Schemas - Validación Estructural")
    print("="*70)
    
    # Test 1: JSON_A válido
    print("\n📝 Test 2.1: Validación de JSON_A válido")
    valid_json_a = {
        "expediente_id": "EXP-001",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "A",
        "timestamp": "2025-10-20T10:00:00Z",
        "actor": "LLM",
        "json": {
            "objeto": "Contratación de servicios informáticos para desarrollo",
            "alcance_resumido": "Servicios de desarrollo web y móvil",
            "ambito": "Nacional"
        },
        "citas_golden": ["rgpd_art25"],
        "citas_normativas": [],
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(valid_json_a, "json_a")
    print(f"  Resultado: {'✅ Válido' if is_valid else '❌ Inválido'}")
    print(f"  Errores: {errors if errors else 'Ninguno'}")
    assert is_valid, f"JSON_A válido debería pasar la validación. Errores: {errors}"
    print(f"  ✅ Validación JSON_A exitosa")
    
    # Test 2: JSON_A inválido (falta campo requerido)
    print("\n📝 Test 2.2: Detección de errores en JSON_A")
    invalid_json_a = {
        "expediente_id": "EXP-002",
        "documento": "JN",
        # Falta "seccion" (campo requerido)
        "nodo": "A",
        "json": {}
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(invalid_json_a, "json_a")
    print(f"  Resultado: {'✅ Válido' if is_valid else '❌ Inválido'}")
    print(f"  Errores detectados:")
    for error in errors:
        print(f"    - {error}")
    assert not is_valid, "JSON_A inválido debería fallar"
    assert len(errors) > 0, "Debería reportar errores"
    print(f"  ✅ Detección de errores exitosa ({len(errors)} errores)")
    
    # Test 3: JSON_A con nodo incorrecto
    print("\n📝 Test 2.3: Validación de campo 'nodo' en JSON_A")
    wrong_node_json_a = {
        "expediente_id": "EXP-003",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "B",  # Debería ser "A"
        "timestamp": "2025-10-20T10:00:00Z",
        "actor": "LLM",
        "json": {"objeto": "test"},
        "citas_golden": [],
        "citas_normativas": [],
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(wrong_node_json_a, "json_a")
    print(f"  Resultado: {'✅ Válido' if is_valid else '❌ Inválido'}")
    print(f"  Errores: {errors}")
    assert not is_valid, "Debería detectar nodo incorrecto"
    print(f"  ✅ Validación de 'nodo' correcta")
    
    # Test 4: JSON_B válido
    print("\n📝 Test 2.4: Validación de JSON_B válido")
    valid_json_b = {
        "expediente_id": "EXP-001",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "B",
        "timestamp": "2025-10-20T10:05:00Z",
        "actor": "LLM",
        "narrativa": "El objeto del expediente consiste en la contratación de servicios informáticos destinados al desarrollo de aplicaciones web y móviles de ámbito nacional.",
        "refs": {
            "hash_json_A": "hash_A_JN1_EXP001",
            "citas_golden": ["rgpd_art25"],
            "citas_normativas": [],
        }
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(valid_json_b, "json_b")
    print(f"  Resultado: {'✅ Válido' if is_valid else '❌ Inválido'}")
    print(f"  Errores: {errors if errors else 'Ninguno'}")
    assert is_valid, f"JSON_B válido debería pasar la validación. Errores: {errors}"
    print(f"  ✅ Validación JSON_B exitosa")
    
    # Test 5: JSON_B con narrativa muy corta
    print("\n📝 Test 2.5: Detección de narrativa muy corta")
    short_narrative_json_b = {
        "expediente_id": "EXP-004",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "B",
        "timestamp": "2025-10-20T10:05:00Z",
        "actor": "LLM",
        "narrativa": "Texto muy corto",  # Menos de 50 caracteres
        "refs": {
            "hash_json_A": "hash_test",
            "citas_golden": [],
            "citas_normativas": [],
        }
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(short_narrative_json_b, "json_b")
    print(f"  Resultado: {'✅ Válido' if is_valid else '❌ Inválido'}")
    print(f"  Errores: {errors}")
    assert not is_valid, "Debería detectar narrativa muy corta"
    print(f"  ✅ Detección de narrativa corta exitosa")
    
    # Test 6: Obtener campos requeridos por sección
    print("\n📝 Test 2.6: Campos requeridos por sección")
    required_jn1 = BinderSchemas.get_section_required_fields("JN.1")
    print(f"  Campos requeridos para JN.1: {required_jn1}")
    assert "objeto" in required_jn1, "JN.1 debería requerir 'objeto'"
    print(f"  ✅ Configuración de esquemas por sección correcta")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "🔬 TESTS DE VALIDACIÓN Y ESQUEMAS (Versión Simplificada)")
    print("="*70)
    
    try:
        test_output_parser()
        test_binder_schemas()
        
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("="*70)
        print("\n💡 Nota: Para tests completos con ValidatorAgent, instalar:")
        print("   pip install langfuse python-dotenv")
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLIDO: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
