from typing import ClassVar


class C:
    __slots__ = ("value",)

    def __init__(self, value: int):
        self.value = value

    x: ClassVar[int]
    y: ClassVar[int] = 2
    z = 3
