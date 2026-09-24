# PR #11043 — review + split

Original branch tip `7756e5460` (34 tests). Reviewed by replaying every issue's **own**
reproduction against current main (pylint 4.1.0-dev0 / astroid 4.3.0), then bisecting
the survivors on Python 3.12 across pylint 2.13 → 4.0.5.

## Outcome

- **18 tests kept** (17 new; main independently added its own 7647 test), rebuilt on a
  fresh branch `regression-tests-fixed-issues` (19 commits, one per test, no issue
  numbers in the messages).
- **16 tests dropped** — their snippet was not the issue's reproduction, and the issue
  still reproduces on current main.

## A. Dropped (16) — issue still reproduces

| Issue | Why the snippet could not fail                                                                                                                        | Still fires on main                               |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| 1934  | captures the loop variable in a `lambda`; the report captures a loop-**body** variable in a nested `def`                                              | `W0640`                                           |
| 2821  | `test2` rewritten to _assign_ `get_table`; the report _reads_ `.return_value`                                                                         | `E1101 ... no 'return_value'`                     |
| 3327  | no module named `builtins` anywhere; uses a `collections.abc` alias                                                                                   | `E1101: Instance of 'dict' has no 'foo'`          |
| 4920  | unannotated parameter is `Uninferable`; the report binds `except Exception as exc`                                                                    | `E1101 ... 'Exception' has no 'status'`           |
| 5823  | dropped the class that uses `super(Dog, self)` — the only form `R1725` can fire on                                                                    | `R1725`                                           |
| 7240  | `.rc` excludes win32, the only platform where `os.getgroups` is absent                                                                                | 2× `E1101` when mirrored with a win32-only member |
| 7891  | `Foo(1)._asdict()` at module level; the report uses `self._asdict()` in a method                                                                      | `_asdict`, `_fields`, `_replace`                  |
| 8050  | extension-less-file discovery bug; a `.py` file in the suite cannot express it                                                                        | `pylint something/something` still silent         |
| 8179  | loads `code_style` but `R6104` is `default_enabled: False`, so nothing runs                                                                           | `R6104` once enabled                              |
| 8250  | `.rc` omits `accept-no-return-doc=no` from the reporter's config                                                                                      | 4× duplicated `W9011`/`W9012`                     |
| 8419  | reporter retracted that snippet; it duplicates `unspecified_encoding_py38.py:66`. The real cases are `(a / 'b.txt').read_text()` and `path.open('r')` | both still silent                                 |
| 10298 | parameter narrowing; the report is about a class variable returned as `list[int]`                                                                     | `E1133`                                           |
| 10374 | `_` assigned once; `R0204` needs two assignments of different types                                                                                   | `R0204`                                           |
| 10422 | `meth_name = "test"` is inferable; the report needs an un-inferable attribute                                                                         | `E1102`                                           |
| 10442 | test file already conforms to camelCase; the report is about `__main__.py`                                                                            | `C0103`                                           |
| 10670 | `min_pyver=3.12` skipped Python 3.11; the cause is not version-specific at all                                                                        | `E1121`                                           |

Two recurring causes: **the checker never ran** (8179, 8250 — plugin loaded but the
message or option never enabled) and **the inference was simplified away** (2821, 4920,
7891, 10298, 10422). Worth keeping as a checklist for the next batch.

Also note 8179, 8250, 10374 and 10442 are labelled _Proposal_ / _Needs decision_ /
_Needs specification_ — open design questions, not bugs awaiting a regression test.

## B. Kept (18) — with verified bisect

| Issue | Verified history                                                                 |
| ----- | -------------------------------------------------------------------------------- |
| 1493  | reproducible up to 2.14, fixed in **pylint 2.15.0**                              |
| 2981  | clean from 2.13 on; the report was Python 3.6-only                               |
| 3603  | up to 3.1, fixed in **3.3.0**                                                    |
| 3893  | up to 3.1, fixed in **3.3.0**                                                    |
| 3925  | up to 3.3, fixed in **4.0.0**                                                    |
| 4554  | reproducible on 2.15, fixed in **3.0.0**                                         |
| 4608  | up to 3.3, fixed in **4.0.0**                                                    |
| 7350  | up to 2.15, fixed in **3.0.0**                                                   |
| 7381  | unreachable since pylint requires Python 3.10 (the union fallback returns early) |
| 7647  | up to 3.0, fixed in **3.1.0** (test now main's, see below)                       |
| 8053  | **regressed in 3.0.0**, present through 4.0.5, fixed by **astroid 4.1.0**        |
| 8068  | up to 3.3, fixed in **4.0.0**                                                    |
| 8805  | reproducible on 2.13, fixed in **2.15.0**                                        |
| 9159  | **regressed in 3.0.0**, present through 4.0.5, fixed by **astroid 4.1.0**        |
| 9470  | clean from 2.13 on                                                               |
| 9497  | false negative up to 2.15, detected from **3.0.0** on                            |
| 9722  | up to 3.1, fixed in **3.3.0**                                                    |
| 10455 | clean from 2.13 on                                                               |

Corrections applied while rebuilding:

- **1493** — replaced the two-callables snippet with the reported list-of-dicts (first
  entry `None`) plus the class-attribute variant from the thread.
- **2981** — added the read-then-write and intermediate-subclass variants.
- **7381** — added the nested-enum and subscript shapes from the thread; renamed a
  module-level name that shadowed a parameter.
- **8053** — restored the three trailing lines the original PR dropped. **This is what
  makes the test worth having**: it is the only part that reproduces, and it caught a
  3.0.0 → 4.0.5 regression fixed by astroid 4.1.0.
- **10455** — annotated the dicts as reported.
- Every version claim in the docstrings was re-derived; the previous "Fix landed before
  pylint 2.13" wording over-claimed what a bisect floor shows.

## C. Closeable

Closeable now: 1493, 3603, 3893, 3925, 4554, 4608, 7350, 7381, 7647, 8053, 8068, 8805,
9159, 9470, 9497, 9722, 10455.

### 10670 is a live bug, Python 3.11 only

Bumping `min_pyver` from 3.12 to 3.11 (correct — `typing.Self` is 3.11, so 3.12 was
always too high) turned the 3.11 CI job red, and it reproduces locally:

    pylint 4.1.0-dev0 / astroid 4.3.0 / Python 3.11.15
    E1121: Too many positional arguments for classmethod call (too-many-function-args)

Clean on 3.12 and 3.13. Root cause, from inferring `super().__new__` inside a
`datetime.datetime` subclass:

| Python | what `super().__new__` infers to                                                          |
| ------ | ----------------------------------------------------------------------------------------- |
| 3.13   | `_pydatetime.datetime.__new__` (9 params) **and** `date.__new__` **and** `object.__new__` |
| 3.11   | **only** `object.__new__` from builtins, params `['self', 'cls']`                         |

So on 3.11 astroid's `super` proxy does not walk the `datetime` MRO and falls back to
`object.__new__`, which takes no extra positionals. Note
`datetime.datetime.getattr("__new__")` resolves fine on 3.11 (9 params) — it is
specifically the `super()` path that fails. The likely trigger is the 3.12 split of the
stdlib into `datetime.py` + `_pydatetime.py`.

That is an astroid bug, and the issue must stay open.

## D. Status

Branch force-pushed to `pierre/regression-tests-fixed-issues` (`7756e5460` ->
`4b0d60db3`), PR 11043 retitled and rewritten: 19 commits, no `#` and no issue URLs in
the title, body or commit messages, so nothing was cross-referenced.

Left to decide: what to do with the 15. Rebuilding one means copying the reporter's
snippet **unmodified**, adding the options they used, and confirming the test fails on a
pylint where the bug existed before calling it a regression test. Since all fifteen
still reproduce, they are bugs to fix rather than tests to land.

## E. 7647 collided with main

Main's astroid 4.3.1 upgrade (`ac6ca5f4b`) added a test at the same path,
`tests/functional/r/regression_03/regression_7647.py`. Merging main conflicted there;
the resolution kept this branch's copy and dropped main's. `1b324f986` puts main's
version back verbatim, so the branch contributes 17 new tests, not 18. The bisected
history (up to pylint 3.0, fixed in 3.1.0) still stands and the issue is still
closeable.

Baseline check on the merged head, with astroid pinned to 4.3.1 in a worktree venv: main
`15 failed, 891 passed`, branch `15 failed, 908 passed` — the same 15 pre-existing
failures (scratch venv missing dev deps), and exactly 17 added passing tests.

## F. 2981 held back

The issue's own reopening comment
(`https://github.com/pylint-dev/pylint/issues/2981#issuecomment-1677679873`) reports the
same `access-member-before-definition` across **two modules**: a subclass in `child.py`
reading an attribute that `Parent.__init__` assigns in `parent.py`.

That does not reproduce here at any combination tried:

| pylint                           | astroid  | Python           | result |
| -------------------------------- | -------- | ---------------- | ------ |
| 2.17.5 (reporter's)              | 2.15.8   | 3.10.21          | clean  |
| 2.13 / 2.14 / 2.15 / 2.16 / 2.17 | matching | 3.11, 3.12       | clean  |
| 3.0.0, 3.3.0, 4.0.5              | matching | 3.10, 3.11, 3.12 | clean  |
| 4.1.0-dev0                       | 4.3.1    | 3.13             | clean  |

Flat directory, package with `__init__.py`, absolute and relative import, linting the
file, the package, and `--recursive=y` — all clean. The snippet is the comment's own,
byte for byte apart from its trailing `# Generates E0203 error` comment.

The negative is controlled, at the reporter's exact stack and on current main:

| control                                           | result                                         |
| ------------------------------------------------- | ---------------------------------------------- |
| `self.x` read then assigned in one file           | `E0203` fires — the checker is live            |
| `Child` reads an attribute `Parent` does not have | `E1101` fires — `parent.py` really is resolved |
| the comment's code                                | no `E0203`, and no `import-error` either       |

So "clean" is a genuine negative rather than an unresolved import quietly producing no
messages. The earlier same-file variants (`tucked`'s read-then-write, `mthuurne`'s
`Middle[int]`) are clean too.

Failing to reproduce is not the same as showing it fixed, so `Closes #2981` was removed:
17 issues close on merge, the test stays as a guard, and the issue waits on a
reproduction from the reporter.

## G. 10670 — the issue already had the diagnosis

Comment 5345397424 (19 August 2026) beat me to it, and goes further than my version
table:

- The fallback `__new__` astroid hands out for C types outside `builtins` was typed
  `(self, cls)`. `__new__` takes the class explicitly, so every further argument counted
  as one too many.
- `datetime` escapes on 3.12+ only because the stdlib split gives it a real
  `_pydatetime.datetime.__new__` to resolve to. That matches what I measured
  (`['self','cls']` from builtins on 3.11, the nine-parameter signature on 3.13) — but
  the interpreter is the symptom, not the cause.
- The same defect is reachable with no `datetime` at all:

      class MyArray(array.array):
          def __new__(cls, data):
              return array.array.__new__(cls, "b", data)  # E1121

  Verified on pylint 4.1.0-dev0 / astroid 4.3.1, on **both** Python 3.11 and 3.13.

- The comment also flags this PR by name: a `min_pyver=3.12` test passes without
  covering the reported case. Correct, and now acted on.

**Status of the fix.** astroid PR 3238 merged 26 August 2026 (`8044012`). astroid 4.3.1
was tagged 17 August, and the fix is 28 commits past that tag — so it is _not_ in the
astroid this branch pins, and the bug is live here. The issue stays open and no test for
it lands now.

**When astroid next releases**, the test to add is the `array.array` one: no `min_pyver`
gate, and it exercises the cause rather than one interpreter's symptom.

**Process note.** `gh issue view 10670` reported one comment and I did not read it. For
an issue that looks fixed, the comments are where the counter-evidence lives — the same
lesson as 2981, where the reopening comment was the thing to reproduce.
