"""Minimal protocol example."""
from typing import TYPE_CHECKING, Protocol

class Example(Protocol):
    """Example protocol."""
    def ordinary(self) -> int:
        """An ordinary protocol method."""
        ...

    if TYPE_CHECKING:
        def static_only(self) -> int:
            """A static-only protocol method."""
            ...
