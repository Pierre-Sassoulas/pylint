"""functools.Placeholder (Python 3.14)."""
from functools import Placeholder, partial


def power(base, exponent, modulo=None):
    """Raise base to exponent."""
    return pow(base, exponent, modulo)


square = partial(power, Placeholder, 2)
print(square(5), square(5, modulo=7))
print(partial(power, Placeholder, Placeholder, 10)(2, 3))
