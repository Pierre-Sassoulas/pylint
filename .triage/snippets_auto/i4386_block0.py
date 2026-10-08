# pylint:disable=missing-docstring
from __future__ import annotations
import functools
from typing import Callable, Union


def variadic(func: Callable[[int], int]):
    @functools.wraps(func)
    def wrapped(*integers: int) -> Union[int, tuple[int, ...]]:
        result = tuple(func(i) for i in integers)
        return result[0] if len(result) == 1 else result

    return wrapped


@variadic
def double(integer: int) -> int:
    return integer * 2


def main():
    doubled = double(1, 2, 3)  # false positive too-many-function-args
    print(doubled)


if __name__ == "__main__":
    main()

