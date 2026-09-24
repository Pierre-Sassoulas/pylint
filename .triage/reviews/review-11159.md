Re-reviewed at `d3ed0ecc9`. All five suggestions from the last round are applied
verbatim, and I re-verified each one instead of reading the diff.

- The quadratic re-walk is gone: `_setattr_names_in_defining_methods` returns the name
  set, `_parent_setattr_names` lifts the ancestor loop out of the per-attribute path,
  and the `parent_setattr_names` memo fills at most once per class.
- The three guards that survived mutation last time are pinned now. At this commit,
  removing the `_,` from the arg pattern, the `classmethod`/`staticmethod` guard, or the
  `safe_infer`/`is_builtin_object` block each fails
  `test_functional[attribute_defined_outside_init]`.
- The order-independence test isn't vacuous either — stubbing `_parent_setattr_names` to
  `return set()` fails both the `child-first` and the `parallel` parametrization.
- `SameClassSetattrThenAssign` and the fragment sentence covering the warning-removal
  direction are in.

Local state here: `tests/checkers/` 452 passed, `tests/test_functional.py` 888 passed
(`no_name_in_module` and `unbalanced_tuple_unpacking` fail on `main` too, unrelated),
`test_self.py` order test green, self-lint 10.00 on `class_checker.py` /
`tests/checkers/unittest_classes.py` / `tests/test_self.py`, mypy clean on the checker,
spell-check clean. Primer on my local clones with only this message enabled: ansible 140
→ 142 — the two real hits in `Base.load_data` and `JsonRpcServer.handle_request` — and
every other package unchanged (astropy 913, django 284, sentry 80, coveragepy 4, flask
0, music21 0).

One nit left, and it's my own doing.

**`custom_dict.txt` grows a `cnode` entry to spell-check one docstring.** The word is
only there because my suggested wording said `*cnode*`. It's a private parameter name,
not project vocabulary, and `custom_dict.txt` is global, so it also silences the word
everywhere else. Rewording avoids the entry:

```suggestion
        """Names the ancestors set with ``setattr`` in one of their defining methods."""
```

and the `custom_dict.txt` change can then be dropped. Checked both ways: with `cnode`
out of the dictionary the current wording raises `C0402`, the reworded one doesn't, and
self-lint stays at 10.00.

Otherwise this is good to go from my side.
