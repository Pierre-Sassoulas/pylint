
"""My module docstring."""
from collections.abc import Sized
from typing import Protocol, TypeVar

from typing_extensions import override, TypeAlias

# pylint: disable=too-few-public-methods

T = TypeVar("T")
V = TypeVar("V")


class MyClass(Sized, Protocol[T, V]):
    """My class docstring."""

    def my_method(self):
        """My docstring."""
        ...  # unnecessary-ellipse, but this is used as implementation "placeholder"


# unsubscriptable-object, but inherits from Generic Protocol
class MySubclass(MyClass[T, V]):
    """My class docstring."""

    def __len__(self) -> int:
        return 0

    @override
    def my_method(self):  # missing-function-docstring, but overrides MyClass
        return


# --------------------------------------------------------------------------- #
class AnotherClass(Protocol[T, V]):
    """My class docstring."""


MyAlias: TypeAlias = AnotherClass[T, int]

foobar = MyAlias[
    bool
]  # unsubscriptable-object, but just aliased the generic type variable above
