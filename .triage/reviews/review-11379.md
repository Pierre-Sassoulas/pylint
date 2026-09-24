# Review — PR #11379 (fix `StatementMissing` crash in `class_checker`)

Branch reviewed: `kishansaaai:fix-statement-missing-class-checker` (`6c1210d30`),
applied on `main` @ `68f02810f`. Environment: repo `venv`, Python 3.13.1, astroid 4.3.0.

## Verdict

Approach is right: it kills the crash, removes two silent false negatives, and replaces
a scope walk with a dict lookup at no runtime cost. Needs test relocation + a second
changelog fragment + one redundant `isinstance` argument dropped.

## Root cause is narrower (and more interesting) than the PR says

The description blames "an ancestor class does not define `node.name`". The actual
trigger is `object`:

`klass.ancestors()` always yields `object`, which lives in `Module.builtins`.
`ClassDef._scope_lookup` escalates to `self.parent.scope()`, so for `object` that
enclosing scope _is_ the builtins module. `Module._scope_lookup` then runs
`_filter_stmts` over `builtins.locals[name]`, and for the names bound to an `EmptyNode`
parented directly to the module root, `node.statement()` walks up to `Module.builtins`
and raises `StatementMissing`.

Names that crash (astroid 4.3.0 / CPython 3.13) — every `builtins` local whose
`statement()` raises:

    Ellipsis, False, None, NotImplemented, True, __debug__, __spec__,
    copyright, credits, exit, help, license, quit

Of those, the ones that are legal method names are `copyright`, `credits`, `exit`,
`help`, `license`, `quit`, `__spec__`, `Ellipsis` and `NotImplemented` (`__debug__`,
`True`, `False` and `None` are syntax errors as `def` names) — which is exactly why the
two independent reports landed on `license` (#8079) and `help` (#11361).

Consequence worth putting in the PR description: **no base class is needed**. #8079's
own minimal repro has no explicit ancestor and still crashes on `main`:

```python
class C:
    def __init__(self):
        self.license = 1

    def license(self):
        return self.license
```

## The patch changes three behaviours; the description covers two

1. **Crash** — documented.
2. **Module-scope false negative** — documented.
3. **Builtin-scope false negative — not documented.** 44 builtin names are real
   `FunctionDef` nodes in `builtins.locals`, so on `main` `ancestor.lookup(name)` finds
   them and `return`s, silently swallowing a legitimate `method-hidden`:

       __build_class__ __import__ abs aiter all anext any ascii bin breakpoint
       callable chr compile delattr dir divmod eval exec format getattr globals
       hasattr hash hex id input isinstance issubclass iter len locals max min
       next oct ord pow print repr round setattr sorted sum vars

   Verified: a class whose ancestor sets `self.format` and which then defines
   `def format(self)` scores a clean 10.00/10 on `main` and correctly emits E0202 with
   the patch.

Point 3 is the half most likely to surprise users, and it is the half with no test.

## Verification run locally

- **Full test suite** (patched): 2142 passed, 46 skipped, 5 xfailed. The only two
  failures — `no_name_in_module` and `unbalanced_tuple_unpacking` — fail identically on
  unpatched `main` here (local astroid 4.3.0 vs the pinned 4.2.0b5). No regressions.
- **Primer sweep**, all 15 packages,
  `--disable=all --enable=method-hidden,astroid-error,fatal`, `main` vs patched: **zero
  delta**. 23 `method-hidden` hits on each side, identical sets, no `astroid-error` on
  either side. None of the 23 hits has a name that shadows a builtin or a module-level
  function, which is why nothing moved — the two false negatives are real but rare in
  the wild.
- **Performance**, `pylint django` with only `method-hidden` enabled, 3 runs each:
  `main` 32.27 / 31.95 / 32.60 s, patched 32.63 / 32.31 / 32.76 s. No measurable
  difference — the lookup is a rounding error against parse and inference. So the fix is
  cost-neutral in practice, not a speedup.
- **Other call sites**: instrumenting `LookupMixIn.lookup` shows `class_checker.py:1509`
  is the only pylint call site that ever hands a builtins-rooted node to `lookup()`. The
  one other builtins-rooted receiver is astroid-internal (`Name._infer`), which is safe
  because `Name` escalation ends in `builtin_lookup()` — that path skips `_filter_stmts`
  entirely.

## Requested changes

**1. Drop the redundant tuple member.** `nodes.AsyncFunctionDef` subclasses
`nodes.FunctionDef` in astroid, so the second member never matches anything the first
does not:

```python
for obj in ancestor.locals.get(node.name, ()):
    if isinstance(obj, nodes.FunctionDef):
        return
```

**2. Move the regression test into `tests/functional/m/method_hidden.py`.** That is the
project convention, the file already owns this message, and the `.txt` pins line and
column. It also exercises the real walk — worth having, because on `main` the crash
aborts `walker.walk(Module)` and silently swallows every `method-hidden` _after_ it in
the file, which a direct `checker.visit_functiondef()` call cannot show. Demonstrated
locally: in a file with a plain `method-hidden` at line 10, a `def help` at line 20 and
another plain `method-hidden` at line 30, `main` reports line 10, crashes, and never
reports line 30.

Verified locally — this block emits exactly the four annotated messages with the patch,
and makes the whole file fatal on `main`:

```python
class BuiltinNameAncestor:
    """The ancestor sets an attribute named like a builtin."""

    def __init__(self):
        self.help = None
        self.format = None


class BuiltinNameChild(BuiltinNameAncestor):
    def help(self):  # [method-hidden]
        pass

    def format(self):  # [method-hidden]
        pass


class BuiltinNameSameClass:
    """``object`` is an implicit ancestor, so no base class is needed."""

    def __init__(self):
        self.license = 1

    def license(self):  # [method-hidden]
        return self.license


def color():
    """A module level function unrelated to the class below."""


class ModuleFunctionNameAncestor:
    def __init__(self):
        self.color = None


class ModuleFunctionNameChild(ModuleFunctionNameAncestor):
    def color(self):  # [method-hidden]
        pass
```

`BuiltinNameSameClass` is #8079's repro and is the case that proves the `object`
ancestor path; `BuiltinNameChild.format` and `ModuleFunctionNameChild.color` cover the
two false negatives.

**3. Changelog.** Add `Closes #8079` to `11361.bugfix`, and add a
`doc/whatsnew/fragments/11361.false_negative` for the new messages — towncrier has that
type and users deserve the heads-up that methods named after a builtin can now raise
E0202.

**4. Nit.** The test docstring's summary line is split across the blank line
("...checking method-hidden" / "with a method name matching..."). Make it one line.

## One call for the maintainer: the backport label

`backport maintenance/4.0.x` is set. The crash half clearly belongs in a patch release;
the false-negative half means a 4.0.x bump could start emitting E0202 on code that was
clean before, and the two cannot be separated — they are the same two lines. (The
`try/except StatementMissing` approach floated in #11361 would fix only the crash, but
it leaves both false negatives in place and keeps the scope walk, so it is the worse
trade.)

The primer argues the practical risk is small: zero delta across 15 packages. Still
worth a conscious decision rather than an inherited label.

## On #8079

Same root cause; this PR fixes the last remaining repro (the
`tuple = namedtuple(None, [])` variant already stopped reproducing under astroid 4).
Three notes before closing it:

- **The "Needs decision" blocker no longer applies.** The 2023 objection was cost —
  "checking that a builtin is indeed a builtin is going to cost an enormous amount of
  computing power". This approach sidesteps it entirely: it does not add a builtin check
  at all — a `dict.get` _replaces_ a full scope walk plus `_filter_stmts`. Measured
  cost-neutral on django (above), so there is nothing left to weigh.
- **Jacob's second point is still live.** With `--jobs=2` a checker crash still escapes
  as a raw `concurrent.futures` RemoteTraceback instead of the `F0002 astroid-error`
  that serial mode emits — verified on `main` today. The follow-up issue he asked for in
  2023 was never opened. Worth opening it rather than letting that half disappear when
  #8079 closes.
- **#8210 (open) is the astroid-side twin**, not a duplicate: the same `_filter_stmts` →
  `statement()`-on-a-raw-built-module defect, but reached from astroid's own
  `ClassDef.ancestors()` rather than from pylint. Not fixed here.

Fixing `_filter_stmts`/`statement()` in astroid would kill this whole family at the
source; this PR is the right local fix in the meantime.
