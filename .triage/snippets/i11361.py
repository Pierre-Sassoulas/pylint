"""Repro for the StatementMissing crash in the class checker.

Minimal case of the older ``Module.builtins`` report: a subclass method
whose name shadows an instance attribute set by the parent. Shorter
than the original and the better regression test of the two.
"""


class C:
    def __init__(self):
        self.help = None


class D(C):
    def help():
        pass
