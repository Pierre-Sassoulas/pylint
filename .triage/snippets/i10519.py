from abc import ABC
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import ParamSpec

_P = ParamSpec("_P")


@dataclass
class Foo[T](ABC):
    _foo: T | None = field(init=False)
    _bar: dict[str, str] = field(init=False)

    def __init_subclass__(cls) -> None:
        def _wrap(func: Callable[_P, None]) -> Callable[_P, None]:
            def _w(*args: _P.args, **kwds: _P.kwargs) -> None:
                self = args[0]
                func(*args, **kwds)
                if not hasattr(self, "_foo"):
                    object.__setattr__(self, "_foo", None)
                if not hasattr(self, "_bar"):
                    object.__setattr__(self, "_bar", {})

            return _w

        cls.__init__ = _wrap(cls.__init__)


@dataclass
class Bar(Foo): ...
