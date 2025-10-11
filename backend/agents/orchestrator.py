"""
Orchestrator (instrumentado)
----------------------------
Flujo LangGraph completo con trazabilidad LangFuse y persistencia Mongo.
"""

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.prompt_manager import PromptManager
from backend.agents.generators.generator_a import GeneratorA
from backend.agents.generators.generator_b import GeneratorB
from backend.agents.validator_agent import ValidatorAgent
from backend.database.outputs_repository import save_output
from backend.core.langfuse_client import observe

# ============================================================
#    1. Estado compartido del grafo
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
#   2. Funciones observables (LangFuse)
# ============================================================
@observe()
async def retriever_node(state: OrchestratorState):
    agent = RetrieverAgent()
    result = await agent.ainvoke(state)
    state.update(result)
    return state


@observe()
async def prompt_manager_node(state: OrchestratorState):
    agent = PromptManager()
    result = await agent.ainvoke(state)
    state.update(result)
    return state


@observe()
async def generator_a_node(state: OrchestratorState):
    agent = GeneratorA()
    result = await agent.ainvoke(state)
    state.update(result)
    # Guardar JSON_A en Mongo
    if "json_a" in result:
        await save_output(
            state["expediente_id"],
            state["documento"],
            state["seccion"],
            "A",
            result["json_a"],
        )
    return state


@observe()
async def validator_a_node(state: OrchestratorState):
    agent = ValidatorAgent(mode="estructurado")
    result = await agent.ainvoke(state)
    state.update(result)
    return state


@observe()
async def generator_b_node(state: OrchestratorState):
    agent = GeneratorB()
    result = await agent.ainvoke(state)
    state.update(result)
    # Guardar JSON_B + métricas en Mongo
    if "json_b" in result:
        await save_output(
            state["expediente_id"],
            state["documento"],
            state["seccion"],
            "B",
            result["json_b"],
        )
    return state


@observe()
async def validator_b_node(state: OrchestratorState):
    agent = ValidatorAgent(mode="narrativa")
    result = await agent.ainvoke(state)
    state.update(result)
    return state


# ============================================================
#    3. Construcción del grafo LangGraph
# ============================================================
def build_orchestrator():
    graph = StateGraph(OrchestratorState)

    graph.add_node("retriever", retriever_node)
    graph.add_node("prompt_manager", prompt_manager_node)
    graph.add_node("generator_a", generator_a_node)
    graph.add_node("validator_a", validator_a_node)
    graph.add_node("generator_b", generator_b_node)
    graph.add_node("validator_b", validator_b_node)

    graph.add_edge(START, "retriever")
    graph.add_edge("retriever", "prompt_manager")
    graph.add_edge("prompt_manager", "generator_a")
    graph.add_edge("generator_a", "validator_a")
    graph.add_edge("validator_a", "generator_b")
    graph.add_edge("generator_b", "validator_b")
    graph.add_edge("validator_b", END)

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
