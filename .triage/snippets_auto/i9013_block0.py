from __future__ import annotations
from abc import ABC, abstractmethod
import attrs


class Abstract(ABC):
    @property
    @abstractmethod
    def my_prop(self) -> int:
        ...


@attrs.define
class Concrete(Abstract):
    my_prop: int


@attrs.define
class Concrete_FalsePositive(Abstract):
    my_prop: int = attrs.field()


conc = Concrete(35)
conc_fp = Concrete_FalsePositive(99)

print(f"conc:{conc.my_prop} fp:{conc_fp.my_prop}")
