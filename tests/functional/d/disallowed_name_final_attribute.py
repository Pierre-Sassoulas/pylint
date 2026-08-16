"""A ``Final`` attribute is still checked against ``bad-names``.

Being a constant, it is not held to the attribute naming style, but that is
no reason to exempt it from the names the user disallowed.
"""
from typing import Final


class Fruit:  # pylint: disable=too-few-public-methods
    """One allowed name, one disallowed."""

    def __init__(self):
        self.apple: Final = 1
        self.foo: Final = 2  # [disallowed-name]
