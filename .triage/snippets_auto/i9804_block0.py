from dataclasses import InitVar
from dataclasses import dataclass


@dataclass
class Base:
    x: int

    def __post_init__(self):
        self.x += 1


@dataclass
class Child(Base):
    y: InitVar[int]

    def __post_init__(self, y):  # this is OK but it triggers `arguments-differ`
        super().__post_init__()
        self.x += y
