# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
from collections import namedtuple
from typing import NamedTuple

Foo = namedtuple('Foo', ('x', 'y'))


class Foo2(NamedTuple):
    x: int
    y: int


Foo(X2=1, y=2)
Foo2(X2=1, y=2)
