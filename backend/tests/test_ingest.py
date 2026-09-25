import pytest
from backend.agent.nodes.ingest_node import ingest_node
from backend.memory.cognee_client import cognee_client


@pytest.mark.asyncio
async def test_ingest_node_stores_events():
    # Run ingest for merchant_001
    result = await ingest_node({"merchant_id": "merchant_001"})
    
    assert "events_stored" in result
    assert result["events_stored"] >= 3

    # Check Cognee graph nodes
    events = cognee_client.get_events("merchant_001")
    assert len(events) >= 3

    # Verify key decision patterns are present
    decision_types = {e.decision_type for e in events}
    assert "discount" in decision_types
    assert "hours" in decision_types
    assert "inventory" in decision_types

    # Verify outcomes and deltas
    discount_event = next(e for e in events if e.decision_type == "discount")
    assert discount_event.outcome == "negative"
    assert discount_event.revenue_delta < 0

    hours_event = next(e for e in events if e.decision_type == "hours")
    assert hours_event.outcome == "positive"
    assert hours_event.revenue_delta > 15.0
