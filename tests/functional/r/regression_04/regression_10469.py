"""Regression test for https://github.com/pylint-dev/pylint/issues/10469.

``isinstance`` did not narrow the inferred type, so calls were checked
against the signature of the other class.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

import random


class OneArg:
    def method(self, a):
        return a


class TwoArgs:
    def method(self, a, b):
        return a * b


def func():
    if random.randint(0, 10) > 5:
        obj = OneArg()
    else:
        obj = TwoArgs()

    if isinstance(obj, TwoArgs):
        print(obj.method(2, 3))
    if isinstance(obj, OneArg):
        print(obj.method(2))
