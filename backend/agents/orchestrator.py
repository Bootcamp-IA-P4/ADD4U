"""
Orquestador principal de Mini-CELIA
Versión actual: funcional con agentes stub (usa .ainvoke)
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.prompt_manager import PromptManager
from backend.agents.validator_agent import ValidatorAgent
from backend.agents.generators.generator_a import GeneratorA
from backend.agents.generators.generator_b import GeneratorB

# ============================================================
# 🔹 1. Definición del esquema de estado
# ============================================================
class OrchestratorState(TypedDict, total=False):
    expediente_id: str
    documento: str
    seccion: str
    user_text: str
    context: str
    prompt_a: str
    prompt_b: str
    json_a: dict
    json_b: dict
    validation_result: str

# ============================================================
# 🔹 2. Grafo funcional con agentes stub y generadores reales
# ============================================================
def build_orchestrator():
    """
    Construye el grafo LangGraph que conecta los agentes.
    Versión de desarrollo: usa .ainvoke para compatibilidad con stubs.
    """
    graph = StateGraph(OrchestratorState)  # 👈 Añadimos el esquema obligatorio

    # Instancias de agentes
    retriever = RetrieverAgent()
    prompt_manager = PromptManager()
    generator_a = GeneratorA()
    validator_a = ValidatorAgent(mode="estructurado")
    generator_b = GeneratorB()
    validator_b = ValidatorAgent(mode="narrativa")

    # Añadir nodos
    graph.add_node("retriever", retriever.ainvoke)
    graph.add_node("prompt_manager", prompt_manager.ainvoke)
    graph.add_node("generator_a", generator_a.ainvoke)
    graph.add_node("validator_a", validator_a.ainvoke)
    graph.add_node("generator_b", generator_b.ainvoke)
    graph.add_node("validator_b", validator_b.ainvoke)

    # Conexiones del flujo
    graph.add_edge("retriever", "prompt_manager")
    graph.add_edge("prompt_manager", "generator_a")
    graph.add_edge("generator_a", "validator_a")
    graph.add_edge("validator_a", "generator_b")
    graph.add_edge("generator_b", "validator_b")
    graph.add_edge("validator_b", END)

    # Compilar el grafo
    return graph.compile()



# ============================================================
# 🧩 VERSIÓN FUTURA – integración nativa con LangGraph
# ============================================================
"""
Cuando todos los agentes estén desarrollados con LangChain y LangGraph,
podremos usar la siguiente versión, que crea nodos nativos mediante .as_node().

def build_orchestrator():
    graph = StateGraph()

    retriever = RetrieverAgent().as_node("retriever")
    prompt_manager = PromptManager().as_node("prompt_manager")
    generator_a = GeneratorA().as_node("generator_a")
    validator_a = ValidatorAgent("estructurado").as_node("validator_a")
    generator_b = GeneratorB().as_node("generator_b")
    validator_b = ValidatorAgent("narrativa").as_node("validator_b")
    save_node = save_output.as_node("save_output")

    graph.add_edge("retriever", "prompt_manager")
    graph.add_edge("prompt_manager", "generator_a")
    graph.add_edge("generator_a", "validator_a")
    graph.add_edge("validator_a", "generator_b")
    graph.add_edge("generator_b", "validator_b")
    graph.add_edge("validator_b", "save_output")
    graph.add_edge("save_output", END)

    return graph.compile()
"""

# ============================================================
# 🔍 Notas
# ============================================================
# - La versión actual (.ainvoke) permite probar el grafo aunque los agentes
#   no estén implementados todavía.
# - La versión futura (.as_node) se activará cuando todos los agentes
#   sean compatibles con LangGraph o LangChain.
# - El orden de los nodos refleja el flujo JN.x:
#   Retriever → Prompt → GeneratorA → ValidatorA → GeneratorB → ValidatorB → END
