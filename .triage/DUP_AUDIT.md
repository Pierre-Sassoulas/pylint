# DUP-issue audit report

The initial triage marked 4 issues as DUP but for 3 of the 4 the direction was reversed
(newer marked canonical, older marked dup). This audit:

1. Verified each pair's snippet reproduces the same root cause on current pylint (4.0.5
   / astroid 4.0.2 — and for the numpy/pandas pairs, numpy 2.4.4 / pandas 3.0.3
   installed in the active venv).
2. Adopted the convention **older issue = canonical, newer = DUP**.
3. Corrected the triage notes so the canonical for each pair is now flagged REPRO and
   the newer report is DUP-of-canonical.

## Pair-by-pair findings

### 1. numpy.finfo.eps no-member (numpy 2.4+)

| Side          | Issue                                                       | Created    | Comments | Labels       | Snippet repro on 4.0.5 + numpy 2.4.4  |
| ------------- | ----------------------------------------------------------- | ---------- | -------: | ------------ | ------------------------------------- |
| **Canonical** | [#10806](https://github.com/pylint-dev/pylint/issues/10806) | 2026-01-08 |        0 | needs triage | `_ = np.finfo(float).eps` → E1101 ✅  |
| Duplicate     | [#10838](https://github.com/pylint-dev/pylint/issues/10838) | 2026-02-04 |        1 | needs triage | `print(np.finfo(1.0).eps)` → E1101 ✅ |

**Root cause:** astroid's numpy brain doesn't track `finfo`'s properties as of numpy
2.4. #10806 includes a pip-bisect showing numpy 2.4.0 introduces the regression and
numpy 2.3.5 works fine. #10838 is a one-liner repro by a different reporter.

**Action:** Close #10838 as duplicate of #10806.

---

### 2. pandas DatetimeIndex no-member

| Side          | Issue                                                       | Created    | Comments | Labels                                            | Snippet repro on 4.0.5 + pandas 3.0.3                           |
| ------------- | ----------------------------------------------------------- | ---------- | -------: | ------------------------------------------------- | --------------------------------------------------------------- |
| **Canonical** | [#10166](https://github.com/pylint-dev/pylint/issues/10166) | 2025-01-03 |        0 | needs triage                                      | `date_range(...).to_pydatetime()` → E1101 on `to_pydatetime` ✅ |
| Duplicate     | [#10796](https://github.com/pylint-dev/pylint/issues/10796) | 2026-01-01 |        5 | False Positive, Lib specific, Needs investigation | `date_range(...).date` → E1101 on `date` ✅                     |

**Root cause:** astroid's pandas brain doesn't expose `DatetimeIndex`'s full public
property set. Two different missing methods (`to_pydatetime` and `date`) but a single
underlying fix would resolve both.

**Caveat:** by date, #10166 is older and the convention says it's canonical. However,
#10796 has substantially more discussion (5 comments, 3 substantive labels) and reporter
`sam-s` filed several related pandas-DatetimeIndex issues. Maintainers may prefer the
inverse direction (keep #10796, close #10166). Either way the underlying issue is the
same and one fix covers both — the audit notes this asymmetry rather than forcing a
choice.

**Action:** Either close #10796 as dup of #10166 (canonical-by-date), or close #10166 as
dup of #10796 (canonical-by-engagement). Consolidate the missing-members list
(`to_pydatetime`, `date`, …) on the surviving issue.

---

### 3. TypeAliasType `__value__` no-member (PEP 695)

| Side          | Issue                                                       | Created    | Comments | Labels                                    | Snippet repro on 4.0.5                                                                             |
| ------------- | ----------------------------------------------------------- | ---------- | -------: | ----------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Canonical** | [#10091](https://github.com/pylint-dev/pylint/issues/10091) | 2024-11-22 |        2 | False Positive, **Needs PR**, python 3.12 | `type X = str; print(X.__value__)` → E1101 'Class str has no **value** member' ✅                  |
| Duplicate     | [#9885](https://github.com/pylint-dev/pylint/issues/9885)   | 2024-08-19 |        0 | needs triage                              | `type Abc = Literal["a"]; print(Abc.__value__)` → E1101 'Class Literal has no **value** member' ✅ |

**Root cause:** astroid doesn't model `TypeAliasType` (the runtime object produced by
`type X = ...`) at all — it sees `Abc` as if it were the wrapped type (`Literal`, `str`,
…) and therefore can't find `__value__` on it.

**Maintainer handling:** even though #9885 is older by date, Jacob Walls explicitly
redirected #10091 via a
[maintainer comment](https://github.com/pylint-dev/pylint/issues/10091) to focus on the
`__value__` no-member bug — the original body of #10091 mixed three PEP-695 bugs, two of
which were already tracked elsewhere (#9335, since closed, for `undefined-variable T` on
`class A[T]:`; and #9884 for `redefined-outer-name T`). The reporter `jesnie` added a
follow-up comment with the `type S = str; print(S.__value__)` example and Jacob's "I'll
refocus this ticket on the 3rd issue you report here with no-member" confirmed #10091 as
the canonical for `__value__`. #9885 had no maintainer attention, so the convention
"older = canonical" is overridden here by explicit maintainer intent.

**Action:** Close #9885 as duplicate of #10091.

---

### 4. PEP 695 redefined-outer-name (W0621)

| Side          | Issue                                                       | Created    | Comments | Labels                                                     | Snippet repro on 4.0.5                                                                      |
| ------------- | ----------------------------------------------------------- | ---------- | -------: | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Canonical** | [#9884](https://github.com/pylint-dev/pylint/issues/9884)   | 2024-08-19 |        1 | Astroid, typing, False Positive, **Needs PR**, python 3.12 | `type Foo[T] = T; def foo[T]: ...` → W0621 ✅                                               |
| Duplicate     | [#10995](https://github.com/pylint-dev/pylint/issues/10995) | 2026-04-30 |        0 | needs triage                                               | `type Alias[T] = T \| list[T]; def identity[T](x: T) -> T:` + @overload variants → W0621 ✅ |

**Root cause:** PEP 695 type-parameters (`[T]`) are statement-scoped per the PEP, but
pylint treats them as module-scope, so reusing `T` in subsequent statements triggers
`redefined-outer-name`.

**Action:** Close #10995 as duplicate of #9884. #10995's @overload variants can be
folded into #9884 as additional test cases.

---

## Summary

| #   | Canonical (keep open) | Duplicate (close) | Bug area                                                                                              |
| --- | --------------------- | ----------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | #10806                | #10838            | numpy.finfo.eps no-member                                                                             |
| 2   | #10166                | #10796            | pandas DatetimeIndex no-member                                                                        |
| 3   | #10091                | #9885             | TypeAliasType.**value** (Jacob refocused #10091 via maintainer comment; #9885 is older but unnoticed) |
| 4   | #9884                 | #10995            | PEP 695 type-param redefined-outer-name                                                               |

Triage state updated: the 4 canonical issues are now `REPRO`, the 4 duplicates are
`DUP-of-NNNN` with a note pointing at the canonical. New verdict tally: **REPRO 177**,
**DUP 4**, **EXTDEP 192**, **FIXED 32**, **DESIGN 598**, **UNCLEAR 18**, **STALE 1**.
