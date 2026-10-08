# pylint: disable=missing-docstring,blacklisted-name

def foo(bar):
    if bar > 4:
        baz = bar + 3
        return baz

    baz = bar - 1  # This line has no effect
    return bar
