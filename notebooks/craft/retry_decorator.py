import random
import time
from functools import wraps


def retry(times=3, backoff=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait = backoff * (2**attempt)
                    print(f"  attempt {attempt+1} failed: {e}, " f"waiting {wait}s")
                    time.sleep(wait)
            raise RuntimeError("All retries exhausted")

        return wrapper

    return decorator


@retry(times=2, backoff=1)
def flaky_call(agent_name):
    raise ConnectionError(f"{agent_name} call failed")


for name in ["CloudShield", "AutoPilot", "Sentinel"]:
    print(f"{name}:")
    try:
        flaky_call(name)
    except RuntimeError as e:
        print(f"  {e}")


def retry_with_jitter(times=3, backoff=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    base_wait = backoff * (2**attempt)
                    jitter = random.uniform(
                        0, base_wait * 0.5
                    )  # nosec B311 - not security-sensitive, just retry jitter
                    wait = base_wait + jitter
                    print(f"  attempt {attempt+1} failed: {e}, " f"waiting {wait:.2f}s")
                    time.sleep(wait)
            raise RuntimeError("All retries exhausted")

        return wrapper

    return decorator


@retry_with_jitter(times=2, backoff=1)
def flaky_call_jitter(agent_name):
    raise ConnectionError(f"{agent_name} call failed")


for name in ["CloudShield", "AutoPilot", "Sentinel"]:
    print(f"{name}:")
    try:
        flaky_call_jitter(name)
    except RuntimeError as e:
        print(f"  {e}")
