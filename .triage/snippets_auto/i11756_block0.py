"""Enum members created with enum.member (Python 3.11+)."""
import enum
from enum import Enum, member


class Operation(Enum):
    """Each member is a function."""

    @member
    def add(a, b):
        return a + b

    @enum.member
    def neg(a):
        return -a

    @member
    @staticmethod
    def zero():
        return 0

    def describe(self):
        return self.name


print(Operation.add.value(1, 2), Operation.neg.value(3), Operation.zero.value(), Operation.add.describe())
