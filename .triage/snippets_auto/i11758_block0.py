"""Generic NamedTuple with PEP 695 syntax."""
from typing import NamedTuple


class Pair[T](NamedTuple):
    """A pair."""
    first: T
    second: T

    def swap(self) -> "Pair[T]":
        """Swap."""
        return Pair(self.second, self.first)


p = Pair(1, 2)
print(p.first + p.second, p._replace(first=3), Pair._fields, p.swap(), p[0])
IntPair = Pair[int]
print(IntPair(3, 4), len(p), p._asdict())
x, y = p
print(x, y)
