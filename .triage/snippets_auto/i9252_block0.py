#pylint: disable=C0114,C0116
from contextlib import contextmanager
from typing import Generator

def subgenerator() -> Generator[int, None, None]:
    yield 0

@contextmanager
def context_manager() -> Generator[int, None, None]:
    # does not work:
    yield from subgenerator()

    # works:
    #for x in subgenerator():
    #    yield x

with context_manager() as cm:
    print(cm.bit_count())
