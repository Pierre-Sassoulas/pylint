from collections.abc import Iterable


def gen(values: Iterable[int] | None) -> Iterable[int]:
    if values is None:
        return []
    return values


def use():
    for x in gen([1, 2, 3]):
        print(x)
