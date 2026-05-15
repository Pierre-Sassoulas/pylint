from typing import Protocol


class P(Protocol):
    def f(self) -> int:
        """Method docstring"""
        ...
