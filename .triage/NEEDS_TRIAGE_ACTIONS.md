# Needs-triage actions — 88 open issues remaining

Initial snapshot: 2026-05-25, pylint 4.1.0-dev0, astroid 4.2.0b3.
Started from 110 needs-triage issues; 22 cleared so far. See
[Progress log](#progress-log) at the bottom.

Source: GitHub label `Needs triage :inbox_tray:` on pylint-dev/pylint + my prior
`.triage/triage_state.json` verdicts (re-verified for the recent / interesting
ones in this session).

Quick navigation:
- [Still closable](#1-still-closable-2) — #9885 (dup) and #9159 (fixed in 4.1)
- [Open PR remains tagged](#2-open-pr-remains-tagged-1) — #10670 (4.0.x fixed)
- [REPRO needing follow-up](#3-repro--leftover-tricky-case-1) — only #10691 left from the REPRO bucket
- [UNCLEAR — ping reporter](#4-unclear--needs-reporter-input-2) — #9983, #10012, #10278 (#11012 already labeled)
- [EXTDEP — external library gap](#5-extdep--external-library-or-astroid-brain-gap-39)
- [DESIGN — enhancement / spec discussion](#6-design--enhancement-or-specification-discussion-43)

| Bucket | Initial | Done | Remaining | Default labels |
|---|---:|---:|---:|---|
| Closable (FIXED / DUP) | 3 | 1 | 2 | close as completed / `Duplicate 🐫` |
| Has open PR | 1 | 1 | 0 | already labeled — see #11013 below |
| Still has triage but already fixed in 4.0.x | — | — | 1 | #10670 |
| REPRO | 19+1 NEW | 19 | 1 | the tricky #10691 — `Discussion 🤔` |
| UNCLEAR | 5 | 2 | 3 | `Needs reproduction :mag:` + `Waiting on author` |
| EXTDEP | 39 | 0 | 39 | `False Positive` + `Needs astroid Brain` (or `Upstream Bug`) |
| DESIGN | 43 | 0 | 43 | `Enhancement` / `Discussion 🤔` / `Proposal 📨` + topic |
| **Total remaining** | **110** | **22** | **88** | |

---

## 1. Still closable (2)

| # | Title | Action |
|---|---|---|
| **#9885** | False positive missing member `__value__` with type statement and Literal under python 3.12 | **Close as duplicate of #10091.** Jacob's comment on #10091 (https://github.com/pylint-dev/pylint/issues/10091) designated it as the canonical tracker. Still open with `Needs triage` as of last check. |
| **#9159** | pylint does not support typing.Self when override | **Close as fixed in 4.1.0.** Re-verified 2026-05-25: bug present on released 4.0.5+astroid 4.0.4; clean on current main (4.1.0-dev0+astroid 4.2.0b3). Likely fixed by an astroid Self-inference upgrade between 4.0.4 and 4.2.0b3. Still open with `Needs triage`. |

---

## 2. Open PR remains tagged (1)

| # | Title | Action |
|---|---|---|
| **#10670** | False Positive for too-many-function-args when subclassing `__new__` | **Already triaged** — labeled `False Positive 🦟`, `Needs triage` removed. Reporter's exact snippet scores 10/10 on pylint 4.0.5+py3.12, so this is fixed in the 4.0.x line. Could be closed-as-fixed now, but leaving open while 4.0.x is in active maintenance is fine. |

The PR I opened (**#11047** for #11013) is in review; #11013 was triaged with `Bug`, `False Positive 🦟`, `Needs astroid update`, `Needs PR`.

---

## 3. REPRO — leftover tricky case (1)

✅ **19 of the 20 REPRO bugs were labeled and stripped of `Needs triage`** on
2026-05-25. See the [Progress log](#progress-log) for the per-issue label set
and the bisect commits attached to each.

The one left:

| # | Title | Why deferred / suggested labels |
|---|---|---|
| **#10691** | Conflicting R2004 (`magic-value`) ↔ R6103 (`consider-using-assignment-expr`) | Neither warning is wrong in isolation; the bug is the circular suggestion when one is applied. Doesn't fit `False Positive 🦟`. Suggested: `Bug`, `Regression`, `Optional Checkers`, `Discussion 🤔`. **Spec call needed** — should R6103 skip walrus rewrite for literal-comparisons, or should R2004 look through walrus? |

---

## 4. UNCLEAR — needs reporter input (3)

#11012 and #11013 (originally UNCLEAR) were bisected and triaged out of this
bucket. The remaining three need a comment asking the reporter for more info.

Default labels: `Needs reproduction :mag:` + `Waiting on author`. Suggested
comments below.

| # | Title | Recommended comment / action |
|---|---|---|
| **#9983** | unexpected-keyword-arg: false positive and confusing error message with Uninferable | Comment: "Confirmed the message format bug is real (`Uninferable_factory_factory` text), but I couldn't reduce your linked private repo to a minimal snippet. Could you share a 10-line repro showing the `**kwargs` dict with an inference failure that triggers this? Then we can land a fix." |
| **#10012** | disable=too-many-line flaky if not on first line | Comment: "I couldn't reproduce on pylint 4.0.5 — a >1000-line file with `# pylint: disable=too-many-lines` on line 4 (after a multi-line module docstring) correctly suppresses C0302. Since you reported this only happened *occasionally* on pylint 2.14/3.2, please re-test on the current release and reopen with a deterministic repro if it still happens; otherwise I'll close." |
| **#10278** | "ImportError: Unable to find module" when using implicit namespaces when they already exist in site-packages | Comment: "I don't see a minimal project layout in the issue body. Could you share the exact directory structure (with `find . -type f -name '*.py'`) and the failing command? Without that I can't reproduce." |

---

## 5. EXTDEP — external library or astroid brain gap (39)

Most need a specific library installed (numpy, scipy, pydantic, torch, etc.) to
reproduce; fixes belong upstream in either the library or astroid's brain.

Default labels: `Bug` + `False Positive 🦟` + `Needs astroid Brain 🧠` for the
"missing inference for lib X" pattern; switch to `Upstream Bug 🪲` when the
issue is in the lib itself.

Cross-reference: `.triage/numpy_2x_plan.md` (in issue-triage-workspace branch)
describes an 8-patch astroid plan that would close ~13 of the numpy/typing
entries below.

### 5a. Numpy / scientific stack (4)
| # | Title | Notes |
|---|---|---|
| **#9956** | E1101 (no-member) for `numpy.dtypes.StringDType` | numpy 2.1+ additions — covered by numpy_2x_plan |
| **#9681** | Infinite recursion of Pyreverse when numpy.array is in class | `pyreverse` + numpy — `Bug` + `pyreverse` |
| **#10440** | FP unbalanced-tuple-unpacking with np.unravel_index | astroid numpy brain: return-tuple length not modeled |
| **#10831** | FP unexpected-keyword-arg with scipy.stats 1.17 | scipy 1.17 added `nan_policy` kwarg |

### 5b. PyTorch (3)
| # | Title | Notes |
|---|---|---|
| **#9218** | Pylint complains functions in torch.linalg not callable | `Needs astroid Brain` (torch brain) |
| **#9311** | False Positive E1136: PyTorch nn.Parameter.repeat | Lib-specific brain |
| **#10710** | E1102 "not-callable" false positive for torch.nn.functional.one_hot | Lib-specific brain |

### 5c. SQLAlchemy / pydantic / advanced-alchemy (4)
| # | Title | Notes |
|---|---|---|
| **#9472** | FP singleton-comparison with sqlalchemy's filter | `sqlalchemy` idiom `field == None` |
| **#9757** | no-value-for-parameter FP with sqlalchemy.ext.hybrid.hybrid_method | hybrid descriptor |
| **#9090** | Pydantic Field(alias=) is not recognized — E1123 | already covered by pylint-pydantic plugin? cross-check |
| **#9874** | FP duplicate-bases with advanced-alchemy repository classes | |
| **#10602** | FP on generic pydantic models (`R0903`) | generic Pydantic BaseModel subclass |

### 5d. Typing / dataclass interactions (7)
| # | Title | Notes |
|---|---|---|
| **#9151** | FP no-member when calling class method on Annotated type | typing.Annotated handling |
| **#9424** | FP arguments-differ for generic ParamSpec method override | `typing`, `C: arguments-differ` |
| **#9518** | FP missing-kwoa (E1125) on inherited dataclasses with kw_only=True | `dataclasses` |
| **#9804** | FP arguments-differ on `__post_init__` in dataclass inheritence | `dataclasses` |
| **#9809** | FP for optional class attribute | needs deeper read |
| **#9843** | FP unused-argument in dataclass `__new__` | `dataclasses` |
| **#9846** | FP with imported variable that shadows class | path-dependent |

### 5e. C-extension / build-time deps (8)
| # | Title | Notes |
|---|---|---|
| **#8024** | Support for cython pure python syntax: cython.declare | Could be a feature request — borderline DESIGN |
| **#8026** | Custom reporters produce no output if markupsafe imported + target imports missing module | Lib interaction |
| **#9013** | E0110 FP when using attrs.field | attrs brain |
| **#9077** | E0401: Unable to import 'apsw' | C-ext |
| **#9425** | FP no-member when importing from matplotlib.cm | matplotlib lazy-import |
| **#9426** | FP import-error and no-name-in-module from python-docx | docx setup |
| **#9762** | E1101: orjson has no 'dumps' member | orjson C-ext brain |
| **#9973** | no-member FP with super() and HuggingFace's `transformers.Trainer` | transformers meta-import |

### 5f. Other lib / runtime patterns (12)
| # | Title | Notes |
|---|---|---|
| **#9168** | Inconsistent circular-import behavior on macOS | `macOS`, `Import system` |
| **#9207** | W0611 unused-import enum FP when file named `signal.py` | name collision |
| **#9208** | load plugin regression since pip 23.1 | `Import system` |
| **#9216** | E1102 should not fire on mock fields with `return_value` | mock |
| **#9470** | FP no-member when using `random.choices` | inference |
| **#9666** | `# pylint: disable=invalid-name` ignored on ctypes Structure | `C: Pragma's`, `C: invalid-name` |
| **#10025** | Non-deterministic `import-self` warnings | `Import system`, ordering |
| **#10082** | E1136/E1137 false positives (lib-specific) | needs user setup |
| **#10181** | Pylint crash when importing `pyarrow.flight` | `Crash 💥` — should also be tagged crash |
| **#10433** | FP E1120 for static method call on GI object in Python 3.14 | `Needs astroid Brain` (PyGObject), py-version 3.14 |
| **#10827** | FP unused-import and unused-wildcard-import | `__all__`-driven wildcard, project-layout dependent |
| **#10916** | E1136 FP on PySide6 overloaded signal subscript | `Needs astroid Brain` |

---

## 6. DESIGN — enhancement or specification discussion (43)

Default labels: `Discussion 🤔` (or `Enhancement ✨` for clear feature
requests) + topic tag. None of these are bugs in the traditional sense — they
need a design decision.

### 6a. New checker / new option requests (8)
| # | Title | Suggested labels |
|---|---|---|
| **#7292** | signature-mutators should silent errors on return type | `Enhancement`, `Configuration` |
| **#7909** | generated-members doesn't work with fully qualified names | `Enhancement`, `Configuration` |
| **#8336** | Split accept-no-return-doc into accept-no-return-doc and accept-no-return-type | `Enhancement`, `Documentation` |
| **#8788** | Add configurable suppressions for classes based on inheritance | `Enhancement`, `Configuration` |
| **#9407** | pyreverse tracking and drawing class data member relations | `Enhancement`, `pyreverse` |
| **#9559** | Pyreverse unable to detect relative imports | `Enhancement`, `pyreverse` |
| **#9807** | Report global object redefinition | `Enhancement`, `Discussion` |
| **#10976** | Warn of module level attributes that may get shadowed by importing submodules | `Enhancement`, `Discussion` |

### 6b. Heuristic-tuning discussions (13)
| # | Title | Suggested labels |
|---|---|---|
| **#9095** | FP unpacking-non-sequence after return | `Discussion`, `Control flow` |
| **#9161** | invalid-field-call FP (another) | `Discussion`, `dataclasses` |
| **#9162** | R1732 consider-using-with regression on `contextlib.ExitStack` | `Discussion`, `Checkers` |
| **#9179** | FP unsubscriptable-object with MutableMapping / pygtrie | `Discussion`, `C: unsubscriptable-object` |
| **#9181** | FP not-a-mapping on `typing.cast` result | `Discussion`, `typing` |
| **#9194** | FP W0143 comparison-with-callable on property | `Discussion`, `Checkers` |
| **#9225** | FP super-init-not-called for subclasses of subclasses of `typing.Protocol` | `Discussion`, `typing` |
| **#9315** | W4701 modified-iterating-list not reported for `glob.glob()` list | `Discussion`, `Checkers` |
| **#9369** | Wrong report "instance of * has not * member" (E1101) with dynamic forwarding | `Discussion`, `inference` |
| **#9416** | protected-access FP in class method of child class | `Discussion`, `Checkers` |
| **#9464** | FP with return guard | `Discussion`, needs more details from reporter |
| **#9480** | FP assignment-from-no-return on generator with nested yield expression | `Discussion`, `Checkers` |
| **#10478** | FP consider-using-namedtuple-or-dataclass | `Discussion`, `Optional Checkers` |

### 6c. invalid-name spec questions (3)
| # | Title | Suggested labels |
|---|---|---|
| **#8885** | Unignorable "invalid-name" when accessing "private" members | `Discussion`, `C: invalid-name` |
| **#9861** | Pylint ignores disable=invalid-name under certain conditions | `Discussion`, `C: invalid-name`, related to #10199 |
| **#11012** | C0103: Variable name false positive for single word all caps at module level | **REPRO + spec call.** Bisected this session: trigger is `HTML = <FunctionDef>` at module-level. Long-running tension with #10700 (closed, Jacob proposed a separate global-name regex). Add labels `False Positive`, `C: invalid-name`, `Discussion`. Cross-link #10700. |

### 6d. Documentation / questions (4)
| # | Title | Suggested labels |
|---|---|---|
| **#9445** | "colorized" ignored when called without shell | `Documentation`, `Usability` |
| **#9487** | spelling of Sphinx parameter descriptions | `Question`, `Documentation` |
| **#9541** | "no-member" not triggered for C-extension member with `--unsafe-load-any-extension=y` | `Question`, `Documentation` |
| **#9758** | How to satisfy `unexpected-keyword-arg` in derived class override method | `Question`, `Documentation` |

### 6e. Attribute / class semantics (10)
| # | Title | Suggested labels |
|---|---|---|
| **#7995** | Class of classmethod does not support `__orig_bases__` while Type does | `Discussion`, `Astroid` |
| **#8865** | FP R0903 Too few public methods with generics and shim imports | `Discussion`, `typing` |
| **#8908** | E1101 for wrong class with partially implemented abstract classmethod | `Discussion`, `inference` |
| **#8939** | FP invalid-overridden-method with decorator | `Discussion`, `Decorators` |
| **#8987** | FP protected-access and unused-private-member with Singleton Pattern | `Discussion`, `Checkers` |
| **#9009** | FP E0203 access-member-before-definition cross-module | `Discussion`, `inference` |
| **#9157** | attribute-defined-outside-init FP for attribute defined on subclass after type-check | `Discussion`, `Checkers` |
| **#9349** | False negative `attribute-defined-outside-init` with class definition in other file | `False Negative`, `Discussion` |
| **#9863** | Unexpected behavior when dealing with Protocol generics | `Discussion`, `typing` |
| **#9766** | missing-function-docstring on overriding methods of generic classes | `Discussion`, `Documentation` |

### 6f. Misc internal / infra (6)
| # | Title | Suggested labels |
|---|---|---|
| **#8315** | Pylint caching issue when run on multiple packages having the same name | `Bug`, `Maintenance` — borderline REPRO if you can verify caching collision |
| **#8505** | FP E1130 bad operand type for unary ~: object | `Discussion`, needs more details |
| **#8781** | logging-fstring-interpolation not raised on function parameter hinted as `logging.Logger` | `False Negative`, `Discussion` |
| **#9673** | line-too-long FP on long comment in function with `disable=line-too-long` | `Discussion`, `C: line-too-long` |
| **#9935** | Possible false-negative for `unused-argument` when function always raises | `False Negative`, `Discussion` |
| **#9937** | Non-deterministic output from the code similarity check | `Bug`, `duplicate-code` |

---

## Progress log

### 2026-05-25 — initial sweep

Action by you / via this session, in order:

1. **PR opened: #11047** (fixes #11013, `typing_extensions.TypeAlias` ambiguous
   inference falling into the `const` naming path). Branch
   `fix-11013-typealias-typing-extensions` on the `pierre` fork.
2. **Bisect run** on all 20 live REPRO snippets across pylint 2.13.9 → main on
   Python 3.10/3.12. Findings written up at `.triage/REPRO_BISECT.md`. Four
   pylint regressions identified with first-bad commit:
   - #9950 declare-non-slot → pylint 3.3.0, commit `1c496e9b3`
   - #9986 unbalanced-dict-unpacking → pylint 2.16.0, commit `f2e8ba369`
   - #10691 magic-value ↔ R6103 conflict → pylint 2.16.0, commit `78770cdab`
   - #10991 TypeVarTuple dataclass → pylint 4.0.0 (astroid 4.x exposed it)
3. **19 REPRO bugs labeled** with `Bug :beetle:` + `False Positive 🦟`/
   `False Negative 🦋` + topic tag. `Needs triage :inbox_tray:` stripped:

   | # | Final labels |
   |---|---|
   | #8221  | `Bug`, `False Negative 🦋`, `Checkers` |
   | #8367  | `Bug`, `False Positive 🦟`, `Astroid`, `inference` |
   | #9359  | `Bug`, `False Positive 🦟`, `Checkers`, `Astroid` |
   | #9389  | `Bug`, `False Positive 🦟`, `dataclasses` |
   | #9488  | `Bug`, `False Positive 🦟`, `dataclasses`, `typing` |
   | #9683  | `Bug`, `False Positive 🦟`, `Needs astroid Brain 🧠` |
   | #9839  | `Bug`, `False Positive 🦟`, `Needs astroid Brain 🧠`, `py-version` |
   | #9850  | `Bug`, `False Positive 🦟`, `Needs astroid Brain 🧠` |
   | #9905  | `Bug`, `False Positive 🦟`, `Checkers`, `Decorators` |
   | #9950  | `Bug`, `False Positive 🦟`, `Regression`, `Checkers` |
   | #9972  | `Bug`, `False Positive 🦟`, `dataclasses` |
   | #9986  | `Bug`, `False Positive 🦟`, `Regression`, `Control flow` |
   | #9994  | `Bug`, `False Positive 🦟`, `Checkers` |
   | #10186 | `Bug`, `False Positive 🦟`, `C: arguments-differ`, `typing` |
   | #10609 | `Bug`, `False Positive 🦟`, `Needs astroid Brain 🧠` |
   | #10784 | `Bug`, `False Positive 🦟`, `Control flow`, `inference` |
   | #10991 | `Bug`, `False Positive 🦟`, `Regression`, `dataclasses`, `typing` |
   | #10994 | `Bug`, `False Positive 🦟`, `inference` |
   | #11032 | `Bug`, `False Positive 🦟`, `inference` |

4. **Side actions by you (Pierre):**
   - #10670 — `False Positive 🦟` applied, `Needs triage` removed (still open
     because it's only fixed in 4.0.x, not closed-as-fixed).
   - #11012 — `False Positive 🦟`, `Needs PR` applied.
   - #11013 — `False Positive 🦟`, `Needs astroid update`, `Needs PR` applied.
5. **#10691 left in the bucket** as the only REPRO needing a spec call (FP vs
   Discussion).

### 2026-05-29 — `Good first issue` sweep across REPRO bucket

Goal: find REPRO bugs that newcomers can pick up — small scope, no astroid /
inference work, not in the variables checker, not control-flow.

Method: filtered `.triage/triage_state.json` REPRO verdicts (180 open),
excluded labels `Control flow`, `C: used-before-assignment`,
`C: undefined-variable`, `Needs astroid Brain 🧠`, `Needs astroid update`,
`Astroid`, `inference`, `infer-all`, `typing`, `High effort 🏋`, `pyreverse`,
`Decorators`, `High priority`, `Lib specific 💅`; dropped notes mentioning
inference keywords (narrow / inferred / metaclass / Protocol / Generic / …).
67 candidates remained; verified the fix locations of the top 9 still apply
on `main`.

Two dropped after assignee/label cross-check:
- **#10813** (logging bytes crash) — already self-assigned to Pierre.
- **#9839** (IntEnum `__slots__` FP) — upstream label `Needs astroid Brain 🧠`
  flags it as astroid work, not a checker tweak.

7 labeled `Good first issue` (count now 19 → 26):

| # | Why GFI | Fix locus |
|---|---|---|
| #8499  | TypeVar regex lacks `\d` | `pylint/checkers/base/name_checker/checker.py:42-46` `DEFAULT_PATTERNS["typevar"]` |
| #5793  | `arguments-differ` wording when param counts match | `pylint/checkers/classes/class_checker.py:2338,2354` |
| #8256  | `unnecessary-comprehension` suggests `dict(dict1)` when iterating dict-of-tuple-keys | refactoring checker; message-correction |
| #6663  | `implicit-str-concat` FP on `r'…' '\n'` mix | format/string checker; skip when adjacent literals have different `r` prefix |
| #10099 | Crash in `consider-using-enumerate` on `len(range(...))` | refactoring checker; already `Needs PR` |
| #9878  | `superfluous-parens` FN when contents are a single string | format checker |
| #10084 | `superfluous-parens` FN on `if (a and b):` | same area as #9878 |

### Process notes (carried over)

- The 109 prior verdicts come from `.triage/triage_state.json` on the
  `issue-triage-workspace` branch (commit 5f3dcffbb). They were last regenerated
  2026-05-12; spot-checks in this session re-verified ~20 of the REPRO ones and
  the closable ones.
- Snippet files live at `.triage/snippets/iNNNN.py` on the same branch. Bisect
  artifacts (per-version JSON, `bisect.sh`, `run.py`, `spec.json`) under
  `/tmp/bisect/` for this session.
- `Needs astroid Brain 🧠` is the right label for "pylint can't infer attribute
  X because astroid doesn't model lib Y" — those issues become PRs against
  pylint-dev/astroid, not pylint.
- For closables, the GitHub convention is to add the relevant `Duplicate`/
  `Cannot reproduce`/`Invalid` label *and* close — so the label survives.
