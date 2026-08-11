import time
import numpy as np
import pandas as pd
import random

response_times = [float(i % 500) for i in range(1_000_000)]


def python_average(values):
    total = 0
    for t in values:
        total += t
    return total / len(values)


start = time.perf_counter()
avg_python = python_average(response_times)
time_python = time.perf_counter() - start
print(f"Python loop:  {time_python:.4f}s, avg={avg_python:.2f}")

arr = np.array(response_times)

start = time.perf_counter()
avg_numpy = arr.mean()
time_numpy = time.perf_counter() - start
print(f"NumPy mean:   {time_numpy:.4f}s, avg={avg_numpy:.2f}")

print(f"Speedup: {time_python / time_numpy:.1f}x")

sla = 300
breaches = arr[arr > sla]
print("Number of breaches:", len(breaches))
print("First 5 breach values:", breaches[:5])

random.seed(42)

agents_list = ["CloudShield", "AutoPilot", "Sentinel"]
statuses = ["done", "failed", "running"]

task_log = pd.DataFrame(
    {
        "task_id": range(1, 21),
        "agent": [random.choice(agents_list) for _ in range(20)],  # nosec B311
        "response_ms": [random.randint(50, 600) for _ in range(20)],  # nosec B311
        "status": [random.choice(statuses) for _ in range(20)],  # nosec B311
    }
)

print(task_log)

slow_tasks = task_log[task_log["response_ms"] > 400]
print("Slow tasks (>400ms):")
print(slow_tasks)

failed_tasks = task_log[task_log["status"] == "failed"]
print("\nFailed tasks:")
print(failed_tasks)

cloudshield_tasks = task_log[task_log["agent"] == "CloudShield"]
print("\nCloudShield tasks:")
print(cloudshield_tasks)

per_agent = task_log.groupby("agent")["response_ms"].agg(["mean", "count", "max"])
print("\nPer-agent stats:")
print(per_agent)

agent_info = pd.DataFrame(
    {
        "agent": ["CloudShield", "AutoPilot", "Sentinel"],
        "region": ["us-east", "us-west", "ap-south"],
        "tier": ["premium", "standard", "premium"],
    }
)

print(agent_info)

merged = task_log.merge(agent_info, on="agent")
print("\nMerged (tasks + agent info):")
print(merged.head(10))

print("\nColumn types:")
print(merged.dtypes)
