I'm using a conditional type definition: A dataclass for Python 3.9+ and a namedtuple otherwise. Then I'm running PyLint with Python 3.12.

PyLint does not detect the unexpected and missing keyword args for that type.

Input:

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
import sys
from dataclasses import dataclass

if sys.version_info >= (3, 9):
    @dataclass
    class Foo:
        x: int
        y: int
else:
    class Foo:
        pass


@dataclass
class Bar:
    x: int
    y: int


Foo(X2=1, y=2)
Bar(X2=1, y=2)


This is reduced, the actual fallback uses `Foo = namedtuple('Foo', ('x', 'y'))` but it shouldn't matter as that branch shouldn't be taken at all. Also swapping the branches and condition such that unused one comes first doesn't change the outcome
