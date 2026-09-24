# UNCLEAR-issue audit

## Starting state

18 issues marked UNCLEAR (no minimal reproduction at triage time).

## Method

For each issue: fetched all GitHub comments via the REST API (saved to
`.triage/unclear_comments.json`), reviewed for maintainer notes and reporter-supplied
repros, then tried to reproduce on current pylint where applicable.

## Outcome

| Verdict transition | Count |
| ------------------ | ----: |
| UNCLEAR → REPRO    |     4 |
| UNCLEAR → EXTDEP   |     5 |
| UNCLEAR (refined)  |     9 |
| **Total**          |    18 |

### Upgraded to REPRO (4)

| Issue      | Why                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **#8079**  | Self-contained reproducer found: class with method named `license` (or any site-builtin) **and** `self.license = ...` in `__init__` crashes `class_checker.visit_functiondef` via `ancestor.lookup`. Crashes on pylint 3.3.8 / 4.0.5 / 4.1-dev. Snippet at `.triage/snippets/i8079.py`. Earlier FIXED determination was based on a different sub-case (`tuple = namedtuple(None, [])` from closed dup #10159), which **is** fixed in astroid 4.0.0 via a different code path. |
| **#10991** | Verified on pylint 4.1.0-dev0 / astroid 4.2.0b3 (origin/main): `E1123 Unexpected keyword argument 'value'` fires on the dataclass+TypeVarTuple chain. My earlier "doesn't reproduce" was on astroid 4.0.2 which lacks PEP-695 TypeVarTuple support; newer astroid surfaces it. Reporter's MCharming98 comment pinpoints the root cause: `_infer_sequence_helper` failing on a Starred-with-TypeVarTuple, breaking MRO + `brain_dataclasses`.                                  |
| **#3602**  | Verified on pylint 4.0.5: pyreverse `-S` on the numpy snippet **hangs** >60s without producing output (vs. the original 2020 max-recursion-depth crash, which is fixed). The performance regression Pierre flagged in 2022 (_"not crashing but taking really fucking long"_) is still present. Workaround: bounded `-s2` finishes in seconds.                                                                                                                                 |
| **#22**    | Verified on pylint 4.0.5: `pyreverse -c <unqualified> <pkg>` still crashes — different exception than the 2013 `ValueError` (now `AttributeError: 'EmptyNode' object has no attribute 'name'` in `pyreverse/inspector.py:467`). Same UX problem (poor error for bad input); workaround is fully-qualified `pyreverse -c top.mod.Class pkg`.                                                                                                                                   |

### Upgraded to EXTDEP (5)

These were "crash on a specific library" reports where the reporter or comments
identified the dependency that triggers it. They're genuine bugs; reproduction needs the
library.

| Issue     | Dependency                              | Notes                                                                                                                                  |
| --------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **#9137** | `pymongo==4.5.0` (via `bson`)           | Reporter provided exact mktemp/venv recipe. Astroid `'UninferableBase' object is not iterable`.                                        |
| **#8049** | `haggis`                                | Runtime monkey-patch of `logging` via `add_trace_level()`. Maintainer (Jacob) confirmed 2023-09: predates 3.0, blocker label could go. |
| **#7680** | `sqlalchemy` `declared_attr.directive`  | Pierre's last comment links to similar crashes in #9479 / #10474.                                                                      |
| **#7389** | `xarray`                                | abel-bzz's MRE: any class inheriting `xr.DataArray` from inside an `__init__.py`.                                                      |
| **#2188** | Zope `Products.CMFPlone` / `OFS.Folder` | C-extension `ExtensionClass.Base` breaks C3 MRO computation. PCManticore + idgserpro analyzed extensively 2018-19.                     |

### Stays UNCLEAR — needs reporter info (9)

Refined the triage note for each with concrete current-pylint behaviour so the next
person sees what was already tried.

| Issue  | What we know                                                                                                                                                                                                         |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| #11013 | Verified clean under default+testing_pylintrc. Reporter has heavy custom config (`pylint-per-file-ignores`, `docparams`, `mccabe`, …); needs their exact `.pylintrc`.                                                |
| #11012 | Same as #11013 — same reporter, same config, same plugin family.                                                                                                                                                     |
| #10941 | Pylint 3.2.2 (>2y old). Pierre asked for a stacktrace / minimal repro 2026-03; reporter never followed up.                                                                                                           |
| #10352 | Needs reporter's "empty custom astroid transform plugin" — never shared minimal version.                                                                                                                             |
| #10278 | ImportError on implicit namespace package; needs reporter's directory tree.                                                                                                                                          |
| #10012 | Verified pylint 4.0.5: `# pylint: disable=too-many-lines` on line 4 (after multi-line docstring) DOES suppress C0302 in a 1025-line file. Reporter described "occasional" CI flakiness, no deterministic reproducer. |
| #9993  | Cryptic title; body refers to a package layout not included.                                                                                                                                                         |
| #9983  | Confusing `Uninferable_factory` message when `**kwargs` dict key is Uninferable. Real bug but reporter never reduced to a snippet; only linked their personal repo.                                                  |
| #7268  | Verified pylint 4.0.5: the `class Color(NamedTuple): RED,…=31,…` snippet doesn't crash. Jacob couldn't reproduce in 2022. Reporter acknowledged a messy VSCode venv. Likely env-specific.                            |

## New tally (open issues only)

```
DESIGN  598
EXTDEP  197  (+5)
REPRO   181  (+4 -1)
FIXED    32  (-1)
UNCLEAR   9  (-9)
DUP       2
STALE     1
```
