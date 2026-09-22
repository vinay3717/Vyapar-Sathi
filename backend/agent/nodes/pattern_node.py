from typing import Dict, Any
from backend.agent.state import AgentState
from backend.memory.cognee_client import cognee_client


async def pattern_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node: queries Cognee graph for merchant_id.
    Segments decision history into failure patterns, personal bests, and network wisdom.
    """
    merchant_id = state.get("merchant_id", "merchant_001")
    patterns = cognee_client.query_patterns(merchant_id)

    return {
        "failure_patterns": patterns.get("failure_patterns", []),
        "personal_bests": patterns.get("personal_bests", []),
        "network_wisdom": patterns.get("network_wisdom", []),
    }
