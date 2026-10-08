"""This is example.py."""

from unittest.mock import Mock
from dataclasses import dataclass
from typing import Callable


# If the following line is commented out, the problem goes away
Mock().example = 123


@dataclass
class _SomeClass:
    example: Callable[[int], int]


def _some_method(x: int) -> int:
    return x


def _unhinted_mock() -> None:
    unhinted_mock = Mock()
    unhinted_mock.example.return_value = 123
    unhinted_mock.example(123) # Should be callable because can deduce it's a Mock


def _hinted_mock() -> None:
    hinted_as_mock: Mock = Mock()
    hinted_as_mock.example.return_value = 123
    hinted_as_mock.example(123) # Should be callable because hinted as a Mock


def _mock_hinted_as_class() -> None:
    hinted_as_class: _SomeClass = Mock()
    hinted_as_class.example.return_value = 123 # Ok because it's really a mock, but goes against type hint
    hinted_as_class.example(123) # Should be callable because hinted as class with this method


def _actual_class() -> None:
    thing: _SomeClass = _SomeClass(_some_method)
    thing.example.return_value = 123  # Should be flagged, not a Mock and no such method on Callable.
    thing.example(123)
