# pylint: disable=missing-docstring
from typing import ParamSpec, Generic, Any


P = ParamSpec("P")


class Base(Generic[P]):
    @classmethod
    def apply(cls, *args: P.args, **kwargs: P.kwargs) -> Any:
        return cls.forward("ctx", *args, **kwargs)

    @staticmethod
    def forward(ctx: str, *args: P.args, **kwargs: P.kwargs) -> Any:
        raise NotImplementedError()


class Derived(Base[int, int]):
    @staticmethod
    def forward(ctx: str, x: int, y: int) -> Any:
        del x, y
        return ctx


Derived.apply(1, 2)
