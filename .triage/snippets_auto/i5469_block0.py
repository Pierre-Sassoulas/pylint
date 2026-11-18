def noop(x):  # pylint: disable=invalid-name
    """Return value unchanged"""
    return x


def add(x, y):  # pylint: disable=invalid-name
    """Add two values"""
    return x + y


def main(param):
    """Should not emit too-many-function-args"""
    tmp = noop
    if param == 0:
        tmp = add   # I'm proposing this emit arguments-differ
    return tmp(1, 1.01)
