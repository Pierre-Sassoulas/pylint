# pylint: disable=missing-docstring
from numpy import arange, empty_like

a = empty_like(arange(10))
a[0] = 1
