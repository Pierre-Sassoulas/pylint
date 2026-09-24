The rebase landed cleanly and the two things I asked about last time are done: the
message loop in the new `else` branch iterates `filtered_nodes` (not `nodes_lst`), so it
can't emit on `del self.x` / `self.x += 1` or on nodes from another module, and the
changelog fragment is there.

CI's primer confirms the shape of the fix: **69 messages removed, 0 added**, across
seven packages (astropy 32, psycopg 18, sentry 7, django 6, pandas 2, pytest 2, black
2). I spot-checked the two packages I hadn't looked at before and both are genuine false
positives:

- `psycopg`: `_cursor_base.__init__` → `self._reset()`, which sets `pgresult` and
  `_pos`; the removals in `cursor.py` / `cursor_async.py` / `_server_cursor.py` come
  from the parent-`__init__` hunk, correctly.
- `black`: `Node.__init__` → `self.invalidate_sibling_maps()`, which sets
  `prev_sibling_map` / `next_sibling_map`; `update_sibling_maps` was being flagged for
  reassigning them.

Both hunks are pinned by the new fixtures — reverting either one alone fails
`test_functional[attribute_defined_outside_init]`. And the "emit on every node" branch
is no longer untested the way it was on the pre-rebase version: replacing
`for node in filtered_nodes:` with `filtered_nodes[:1]` in the `else` now fails
`regression_10892`, so my earlier request for a multi-assignment fixture is moot.

Two nits and one thing for a follow-up.

**Nit: two blank lines before `class HDerived(HParent)`.** black skips
`tests/functional/`, so CI won't tell you.

**Nit: name the message in the fragment.** The convention is to reference it, e.g.

```rst
Fix a false positive for :ref:`attribute-defined-outside-init` when the attribute is assigned in a
helper method called from ``__init__`` (or from another ``defining-attr-methods`` method), including
when the helper is inherited.

Closes #5214
```

**Your `for`/`else` is equivalent to `any()`, and the dead guard is worth deleting.**
You were right that `if node.frame().name not in defining_methods:` is redundant — it is
dead, because the earlier
`any(frame.name in defining_methods or is_property_setter(frame) ...)` has already
`continue`d. It's harmless today, but the loop body and the `else` branch now disagree
about which nodes they cover: if that guard ever became live, the `else` would emit on
the very nodes the loop body skipped.

```diff
+            # If the attribute was set by a call made in any of the defining
+            # methods, then it is initialized after all: don't emit for any
+            # of the assignments.
+            if any(
+                _called_in_methods(node.frame(), cnode, defining_methods)
+                for node in filtered_nodes
+            ):
+                continue
+
             for node in filtered_nodes:
-                if node.frame().name not in defining_methods:
-                    # If the attribute was set by a call in any
-                    # of the defining methods, then don't emit
-                    # the warning.
-                    if _called_in_methods(node.frame(), cnode, defining_methods):
-                        break
-            else:
-                for node in filtered_nodes:
-                    self.add_message(
-                        "attribute-defined-outside-init", args=attr, node=node
-                    )
+                self.add_message("attribute-defined-outside-init", args=attr, node=node)
```

(That is what `black` produces — the collapsed `add_message` call lands on exactly 88
characters. The functional suite is unchanged with it.)

**Follow-up, not for this PR.** `_called_in_methods` matches on name only
(`func_obj.name == func.name`, no check on the receiver), so a call to a same-named
method on _another_ object inside `__init__` counts. That imprecision predates you, but
this PR grows its blast radius from one node to every assignment of the attribute:

```python
class Unrelated:
    def helper(self):
        """Does nothing."""


class NameCollision:
    def __init__(self):
        self.other = Unrelated()
        self.other.helper()   # Unrelated.helper, not self.helper

    def helper(self):
        self.oops = 1         # flagged on main, silent with this PR

    def later(self):
        self.oops = 2         # flagged on main, silent with this PR
```

Tightening the comparison to `func_obj is func` fixes that snippet and keeps the
class/attribute functional tests green locally, but it needs its own primer run to be
sure it doesn't cost real suppressions, so it belongs in a separate PR.

Given 69 removals and 0 additions I'd take the trade. With the fragment wording, the
blank line and (optionally) the `any()` simplification, this is good to go.
