from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Base:
    value: str


@dataclass(frozen=True, kw_only=True)
class Middle[T, *Shape](Base):
    pass


@dataclass(frozen=True, kw_only=True)
class Upper[T, *Shape](Middle[T, *Shape]):
    pass


obj = Upper[str, int](value="hello")
