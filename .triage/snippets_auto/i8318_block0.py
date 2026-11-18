# pylint: disable=missing-module-docstring,missing-function-docstring

from typing import NoReturn

def way_one() -> NoReturn:
    raise ValueError  # C code instantiation of ValueError

def way_two() -> NoReturn:
    raise ValueError()  # Interpreter instantiation of ValueError (slower)
