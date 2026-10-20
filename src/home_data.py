import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from src.agent import AutoPilotAgent, CloudShieldAgent
from src.clients import get_autopilot_status, get_cloudshield_status
from src.registry import AgentRegistry
from src.versions import current_version, load_versions

TASK_HISTORY_FILE = Path("task_history.csv")

ROUTE_GRAPH = {
    "CloudShield": ["Sentinel"],
    "Sentinel": ["CloudShield", "AutoPilot"],
    "AutoPilot": ["Sentinel"],
}

ROUTE_MAP_SIZE = "4,2"

SYSTEM_CHECKS = {
    "CloudShield": get_cloudshield_status,
    "AutoPilot": get_autopilot_status,
}


def build_agents():
    return [
        CloudShieldAgent("CloudShield"),
        AutoPilotAgent("AutoPilot"),
    ]


def build_registry(agents=None):
    if agents is None:
        agents = build_agents()
    registry = AgentRegistry()
    for agent_id, agent in enumerate(agents, start=1):
        registry.add_agent(agent_id, agent.name)
    return registry


def agents_registered(registry):
    return len(registry.agents)


def _check(name, fetch):
    result = fetch()
    return {
        "name": name,
        "status": result["status"],
        "data": result["data"],
        "checked_at": datetime.now(timezone.utc),
    }


def check_systems(checks=None):
    # Query both systems in parallel.
    if checks is None:
        checks = SYSTEM_CHECKS
    with ThreadPoolExecutor(max_workers=len(checks)) as pool:
        futures = [pool.submit(_check, name, fetch) for name, fetch in checks.items()]
        return [f.result() for f in futures]


def display_status(status):
    return "online" if status == "online" else "not reachable"


def systems_online(checks):
    return sum(1 for c in checks if c["status"] == "online")


def load_task_history(path=TASK_HISTORY_FILE):
    path = Path(path)
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [
            {"urgency": int(row[0]), "task": row[1], "trace_id": row[2]}
            for row in csv.reader(f)
            if len(row) == 3
        ]


def tasks_recorded(rows):
    return len(rows)


URGENCY_LEVELS = range(1, 6)


def urgency_counts(rows):
    # Count recorded tasks per urgency.
    return {
        "Urgency": [str(u) for u in URGENCY_LEVELS],
        "Tasks": [sum(1 for r in rows if r["urgency"] == u) for u in URGENCY_LEVELS],
    }


def tests_passing(version_list=None):
    return current_version(version_list)["tests"]


def route_map_dot(graph=None):
    # Build DOT text with hop labels.
    if graph is None:
        graph = ROUTE_GRAPH
    lines = [
        "graph routes {",
        f'  size="{ROUTE_MAP_SIZE}";',
        "  rankdir=LR;",
        "  node [shape=box];",
    ]
    seen = set()
    for node, neighbours in graph.items():
        for other in neighbours:
            edge = frozenset((node, other))
            if edge in seen:
                continue
            seen.add(edge)
            lines.append(f'  "{node}" -- "{other}" [label="1 hop"];')
    lines.append("}")
    return "\n".join(lines)


def system_healthy():
    # Check Sentinel's own parts load.
    try:
        load_versions()
    except (FileNotFoundError, ValueError):
        return False
    return agents_registered(build_registry()) > 0
