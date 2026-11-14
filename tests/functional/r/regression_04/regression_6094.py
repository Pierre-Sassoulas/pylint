"""Regression test for https://github.com/pylint-dev/pylint/issues/6094.

``__getattribute__`` on a module was reported as ``no-member``.
"""

import sys

print(sys.__getattribute__("argv"))
