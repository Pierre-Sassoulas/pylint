"""Repro attempt for the pyreverse -S recursion report.

Run with ``pyreverse -S -o dot -p x`` — it does not crash any more, it
runs past 120 seconds without writing a diagram. ``-s2`` finishes at
once, which is the workaround to give reporters.
"""

import numpy as np


class ExempleClass:
    typ = np.uint32

    def __init__(self, D):
        self.X = np.zeros(D, dtype=self.typ)
