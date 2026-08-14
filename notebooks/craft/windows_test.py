import time
import random
import sys
from src.windows import (
    SlidingWindowAverage,
    SegmentTree,
    next_greater_element,
    align_event_streams,
)  # noqa: E402

sys.path.insert(0, ".")  # noqa: E402

random.seed(4)
N = 10_000
values = [random.randint(50, 600) for _ in range(N)]  # nosec B311

start = time.perf_counter()
sw = SlidingWindowAverage(window_size=50)
for v in values:
    sw.add(v)
    _ = sw.average()
time_sliding = time.perf_counter() - start


def naive_rolling_average(values, window_size=50):
    window = []
    results = []
    for v in values:
        window.append(v)
        if len(window) > window_size:
            window.pop(0)
        results.append(sum(window) / len(window))
    return results


start = time.perf_counter()
naive_rolling_average(values, window_size=50)
time_naive = time.perf_counter() - start

print(f"Sliding window: {time_sliding:.4f}s")
print(f"Naive (sum each time): {time_naive:.4f}s")

start = time.perf_counter()
sw_big = SlidingWindowAverage(window_size=5000)
for v in values:
    sw_big.add(v)
    _ = sw_big.average()
time_sliding_big = time.perf_counter() - start

start = time.perf_counter()
naive_rolling_average(values, window_size=5000)
time_naive_big = time.perf_counter() - start

print(f"Sliding window (window=5000): {time_sliding_big:.4f}s")
print(f"Naive (window=5000): {time_naive_big:.4f}s")

response_times = [120, 340, 89, 560, 210, 45, 670, 130]
seg_tree = SegmentTree(response_times)

print("Max in range [0,3]:", seg_tree.query_max(0, 3))
print("Max in range [4,7]:", seg_tree.query_max(4, 7))

seg_tree.update(2, 999)
print("After update, max in [0,3]:", seg_tree.query_max(0, 3))

response_times = [120, 340, 89, 560, 210, 45, 670, 130]
next_greater = next_greater_element(response_times)
print("Next greater for each:", list(zip(response_times, next_greater)))

random.seed(5)

stream_a = sorted(random.sample(range(100_000), 5000))  # nosec B311
stream_b = sorted(random.sample(range(100_000), 5000))  # nosec B311

start = time.perf_counter()
aligned_two_pointer = align_event_streams(stream_a, stream_b, max_gap=2)
time_two_pointer = time.perf_counter() - start


def nested_loop_align(a, b, max_gap=2):
    aligned = []
    for x in a:
        for y in b:
            if abs(x - y) <= max_gap:
                aligned.append((x, y))
                break
    return aligned


start = time.perf_counter()
aligned_nested = nested_loop_align(stream_a, stream_b, max_gap=2)
time_nested = time.perf_counter() - start

print(f"Two pointers: {len(aligned_two_pointer)} pairs, {time_two_pointer:.4f}s")
print(f"Nested loop:  {len(aligned_nested)} pairs, {time_nested:.4f}s")
