"""Regression test for https://github.com/pylint-dev/pylint/issues/8074.

Once the function was called with a list, the result of a later call
returning a dict was reported as ``not-a-mapping``.
"""

# pylint: disable=use-dict-literal

from typing import TypeVar, cast

T = TypeVar("T")


def ident(thing: T) -> T:
    """Return thing."""
    return cast(T, thing)


_ = ident([])
dict(**ident({}))
