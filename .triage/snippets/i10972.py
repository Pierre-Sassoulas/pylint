from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Base(Generic[T], ABC):
    @abstractmethod
    def get_item(self) -> T: ...


class Middle[NpDtype, *Shape]:
    def get_item(self) -> NpDtype:
        raise NotImplementedError


class Concrete[NpDtype, *Shape](Middle[NpDtype, *Shape], Base[NpDtype]):
    """All abstract methods are satisfied via Middle."""


obj = Concrete()
