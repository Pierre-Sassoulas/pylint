from typing import TypeAlias, TypeVar

T = TypeVar("T")

Alias1: TypeAlias = list[T]
Alias2: TypeAlias = "list[T]"

x1: Alias1[int]
x2: Alias2[int]
