"""Regression test for https://github.com/pylint-dev/pylint/issues/10158.

``__required_keys__`` and ``__optional_keys__`` on a ``TypedDict`` class
were reported as ``no-member``.
"""

# pylint: disable=missing-class-docstring

from typing import NotRequired, Required, TypedDict


class MyDict(TypedDict):
    required: Required[str]
    not_required: NotRequired[str]
    implicitly_required: str


print(MyDict.__required_keys__)
print(MyDict.__optional_keys__)
