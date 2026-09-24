from collections.abc import Callable
from typing import Protocol


class Proto(Protocol):
    @property
    def fun(self) -> Callable[[int], None] | None: ...


class Class(Proto):
    def fun(self, i: int) -> None:
        print(i)
