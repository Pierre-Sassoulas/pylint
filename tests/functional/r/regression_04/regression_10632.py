"""Regression test for https://github.com/pylint-dev/pylint/issues/10632.

``concurrent.futures`` defines ``ProcessPoolExecutor`` lazily on Python 3.14,
which was reported as ``no-name-in-module``.
"""

from concurrent.futures import ProcessPoolExecutor

print(ProcessPoolExecutor)
