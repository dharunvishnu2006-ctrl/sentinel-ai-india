import logging
import random
import time
from functools import wraps

logger = logging.getLogger(f"sentinel.{__name__}")


def retry(times=3, backoff=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    base_wait = backoff * (2**attempt)
                    jitter = random.uniform(0, base_wait * 0.5)  # nosec B311
                    wait = base_wait + jitter
                    logger.warning(
                        f"{func.__name__} attempt {attempt+1} "
                        f"failed: {e}, waiting {wait:.2f}s"
                    )
                    time.sleep(wait)
            raise RuntimeError(f"{func.__name__}: all retries exhausted")

        return wrapper

    return decorator
