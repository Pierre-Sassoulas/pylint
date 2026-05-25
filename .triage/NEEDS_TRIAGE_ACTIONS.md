# Needs-triage actions — 110 open issues

Snapshot: 2026-05-25, pylint 4.1.0-dev0, astroid 4.2.0b3.
Source: GitHub label `Needs triage :inbox_tray:` on pylint-dev/pylint + my prior
`.triage/triage_state.json` verdicts (re-verified for the recent / interesting
ones in this session).

Quick navigation:
- [Closable immediately](#1-closable-immediately-3) — close as fixed/dup, no extra work
- [Has open PR](#2-has-open-pr-1) — link & remove triage label
- [REPRO bugs ready to label](#3-repro--real-bugs-ready-to-label-19) — confirmed reproducible
- [UNCLEAR — ping reporter](#4-unclear--needs-reporter-input-3) — can't reproduce w/o more info
- [EXTDEP — external library gap](#5-extdep--external-library-or-astroid-brain-gap-39)
- [DESIGN — enhancement / spec discussion](#6-design--enhancement-or-specification-discussion-43)
- [NEW — fresh issue](#7-new-issue-1)

| Bucket | Count | Default labels |
|---|---:|---|
| Closable (FIXED) | 2 | close as completed, comment with fixing commit/PR |
| Closable (DUP) | 1 | `Duplicate 🐫`, close as duplicate of canonical issue |
| Has open PR | 1 | link PR, remove `Needs triage` |
| REPRO | 19 | `Bug` or `False Positive`/`False Negative` + topic tag |
| UNCLEAR | 3 | `Needs reproduction :mag:` + `Waiting on author` |
| EXTDEP | 39 | `False Positive` + `Needs astroid Brain` (or `Upstream Bug`) |
| DESIGN | 43 | `Enhancement` / `Discussion 🤔` / `Proposal 📨` + topic |
| NEW | 1 | (triage in row) |
| **Total** | **110** | |

---

## 1. Closable immediately (3)

| # | Title | Action |
|---|---|---|
| **#10670** | False Positive for too-many-function-args when subclassing `__new__` | **Close as fixed.** Re-verified 2026-05-25 on pylint 4.0.5+py3.12 with reporter's exact snippet: 10/10. Fixed between 4.0.1 and 4.0.5. |
| **#9885** | False positive missing member `__value__` with type statement and Literal under python 3.12 | **Close as duplicate of #10091.** Jacob's comment on #10091 (https://github.com/pylint-dev/pylint/issues/10091) designated it as the canonical tracker. |
| **#9159** | pylint does not support typing.Self when override | **Close as fixed.** Re-verified 2026-05-25: bug present on released 4.0.5+astroid 4.0.4; clean on current main (4.1.0-dev0+astroid 4.2.0b3). Likely fixed by an astroid Self-inference upgrade between 4.0.4 and 4.2.0b3. |

---

## 2. Has open PR (1)

| # | Title | Action |
|---|---|---|
| **#11013** | C0103: Constant name false positive when typing variables nested in `TYPE_CHECKING` | **PR #11047 open.** Add labels `Bug`, `False Positive 🦟`, `C: invalid-name`, `typing`. Remove `Needs triage`. |

---

## 3. REPRO — real bugs ready to label (19)

All re-verified to still reproduce on `origin/main` 2026-05-25 with the snippets in
`.triage/snippets/iNNNN.py` (issue-triage-workspace branch).

Default labels: `Bug` + `False Positive 🦟` (or `False Negative 🦋`) + the
topic/checker tag in the **Topic** column. Bonus tags in parens when applicable.

| # | Title | Topic / suggested labels |
|---|---|---|
| **#8221** | cell-var-from-loop ignores generator expressions | `False Negative`, `Checkers`, `C: cell-var-from-loop` (if you want a new C: label) |
| **#8367** | Incorrect type inferred when inner class definition closes over variable from outer class's method | `False Positive`, `inference`, `Astroid`, `Needs astroid Brain` |
| **#9359** | useless-parent-delegation false positive when `__init__` signatures differ but parent is built-in type | `False Positive`, `Checkers` |
| **#9389** | False-positive E1121 when using dataclass with init=False | `False Positive`, `dataclasses` |
| **#9488** | Unexpected keyword argument for Generic dataclass with ABC bounded TypeVar | `False Positive`, `dataclasses`, `typing` |
| **#9683** | False positive invalid-sequence-index using properties of range object as index | `False Positive`, `Needs astroid Brain` (range start/stop/step not exposed as int) |
| **#9839** | E0238 false positive when defining `__slots__` in IntEnum class | `False Positive`, `Checkers` |
| **#9850** | AddressFamily and SocketKind are not visible in module socket | `False Positive`, `Needs astroid Brain` (socket stub gap) |
| **#9905** | False positive `invalid-overridden-method` when overridding `Enum.value` | `False Positive`, `Checkers` |
| **#9950** | False positive `declare-non-slot` on classvar | `False Positive`, `Checkers` |
| **#9972** | False positive `no-member` when wrapping dataclasses `field` | `False Positive`, `dataclasses` |
| **#9986** | False positive `unbalanced-dict-unpacking` | `False Positive`, `Control flow` |
| **#9994** | False positive: useless-parent-delegation on `__init__` method of class derived from `Exception` | `False Positive`, `Checkers` |
| **#10186** | False positive with `arguments-differ` rule in overridden overloaded methods in subclass | `False Positive`, `C: arguments-differ`, `typing` |
| **#10609** | False positive E1121: Too many positional arguments error for Subclassed Enums instanciated with functional API | `False Positive`, `Needs astroid Brain` (Enum functional API subclass) |
| **#10691** | Conflicting warnings R2004 (`pylint.extensions.magic_value`) and R6103 (`pylint.extensions.code_style`) | `Bug`, `Optional Checkers` — circular suggestion: walrus-rewrite still trips magic-value |
| **#10784** | Type narrowing fails due to unrelated instance assignment | `False Positive`, `Control flow`, `inference` |
| **#10991** | Unexpected kwarg false-positive when using TypeVarTuple | `False Positive`, `typing`, `Needs astroid Brain` (PEP 646 TypeVarTuple) — related to #10972 |
| **#10994** | False positives when 'type' builtin is overwritten | `False Positive`, `inference` |

---

## 4. UNCLEAR — needs reporter input (3)

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

## 7. NEW issue (1)

| # | Title | Triage |
|---|---|---|
| **#11032** | E1121 triggered incorrectly when metaclass `__call__` accepts more arguments than class `__init__` | **REPRO** — verified 2026-05-25 on pylint 4.0.5+main: `MyClass(1, 2)` flagged as too-many-function-args when `Meta.__call__` accepts 2 args but `MyClass.__init__` accepts 1. Pylint should consult `Meta.__call__` signature when one exists rather than always checking `__init__`. Labels: `Bug`, `False Positive 🦟`, `Checkers`, `inference`. |

---

## Process notes

- The 109 prior verdicts come from `.triage/triage_state.json` on the
  `issue-triage-workspace` branch (commit 5f3dcffbb). They were last regenerated
  2026-05-12; spot-checks in this session re-verified ~20 of the REPRO ones and
  the closable ones.
- Snippet files live at `.triage/snippets/iNNNN.py` on the same branch.
- `Needs astroid Brain 🧠` is the right label for "pylint can't infer attribute
  X because astroid doesn't model lib Y" — those issues become PRs against
  pylint-dev/astroid, not pylint.
- For closables, the GitHub convention is to add the relevant `Duplicate`/
  `Cannot reproduce`/`Invalid` label *and* close — so the label survives.
