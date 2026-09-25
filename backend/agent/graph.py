from langgraph.graph import StateGraph, START, END
from backend.agent.state import AgentState
from backend.agent.nodes.ingest_node import ingest_node
from backend.agent.nodes.pattern_node import pattern_node
from backend.agent.nodes.suggestion_node import suggestion_node
from backend.agent.nodes.voice_node import voice_node


def build_graph():
    """
    Constructs and compiles the 4-node LangGraph StateGraph:
    START -> ingest_node -> pattern_node -> suggestion_node -> voice_node -> END.
    """
    builder = StateGraph(AgentState)

    builder.add_node("ingest_node", ingest_node)
    builder.add_node("pattern_node", pattern_node)
    builder.add_node("suggestion_node", suggestion_node)
    builder.add_node("voice_node", voice_node)

    builder.add_edge(START, "ingest_node")
    builder.add_edge("ingest_node", "pattern_node")
    builder.add_edge("pattern_node", "suggestion_node")
    builder.add_edge("suggestion_node", "voice_node")
    builder.add_edge("voice_node", END)

    return builder.compile()
