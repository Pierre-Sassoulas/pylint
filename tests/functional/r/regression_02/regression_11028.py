"""Regression test for https://github.com/pylint-dev/pylint/issues/11028.

Calling ``len()`` with no arguments inside a boolean context crashed the
implicit-booleaness checker, which assumed the call always had at least
one argument.
"""

if len():
    pass
