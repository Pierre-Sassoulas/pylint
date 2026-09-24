# Review — PR #11163 (skip `unspecified-encoding` for unknown `open` modes)

Round 2, on head `3fffeb533` (was `f3f86a171`). Verified on worktrees of the PR head and
the merge-base `9b5b337d5`, `venv/bin/python` (3.13.1).

## Status of round-1 points

| Point                                                                                                    | State                                |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Collapse the double `func_name in OPEN_FILES_MODE` test / drop the `mode_arg_is_unknown` double negative | **done**, exactly as suggested       |
| Missing test for `encoding=None` with an unknown mode                                                    | **done**                             |
| Changelog fragment should link the message                                                               | **not done** — pushed as `4ca21b930` |

Two review threads on `stdlib.py` are still marked unresolved but are outdated (the code
they point at is gone). Resolve them.

## Verification

- `pytest tests/` → `2 failed, 2173 passed`; failures are `no_name_in_module` and
  `unbalanced_tuple_unpacking`, both pre-existing on the merge-base.
- `pytest tests/test_functional.py -k "unspecified_encoding or bad_open_mode"` → 3
  passed.
- `pylint --rcfile=pylintrc pylint/checkers/stdlib.py` → 10.00.
- Behaviour on a 12-case sample, base vs PR
  (`--enable=unspecified-encoding,bad-open-mode`):

  | case                                                                                                                       | base               | PR                       |
  | -------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------ |
  | `open(F, mode)` / `open(F, mode=mode)` / `Path(F).open(mode)` / `Path(F).open(mode=mode)` / `open(F, mode, encoding=None)` | W1514 ×5           | silent ✅                |
  | `def read(p, mode="rb"): open(p, mode)`                                                                                    | W1514              | silent ✅ (the real fix) |
  | `def read(p, mode="r"): open(p, mode)`                                                                                     | W1514              | silent — note A          |
  | `mode = "r" if fruit else "rb"; open(F, mode)`                                                                             | W1514              | W1514 — note B           |
  | `open(F, str(fruit))`                                                                                                      | W1501 `""` + W1514 | unchanged — note C       |
  | every literal-mode case (`"w"`, `"wb"`, `"zz"`, …)                                                                         | —                  | unchanged ✅             |

  No message added anywhere.

The code change is right and reads well now. Two things left, both of them my own typos
in the suggestions you applied — sorry about that.

## 1. Fragment: `:ref:` not `` `ref:` ``

My suggestion put the `ref:` _inside_ the double backticks, which makes it literal text
instead of a link. It should be:

```rst
Fix a false positive for :ref:`unspecified-encoding` when an ``open`` call uses a mode
argument that cannot be inferred, including when the mode is a parameter with a default
value.

Closes #10201
```

Compare `doc/whatsnew/fragments/11148.bugfix` for the house style.

The added half-sentence is note A below: worth saying out loud, because it is a wider
bite than "cannot be inferred" suggests.

## 2. Test: `f` is a file object, not a filename

```python
    open(f, mode, encoding=None)
```

`f` resolves to the module-level `with open(FILENAME, ...) as f` binding — a file object
being passed as a path. It runs and the test passes, but functional tests get read as
examples, so:

```suggestion
    open(FILENAME, mode, encoding=None)
```

While you are there, `Path(FILENAME).open(mode=mode)` is the one spelling not covered;
one more line if you feel like it, low value since it goes through the same
`get_argument_from_call`.

## Note A — a default value now suppresses too

```python
def read(path, mode="r"):
    open(path, mode)  # base: W1514, PR: silent
```

`safe_infer` returns `None` here, because astroid infers both `Const('r')` and
`Uninferable` for the parameter and that counts as ambiguity. So the "documented
default, callers may override" pattern goes quiet as well.

Two-sided, and the primer shows the good side: with a _binary_ default (django's
`_open(self, name, mode="rb")`) it kills a plain false positive. With a text default we
lose a message a caller could still make wrong. Net positive — just document it, per
point 1.

## Note B — same family, still a false positive (out of scope)

```python
mode = "r" if fruit else "rb"
open(FILENAME, mode)  # still W1514
```

`safe_infer` returns the first `Const` when every inferred value has the same _type_, so
this "variable that can be `b`" — the literal title of #10201 — survives. Fixing it
means walking all inferred values and emitting only when every one is a text-mode
`Const`. Fine to leave; just do not expect #10201 to stay closed forever.

## Note C — pre-existing bug next door (separate issue, not this PR)

```python
open(FILENAME, str(fruit))
# W1501: "" is not a valid mode for open. (bad-open-mode)
```

astroid infers `str(x)` to `Const('')`, so a perfectly unknown mode is reported as an
_invalid_ one. Present on the merge-base too, and the `Const` check cannot see through
it. Deserves its own issue.

## Pushed

Points 1 and 2 applied directly to the branch as `4ca21b930` (both were my own typos in
the round-1 suggestions, not worth another round trip). `Path(FILENAME).open(mode=mode)`
added to the functional test at the same time. Pre-commit green on all three touched
files, functional tests pass.

Still to do by hand: resolve the two outdated `stdlib.py` threads (the GraphQL mutation
was blocked locally).
