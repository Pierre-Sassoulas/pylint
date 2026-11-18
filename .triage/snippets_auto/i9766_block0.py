"""Repro code."""
# pylint: disable=undefined-variable
import abc
from typing import Generic, override, TypeVar
T = TypeVar("T")

class AbstractClass(abc.ABC, Generic[T]):
    """Abstract class."""
    @abc.abstractmethod
    def method(self) -> T:
        """Abstract method."""

class Subclass(AbstractClass[foo]):
    """Concrete class."""
    @override
    def method(self) -> foo:
        return 42
