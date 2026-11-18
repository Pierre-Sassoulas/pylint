# pylint: disable=missing-docstring,too-few-public-methods

from abc import ABC, abstractmethod


class MyABC(ABC):
    @abstractmethod
    def do_something(self):
        print("Some implementation!")


class MyConcrete(MyABC):
    def do_something(self):
        super().do_something()
