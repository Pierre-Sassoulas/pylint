# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import sys
from contextlib import contextmanager
from io import StringIO
from collections.abc import Generator


def ctx() -> StringIO:
    sys.stderr = StringIO()
    return sys.stderr


@contextmanager
def ctx2() -> Generator[StringIO]:
    sys.stderr = StringIO()
    yield sys.stderr


c1 = ctx()
print(c1.getvalue())

with ctx2() as c2:
    print(c2.getvalue())
