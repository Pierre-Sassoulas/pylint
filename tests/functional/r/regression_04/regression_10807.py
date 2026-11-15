"""Regression test for https://github.com/pylint-dev/pylint/issues/10807.

A method annotated to return ``typing.Self`` and called through ``super()``
was inferred as the base class, so subclass members were reported as
``no-member``.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

import typing


class A:
    def parent_meth(self) -> typing.Self:
        return self


class B(A):
    def meth(self) -> typing.Self:
        return super().parent_meth()

    def f2(self):
        pass


B().meth().f2()
