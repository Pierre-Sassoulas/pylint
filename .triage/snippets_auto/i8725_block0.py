"""Module level docstring"""

def enable_here():
    """This function should have a warning."""
    x = "bad name"
    return x


def disable_here():
    """No pylint warnings in this function, please."""
    # pylint: disable=all
    x = "bad name"
    return x
