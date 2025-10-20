"""
Test End-to-End del Orquestador LangGraph
==========================================
Prueba el flujo completo de generación de una sección JN usando el orquestador.
"""
import pytest
import asyncio
from backend.agents.orchestrator import build_orchestrator


@pytest.mark.asyncio
async def test_orchestrator_jn1_flow():
    """
    Test del flujo completo para generar JN.1 (Objeto y Alcance)
    """
    # Construir orquestador
    orchestrator = build_orchestrator(debug_mode=True)
    
    # Estado inicial
    initial_state = {
        "expediente_id": "TEST-EXP-001",
        "documento": "JN",
        "seccion": "JN.1",
        "user_text": """
        Necesitamos contratar 50 ordenadores portátiles para el ayuntamiento de Madrid.
        Los equipos deben ser instalados en 10 edificios municipales distintos.
        El objetivo es modernizar las estaciones de trabajo de los funcionarios
        del departamento de Urbanismo y Medio Ambiente.
        Plazo estimado: 6 meses.
        """
    }
    
    # Ejecutar grafo
    final_state = await orchestrator.ainvoke(initial_state)
    
    # Assertions
    assert final_state is not None, "El estado final no debe ser None"
    assert "json_a" in final_state, "Debe existir JSON_A en el estado final"
    assert "json_b" in final_state, "Debe existir JSON_B en el estado final"
    
    # Validar JSON_A
    json_a = final_state["json_a"]
    # JSON_A puede tener 'data' o ser directamente el dict con los campos
    data = json_a.get("data", json_a)
    assert "objeto" in data or "secciones_JN" in json_a, "JSON_A debe contener 'objeto' o 'secciones_JN'"
    
    # Obtener el objeto según la estructura
    if "secciones_JN" in json_a:
        objeto = json_a["secciones_JN"].get("objeto", "")
    else:
        objeto = data.get("objeto", "")
    
    assert len(objeto) > 10, "El objeto debe tener contenido"
    
    # Validar JSON_B
    json_b = final_state["json_b"]
    assert "narrativa" in json_b, "JSON_B debe tener campo 'narrativa'"
    assert len(json_b["narrativa"]) > 100, "La narrativa debe tener al menos 100 caracteres"
    
    # Validar RAG
    assert "rag_results" in final_state, "Debe haber resultados RAG"
    
    print("\n✅ Test JN.1 PASSED")
    print(f"   - JSON_A generado: {len(str(json_a))} caracteres")
    print(f"   - JSON_B generado: {len(json_b['narrativa'])} caracteres")
    print(f"   - RAG results: {len(final_state['rag_results'])} documentos")


@pytest.mark.asyncio
async def test_orchestrator_jn2_flow():
    """
    Test del flujo completo para generar JN.2 (Contexto y Problema)
    """
    orchestrator = build_orchestrator(debug_mode=True)
    
    initial_state = {
        "expediente_id": "TEST-EXP-002",
        "documento": "JN",
        "seccion": "JN.2",
        "user_text": """
        Actualmente los funcionarios trabajan con equipos obsoletos de más de 8 años.
        Esto causa lentitud, pérdida de productividad y riesgo de fallos técnicos.
        El impacto es significativo: retrasos en tramitaciones y quejas ciudadanas.
        Si no actuamos, el problema empeorará y afectará la calidad del servicio público.
        """
    }
    
    final_state = await orchestrator.ainvoke(initial_state)
    
    # Assertions
    assert "json_a" in final_state
    assert "json_b" in final_state
    
    json_a = final_state["json_a"]
    assert "contexto" in json_a["data"], "JN.2 debe contener 'contexto'"
    assert "dolor_actual" in json_a["data"], "JN.2 debe contener 'dolor_actual'"
    
    print("\n✅ Test JN.2 PASSED")


@pytest.mark.asyncio
async def test_orchestrator_jn3_flow():
    """
    Test del flujo completo para generar JN.3 (Objetivos)
    """
    orchestrator = build_orchestrator(debug_mode=True)
    
    initial_state = {
        "expediente_id": "TEST-EXP-003",
        "documento": "JN",
        "seccion": "JN.3",
        "user_text": """
        Objetivo 1: Modernizar equipos informáticos en 10 edificios municipales.
        Indicador: 100% de equipos renovados en 6 meses.
        
        Objetivo 2: Mejorar productividad de funcionarios.
        Indicador: Reducción de 30% en tiempos de tramitación.
        
        Objetivo 3: Reducir costes de mantenimiento.
        Indicador: Ahorro de 20% en gastos de reparaciones.
        """
    }
    
    final_state = await orchestrator.ainvoke(initial_state)
    
    # Assertions
    assert "json_a" in final_state
    assert "json_b" in final_state
    
    json_a = final_state["json_a"]
    assert "objetivos" in json_a["data"], "JN.3 debe contener 'objetivos'"
    assert isinstance(json_a["data"]["objetivos"], list), "Objetivos debe ser una lista"
    assert len(json_a["data"]["objetivos"]) >= 1, "Debe haber al menos 1 objetivo"
    
    # Validar estructura de objetivos
    objetivo = json_a["data"]["objetivos"][0]
    assert "descripcion" in objetivo, "Cada objetivo debe tener 'descripcion'"
    assert "indicador_exito" in objetivo, "Cada objetivo debe tener 'indicador_exito'"
    
    print("\n✅ Test JN.3 PASSED")
    print(f"   - Objetivos detectados: {len(json_a['data']['objetivos'])}")


@pytest.mark.asyncio
async def test_orchestrator_error_handling():
    """
    Test de manejo de errores con input vacío
    """
    orchestrator = build_orchestrator(debug_mode=True)
    
    initial_state = {
        "expediente_id": "TEST-EXP-ERROR",
        "documento": "JN",
        "seccion": "JN.1",
        "user_text": ""  # Input vacío
    }
    
    try:
        final_state = await orchestrator.ainvoke(initial_state)
        # El orquestador debe manejar el error o devolver faltantes
        assert "json_a" in final_state or "json_b" in final_state
        print("\n✅ Test Error Handling PASSED (manejó input vacío)")
    except Exception as e:
        # Si lanza excepción, debe ser controlada
        assert "user_text" in str(e).lower() or "input" in str(e).lower()
        print(f"\n✅ Test Error Handling PASSED (excepción controlada: {str(e)[:50]})")


@pytest.mark.asyncio
async def test_orchestrator_rag_integration():
    """
    Test de integración RAG (recuperación de contexto)
    """
    orchestrator = build_orchestrator(debug_mode=True)
    
    initial_state = {
        "expediente_id": "TEST-EXP-RAG",
        "documento": "JN",
        "seccion": "JN.1",
        "user_text": "Contratación de servicios informáticos para administración pública"
    }
    
    final_state = await orchestrator.ainvoke(initial_state)
    
    # Validar que RAG recuperó contexto
    assert "rag_results" in final_state, "Debe haber resultados RAG"
    rag_results = final_state.get("rag_results", [])
    
    # Puede no haber resultados si la BD está vacía, pero la estructura debe existir
    assert isinstance(rag_results, list), "RAG results debe ser una lista"
    
    print(f"\n✅ Test RAG Integration PASSED")
    print(f"   - Documentos recuperados: {len(rag_results)}")


if __name__ == "__main__":
    """
    Ejecutar tests manualmente sin pytest
    """
    async def run_all_tests():
        print("=" * 60)
        print("🧪 TESTS END-TO-END DEL ORQUESTADOR LANGGRAPH")
        print("=" * 60)
        
        await test_orchestrator_jn1_flow()
        await test_orchestrator_jn2_flow()
        await test_orchestrator_jn3_flow()
        await test_orchestrator_error_handling()
        await test_orchestrator_rag_integration()
        
        print("\n" + "=" * 60)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("=" * 60)
    
    asyncio.run(run_all_tests())
