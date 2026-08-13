import pytest
from datetime import datetime, timezone
from src.agent import CloudShieldAgent
from src.orchestrator import Orchestrator, UrgencyCheck
from src.routing import shortest_path
from unittest.mock import patch, MagicMock
from src.clients import get_cloudshield_status
from pydantic import ValidationError
from src.summarise import verify_summary
from src.registry import AgentRegistry, min_capacity_that_fits
from src.sorting import counting_sort
from src.history import SinglyLinkedList, RecentActionsCache, UndoStack
from src.hashtable import HashTable, BrokenHashTable
from src.tree import BST, AVLTree
from src.routing_advanced import (
    bfs_shortest_path,
    dijkstra,
    bellman_ford,
    floyd_warshall,
)


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


def test_verify_summary_catches_fabricated_agent():
    events = [
        {"agent": "CloudShield", "kind": "info", "payload": "12 alerts detected"},
    ]
    known_agents = {"CloudShield", "AutoPilot", "Sentinel"}
    fabricated = (
        "CloudShield reported 12 alerts, with AutoPilot handling "
        "the overflow smoothly."
    )
    result = verify_summary(fabricated, events, known_agents)
    assert result["verified"] is False
    assert "AutoPilot" in result["unverified_agents"]


def test_verify_summary_passes_honest_summary():
    events = [
        {"agent": "CloudShield", "kind": "info", "payload": "12 alerts detected"},
    ]
    known_agents = {"CloudShield", "AutoPilot", "Sentinel"}
    honest = "CloudShield reported 12 alerts. No other agents involved."
    result = verify_summary(honest, events, known_agents)
    assert result["verified"] is True


def test_binary_find_matches_linear_find():
    registry = AgentRegistry()
    for i in range(100):
        registry.add_agent(i, f"Agent-{i}")

    linear_result, _ = registry.linear_find(47)
    binary_result, _ = registry.binary_find(47)
    assert linear_result == binary_result == "Agent-47"


def test_min_capacity_that_fits():
    result, checks = min_capacity_that_fits(load=500, max_capacity=1000)
    assert result == 500
    assert checks < 20


def test_counting_sort_matches_builtin():
    data = [3, 1, 4, 1, 5, 2, 3, 1]
    assert counting_sort(data, max_value=5) == sorted(data)


def test_sorted_is_stable():
    agents = [("A", 200), ("B", 100), ("C", 200), ("D", 100)]
    result = sorted(agents, key=lambda a: a[1])
    assert result[0][0] == "B"
    assert result[1][0] == "D"


def test_linked_list_head_insert_order():
    ll = SinglyLinkedList()
    for i in [1, 2, 3]:
        ll.insert_at_head(i)
    assert ll.search(3) == 1
    assert ll.search(1) == 3


def test_recent_actions_cache_eviction():
    cache = RecentActionsCache(capacity=3)
    for i in range(5):
        cache.add_action(i)
    assert cache.walk_forward() == [4, 3, 2]
    assert cache.walk_backward() == [2, 3, 4]


def test_undo_stack_reverses_and_handles_empty():
    stack = UndoStack()
    state = {"value": 1}

    def reverse():
        state["value"] = 1

    state["value"] = 2
    stack.push("set to 2", reverse)
    stack.undo()
    assert state["value"] == 1
    assert stack.undo() is None


def test_hashtable_put_and_get():
    ht = HashTable()
    ht.put("key1", "value1")
    ht.put("key2", "value2")
    assert ht.get("key1") == "value1"
    assert ht.get("key2") == "value2"
    assert ht.get("missing") is None


def test_hashtable_resizes():
    ht = HashTable(size=4)
    for i in range(10):
        ht.put(f"k{i}", i)
    assert ht.size > 4
    assert ht.get("k5") == 5


def test_broken_hash_still_correct_just_slow():
    bht = BrokenHashTable()
    for i in range(50):
        bht.put(f"k{i}", i)
    assert bht.get("k25") == 25


def test_bst_degenerates_on_ascending_input():
    bst = BST()
    for i in range(50):
        bst.insert(i)
    assert bst.depth() == 50


def test_avl_stays_balanced_on_ascending_input():
    avl = AVLTree()
    for i in range(50):
        avl.insert(i)
    assert avl.depth() < 10


def test_dijkstra_beats_bfs_on_weighted_graph():
    graph = {
        "Sentinel": {"A": 250, "X": 30},
        "A": {"Target": 250},
        "X": {"Y": 30},
        "Y": {"Target": 30},
        "Target": {},
    }
    bfs_path = bfs_shortest_path(graph, "Sentinel", "Target")
    dijkstra_path, dijkstra_cost = dijkstra(graph, "Sentinel", "Target")

    assert bfs_path == ["Sentinel", "A", "Target"]
    assert dijkstra_path == ["Sentinel", "X", "Y", "Target"]
    assert dijkstra_cost == 90
    assert dijkstra_cost < 500


def test_bellman_ford_detects_negative_cycle():
    graph = {"A": {"B": 1}, "B": {"C": -2}, "C": {"A": -2}}
    _, has_cycle = bellman_ford(graph, "A")
    assert has_cycle is True


def test_floyd_warshall_matches_dijkstra():
    graph = {
        "Sentinel": {"A": 250, "X": 30},
        "A": {"Target": 250},
        "X": {"Y": 30},
        "Y": {"Target": 30},
        "Target": {},
    }
    table = floyd_warshall(graph)
    _, dijkstra_cost = dijkstra(graph, "Sentinel", "Target")
    assert table["Sentinel"]["Target"] == dijkstra_cost
