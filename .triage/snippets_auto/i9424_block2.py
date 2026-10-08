# pylint: disable=missing-docstring
from typing import Any


class Base:
    @classmethod
    def apply(cls, *args: Any, **kwargs: Any) -> Any:
        return cls.forward("ctx", *args, **kwargs)

    @staticmethod
    def forward(ctx: str, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()


class Derived(Base):
    @staticmethod
    def forward(ctx: str, x: int, y: int) -> Any:
        del x, y
        return ctx


Derived.apply(1, 2)
