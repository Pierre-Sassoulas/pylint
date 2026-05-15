from typing import NamedTuple


class Foo(NamedTuple):
    x: int


Foo(1)._asdict()
