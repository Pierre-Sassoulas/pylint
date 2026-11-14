"""Regression test for https://github.com/pylint-dev/pylint/issues/11101.

An instance created by calling ``cls`` in a classmethod and stored on
``self`` was reported as ``no-member``.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods,attribute-defined-outside-init


class Maker:
    def method(self):
        return 0

    @classmethod
    def make(cls):
        return cls(), 0


class User:
    def use(self):
        self.made = Maker.make()[0]
        self.made.method()
