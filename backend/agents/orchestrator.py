
from langgraph.graph import StateGraph, END
from backend.agents.retriever_agent import RetrieverAgent
from backend.agents.prompt_manager import PromptManager
from backend.agents.validator_agent import ValidatorAgent
from backend.agents.jn_agent import GeneratorA, GeneratorB
from backend.database.outputs_repository import save_output

def build_orchestrator():
    graph = StateGraph()

    # Nodos
    retriever = RetrieverAgent().as_node("retriever")
    prompt_manager = PromptManager().as_node("prompt_manager")
    generator_a = GeneratorA().as_node("generator_a")
    validator_a = ValidatorAgent("estructurado").as_node("validator_a")
    generator_b = GeneratorB().as_node("generator_b")
    validator_b = ValidatorAgent("narrativa").as_node("validator_b")
    save_node = save_output.as_node("save_output")

    # Enlaces entre nodos
    graph.add_edge("retriever", "prompt_manager")
    graph.add_edge("prompt_manager", "generator_a")
    graph.add_edge("generator_a", "validator_a")
    graph.add_edge("validator_a", "generator_b")
    graph.add_edge("generator_b", "validator_b")
    graph.add_edge("validator_b", "save_output")
    graph.add_edge("save_output", END)

    return graph.compile()
