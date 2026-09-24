from typing import TypedDict


class ADict(TypedDict):
    a: int


def f() -> None:
    x: ADict | None = None
    while x is None or "a" in x:
        print("test")
