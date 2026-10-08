from dataclasses import dataclass, field

@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False, frozen=True)
class Parent():
    name: str = field(init=False)

class Child(Parent):
    age: int = field(init=False)
