from abc import ABC, abstractmethod
from typing import Literal, overload


class A(ABC):
    @staticmethod
    @abstractmethod
    @overload
    def func(*, b: Literal[True]): ...

    @staticmethod
    @abstractmethod
    @overload
    def func(*, b: Literal[False], p: int): ...

    @staticmethod
    @abstractmethod
    @overload
    def func(*, s: str): ...

    @staticmethod
    @abstractmethod
    def func(*, b=None, p=None, s=None):
        """The implementation"""


class B(A):
    @staticmethod
    @overload
    def func(*, b: Literal[True]): ...

    @staticmethod
    @overload
    def func(*, b: Literal[False], p: int): ...

    @staticmethod
    @overload
    def func(*, s: str): ...

    @staticmethod
    def func(*, b=None, p=None, s=None):
        print(f"Params are '{b}' and '{p}' and {s}.")
