from dataclasses import dataclass


@dataclass
class Foo:
    name: str
    val: int


lorem = (Foo(name="lorem", val=0), 0)
ipsum = (Foo(name="ipsum", val=1), 1)
dolor = (Foo(name="dolor", val=2), 2)

names = [sth.name for sth, _ in [lorem, ipsum, dolor]]
print(names)
