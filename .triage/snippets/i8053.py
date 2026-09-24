from typing import Any, cast


class MyDescriptor:
    __slots__ = ("offset", "value")

    def __init__(self, offset: int) -> None:
        self.offset = offset
        self.value = 0

    def __set__(self, instance: Any, value: int) -> None:
        self.value = value

    def __get__(self, instance: Any, owner: Any) -> int:
        return self.value


class Parent:
    __slots__ = ()
    MyParentField = MyDescriptor(0)

    def copy(self) -> "Parent":
        return type(self)()


class Child(Parent):
    __slots__ = ()
    MyChildField = MyDescriptor(1)

    def copy(self) -> "Child":
        return cast(Child, super().copy())


if __name__ == "__main__":
    child = Child()
    child.MyChildField = 0
    child.MyParentField = 0
