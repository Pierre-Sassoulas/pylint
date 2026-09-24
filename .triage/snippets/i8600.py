from typing import Generic, TypeVar

T = TypeVar("T")


class Parent(Generic[T]):
    def _foo(self):
        pass


class Child(Parent[T]):
    def _foo(self):
        Parent._foo(self)
