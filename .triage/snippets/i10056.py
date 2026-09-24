from dataclasses import dataclass, field


@dataclass
class Base:
    id: int
    subid: int


@dataclass
class Derived(Base):
    id: int = field(default=0, init=False)


@dataclass
class Child(Derived):
    subid: int = field(default=1, init=False)


d = Derived(subid=1)
c = Child()
