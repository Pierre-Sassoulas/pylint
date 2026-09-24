# Triage — issue #11295 (`arguments-differ` not raised for dunder methods)

Verified locally on `is-module-member` (`5db503e88`), `venv/bin/python` (3.13.1).

## Verdict

Partly a real false negative, partly correct-by-design.

| Derived method in the report                                             | Emitted? | Verdict                                        |
| ------------------------------------------------------------------------ | -------- | ---------------------------------------------- |
| `__call__(self, apple, banana, cherry)` vs base `(self, apple, banana)`  | no       | **real false negative**                        |
| `__init__(self, apple, banana, cherry)` vs base `(self, apple, banana)`  | no       | by design — constructors are not substitutable |
| `__exit__(self, *args)` vs base `(self, exc_type, exc_value, traceback)` | no       | correct — `*args` _widens_, no LSP violation   |
| `__enter__`                                                              | n/a      | not overridden in the sample                   |

`abstractmethod` is a red herring — the false negative reproduces on plain classes:

```python
class Fruit:
    def __call__(self, apple, banana): ...
    def other(self, apple, banana): ...

class Basket(Fruit):
    def __call__(self, apple, banana, cherry): ...   # silent  <-- bug
    def other(self, apple, banana, cherry): ...      # W0221
```

## Root cause

`pylint/checkers/classes/class_checker.py:381-387`, end of `_different_parameters`:

```python
if original.name in PYMETHODS:
    # Ignore the difference for special methods. If the parameter
    # numbers are different, then that is going to be caught by
    # unexpected-special-method-signature.
    # If the names are different, it doesn't matter, since they can't
    # be used as keyword arguments anyway.
    output_messages.clear()
```

Introduced in `f214ab129` (2016) for #1042, which was only about **renamed** parameters
(`__getitem__(self, key)` overridden as `__getitem__(self, cheie)`). The fix cleared
_every_ message, not just the rename. `5e233c573` (#8927 / #8919) later moved the block
below the variadics check so it also swallows `Variadics removed in`.

The comment's justification does not hold for all of `PYMETHODS`.
`E0302 unexpected-special-method-signature` only fires against the **builtin** expected
arity in `SPECIAL_METHODS_PARAMS`, and four entries there map to `None` (variable
arity): `__new__`, `__init__`, `__call__`, `__init_subclass__`. For those, a count
mismatch against a **user-defined** base is reported by nothing at all. The tuple-arity
entries (`__round__` `(0, 1)`, `__pow__` `(1, 2)`) have the same hole in a narrower
form.

Confirmed: `__getitem__` (fixed arity 1) with an extra param → `E0302` fires, so the
comment is right there; `__call__` → nothing.

Second, independent cause for `__init__` only — `visit_functiondef` returns before the
ancestor loop that calls `_check_signature`, so `__init__` never reaches
`_different_parameters`:

```python
# class_checker.py:1421-1423
if node.name == "__init__":
    self._check_init(node, klass)
    return
```

That one I'd keep. `Derived(Base)` taking extra constructor arguments is idiomatic
Python and callers name the concrete class, so it is not a substitutability violation.

## Candidate fix (validated locally, not committed)

Keep the exemption for the constructor family, narrow it to name/variadics differences
elsewhere:

```python
if original.name in {"__new__", "__init__", "__init_subclass__", "__post_init__"}:
    output_messages.clear()
elif original.name in PYMETHODS:
    output_messages[:] = [m for m in output_messages if "Number" in m]
```

The constructor branch is required, not cosmetic: without it
`tests/functional/r/regression_02/ regression_enum_1734.py` starts failing, because an
`Enum` with a custom `__new__(cls, value, recoverable)` widening `object.__new__` is
exactly the idiomatic pattern. `__init_subclass__` is the same story (PEP 487 — subclass
kwargs differ by design, cf. #8919).

Results with that patch:

- `Derived.__call__` now flagged; `__init__` / `__new__` / `__init_subclass__` still
  silent; `__exit__(self, *args)` still silent.
- Old false positives stay fixed: #1042 (`__getitem__` rename) and #8919
  (`__init_subclass__(cls, /, **kwargs)` under `Generic[T]`) both clean.
- `pytest tests/test_functional.py` → `2 failed, 891 passed, 30 skipped`, identical to
  my clean checkout (`no_name_in_module`, `unbalanced_tuple_unpacking` are pre-existing
  here).
- No new functional test needed to be updated: the two existing dunder cases in
  `tests/functional/a/arguments_differ.py` (lines 222-232, 363-370) only exercise
  renames and variadics, never a count difference.

## False-positive risk: none measured

`--enable=arguments-differ,arguments-renamed` over ansible, astropy, django,
home-assistant, CPython `Lib`, sentry and music21 (10 487 output lines): **zero message
delta** between clean and patched. The only diff lines were two pre-existing tracebacks
whose `class_checker.py` line numbers shifted.

So the change is safe, but the pattern is also rare in the wild — worth fixing as a
correctness gap, not urgent.

## Suggested labels

`False Negative 🦋`, `Checkers`, `Needs decision 🔒` (the `__init__` half is a design
question, and the reporter explicitly expects `__init__` to be flagged).

## Reply sketch

Confirm `__call__`, explain that `__exit__(self, *args)` is a legitimate widening, and
that `__init__` is deliberately exempt (subclass constructors routinely take different
arguments).
