from typing import Generic, TypeVar

_T = TypeVar("_T")


class Base(Generic[_T]):
    foo = "test"

    def __class_getitem__(cls, item):
        return super().__class_getitem__(item)


class Derrived(Base[int]): ...


print(Derrived.foo)
