"""Example of slight wonkiness with type params"""
# pylint: disable=too-few-public-methods

from typing import TypeVar, Generic


# ------------------------------------------------------------------------------
# Using new-style (Python 3.12) template parameters results in a
# complaint about missing docstrings in a method we override.
#
# This complaint seems very dependent on these specific conditions. If
# we disable the empty pylint plugin, take the middle class out of the
# equation, remove the __init__() from the child class, or even switch
# the order of the do_something_* overrides in the child class, the
# complaint goes away.

class BaseClass[T]:
    """A generic class"""

    def do_something(self) -> None:
        """Method meant to be overridden by child classes"""

class MiddleClass[T](BaseClass[T]):
    """Inherits from base generic class"""

    def do_something_2(self) -> None:
        """Method meant to be overridden by child classes"""


class ChildClass(MiddleClass[int]):
    """Concrete subclass of the middle one above"""

    def __init__(self) -> None:
        pass

    # Trying to override base class method results in pylint complaining
    # about a missing docstring.
    def do_something(self) -> None:
        pass

    # Trying to override middle class method does not complain about
    # missing docstring (expected behavior).
    def do_something_2(self) -> None:
        pass


# ------------------------------------------------------------------------------
# If we define the equivalent setup using old style TypeVar/Generic, we
# get no missing-docstring complaints.

T = TypeVar('T')

class BaseClassOld(Generic[T]):
    """A generic class using old-style type-vars"""

    def do_something(self) -> None:
        """Method meant to be overridden by child classes"""

class MiddleClassOld(BaseClassOld[T]):
    """Inherits from base generic class"""

    def do_something_2(self) -> None:
        """Method meant to be overridden by child classes"""


class ChildClassOld(MiddleClassOld[int]):
    """Concrete subclass of the middle one above"""

    def __init__(self) -> None:
        pass

    # In this case, neither method override results in missing-docstring
    # complaints.

    def do_something(self) -> None:
        pass

    def do_something_2(self) -> None:
        pass
