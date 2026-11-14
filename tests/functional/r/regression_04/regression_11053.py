"""Regression test for https://github.com/pylint-dev/pylint/issues/11053.

Attribute access on a PEP 695 type parameter crashed ``visit_attribute``
because the ``TypeVar`` astroid node has no ``pytype()`` method.
"""

# pylint: disable=missing-function-docstring,pointless-statement


def func[T]():
    T.a
