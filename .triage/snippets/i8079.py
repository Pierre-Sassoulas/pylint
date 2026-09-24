"""Crash repro for https://github.com/pylint-dev/pylint/issues/8079.

A class with both a method named after a site-installed builtin
(license / copyright / credits / exit / quit) AND that name bound as
an instance attribute via ``self.NAME = ...`` in ``__init__``.

This is the minimal self-contained shape of the original funkwhale
crash. Funkwhale renamed
``@factory.post_generation\ndef license(...)`` to
``_license_post_generation`` in commit 6528039e of funkwhale/funkwhale
to work around it. The simpler sub-case from #10159 (closed as dup)
``tuple = namedtuple(None, [])`` was fixed in astroid 4.0.0, but the
funkwhale-flavored class-method-shadowing-site-builtin path here is
still live on pylint 4.0.5 / 4.1.0-dev (astroid up to 4.2.0b3).

Crash path (pylint 3.3.8 → main):
  pylint/checkers/classes/class_checker.py:visit_functiondef
    -> for ancestor in klass.ancestors():
         for obj in ancestor.lookup(node.name)[1]:   # <- name = "license"
  astroid/nodes/scoped_nodes/mixin.py:_scope_lookup
    -> _filter_stmts(node, self.locals[name], self, offset)
  astroid/filter_statements.py:_get_filtered_node_statements
    -> [(node, node.statement()) for node in stmt_nodes]
  astroid/nodes/scoped_nodes/scoped_nodes.py:Module.statement
    -> raise StatementMissing(target=self)
  -> reported by pylint as F0002 astroid-error.

Other site builtins that reproduce the same crash with the same shape:
``copyright``, ``credits``, ``exit``, ``quit``. Real-class builtins
(``tuple``, ``list``, ``dict``, …) don't trip this particular path —
their entries in ``builtins.locals`` are ClassDef nodes which take a
different astroid code path.
"""


class C:
    def __init__(self):
        self.license = 1

    def license(self):
        return self.license
