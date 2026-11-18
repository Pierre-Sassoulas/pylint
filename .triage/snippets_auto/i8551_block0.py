"""b.py"""

# pylint: disable=missing-function-docstring

from collections.abc import Iterator
from contextlib import contextmanager

@contextmanager
def some_context_manager() -> Iterator[None]:
    yield
