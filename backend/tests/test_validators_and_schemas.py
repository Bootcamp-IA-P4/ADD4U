"""
Test de Validadores y Esquemas
-------------------------------
Prueba la validación estructural de JSON_A y JSON_B contra los esquemas del binder.
"""

import asyncio
import json
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from backend.agents.validator import ValidatorAgent
from backend.agents.schemas.json_schemas import BinderSchemas
from backend.agents.generators.output_parser import OutputParser


def test_output_parser():
    """Prueba el OutputParser"""
    print("\n" + "="*60)
    print("TEST 1: OutputParser")
    print("="*60)
    
    # Test 1: Limpieza de JSON
    raw_json = """
    ```json
    {
        "objeto": "Contratación de servicios",
        "alcance": "Nacional"
    }
    ```
    """
    
    cleaned = OutputParser.clean_json_response(raw_json)
    print(f"✅ Limpieza exitosa: {cleaned[:100]}...")
    
    # Test 2: Parsing robusto
    parsed, error = OutputParser.parse_json(raw_json, strict=False)
    assert parsed is not None, "El parsing debería devolver un resultado"
    assert "objeto" in parsed, "Debería parsear correctamente el campo 'objeto'"
    print(f"✅ Parsing exitoso: {len(parsed)} campos encontrados")
    
    # Test 3: Truncamiento inteligente
    long_text = "Lorem ipsum " * 200
    truncated = OutputParser.truncate_text(long_text, max_length=100)
    assert len(truncated) <= 120, "El texto debería truncarse"
    print(f"✅ Truncamiento exitoso: {len(long_text)} → {len(truncated)} chars")


def test_binder_schemas():
    """Prueba los esquemas del binder"""
    print("\n" + "="*60)
    print("TEST 2: Binder Schemas")
    print("="*60)
    
    # JSON_A válido
    valid_json_a = {
        "expediente_id": "EXP-001",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "A",
        "timestamp": "2025-10-20T10:00:00Z",
        "actor": "LLM",
        "json": {
            "objeto": "Contratación de servicios informáticos",
            "alcance_resumido": "Servicios de desarrollo",
        },
        "citas_golden": ["rgpd_art25"],
        "citas_normativas": [],
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(valid_json_a, "json_a")
    assert is_valid, f"JSON_A válido debería pasar la validación. Errores: {errors}"
    print(f"✅ Validación JSON_A exitosa (0 errores)")
    
    # JSON_A inválido (falta campo requerido)
    invalid_json_a = {
        "expediente_id": "EXP-002",
        "documento": "JN",
        # Falta "seccion"
        "nodo": "A",
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(invalid_json_a, "json_a")
    assert not is_valid, "JSON_A inválido debería fallar"
    assert len(errors) > 0, "Debería reportar errores"
    print(f"✅ Detección de errores exitosa ({len(errors)} errores encontrados)")
    
    # JSON_B válido
    valid_json_b = {
        "expediente_id": "EXP-001",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "B",
        "timestamp": "2025-10-20T10:05:00Z",
        "actor": "LLM",
        "narrativa": "El objeto del expediente consiste en la contratación de servicios informáticos para el desarrollo de aplicaciones.",
        "refs": {
            "hash_json_A": "hash_A_JN1_EXP001",
            "citas_golden": ["rgpd_art25"],
            "citas_normativas": [],
        }
    }
    
    is_valid, errors = BinderSchemas.validate_basic_structure(valid_json_b, "json_b")
    assert is_valid, f"JSON_B válido debería pasar la validación. Errores: {errors}"
    print(f"✅ Validación JSON_B exitosa (0 errores)")


async def test_validator_agent():
    """Prueba el ValidatorAgent mejorado"""
    print("\n" + "="*60)
    print("TEST 3: ValidatorAgent")
    print("="*60)
    
    # Test ValidatorA
    validator_a = ValidatorAgent(mode="estructurado", strict=True)
    
    state_a = {
        "json_a": {
            "expediente_id": "EXP-TEST-001",
            "documento": "JN",
            "seccion": "JN.1",
            "nodo": "A",
            "timestamp": "2025-10-20T10:00:00Z",
            "actor": "LLM",
            "json": {
                "objeto": "Contratación de equipos informáticos",
                "alcance_resumido": "200 equipos para oficinas municipales",
                "ambito": "Ayuntamiento",
            },
            "citas_golden": [],
            "citas_normativas": [],
        },
        "seccion": "JN.1",
    }
    
    result_a = await validator_a.ainvoke(state_a)
    assert "validation_a_result" in result_a, "Debería tener resultado de validación"
    assert result_a["validation_a_passed"], "Debería pasar la validación"
    print(f"✅ ValidatorA: {result_a['validation_a_result']['severity']}")
    
    # Test ValidatorB
    validator_b = ValidatorAgent(mode="narrativa", strict=True)
    
    state_b = {
        "json_a": state_a["json_a"],
        "json_b": {
            "expediente_id": "EXP-TEST-001",
            "documento": "JN",
            "seccion": "JN.1",
            "nodo": "B",
            "timestamp": "2025-10-20T10:05:00Z",
            "actor": "LLM",
            "narrativa": "El objeto del expediente consiste en la contratación de equipos informáticos, específicamente 200 equipos destinados a las oficinas municipales del Ayuntamiento.",
            "refs": {
                "hash_json_A": "hash_A_JN1",
                "citas_golden": [],
                "citas_normativas": [],
            }
        },
        "seccion": "JN.1",
    }
    
    result_b = await validator_b.ainvoke(state_b)
    assert "validation_b_result" in result_b, "Debería tener resultado de validación"
    print(f"✅ ValidatorB: {result_b['validation_b_result']['severity']}")
    
    # Test validación estricta con error
    print("\n--- Test de bloqueo en modo strict ---")
    validator_strict = ValidatorAgent(mode="estructurado", strict=True)
    
    state_invalid = {
        "json_a": {
            "expediente_id": "EXP-INVALID",
            # Faltan campos obligatorios
            "json": {},
        },
        "seccion": "JN.1",
    }
    
    result_invalid = await validator_strict.ainvoke(state_invalid)
    assert not result_invalid.get("validation_a_passed"), "Debería fallar la validación"
    assert result_invalid.get("validation_failed"), "Debería marcar validation_failed=True"
    print(f"✅ Bloqueo en strict mode: validation_failed={result_invalid.get('validation_failed')}")
    print(f"   Mensaje: {result_invalid.get('validation_error_message', '')[:100]}...")


async def main():
    """Ejecuta todos los tests"""
    print("\n" + "🔬 INICIANDO TESTS DE VALIDACIÓN Y ESQUEMAS")
    
    try:
        test_output_parser()
        test_binder_schemas()
        await test_validator_agent()
        
        print("\n" + "="*60)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLIDO: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
