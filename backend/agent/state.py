from typing import TypedDict, List, Dict, Any, Optional
from backend.models import DecisionEvent, Suggestion


class AgentState(TypedDict, total=False):
    merchant_id: str
    language: Optional[str]
    csv_path: Optional[str]
    csv_data: Optional[str]
    events: Optional[List[DecisionEvent]]
    events_stored: Optional[int]
    failure_patterns: Optional[List[DecisionEvent]]
    personal_bests: Optional[List[DecisionEvent]]
    network_wisdom: Optional[List[Dict[str, Any]]]
    suggestions: Optional[List[Suggestion]]
