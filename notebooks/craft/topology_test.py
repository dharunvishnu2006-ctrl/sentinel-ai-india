import sys

sys.path.insert(0, ".")  # noqa: E402
from src.topology import UnionFind, topological_sort  # noqa: E402

agents = ["Agent1", "Agent2", "Agent3", "Agent4", "Agent5", "Agent6"]
uf = UnionFind(agents)

uf.union("Agent1", "Agent2")
uf.union("Agent2", "Agent3")
uf.union("Agent4", "Agent5")

domains: dict = {}
for agent in agents:
    root = uf.find(agent)
    domains.setdefault(root, []).append(agent)

print("Failure domains:")
for root, members in domains.items():
    print(f"  {root}: {members}")

dependencies = {
    "deploy": ["build"],
    "build": [],
    "test": ["build"],
}

order = topological_sort(dependencies)
print("Safe execution order:", order)

cyclic_dependencies = {
    "deploy": ["build"],
    "build": ["test"],
    "test": ["deploy"],
}

cyclic_order = topological_sort(cyclic_dependencies)
print("Cyclic order result:", cyclic_order)
