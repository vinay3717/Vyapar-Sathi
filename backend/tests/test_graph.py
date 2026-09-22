import pytest
from backend.main import app, lifespan
from backend.agent.graph import build_graph


@pytest.mark.asyncio
async def test_graph_compilation_and_invocation():
    async with lifespan(app):
        assert app.state.graph is not None
        
        # Invoke compiled graph for merchant_001
        result = await app.state.graph.ainvoke({"merchant_id": "merchant_001"})
        
        assert "events" in result or "failure_patterns" in result
        assert "suggestions" in result
        suggestions = result["suggestions"]
        assert len(suggestions) == 3
        
        types = {s.type for s in suggestions}
        assert types == {"failure_guard", "personal_best", "network_wisdom"}
