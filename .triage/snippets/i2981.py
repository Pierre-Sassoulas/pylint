from typing import Generic, TypeVar

T = TypeVar("T")


class Base(Generic[T]):
    def __init__(self):
        self.val = False


class Derived(Base[T]):
    def func(self):
        self.val = True


a = Derived()
a.func()
print(a.val)
