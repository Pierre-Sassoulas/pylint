# FIXED-issue audit report

Following the FIXED triage classification (32 issues), this audit:

1. Verified each "FIXED" claim with pylint 4.0.5 using
   `pylint/testutils/testing_pylintrc` (rather than pylint's own pylintrc, which
   silences many checkers and masked false-FIXED classifications during the initial
   sweep).
2. Bisected pylint versions 2.13 → 4.0.5 to find the minor release that introduced the
   fix.
3. Added 32 regression tests under `tests/functional/r/regression_03/`.

## Re-verification corrections

After re-running with the test rcfile, **9 of the originally-FIXED issues were actually
still REPRO**:

- #10768, #10766 — invalid-name still fires (pylint's own pylintrc disables
  `invalid-name`)
- #8600 — protected-access still fires (pylintrc disables `protected-access`)
- #8499 — invalid-name still fires
- #3325 — attribute-defined-outside-init still fires (pylintrc disables it)
- #7934 — missing-function-docstring still fires (pylintrc disables `missing-docstring`)
- #8201 — trailing-comma-tuple FN persists
- #7950 — abstract-method FN persists
- #241 — unused-import FN persists

These were moved back to REPRO in the triage state.

## Closed by merges since the audit (2026-05-18 refresh)

Three issues closed since the audit, all by PRs merged to `main`. No bisect needed —
the fix commit is the PR itself.

| Issue | Closed by | Notes |
| ----- | --------- | ----- |
| #7950 | PR #7955 (commit `9f08fc7bb`) | Takeover from sshane; `class_is_abstract` now flags concrete subclasses without explicit `abc.ABC` opt-in |
| #6211 | PR #7360 (commit `c0aa7e58e`) | Takeover from adam-grant-hendry; NumPy `default ...` markers in the type field now accepted |
| #3716 | PR #10989 (commit `3d7ac126f`) | `dangerous-default-value` now reports `typing.NamedTuple` default args |

Verdict tally after refresh: DESIGN 596, EXTDEP 197, REPRO 180, **FIXED 32**, UNCLEAR
9, DUP 2, STALE 1 (1017 open). FIXED count is unchanged because the three new closures
replace the three that were never claimed as FIXED by the original audit — they were
DESIGN/REPRO before being addressed by takeovers.

## Confirmed-fixed by version

Bisect run on Python 3.12. pylint 2.10 and earlier don't run on Python 3.12 (wrapt
import error), so the oldest tested version is 2.13.

| Fix version | Issues                                                                                                                                        |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **4.0.0**   | #8068 (unsupported-delete-operation), #4608 (invalid-unary-operand-type after ternary), #3925 (not-callable after destructure)                |
| **3.3.0**   | #9722 (comparison-with-callable on multi-level property subclass), #3893 (E1123 class chosen by loop), #3603 (E1123 if/else class definition) |
| **3.1.0**   | #7647 (unnecessary-lambda + conditional kwargs)                                                                                               |
| **3.0.0**   | #9497 (datetime.datetime no-member FN), #7350 (E0601 nested try/raise), #4554 (no-value-for-parameter \*list(...))                            |
| **2.15.0**  | #8805 (zipimport no-member), #7240 (no-member in sys.platform-guarded comprehension), #3327 (no-member on from-imported "builtins")           |
| **≤ 2.13**  | 19 issues (fix predates the oldest Python-3.12-compatible pylint). See full table in `.triage/fix_versions.json`                              |

The "≤ 2.13" bucket includes #10670, #10455, #10442, #10422, #10374, #10298, #8419 (FN),
#8250, #8179, #8053, #8050, #7891, #7381, #5823, #4920, #2981, #2821, #1934, #1493. For
these the original report was filed on a more recent version, meaning either:

- The bug was fixed long before the report (reporter's version was already-fixed, but
  their config or library version made the bug present again)
- My minimal snippet doesn't reproduce the original bug at any version (the regression
  test only verifies that the snippet behaves correctly on current pylint)

## Regression tests added

All 32 tests live under `tests/functional/r/regression_03/`. Naming convention:
`regression_NNNNN.py` (where NNNNN is the issue number).

One exception: `regressionMain10442.py` uses camelCase naming because the test exercises
`module-naming-style=camelCase` (and the test filename itself must satisfy that style).

Helper artifacts written alongside each test:

- `regression_NNNNN.rc` — when a non-default config is required (e.g. extension plugins,
  naming style)
- `regression_NNNNN.txt` — when the test expects pylint to emit a message (i.e.
  false-negative fixes)

Tests with rc files: #10422, #10374, #10442 (renamed), #8179, #8250 Tests with txt
files: #9497, #8419

## Run the tests

```sh
python -m pytest tests/test_functional.py -k regression_03
```

or for a specific issue:

```sh
python -m pytest tests/test_functional.py -k regression_10670
```

To regenerate expected `.txt` files after editing a snippet:

```sh
python tests/test_functional.py --update-functional-output -k "test_functional[regression_NNNNN]"
```

## Supporting files

- `.triage/bisect_versions.py` — the bisect runner used to identify fix versions
- `.triage/bisect_results.json` — raw bisect data (behavior × version)
- `.triage/fix_versions.json` — derived "first version with fix"
- `.triage/reverify_fixed.py` — the re-verifier that caught the 9 false-FIXED
  determinations
- `.triage/build_regression_tests.py` — generator for the regression test files

## Caveats

1. **Coarse bisect granularity:** I tested major+minor releases (2.13, 2.15, 2.17,
   3.0…3.3, 4.0, 4.0.5), not patch releases. For exact-commit identification, a finer
   pass would test each patch tag.
2. **Snippet completeness:** A "<= 2.13" verdict can mean either (a) the fix predates
   2.13, or (b) my minimal snippet doesn't reproduce the bug at all. For category (b)
   the regression test will pass trivially on all versions; that's still a useful
   "lock-in" test but doesn't add coverage for the original bug.
3. **Pre-2.13 versions untested:** pylint 2.10 and earlier fail to import on Python 3.12
   (wrapt's use of `inspect.formatargspec`, removed in 3.11). A second pass with Python
   3.10 would let us bisect that older range.
4. **No fragments added:** the user opted to skip towncrier fragments since fixes
   already shipped in their respective releases.
