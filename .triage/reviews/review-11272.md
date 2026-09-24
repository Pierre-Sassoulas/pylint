# Review — PR #11272 (fix crashes for classes with duplicate or inconsistent bases)

Verified locally: worktree of `d27e453d4`, own venv, `astroid==4.2.0b5` as pinned by
`requirements_test.txt`, pylint installed editable so edits actually take effect.

## Verification

- Each of the three claimed crashes reproduces on `main` as `F0002` (astroid-error) and
  is gone on the branch: `invalid-name` on an instance, `assigning-non-slot`,
  `stop-iteration-return`, plus the inconsistent-MRO twins of all three.
- `pytest tests/` → `2190 passed, 272 skipped, 5 xfailed`, no failures.
- `mypy` on the four changed modules → clean. `pylint --rcfile=pylintrc` on them →
  10.00/10.
- Wider sweep of MRO-less shapes (broken metaclass, `abc.ABC, abc.ABC` + unimplemented
  abstract method, `Enum, Enum`, `super()` inside a duplicate-bases class, attribute
  access on instances of all of them) → no fatal message anywhere.
- I audited the other `mro()` call sites so the "every other one is guarded" claim
  holds: `utils.py:962` catches `ResolveError` (`MroError` is a subclass),
  `typecheck.py:155` and `:795` catch it explicitly, `typecheck.py:515` is safe because
  `super_mro()` already called `self.type.mro()` in the `try` above it, and
  `class_checker.py:1020` is the detector that turns the error into `duplicate-bases`.
  Correct.

## 1. Two crash sites in the same family are still open (please fix)

`slots()` raises too, and it is called in three places, not one. The PR guarded
`_check_in_slots` and left the other two. Both still abort the whole file:

`class_checker.py:1778`, in `_check_redefined_slots` — this is the line the earlier
review pointed at (`class_checker.py:1780` on `main`):

```python
class Broken(list, list):
    __slots__ = ("fruit",)

class Child(Broken):
    __slots__ = ("fruit",)
```

`class_checker.py:551`, in `_has_same_layout_slots`, reached from the `__class__` branch
of `_check_in_slots` — so the very check the PR is fixing still has a live crash next
door:

```python
class Broken(list, list):
    __slots__ = ("fruit",)

class Cat:
    __slots__ = ("fruit",)

    def swap(self):
        self.__class__ = Broken
```

Both give `duplicate-bases` and then `F0002: Fatal error while checking` on the branch.

A `safe_slots` sibling to `safe_mro` covers all three sites and lets the local
`try`/`except` in `_check_in_slots` go away, so `class_checker.py` gets _shorter_:

```python
def safe_slots(node: nodes.ClassDef) -> list[nodes.Const] | None:
    """Return the slots of ``node``, or None if it does not have a usable MRO.

    ``slots()`` walks the MRO internally, so it gives up on exactly the classes
    ``safe_mro`` has nothing to return for. It raises ``NotImplementedError``
    rather than the ``MroError`` underneath. A class without a usable MRO gets
    the same answer as a class that defines no slot at all.
    """
    try:
        return node.slots()  # type: ignore[no-any-return]
    except NotImplementedError:
        return None
```

I applied it locally (`safe_slots(inferred)` at 551, `safe_slots(ancestor) or []` at
1778, `slots = safe_slots(klass)` replacing the `try`/`except` at 1948): all eight repro
files fatal-free, `2190 passed`, mypy clean, self-lint 10.00/10, net −6 lines in
`class_checker.py`.

One judgment call comes with the 551 site: `_has_same_layout_slots` reads `None` as
"different layout", so `self.__class__ = Broken` now reports `assigning-non-slot`. That
is the same answer any other incompatible class gets and I think it is fine, but
returning early with no message is also defensible since the layout is genuinely
unknowable. Your call — worth a line in the test either way.

## 2. `duplicate_bases.py` was converted from CRLF to LF (please restore)

`.gitattributes` sets `tests/**/functional/** -text`, so git keeps whatever bytes are
committed, and `duplicate_bases.py` has been CRLF since forever. The branch rewrote it
as LF, which turns a 6-line addition into a 24-line whole-file diff:

```
main:   i/crlf  w/crlf  attr/-text   tests/functional/d/duplicate/duplicate_bases.py
branch: i/lf    w/lf    attr/-text   tests/functional/d/duplicate/duplicate_bases.py
```

`inconsistent_mro.py` was handled correctly — still CRLF, new lines added with CRLF, no
mixed endings. Just `duplicate_bases.py` to put back.

## 3. `astroid.MroError` in the new `except` tuple is unreachable

```python
except (NotImplementedError, astroid.MroError):
```

The comment right below it explains why: astroid's `_all_slots` catches `MroError` and
re-raises it as `NotImplementedError`, so the second arm can never fire. Dead branch,
and a branch coverage can never reach. Dropping it (or adopting `safe_slots` from point
1, which drops it for you) is the tidier answer.

## 4. Optional: `stop-iteration-return` loses a real message

`safe_mro` returning `[]` is the conservative choice, but at the
`_check_exception_inherit_from_stopiteration` site it silences a message that is
genuinely correct:

```python
class Fine(StopIteration): ...
class Boom(StopIteration, StopIteration): ...

def good():
    yield "apple"
    raise Fine()   # R1708 stop-iteration-return

def bad():
    yield "apple"
    raise Boom()   # nothing on the branch
```

`main` crashes on `bad()`, so this is not a regression — but `ancestors()` still answers
correctly for both flavours of broken MRO, and `typecheck.py:155-157` already
establishes `ancestors()` as the fallback rather than nothing:

```python
>>> Boom.ancestors()
['builtins.StopIteration', 'builtins.Exception', 'builtins.BaseException', 'builtins.object']
>>> Inconsistent.ancestors()      # str, Str
['builtins.str', 'builtins.object', '.Str']
```

Not a blocker, and I would not touch the `EnumMeta` site this way (a metaclass is not in
`ancestors()`). But `any(... for _class in utils.safe_mro(exc) or exc.ancestors())` at
the one site keeps the message. Happy to leave it as a follow-up if you would rather
keep this PR narrow.

## 5. Nit: the PR description no longer matches the PR

The body still describes only `_should_check_class_regex`, and says "No changelog
fragment yet". Fragment `11272.bugfix` is in the diff and reads well, and `Refs #11272`
is an established form in `doc/whatsnew/fragments/`. Only the description needs a
refresh — the squash message is what lands, so this is cosmetic.

## Good

- `safe_mro` is the right shape, lives next to `has_known_bases`, and the docstring says
  _why_ an empty list is the right answer rather than just what the code does.
- The three unit tests pin the real MRO, duplicate bases and inconsistent bases
  separately, so the success branch is covered and not just the `except`.
- Functional tests are split one crash per file with fruit/animal names and a docstring
  explaining what sends the checker at the MRO. `inconsistent_mro.py` proving that the
  second class is now reported at all is a nice touch — on `main` the file died before
  reaching it.
- Primer: no effect. Codecov patch: 100% on `d27e453`.
