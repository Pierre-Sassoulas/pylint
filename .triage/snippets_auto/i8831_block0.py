# a.py

# pylint: disable=missing-docstring
from typing import Literal


def false_unused_imports() -> "int | Literal[True]":
    return True


# def annotation_error() -> int | "Literal[True]":
#     return True
