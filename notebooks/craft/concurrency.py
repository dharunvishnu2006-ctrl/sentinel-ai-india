import time
import threading
import multiprocessing
import asyncio
import cProfile
import pstats
import sys

sys.path.insert(0, ".")
from src.orchestrator import Orchestrator  # noqa: E402 - path must be set first


def cpu_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


def run_sequential(workload, count):
    start = time.perf_counter()
    for _ in range(count):
        workload(2_000_000)
    return time.perf_counter() - start


def run_threaded(workload, count):
    start = time.perf_counter()
    threads = []
    for _ in range(count):
        t = threading.Thread(target=workload, args=(2_000_000,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


def run_multiprocess(workload, count):
    start = time.perf_counter()
    processes = []
    for _ in range(count):
        p = multiprocessing.Process(target=workload, args=(2_000_000,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    return time.perf_counter() - start


def io_task_sync(delay=0.1):
    time.sleep(delay)


async def io_task_async(delay=0.1):
    await asyncio.sleep(delay)


def run_sequential_io(count):
    start = time.perf_counter()
    for _ in range(count):
        io_task_sync()
    return time.perf_counter() - start


def run_threaded_io(count):
    start = time.perf_counter()
    threads = []
    for _ in range(count):
        t = threading.Thread(target=io_task_sync)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


async def run_async_io(count):
    start = time.perf_counter()
    tasks = [io_task_async() for _ in range(count)]
    await asyncio.gather(*tasks)
    return time.perf_counter() - start


def profile_orchestrator():
    orch = Orchestrator()
    for i in range(1000):
        orch.add_task((i % 5) + 1, f"Task {i}")


if __name__ == "__main__":
    count = 4

    seq_time = run_sequential(cpu_task, count)
    print(f"Sequential: {seq_time:.4f}s")

    thread_time = run_threaded(cpu_task, count)
    print(f"Threaded:   {thread_time:.4f}s")

    process_time = run_multiprocess(cpu_task, count)
    print(f"Multiprocess: {process_time:.4f}s")

    io_count = 50

    seq_io_time = run_sequential_io(io_count)
    print(f"Sequential I/O: {seq_io_time:.4f}s")

    thread_io_time = run_threaded_io(io_count)
    print(f"Threaded I/O:   {thread_io_time:.4f}s")

    async_io_time = asyncio.run(run_async_io(io_count))
    print(f"Async I/O:      {async_io_time:.4f}s")

    profiler = cProfile.Profile()
    profiler.enable()
    profile_orchestrator()
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(10)
