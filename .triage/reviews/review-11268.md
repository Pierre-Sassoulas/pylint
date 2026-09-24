# Review — PR #11268 (fix class checker crashes on `x.__class__` targets)

Verified locally: worktree of `ba1024acd`, `venv/bin/python` (3.13.1), astroid pinned as
in repo.

## Verification

- Reported crash reproduces on base (`F0002` astroid-error), gone on the branch.
- `pytest tests/test_functional.py` → `2 failed, 890 passed, 25 skipped`; the same 2
  (`no_name_in_module`, `unbalanced_tuple_unpacking`) fail on my base checkout →
  pre-existing.
- `pylint --rcfile=pylintrc pylint/checkers/classes/class_checker.py` → 10.00.
- Extra shapes I threw at it (async for, chained assign, nested `with`, `+=`, class
  body, module level) → no crash on the branch, several crash on base. Good coverage of
  the family.

## 1. Regression: starred targets lose real messages (please fix)

`nodes.Starred` is the one non-`Assign` parent that _does_ expose a usable `.value` (it
is the `AssignAttr` itself, which astroid resolves through `starred_assigned_stmts`). It
did not crash on base, so the new guards silence it for nothing:

```python
class Cat:
    __slots__ = ("name",)

def f(cat):
    first, *cat.__class__ = [1, 2, 3]   # base: E0243 (+ E0237 when slotted); PR: silent
    print(first)

class Basket:
    def method(self):
        *self.__class__, myvar = [1, 2]  # base: E0243; PR: silent
        print(myvar)
```

Runtime agrees with base:
`TypeError: __class__ must be set to a class, not 'list' object`.

Fix is one token in each of the two new `isinstance` tuples — add `nodes.Starred`. I
applied it locally: parity with base restored, no crash on any of the exotic shapes,
full functional suite still at the 2 pre-existing failures.

## 2. `nodes.List` target: crash traded for a silent false negative

```python
class Bar:
    def m(self):
        [self.__class__, myvar] = 1, 2   # base: F0002 crash; PR: silent
        print(myvar)
```

The tuple branch keys on `isinstance(node.parent, nodes.Tuple)`, so a list target falls
into the `else` branch and is skipped.
`isinstance(node.parent, (nodes.Tuple, nodes.List))` recovers the true positive
(verified: emits E0243 for `Const`, suite green).

## 3. Same function, bigger crash still open: `inferred.slots()` can be `None`

The PR hardens the line above it, but leaves this one:

```python
class Cat:
    __slots__ = ("name",)

class Dog:
    pass

cat = Cat()
cat.__class__ = Dog     # TypeError: 'NoneType' object is not iterable -> F0002
```

`ClassDef.slots()` returns `None` when any class in the MRO has no `__slots__`, and
`zip_longest(slots, None)` raises. This is the plain, canonical shape of the very thing
the PR is about — slotted class reassigning `__class__` to a non-slotted class — and
CPython rejects it too (`__class__ assignment: 'Dog' object layout differs from 'Cat'`),
so `assigning-non-slot` is the right answer. `if other_slots is None: return False`
fixes it (verified). Pre-existing, so a follow-up issue is acceptable, but it is three
lines away from code this PR is already editing and the fragment already claims to fix
the `assigning-non-slot` crash family.

(Same neighbourhood, lower priority: `klass.mro()` in `_check_in_slots` and
`inferred.slots()` can raise `InconsistentMroError` / `NotImplementedError` on an
inconsistent MRO. Pre-existing, not this PR's job.)

## 4. Pre-existing, worth its own issue: `class_index` keeps the _last_ match

```python
self.__class__, other.__class__ = Dog, 1
```

Both `AssignAttr` visits read `elts[1]`, so `self.__class__` — which correctly gets
`Dog` — is reported as `Const`. Mirror the operands and the genuine error is silently
dropped instead. A false positive on an E-message.
`class_index = node.parent.elts.index(node)` is the honest version. Same class of bug as
the pre-existing starred-before-`__class__` mismatch
(`*rest, self.__class__ = 1, 2, Foo` → false `Const`), which the PR description reads as
fully handled — it is only handled for a trailing star.

Not asking for it in this PR; just note that the PR body's starred-unpacking claim is
half true.

## Nits

- The 7-line `isinstance(...) or ... is None` guard is duplicated verbatim in
  `_check_invalid_class_object` and `_check_in_slots`. A module-level
  `_assigned_value(node: nodes.AssignAttr) -> nodes.NodeNG | None` used by both would
  read better and keep the two checks from drifting apart (they already disagree: the
  tuple branch analyses tuple unpacking, `_check_in_slots` bails on it).
- `nodes.AugAssign` in the guard treats `X` as the assigned value, but
  `self.__class__ += X` binds `__class__ + X`. Pre-existing behaviour, just noting it is
  now written down explicitly.
- `hasattr(elt, "attrname")` in the tuple scan — `isinstance(elt, nodes.AssignAttr)` is
  the house style (AGENTS.md).
- Test naming: `Crash11267` matches the existing convention (`Crash4755Context`) better
  than `CrashRegression11267`.
- `_has_same_layout_slots`: `safe_infer` would replace the `try/except`, but it also
  returns `None` on ambiguous inference where `next(...infer())` takes the first result
  — so the explicit `except astroid.InferenceError` is the conservative choice. Keep it.

## Test gaps

The new cases pin "no crash" well, but not the intended silence or the intended
messages:

- No case for a `nodes.List` target, a `Starred` target, `async for` / `async with`.
- `nodes.AnnAssign`, `nodes.AugAssign` and `nodes.List` in the new allow-lists are
  unpinned — removing any of them keeps the suite green.
- `release_in_tuple` assigns `ClassWithSlots` (same layout), so it would pass even
  without the guard; a differing-layout class would actually pin the new early return.
