from collections.abc import Callable
from functools import wraps


def cast_to_str(func) -> Callable[..., str]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return str(func(*args, **kwargs))

    return wrapper


@cast_to_str
def get_num() -> int:
    return 5


get_num().strip()
