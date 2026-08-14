import sys

sys.path.insert(0, ".")  # noqa: E402
from src.assign import Agent, greedy_assign, backtracking_assign  # noqa: E402

agent_a = Agent("A", {"scan", "deploy"})
agent_b = Agent("B", {"scan"})

tasks = [
    ("task1", "scan"),
    ("task2", "deploy"),
]

result = greedy_assign(tasks, [agent_a, agent_b])
print("Greedy assignment:", result)

result_bt = backtracking_assign(tasks, [agent_a, agent_b])
print("Backtracking assignment:", result_bt)
