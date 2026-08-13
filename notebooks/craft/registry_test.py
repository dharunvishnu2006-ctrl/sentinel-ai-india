import time
import sys

sys.path.insert(0, ".")
from src.registry import AgentRegistry  # noqa: E402 - path must be set first

registry = AgentRegistry()
for i in range(10_000):
    registry.add_agent(i, f"Agent-{i}")

target = 7431

start = time.perf_counter()
name, comparisons_linear = registry.linear_find(target)
time_linear = time.perf_counter() - start

start = time.perf_counter()
name2, comparisons_binary = registry.binary_find(target)
time_binary = time.perf_counter() - start

print(
    f"Linear:  found={name}, comparisons={comparisons_linear}, "
    f"time={time_linear:.6f}s"
)
print(
    f"Binary:  found={name2}, comparisons={comparisons_binary}, "
    f"time={time_binary:.6f}s"
)

new_registry = AgentRegistry()

start = time.perf_counter()
for i in range(1000):
    new_registry.add_agent(i, f"Agent-{i}")
time_insert = time.perf_counter() - start

print(f"Inserting 1000 agents (with re-sort each time): " f"{time_insert:.4f}s")

big_registry = AgentRegistry()

start = time.perf_counter()
for i in range(10_000):
    big_registry.add_agent(i, f"Agent-{i}")
time_insert_big = time.perf_counter() - start

print(f"Inserting 10,000 agents (with re-sort each time): " f"{time_insert_big:.4f}s")
