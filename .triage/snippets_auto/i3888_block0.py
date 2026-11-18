"""Test cases."""

def f(
):  # pylint: disable=unused-variable
    # works
    i_am_unused = 42

def g():  # pylint:disable=unused-variable
    # fails
    i_am_unused = 42

def h(
) -> None:  # pylint:disable=unused-variable
    # fails
    i_am_unused = 42
