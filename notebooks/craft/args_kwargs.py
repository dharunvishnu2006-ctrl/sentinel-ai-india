import time
from functools import wraps


def show_args(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)


show_args(3, 5)
show_args(3, 5, greeting="Hello", loud=True)


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result

    return wrapper


@timed
def add(a, b):
    return a + b


@timed
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(add(3, 5))
print(greet("Dharun", greeting="Vanakkam"))
