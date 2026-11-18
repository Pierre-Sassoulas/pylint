# pylint: disable=missing-docstring,too-few-public-methods
from typing import Generic, TypeVar, Type

T = TypeVar("T")

class Base(Generic[T]):
    @classmethod
    def get_type(cls) -> Type:
        # the following line yields a no-member error for __orig_bases__
        return cls.__orig_bases__[0].__args__[0]


class SubClass(Base[int]):
    pass


def get_type(cls: Type) -> Type:
    return cls.__orig_bases__[0]


# all three lines give the correct result <class 'int'>
print(SubClass.get_type())
# the following line yields a no-member error for __orig_bases__
print(SubClass.__orig_bases__[0].__args__[0])
# the following line yields no error
print(get_type(SubClass).__args__[0])
