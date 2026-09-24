from typing import overload

type Alias[T] = T | list[T]


def identity[T](x: T) -> T:
    return x


@overload
def process(x: str) -> str: ...
@overload
def process[T](x: list[T]) -> T: ...
def process[T](x):
    if isinstance(x, list):
        return x[0]
    return x
