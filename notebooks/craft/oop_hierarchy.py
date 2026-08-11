class BaseAgent:
    def __init__(self, name):
        self.name = name

    def handle(self, message):
        raise NotImplementedError


class CloudShieldAgent(BaseAgent):
    def handle(self, message):
        print(f"[{self.name}] Security alert: {message}")


class AutoPilotAgent(BaseAgent):
    def handle(self, message):
        print(f"[{self.name}] Dataset event: {message}")


class SentinelAgent(BaseAgent):
    def handle(self, message):
        print(f"[{self.name}] Routing decision: {message}")


agents = [
    CloudShieldAgent("CloudShield"),
    AutoPilotAgent("AutoPilot"),
]

for a in agents:
    a.handle("test message")


agents.append(SentinelAgent("Sentinel"))

for a in agents:
    a.handle("test message")


class AgentFactory:
    _registry = {
        "cloudshield": CloudShieldAgent,
        "autopilot": AutoPilotAgent,
        "sentinel": SentinelAgent,
    }

    @staticmethod
    def create(kind, name):
        agent_class = AgentFactory._registry.get(kind)
        if agent_class is None:
            raise ValueError(f"Unknown agent kind: {kind!r}")
        return agent_class(name)


agent_configs = [
    {"kind": "cloudshield", "name": "CloudShield"},
    {"kind": "autopilot", "name": "AutoPilot"},
    {"kind": "sentinel", "name": "Sentinel"},
]

built_agents = [AgentFactory.create(cfg["kind"], cfg["name"]) for cfg in agent_configs]

for a in built_agents:
    print(type(a).__name__, "-", a.name)


def route_by_bfs(graph, start, goal):
    return f"BFS route from {start} to {goal}"


def route_by_dijkstra(graph, start, goal):
    return f"Dijkstra route from {start} to {goal}"


class Router:
    def __init__(self, strategy):
        self.strategy = strategy

    def find_route(self, graph, start, goal):
        return self.strategy(graph, start, goal)


r1 = Router(route_by_bfs)
r2 = Router(route_by_dijkstra)

print(r1.find_route({}, "CloudShield", "AutoPilot"))
print(r2.find_route({}, "CloudShield", "AutoPilot"))
