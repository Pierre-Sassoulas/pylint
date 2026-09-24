# REPRO bisect report

For each of the 20 live REPRO snippets (19 from the prior REPRO bucket
plus #11032 NEW), this report records when the false positive / negative
first surfaced in **pylint** release history.

Test harness: `/tmp/bisect/run.py` runs each snippet under each pinned
pylint version (uv-managed) with `--disable=all --enable=<msg>` and grep
for the expected message. Snippet files live at
`/tmp/bisect/iNNNN.py` (extracted from the
`issue-triage-workspace` branch). Spec at `/tmp/bisect/spec.json`.

For false positives, **BUG** = message *is* emitted (shouldn't be).
For false negatives, **BUG** = message *not* emitted (should be).
**OK** = no defect at this version. **CRASH** = pylint exits with traceback.

## Methodology notes

- Python 3.12 used for 2.15.10 → main (apples-to-apples).
- Python 3.10 added for 2.13.9 / 2.14.5, which don't run on py3.12.
- One snippet (#9839 IntEnum `__slots__`) is Python-version dependent —
  it's a runtime change in py3.12, not a pylint regression.
- For each newly-OK→BUG transition I grepped the pylint commit log
  between the bracketing versions to find the introducing PR.

## Matrix (Python 3.12 unless noted)

Columns are pylint versions, ordered oldest→newest.

| Issue | 2.15.10 | 2.16.4 | 2.17.7 | 3.0.0 | 3.0.4 | 3.1.1 | 3.2.0 | 3.2.7 | 3.3.0 | 3.3.5 | 4.0.0 | 4.0.5 | main | Bisect verdict |
|-------|---------|--------|--------|-------|-------|-------|-------|-------|-------|-------|-------|-------|------|-----------------|
| #8221  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 (also BUG on 2.13.9/py3.10) |
| #8367  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| #9359  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | OK in 2.13.9/2.14.5 (py3.10), BUG in 2.15.10. Surfaces with astroid 2.11→2.13 bump |
| #9389  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | same window as #9359 — surfaces 2.14→2.15 (astroid 2.11→2.13) |
| #9488  |CRASH|CRASH|CRASH| BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | crashed pre-3.0, FP since 3.0 |
| #9683  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| #9839  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | Python 3.12-only (OK on py3.10/3.11 at 2.17.7) — IntEnum runtime change, not a pylint regression |
| #9850  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| #9905  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| **#9950** | OK | OK | OK | OK | OK | OK | OK | OK | **BUG** | BUG | BUG | BUG | BUG | **regression: pylint 3.3.0, commit `1c496e9b3` (PR #9564 "Add a new ``declare-non-slot`` error code"). FP shipped with the new checker.** |
| #9972  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| **#9986** | OK | **BUG** | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | **regression: pylint 2.16.0, commit `f2e8ba369` (PR #7750 "New checker `unbalanced dict unpacking`"). FP shipped with the new checker.** |
| #9994  | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | OK in 2.13.9/2.14.5 (py3.10), BUG in 2.15.10. Same window as #9359 |
| #10186 |CRASH|CRASH|CRASH| BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | crashed pre-3.0, FP since 3.0 |
| #10609 | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| **#10691**| OK | **BUG** | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | **regression: pylint 2.16.0, commit `78770cdab` (PR #7526 "Add `magic-number` checker"). Conflict with R6103 (consider-using-assignment-expr, added pylint 2.11 by `a754d8dd7`) shipped uncoordinated.** |
| #10784 | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| **#10991**| OK | OK | OK | OK | OK | OK | OK | OK | OK | OK | **BUG** | BUG | BUG | **regression: pylint 4.0.0** (astroid 4.0.x added PEP 646 TypeVarTuple support, exposing a pre-existing dataclass-`__init__` reconstruction FP that was previously hidden because astroid couldn't see through `Generic[T, *Shape]`). |
| #10994 | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 |
| #11032 | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | BUG | predates 2.15 — metaclass `__call__` signature handling has never consulted astroid for `__init__` override |

## Bucket summary

### Real pylint regressions (4)
| Issue | First-bad pylint | Commit | PR |
|-------|------------------|--------|----|
| **#9950** | 3.3.0 | `1c496e9b3` | #9564 (new checker `declare-non-slot`) |
| **#9986** | 2.16.0 | `f2e8ba369` | #7750 (new checker `unbalanced-dict-unpacking`) |
| **#10691** | 2.16.0 | `78770cdab` | #7526 (new checker `magic-value-comparison`, conflicts with #4876 R6103) |
| **#10991** | 4.0.0 | (astroid 4.0.x via PEP 646 brain) | (none — astroid bump exposed pre-existing dataclass FP) |

For the three "shipped-with-new-checker" regressions (#9950, #9986, #10691):
the underlying FP was inherent to the heuristic on day-one. The "regression"
is just the day the checker landed. Most actionable: tighten the heuristic
in a focused PR.

### Surfaces with astroid bump 2.11→2.13 (in pylint 2.14→2.15) (3)
| Issue | Notes |
|-------|-------|
| #9359 | `useless-parent-delegation` on child-of-builtin (list/dict) — different inference for builtin `__init__` |
| #9389 | dataclass(init=False) inherited subclass `too-many-function-args` — dataclass init reconstruction |
| #9994 | `useless-parent-delegation` on Exception subclass with `super().__init__()` — Exception's `__init__` varargs handling |

These are "pylint side" only in the trivial sense (pylint consumes astroid). Root
cause is astroid 2.12/2.13 inference change. Filing PRs against astroid would be
more impactful than touching pylint.

### Surfaces only on Python 3.12 (1)
| Issue | Notes |
|-------|-------|
| #9839 | E0238 `invalid-slots` on IntEnum `__slots__ = ()` — Python 3.12 changed IntEnum representation; astroid stub catches up partially. Not a pylint regression. |

### Predate the oldest stably-testable pylint (2.15) — 11
#8221, #8367, #9488 (crashed pre-3.0), #9683, #9850, #9905, #9972, #10186 (crashed pre-3.0), #10609, #10784, #10994, #11032.

These are old, structural bugs in pylint's inference / checker logic.
For triage: label them `False Positive 🦟`/`False Negative 🦋` and let
contributors pick.

## Raw outputs

Per-version JSON: `/tmp/bisect/results/result_<version>.json`.

## Reproducing

```bash
bash /tmp/bisect/bisect.sh           # main matrix (2.15→main on py3.12)
# Then manually for 2.13/2.14 on py3.10:
cd /tmp/bisect && uv run --no-project --python 3.10 --with "pylint==2.13.9" python /tmp/bisect/run.py
```
