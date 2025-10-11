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
async def retriever_node(state: OrchestratorState):
    @observe()
    async def run_retriever():
        agent = RetrieverAgent()
        return await agent.ainvoke(state)

    result = await run_retriever()
    state.update(result)
    return state


async def prompt_manager_node(state: OrchestratorState):
    @observe()
    async def run_prompt_manager():
        agent = PromptManager()
        return await agent.ainvoke(state)

    result = await run_prompt_manager()
    state.update(result)
    return state


async def generator_a_node(state: OrchestratorState):
    @observe()
    async def run_generator_a():
        agent = GeneratorA()
        return await agent.ainvoke(state)

    result = await run_generator_a()
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


async def validator_a_node(state: OrchestratorState):
    @observe()
    async def run_validator_a():
        agent = ValidatorAgent(mode="estructurado")
        return await agent.ainvoke(state)

    result = await run_validator_a()
    state.update(result)
    return state


async def generator_b_node(state: OrchestratorState):
    @observe()
    async def run_generator_b():
        agent = GeneratorB()
        return await agent.ainvoke(state)

    result = await run_generator_b()
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


async def validator_b_node(state: OrchestratorState):
    @observe()
    async def run_validator_b():
        agent = ValidatorAgent(mode="narrativa")
        return await agent.ainvoke(state)

    result = await run_validator_b()
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
# - Ahora los nodos usan @observe() internamente (compatibles con LangGraph).
# - Cada ejecución se registra en LangFuse sin romper la asincronía.
# - La estructura general del flujo se mantiene idéntica.
# - La versión futura (.as_node) podrá activarse cuando los agentes
#   sean nativos de LangGraph o LangChain.
# - Orden del flujo: Retriever → Prompt → GeneratorA → ValidatorA → GeneratorB → ValidatorB → END
