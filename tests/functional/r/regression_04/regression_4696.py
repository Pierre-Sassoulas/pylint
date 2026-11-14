"""Regression test for https://github.com/pylint-dev/pylint/issues/4696.

Unpacking the result of an overloaded method was reported as
``unpacking-non-sequence``. The overloaded function was fine.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,unused-argument,invalid-name,too-few-public-methods

import typing


class Overloaded:
    @typing.overload
    def method(self, arg: str) -> typing.Tuple[str, str]: ...

    @typing.overload
    def method(self, arg: bytes) -> typing.Tuple[bytes, bytes]: ...

    def method(self, arg: typing.Union[str, bytes]) -> typing.Tuple[str, str]:
        return "x", "y"


A, B = Overloaded().method("x")
