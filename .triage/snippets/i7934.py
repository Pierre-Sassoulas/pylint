import abc
import typing as typ

T_Test = typ.TypeVar("T_Test")


class Bases(typ.Generic[T_Test]):
    @abc.abstractmethod
    def method(self) -> T_Test:
        """Method Doc"""


class typed_dict(typ.TypedDict):
    test: int


class Child(Bases[typed_dict]):
    def method(self):
        return {"test": 0}
