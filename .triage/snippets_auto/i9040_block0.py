import abc, dataclasses

@dataclasses.dataclass
class Parent(abc.ABC):
    _: dataclasses.KW_ONLY
    id: int | None = None

@dataclasses.dataclass
class Child(Parent):
    name: str

c = Child(id=1, name="foo")
