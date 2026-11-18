# pylint: disable=missing-docstring,unnecessary-lambda,too-few-public-methods
from dataclasses import dataclass, field

def mydataclass(cls):
    cls.myfun = lambda self: print(self)
    return dataclass(cls)

@mydataclass
class TestDC:
    a_dict: dict[int, int] = field(default_factory=dict)

dc = TestDC()
dc.a_dict[0] = 0
