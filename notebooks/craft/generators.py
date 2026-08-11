import os
import time
import tracemalloc
from pathlib import Path


def make_test_file(path, num_lines=1_000_000):
    with open(path, "w", encoding="utf-8") as f:
        for i in range(num_lines):
            f.write(f"log line {i}\n")


test_path = Path("notebooks/craft/big_log.txt")
if not test_path.exists():
    print("Generating test file...")
    make_test_file(test_path)
    print("Done.")


def read_all(path):
    lines = []
    with open(path) as f:
        for line in f:
            lines.append(line)
    return lines


def read_lazy(path):
    with open(path) as f:
        for line in f:
            yield line


start = time.perf_counter()
result_all = read_all(test_path)
elapsed_all = time.perf_counter() - start
print(f"read_all() call took: {elapsed_all:.4f}s")

start = time.perf_counter()
result_lazy = read_lazy(test_path)
elapsed_lazy = time.perf_counter() - start
print(f"read_lazy() call took: {elapsed_lazy:.4f}s")

start = time.perf_counter()
count = 0
for line in result_lazy:
    count += 1
elapsed_iterate = time.perf_counter() - start
print(f"Iterating read_lazy() result took: {elapsed_iterate:.4f}s")
print(f"Total lines: {count}")

tracemalloc.start()
all_lines = read_all(test_path)
current, peak_all = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"read_all() peak memory: {peak_all / 1_000_000:.2f} MB")

tracemalloc.start()
count = 0
for line in read_lazy(test_path):
    count += 1
current, peak_lazy = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"read_lazy() peak memory: {peak_lazy / 1_000_000:.2f} MB")

logs_dir = Path("notebooks/craft/test_logs")

for subfolder in ["cloudshield", "autopilot", "sentinel"]:
    folder = logs_dir / subfolder
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{subfolder}.log").write_text("test log entry\n")

found_logs = list(logs_dir.glob("**/*.log"))
print("Found log files:")
for log_file in found_logs:
    print(" -", log_file)


def atomic_write(path, content):
    temp_path = str(path) + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(content)
    os.replace(temp_path, path)


config_path = Path("notebooks/craft/config.txt")
atomic_write(config_path, "version=1.1\nstatus=active\n")
print("Written safely:", config_path.read_text())

config_path.write_text("version=1.0\nstatus=stable\n")
print("Before crash simulation:", config_path.read_text())

try:
    temp_path = str(config_path) + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write("version=2.0\n")
        raise RuntimeError("Simulated crash mid-write!")
        f.write("status=active\n")
except RuntimeError as e:
    print("Crash occurred:", e)

print("After crash simulation:", config_path.read_text())
