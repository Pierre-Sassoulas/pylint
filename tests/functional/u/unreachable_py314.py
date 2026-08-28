"""Test ``unreachable`` (W0101) for tests that always raise on Python 3.14+.

``bool(NotImplemented)`` raises ``TypeError`` on Python 3.14+ (and emitted
a ``DeprecationWarning`` on earlier versions), so an ``if`` / ``while`` /
``assert`` whose test always infers to ``NotImplemented`` cannot proceed
past the test expression: neither branch is selected and any code after
the statement is also unreachable.
"""
# pylint: disable=missing-function-docstring,using-constant-test


if NotImplemented:
    print("body unreachable")  # [unreachable]
else:
    print("else unreachable")  # [unreachable]
print("sibling unreachable")  # [unreachable]


def in_function() -> None:
    while NotImplemented:
        break  # [unreachable]
    print("after-while unreachable")  # [unreachable]


def with_assert() -> None:
    assert NotImplemented
    print("after-assert unreachable")  # [unreachable]
