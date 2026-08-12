import requests
import time

start = time.perf_counter()
try:
    response = requests.get("http://10.255.255.1/", timeout=5)
except requests.exceptions.RequestException as e:
    elapsed = time.perf_counter() - start
    print(f"Failed after {elapsed:.2f}s: {type(e).__name__}")

print("Testing with NO timeout (this may take a while)...")
start = time.perf_counter()
try:
    response = requests.get(
        "http://10.255.255.1/"
    )  # nosec B113 - deliberately no timeout, demonstrating the risk
except requests.exceptions.RequestException as e:
    elapsed = time.perf_counter() - start
    print(f"Failed after {elapsed:.2f}s: {type(e).__name__}")
