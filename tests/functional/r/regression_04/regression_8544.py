"""Regression test for https://github.com/pylint-dev/pylint/issues/8544.

Only the first inferred value of ``nums`` was used, so star-args unpacking
of a possibly empty tuple was reported as ``no-value-for-parameter``.
"""

# pylint: disable=missing-function-docstring


def get_nums():
    nums = ()
    if input() == "1":
        nums = (1, 2)
    return nums


def add(x, y):
    return x + y


NUMS = get_nums()
if NUMS:
    add(*NUMS)
