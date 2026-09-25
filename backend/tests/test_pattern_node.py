import pytest
from backend.agent.nodes.ingest_node import ingest_node
from backend.agent.nodes.pattern_node import pattern_node


@pytest.mark.asyncio
async def test_pattern_node_buckets():
    # Ensure merchant data is ingested
    await ingest_node({"merchant_id": "merchant_001"})

    # Run pattern_node
    result = await pattern_node({"merchant_id": "merchant_001"})

    assert "failure_patterns" in result
    assert "personal_bests" in result
    assert "network_wisdom" in result

    # Verify failure patterns (e.g. week 3 discount)
    failure_patterns = result["failure_patterns"]
    assert len(failure_patterns) >= 1
    discount_fail = next((p for p in failure_patterns if p.decision_type == "discount"), None)
    assert discount_fail is not None
    assert discount_fail.outcome == "negative"

    # Verify personal bests (e.g. week 6 hours extension)
    personal_bests = result["personal_bests"]
    assert len(personal_bests) >= 1
    hours_pb = next((p for p in personal_bests if p.decision_type == "hours"), None)
    assert hours_pb is not None
    assert hours_pb.outcome == "positive"
    assert hours_pb.revenue_delta > 15.0

    # Verify network wisdom
    network_wisdom = result["network_wisdom"]
    assert len(network_wisdom) >= 2
    for item in network_wisdom:
        assert item.get("source") == "network"
