import pytest
from datetime import datetime, timezone
from src.agent import CloudShieldAgent
from src.orchestrator import Orchestrator, UrgencyCheck
from src.routing import shortest_path
from unittest.mock import patch, MagicMock
from src.clients import get_cloudshield_status
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_agent_receives_valid_message():

    agent = CloudShieldAgent("TestAgent")
    await agent.inbox.put(
        {
            "id": 1,
            "urgency": 2,
            "name": "test task",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )

    msg = await agent.receive()
    assert msg is not None
    assert msg.name == "test task"


def test_orchestrator_priority_order():
    orch = Orchestrator()
    orch.add_task(3, "Routine report")
    orch.add_task(1, "Security breach!")
    orch.add_task(2, "Dataset profiling done")

    first = orch.next_task()
    assert first[0] == 1


def test_bfs_finds_shortest_path():
    graph = {
        "CloudShield": ["Sentinel"],
        "Sentinel": ["CloudShield", "AutoPilot"],
        "AutoPilot": ["Sentinel"],
    }
    path = shortest_path(graph, "CloudShield", "AutoPilot")
    assert path == ["CloudShield", "Sentinel", "AutoPilot"]


def test_unified_status_aggregates():
    from src.api import app

    client = app.test_client()
    response = client.get("/status")
    data = response.get_json()

    assert "cloudshield" in data
    assert "autopilot" in data


def test_no_path_handled():
    graph = {
        "CloudShield": ["Sentinel"],
        "Sentinel": ["CloudShield", "AutoPilot"],
        "AutoPilot": ["Sentinel"],
    }
    path = shortest_path(graph, "CloudShield", "UnknownAgent")
    assert path == []


@pytest.mark.parametrize(
    "urgency,should_pass",
    [
        (1, True),
        (3, True),
        (5, True),
        (0, False),
        (-5, False),
        (6, False),
        (99, False),
    ],
)
def test_urgency_validation(urgency, should_pass):
    if should_pass:
        check = UrgencyCheck(urgency=urgency)
        assert check.urgency == urgency
    else:
        with pytest.raises(ValidationError):
            UrgencyCheck(urgency=urgency)


def test_cloudshield_status_online():
    mock_response = MagicMock()
    mock_response.json.return_value = {"alerts_count": 5, "timestamp": "2026-08-12"}
    mock_response.raise_for_status.return_value = None

    with patch("src.clients.requests.get", return_value=mock_response):
        result = get_cloudshield_status()

    assert result["status"] == "online"
    assert result["data"]["alerts_count"] == 5


def test_cloudshield_status_degraded():
    with patch(
        "src.clients.requests.get",
        side_effect=ConnectionError("simulated failure"),
    ):
        result = get_cloudshield_status()

    assert result["status"] == "degraded"
    assert result["data"] is None


@pytest.fixture
def fresh_orchestrator():
    return Orchestrator()


def test_orchestrator_starts_empty(fresh_orchestrator):
    assert fresh_orchestrator.next_task() is None


def test_orchestrator_single_task(fresh_orchestrator):
    fresh_orchestrator.add_task(2, "one task")
    task = fresh_orchestrator.next_task()
    assert task[0] == 2
    assert task[2] == "one task"
