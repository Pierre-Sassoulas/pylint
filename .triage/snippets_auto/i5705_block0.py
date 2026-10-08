from collections import abc
from typing import TypeVar

_T = TypeVar("_T")

class Data(abc.Iterable[_T]):
    """The _data is in slots."""

    __slots__ = {"_data"}

    def __init__(self, elements):
        """Initialize with `Data` instances."""
        self._data = list(elements)  # E0237: Assigning to attribute '_data' not defined in class slots (assigning-non-slot

class Data(abc.Iterable[int]):
    """The _data is in slots."""

    __slots__ = {"_data"}

    def __init__(self, elements):
        """Initialize with `Data` instances."""
        self._data = list(elements)

class Data(abc.Container[_T]):
    """The _data is in slots."""

    __slots__ = {"_data"}

    def __init__(self, elements):
        """Initialize with `Data` instances."""
        self._data = list(elements)  # E0237: Assigning to attribute '_data' not defined in class slots (assigning-non-slot)

class Data(abc.Container[int]):
    """The _data is in slots."""

    __slots__ = {"_data"}

    def __init__(self, elements):
        """Initialize with `Data` instances."""
        self._data = list(elements)
