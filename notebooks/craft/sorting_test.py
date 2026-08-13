import random
import time
import sys

sys.path.insert(0, ".")  # noqa: E402
from src.sorting import (  # noqa: E402
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    counting_sort,
)

random.seed(1)

algorithms = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
    "timsort (sorted())": sorted,
}

for size in [1_000, 5_000]:
    data = [random.randint(0, 100_000) for _ in range(size)]  # nosec B311
    print(f"\n--- n={size}, random order ---")
    for name, func in algorithms.items():
        start = time.perf_counter()
        func(data)  # type: ignore[operator]
        elapsed = time.perf_counter() - start
        print(f"{name:20s} {elapsed:.4f}s")

print("\n--- n=1000, NEARLY SORTED ---")
nearly_sorted = list(range(1000))
nearly_sorted[500], nearly_sorted[501] = (nearly_sorted[501], nearly_sorted[500])

for name, func in algorithms.items():
    try:
        start = time.perf_counter()
        func(nearly_sorted)  # type: ignore[operator]
        elapsed = time.perf_counter() - start
        print(f"{name:20s} {elapsed:.4f}s")
    except RecursionError:
        print(f"{name:20s} CRASHED (RecursionError - worst-case pivot)")


def test_stability():
    agents = [
        ("CloudShield", 200),
        ("AutoPilot", 100),
        ("Sentinel", 200),
        ("Backup", 100),
    ]
    sorted_agents = sorted(agents, key=lambda a: a[1])
    print(sorted_agents)


test_stability()

random.seed(2)
urgencies = [random.randint(1, 5) for _ in range(100_000)]  # nosec B311

start = time.perf_counter()
result_counting = counting_sort(urgencies, max_value=5)
time_counting = time.perf_counter() - start

start = time.perf_counter()
result_builtin = sorted(urgencies)
time_builtin = time.perf_counter() - start

print(f"Counting sort: {time_counting:.4f}s")
print(f"Built-in sorted(): {time_builtin:.4f}s")
print(f"Results match: {result_counting == result_builtin}")
