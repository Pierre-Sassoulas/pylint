import typing


class A(typing.TypedDict):
    a: int


class B(typing.TypedDict):
    b: int


class ABC(A, B):
    c: int


class ABCD(ABC):
    d: int
