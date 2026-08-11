class AgentStat:
    def __init__(self, name, avg_ms):
        self.name = name
        self.avg_ms = avg_ms

    def __repr__(self):
        return f"AgentStat({self.name}, {self.avg_ms}ms)"


agents = [
    AgentStat("CloudShield", 250),
    AgentStat("AutoPilot", 90),
    AgentStat("Sentinel", 400),
]

sorted_agents = sorted(agents, key=lambda a: a.avg_ms)
print(sorted_agents)
