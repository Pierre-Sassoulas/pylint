# minimal.py
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Base:
    x: int
    y: int


class SumMixin:

    def sum(self):
        return self.x + self.y


@dataclass(kw_only=True)
class Intermediate(Base, SumMixin):

    x: int = field(init=False)

    def __post_init__(self):
        self.x = 4


@dataclass(kw_only=True)
class Example(Intermediate):

    message: str

    def help(self):
        return self.message.format(self.sum())


if __name__ == "__main__":
    print(Example(y=3, message="Here it is: {}").sum())
