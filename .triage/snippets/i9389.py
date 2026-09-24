from dataclasses import dataclass


@dataclass(init=False, frozen=True)
class A:
    a: str


@dataclass(frozen=True)
class B(A):
    b: str


B("a", "b")
