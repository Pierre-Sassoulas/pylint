"""Repro attempt for the pyreverse EmptyNode report.

Run with ``pyreverse -o dot -p x``. Both class shapes that astroid
rebuilds through a brain — namedtuple and argparse.Namespace — walk
cleanly, so this does not reach the reported code path. The open PR
builds the EmptyNode by hand in its test.
"""

import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Sub(Point):
    def __init__(self, *args):
        super().__init__()
        self.extra = 1


class NS(argparse.Namespace):
    def __init__(self):
        super().__init__()
        self.thing = 2
