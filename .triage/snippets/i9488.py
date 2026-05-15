from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar


class Base:
    pass


class AbstractBase(ABC):
    pass


_T = TypeVar("_T", bound=Base | AbstractBase)


@dataclass
class GenericClass(Generic[_T]):
    field: _T


@dataclass
class ConcreteGeneric(GenericClass[Base | AbstractBase]):
    pass


a = ConcreteGeneric(field=Base())
