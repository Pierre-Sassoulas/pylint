"""Repro for the AssignAttr InferenceError crash (from a fuzzing run).

``typecheck.visit_attribute`` calls ``owner.getattr`` and the metaclass
lookup underneath it raises instead of yielding Uninferable.
"""

from collections.abc import GenericAlias


class C:
    pass


x = C.a

for GenericAlias.a in _:
    pass
