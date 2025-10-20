"""
Test Suite para las Mejoras del Sistema de Validación
======================================================
Prueba las nuevas funcionalidades:
- Sanitización de "faltantes"
- Auto-retry con repair prompt
- Validación mejorada
"""

import asyncio
import json
from backend.agents.validator import ValidatorAgent


def test_sanitize_faltantes():
    """Test 1: Sanitización de valores 'faltantes'"""
    print("\n" + "="*60)
    print("TEST 1: Sanitización de valores 'faltantes'")
    print("="*60)
    
    validator = ValidatorAgent(mode="estructurado", strict=False)
    
    # JSON con valores "faltantes"
    test_data = {
        "objeto": "Servicio de limpieza",
        "alcance": "faltantes",
        "ambito": "Nacional",
        "nested": {
            "campo1": "valor1",
            "campo2": "faltantes"
        },
        "lista": ["valor_a", "faltantes", "valor_c"]
    }
    
    sanitized, warnings = validator.sanitize_faltantes(test_data)
    
    print("\nJSON ORIGINAL:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    
    print("\nJSON SANITIZADO:")
    print(json.dumps(sanitized, indent=2, ensure_ascii=False))
    
    print("\nADVERTENCIAS:")
    for w in warnings:
        print(f"  - {w}")
    
    # Verificaciones
    assert sanitized["alcance"] == "", "El campo 'alcance' debe ser cadena vacía"
    assert sanitized["nested"]["campo2"] == "", "El campo anidado debe ser cadena vacía"
    assert sanitized["lista"][1] == "", "El elemento de lista debe ser cadena vacía"
    assert len(warnings) == 3, "Debe haber 3 advertencias"
    
    print("\n✅ Test 1 PASADO: Sanitización funciona correctamente")


def test_validate_json_a_with_missing_fields():
    """Test 2: Validación de JSON_A con campos faltantes"""
    print("\n" + "="*60)
    print("TEST 2: Validación de JSON_A con campos faltantes")
    print("="*60)
    
    validator = ValidatorAgent(mode="estructurado", strict=False)
    
    # JSON_A incompleto (falta campo 'objeto' en secciones_JN)
    incomplete_json_a = {
        "expediente_id": "TEST-001",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "A",
        "timestamp": "2025-10-20T12:00:00Z",
        "actor": "LLM",
        "json": {
            "secciones_JN": {
                "alcance": "Servicio de limpieza urbana",
                "ambito": "Nacional"
                # Falta "objeto"
            }
        },
        "citas_golden": [],
        "citas_normativas": []
    }
    
    result = validator.validate_json_a(incomplete_json_a, "JN.1")
    result_dict = result.to_dict()
    
    print("\nRESULTADO DE VALIDACIÓN:")
    print(f"  - Es válido: {result.is_valid}")
    print(f"  - Errores: {len(result.errors)}")
    print(f"  - Advertencias: {len(result.warnings)}")
    
    if result.errors:
        print("\nERRORES DETECTADOS:")
        for error in result.errors:
            print(f"  🔴 {error}")
    
    if result.warnings:
        print("\nADVERTENCIAS:")
        for warning in result.warnings:
            print(f"  ⚠️  {warning}")
    
    assert not result.is_valid, "El JSON debe ser inválido (falta campo 'objeto')"
    assert any("objeto" in error for error in result.errors), "Debe detectar campo 'objeto' faltante"
    
    print("\n✅ Test 2 PASADO: Validación detecta campos faltantes")


def test_validate_json_a_complete():
    """Test 3: Validación de JSON_A completo"""
    print("\n" + "="*60)
    print("TEST 3: Validación de JSON_A completo y correcto")
    print("="*60)
    
    validator = ValidatorAgent(mode="estructurado", strict=False)
    
    # JSON_A completo y correcto
    complete_json_a = {
        "expediente_id": "TEST-002",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "A",
        "timestamp": "2025-10-20T12:00:00Z",
        "actor": "LLM",
        "json": {
            "secciones_JN": {
                "objeto": "Contratación de servicio de limpieza urbana",
                "alcance": "Limpieza de calles, parques y espacios públicos",
                "ambito": "Nacional - Todas las provincias"
            }
        },
        "citas_golden": [],
        "citas_normativas": [],
        "metadata": {
            "model": "gpt-4o",
            "status": "success"
        }
    }
    
    result = validator.validate_json_a(complete_json_a, "JN.1")
    
    print("\nRESULTADO DE VALIDACIÓN:")
    print(f"  - Es válido: {result.is_valid}")
    print(f"  - Errores: {len(result.errors)}")
    print(f"  - Advertencias: {len(result.warnings)}")
    
    if result.errors:
        print("\nERRORES:")
        for error in result.errors:
            print(f"  🔴 {error}")
    
    assert result.is_valid, "El JSON completo debe ser válido"
    assert len(result.errors) == 0, "No debe haber errores"
    
    print("\n✅ Test 3 PASADO: JSON_A completo pasa validación")


def test_generate_repair_prompt():
    """Test 4: Generación de prompt de reparación"""
    print("\n" + "="*60)
    print("TEST 4: Generación de prompt de reparación")
    print("="*60)
    
    validator = ValidatorAgent(mode="estructurado", strict=False)
    
    incomplete_data = {
        "secciones_JN": {
            "alcance": "Servicios varios",
            "ambito": "Local"
            # Falta "objeto"
        }
    }
    
    errors = [
        "Campo obligatorio faltante en 'json': 'objeto'",
        "El campo 'objeto' es requerido para JN.1"
    ]
    
    repair_prompt = validator.generate_repair_prompt(incomplete_data, errors, "JN.1")
    
    print("\nPROMPT DE REPARACIÓN GENERADO:")
    print("-" * 60)
    print(repair_prompt)
    print("-" * 60)
    
    # Verificaciones básicas del prompt
    assert "JSON ORIGINAL" in repair_prompt
    assert "ERRORES DETECTADOS" in repair_prompt
    assert "CAMPOS REQUERIDOS" in repair_prompt
    assert "objeto" in repair_prompt
    assert "alcance" in repair_prompt
    assert "ambito" in repair_prompt
    assert "NUNCA uses \"faltantes\"" in repair_prompt
    
    print("\n✅ Test 4 PASADO: Prompt de reparación generado correctamente")


async def test_auto_repair_simulation():
    """Test 5: Simulación de auto-reparación (sin LLM real)"""
    print("\n" + "="*60)
    print("TEST 5: Simulación del flujo de auto-reparación")
    print("="*60)
    
    print("\nNOTA: Este test simula el flujo sin invocar LLM real")
    print("Para test completo, ejecutar con backend activo\n")
    
    # JSON_A incompleto pero con estructura básica correcta
    incomplete_json_a = {
        "expediente_id": "TEST-REPAIR",
        "documento": "JN",
        "seccion": "JN.1",
        "nodo": "A",
        "timestamp": "2025-10-20T12:00:00Z",
        "actor": "LLM",
        "json": {
            "secciones_JN": {
                "alcance": "Servicios de mantenimiento",
                "ambito": "Regional"
                # Falta "objeto"
            }
        },
        "citas_golden": [],
        "citas_normativas": [],
        "metadata": {}
    }
    
    # Estado simulado
    state = {
        "json_a": incomplete_json_a,
        "seccion": "JN.1"
    }
    
    validator = ValidatorAgent(mode="estructurado", strict=True, max_retries=2)
    
    # Primera validación (debe fallar por campo faltante)
    result = validator.validate_json_a(state["json_a"], state["seccion"])
    
    print("VALIDACIÓN INICIAL:")
    print(f"  - Es válido: {result.is_valid}")
    print(f"  - Errores: {len(result.errors)}")
    
    if not result.is_valid:
        print("\n🔧 En un flujo real, aquí se activaría auto_repair_json_a():")
        print("   1. Se genera repair_prompt con el JSON incompleto")
        print("   2. Se invoca LLM con temperatura 0.1")
        print("   3. Se parsea el JSON reparado")
        print("   4. Se actualiza state['json_a']")
        print("   5. Se re-valida")
        
        # Simular reparación: añadir el campo faltante
        print("\n✅ Simulación: JSON reparado añadiendo campo 'objeto'")
        
        state["json_a"]["json"]["secciones_JN"]["objeto"] = "Servicios de mantenimiento urbano"
        state["json_a"]["metadata"]["repaired"] = True
        
        # Segunda validación (debe pasar)
        result2 = validator.validate_json_a(state["json_a"], state["seccion"])
        
        print("\nVALIDACIÓN DESPUÉS DE REPARACIÓN:")
        print(f"  - Es válido: {result2.is_valid}")
        print(f"  - Errores: {len(result2.errors)}")
        
        if result2.errors:
            print("\nERRORES RESTANTES:")
            for error in result2.errors:
                print(f"  🔴 {error}")
        
        assert result2.is_valid, "JSON reparado debe ser válido"
    
    print("\n✅ Test 5 PASADO: Flujo de reparación simulado correctamente")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print(" SUITE DE PRUEBAS: MEJORAS DEL SISTEMA DE VALIDACIÓN")
    print("="*70)
    
    try:
        # Tests síncronos
        test_sanitize_faltantes()
        test_validate_json_a_with_missing_fields()
        test_validate_json_a_complete()
        test_generate_repair_prompt()
        
        # Test asíncrono
        asyncio.run(test_auto_repair_simulation())
        
        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("="*70)
        print("\nResumen:")
        print("  ✅ Test 1: Sanitización de 'faltantes'")
        print("  ✅ Test 2: Detección de campos faltantes")
        print("  ✅ Test 3: Validación de JSON completo")
        print("  ✅ Test 4: Generación de repair prompt")
        print("  ✅ Test 5: Simulación de auto-repair")
        print("\n💡 Para test completo de auto-repair, ejecutar con backend activo")
        
    except AssertionError as e:
        print(f"\n❌ TEST FALLÓ: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
