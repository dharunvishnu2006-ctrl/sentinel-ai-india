import time
import sys

sys.path.insert(0, ".")  # noqa: E402
from src.hashtable import HashTable, BrokenHashTable  # noqa: E402

N = 10_000

capability_cache = HashTable()
for i in range(N):
    capability_cache.put(f"agent-{i}", f"capability-set-{i % 5}")

target = "agent-7431"

start = time.perf_counter()
result_hash = capability_cache.get(target)
time_hash = time.perf_counter() - start

agents_list = [(f"agent-{i}", f"capability-set-{i % 5}") for i in range(N)]

start = time.perf_counter()
result_scan = None
for k, v in agents_list:
    if k == target:
        result_scan = v
        break
time_scan = time.perf_counter() - start

print(f"Hash table get(): {time_hash:.8f}s, result={result_hash}")
print(f"Full scan:        {time_scan:.8f}s, result={result_scan}")

broken_cache = BrokenHashTable()
for i in range(N):
    broken_cache.put(f"agent-{i}", f"capability-set-{i % 5}")

start = time.perf_counter()
result_broken = broken_cache.get(target)
time_broken = time.perf_counter() - start

print(f"Broken hash get(): {time_broken:.8f}s, result={result_broken}")

py_dict: dict = {}
start = time.perf_counter()
for i in range(N):
    py_dict[f"agent-{i}"] = f"capability-set-{i % 5}"
time_dict_build = time.perf_counter() - start

start = time.perf_counter()
result_dict = py_dict.get(target)
time_dict_get = time.perf_counter() - start

print(f"dict build: {time_dict_build:.6f}s")
print(f"dict get(): {time_dict_get:.8f}s, result={result_dict}")
