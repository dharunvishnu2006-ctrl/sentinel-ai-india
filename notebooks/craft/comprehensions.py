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


slow_names_loop = []
for a in agents:
    if a.avg_ms > 200:
        slow_names_loop.append(a.name)

slow_names_comp = [a.name for a in agents if a.avg_ms > 200]

print("Loop version:", slow_names_loop)
print("Comprehension:", slow_names_comp)

doubled_loop = []
for a in agents:
    doubled_loop.append(a.avg_ms * 2)

doubled_comp = [a.avg_ms * 2 for a in agents]

print("Loop version:", doubled_loop)
print("Comprehension:", doubled_comp)


labels_loop = []
for a in agents:
    if a.avg_ms < 300:
        labels_loop.append(f"{a.name}: {a.avg_ms}ms")

labels_comp = [f"{a.name}: {a.avg_ms}ms" for a in agents if a.avg_ms < 300]

print("Loop version:", labels_loop)
print("Comprehension:", labels_comp)
