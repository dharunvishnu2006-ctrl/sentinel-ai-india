import sys
import time
import random

sys.path.insert(0, ".")
from src.capacity import (  # noqa: E402
    SCAN,
    ROUTE,
    DEPLOY,
    can_handle,
    brute_force_knapsack,
    knapsack_dp,
    urgency_order_selection,
)

agent = SCAN | ROUTE
task = SCAN | ROUTE

print(f"Agent mask: {bin(agent)}")
print(f"Task mask:  {bin(task)}")
print(f"AND result: {bin(agent & task)}")
print(f"Can handle: {can_handle(agent, task)}")

task_needs_deploy = SCAN | DEPLOY
print(f"Can handle deploy task: {can_handle(agent, task_needs_deploy)}")

random.seed(6)


def make_tasks(n):
    return [
        (random.randint(1, 20), random.randint(10, 100)) for _ in range(n)  # nosec B311
    ]


for n in [10, 15, 20, 22]:
    tasks = make_tasks(n)
    start = time.perf_counter()
    value, chosen = brute_force_knapsack(tasks, capacity=50)
    elapsed = time.perf_counter() - start
    print(f"n={n}: best_value={value}, time={elapsed:.4f}s")

random.seed(6)
tasks_20 = make_tasks(20)

start = time.perf_counter()
dp_value, dp_chosen = knapsack_dp(tasks_20, capacity=50)
time_dp = time.perf_counter() - start

print(f"DP:    best_value={dp_value}, time={time_dp:.6f}s")

random.seed(6)
tasks_10 = make_tasks(10)
tasks_15 = make_tasks(15)
tasks_20_from_loop = make_tasks(20)

random.seed(6)
tasks_20_standalone = make_tasks(20)

print("Same tasks?", tasks_20_from_loop == tasks_20_standalone)

random.seed(7)
comparison_tasks = make_tasks(18)

start = time.perf_counter()
bf_value, bf_chosen = brute_force_knapsack(comparison_tasks, capacity=50)
time_bf = time.perf_counter() - start

start = time.perf_counter()
dp_value, dp_chosen = knapsack_dp(comparison_tasks, capacity=50)
time_dp2 = time.perf_counter() - start

print(f"Brute force: value={bf_value}, time={time_bf:.4f}s")
print(f"DP:          value={dp_value}, time={time_dp2:.6f}s")
print(f"Values match: {bf_value == dp_value}")

urgency_value, urgency_chosen = urgency_order_selection(comparison_tasks, capacity=50)

print(f"DP (optimal):     value={dp_value}")
print(f"Urgency order:    value={urgency_value}")
print(f"Gap: DP found {dp_value - urgency_value} more value")
