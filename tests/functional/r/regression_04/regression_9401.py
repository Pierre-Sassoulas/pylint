"""Regression test for https://github.com/pylint-dev/pylint/issues/9401.

``P.args`` and ``P.kwargs`` were reported as ``no-member`` on Python 3.12.
"""

from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def call(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """Call func."""
    return func(*args, **kwargs)
