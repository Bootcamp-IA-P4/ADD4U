"""
Orquestador principal de Mini-CELIA
Versión actual: funcional con agentes stub (usa .ainvoke)
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.prompt_manager import PromptManager
from backend.agents.validator import ValidatorAgent
from backend.agents.generators.generator_a import GeneratorA
from backend.agents.generators.generator_b import GeneratorB
from backend.prompts.jn_prompts import prompt_a_template, prompt_b_template

# ============================================================
# 🔹 1. Definición del esquema de estado
# ============================================================
class OrchestratorState(TypedDict, total=False):
    expediente_id: str
    documento: str
    seccion: str
    user_text: str
    context: str
    rag_results: list # Cambiado de 'context' a 'rag_results'
    prompt_a: str
    prompt_b: str
    json_a: dict
    json_b: dict
    validation_result: str

# ============================================================
# 🔹 2. Grafo funcional con agentes stub y generadores reales
# ============================================================
def build_orchestrator(debug_mode: bool = False):
    """
    Construye el grafo LangGraph que conecta los agentes.
    Versión de desarrollo: usa .ainvoke para compatibilidad con stubs.
    """
    graph = StateGraph(OrchestratorState) 

    # Instancias de agentes
    retriever = RetrieverAgent()
    prompt_manager = PromptManager(prompt_a_template, prompt_b_template, debug_mode=debug_mode)
    generator_a = GeneratorA()
    validator_a = ValidatorAgent(mode="estructurado")
    generator_b = GeneratorB()
    validator_b = ValidatorAgent(mode="narrativa")

    generator_b = GeneratorB()
    validator_b = ValidatorAgent(mode="narrativa")

    # Definir el nodo prompt_manager_node como una función que envuelve la lógica de PromptManager
    def prompt_manager_node(state: OrchestratorState):
        user_text = state.get("user_text", "")
        rag_results = state.get("rag_results", [])
        # Asumiendo que format_instructions se genera en algún punto o es constante
        # Para este ejemplo, lo dejaremos como un placeholder
        format_instructions = "Instrucciones de formato Pydantic para OutputJsonA..."

        prompt_a = prompt_manager.build_prompt_a(
            user_input=user_text,
            format_instructions=format_instructions,
            rag_results=rag_results
        )
        # Aquí, structured_data vendría del output de GeneratorA, pero para el prompt_b
        # en este punto del flujo, aún no lo tenemos. Se pasará en el siguiente paso.
        prompt_b = prompt_manager.build_prompt_b(
            user_input=user_text,
            format_instructions="", # No se usa para prompt B directamente
            rag_results=rag_results
        )
        return {"prompt_a": prompt_a, "prompt_b": prompt_b}

    # Añadir nodos
    graph.add_node("retriever", retriever.ainvoke)
    graph.add_node("prompt_manager", prompt_manager_node)
    graph.add_node("generator_a", generator_a.ainvoke)
    graph.add_node("validator_a", validator_a.ainvoke)
    graph.add_node("generator_b", generator_b.ainvoke)
    graph.add_node("validator_b", validator_b.ainvoke)

    # Conexiones del flujo
    graph.add_edge(START, "retriever")
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
