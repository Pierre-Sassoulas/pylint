# Needs-investigation actions — 87 open issues remaining

Snapshot: 2026-09-13, pylint 4.1.0-dev0, astroid 4.2.0b5 (CI pin) / 4.3.0 (resolved).
Started from 91 issues on `Needs investigation :microscope:`; 4 cleared so far.

Every issue carrying a runnable snippet was rebuilt and re-run against `main` with the
reporter's library installed. Where one stopped reproducing it was bisected to the commit
that fixed it, in astroid as well as pylint — see `.triage/BISECT_FIXED.md` for the harness,
the per-issue bisect log, and three ways a bisect over this repo will lie to you.

Two habits this sweep argues for:

- **Pin the reporter's era, not just their pylint.** 4577 is clean on pandas 3.x and
  reproduces on 1.5.3; 9311 was fixed by torch 2.8.0 with pylint untouched.
- **Read the whole thread.** 4577's body snippet is genuinely fixed, but a comment snippet
  still fires on `main`. The tell was a comment postdating the fixing commit by three years.

| Bucket | Count | Done | Default labels |
|---|---:|---:|---|
| Reproduces on main | 29 | 1 | `Needs PR` + topic |
| Fixed — bisected to the commit | 3 | 3 | close as completed |
| Never reproduced at the version filed | 6 | 0 | `Needs reproduction` + `Waiting on author` |
| Enhancement — nothing to reproduce | 12 | 0 | `Enhancement` / `Proposal` + topic |
| Needs the reporter's own code | 15 | 0 | `Needs reproduction` + `Waiting on author` |
| No minimal case in the body | 11 | 0 | `Needs reproduction` |
| Other platform | 7 | 0 | platform label, or close as unactionable |
| Tracking / research | 6 | 0 | `Discussion` or close |
| Obsolete | 1 | 0 | close as completed |
| Needs a decision, not an investigation | 1 | 0 | `Needs decision` |
| **Total** | **91** | **4** | |

---

## Reproduces on main (29)

Confirmed against pylint 4.1.0-dev0 with the reporter's library at a version that shows it. Ready for `Needs PR` plus a topic label.

| # | Title | Finding |
|---|---|---|
| **#10796** | False Positive "no-member" with pandas `DatetimeIndex` | Reproduces on current pandas. |
| **#10761** | False positive for `unreachable` when doing OpenGL (Pyglet.gl) calls | Reproduces on current pyglet: a pyglet.gl call makes the following line look unreachable. |
| **#9549** | False positive unsubscriptable-object | Reproduces once the reporter's implied Base and RoleGroup are supplied: every Mapped[...] annotation in the class draws 'Value Mapped is unsubscriptable', triggered by the self-referencing relationship line. Removing that line clears them all, exactly as reported. |
| **#9421** | `unexpected-keyword-arg` (E1123) and `missing-kwoa` (E1125) false positives with changing dict | Reproduces both messages: a dict literal mutated by update()/pop() before target(**data) is still matched against the original literal keys, so pylint sees the removed key and misses the added one. |
| **#9340** | Dictionary is unsubscriptable false positive when using ``random.sample`` | Reproduces: after items = random.sample(results, 5) the loop variable is judged unsubscriptable, despite the list[dict[str, str]] annotation on the assignment. Wrapping in list() silences it, as reported. |
| **#9332** | cv2.error recognised as exception on Linux, not macOS | Reproduces on Linux, and wider than filed: with opencv-python-headless both cv2.imread and cv2.error are unknown, with or without --extension-pkg-allow-list=cv2. The macOS/Linux split in the title is a symptom of the same dynamic __init__ shim. |
| **#9238** | False positive `import-error` with distutils.errors | Reproduces on CPython 3.13, where distutils is no longer in the stdlib: the runtime import works (setuptools ships the shim) while pylint reports import-error. Pylint also, correctly, adds deprecated-module now. |
| **#9223** | False positive for unused-import when only usage is inside of forward references | Reproduces: an import used only inside a quoted forward reference (a TypeAlias holding a string annotation) is still reported unused. |
| **#9169** | Pylint treats tabs like spaces | The reporter's framing was off but the bug is real: a file indented with TABS gets 'Bad indentation. Found 1 spaces, expected 4'. The count is the tab count and the word is wrong. Cosmetic, contained, good first issue. |
| **#8986** | `invalid-name` and `arguments-renamed` not triggered by constructor arguments in derived class | Reproduces as a false negative: a derived __init__ renaming config to c draws neither invalid-name nor arguments-renamed. Worth deciding whether __init__ is deliberately exempt from arguments-renamed before treating it as a bug. |
| **#8894** | false positive `no-member` warnings in pydantic 2.0 | Reproduces on pydantic 2.13.5 - the original 2.0 report is still live three years on. |
| **#8497** | false-positive errors with pyroute2 0.7.6 | Reproduces on current pyroute2, though the message has moved: the reported E1121/E1136 are gone and 'Instance of IPRoute has no link_lookup member' takes their place. Same dynamic-attribute root cause, different symptom - worth re-titling. |
| **#8303** | decorators not processed successfully with alpha_vantage | Reproduces on current alpha_vantage: the decorator is not followed, so the decorated method's return is mis-inferred. |
| **#8050** | Pylint doesn't check file if it's named exactly like the directory where the file is | Reproduces: pylint something/something (file named exactly like its directory) prints nothing at all and exits, while renaming the file, adding __init__.py, or cd-ing into the directory all make it work. |
| **#7641** | Initializing DataFrame in __init__ hangs pyreverse | Reproduces: pyreverse -c Foo on a class whose __init__ assigns a pandas DataFrame produced no output and was killed at the 180 s mark. |
| **#7538** | False positive `used-before-assignment` with walrus operator inside binary operation | Reproduces exactly as filed: the two walrus expressions inside a string concatenation draw used-before-assignment, the identical expression without the + does not. |
| **#7424** | invalid-sequence-index when unpacking a sequence of sequences | Reproduces verbatim: unpacking a 4-tuple out of a list of 4 identical tuples, then indexing the dict element, raises E1126. The reporter's own observation holds - shrink the list to 3 entries and it goes away, so the length of the outer list is what steers the (wrong) inference. |
| **#7269** | time.sleep false negative! | Reproduces as a false negative: from time import time then time.sleep(1) scores 10.00/10. The name is the function, not the module, so no-member should fire and does not. |
| **#5835** | Slow with all checks disabled using pandas + dataclass | Reproduces, and the reporter's workaround no longer works: @dataclass with a DataFrame annotation takes 6.67 s against 0.89 s for the same dataclass with an int. Optional[DataFrame], which they found brought it under 2 s, now costs 6.71 s - the same as the plain annotation. |
| **#5761** | False positive invalid-overridden-method for async generators overriding AsyncIterable | Reproduces: an async generator overriding a Protocol method annotated AsyncIterable[str] draws 'expected non-async, found async'. The reporter's point stands - an async generator is not a coroutine, so the override is correct. |
| **#4577** | False positives on ``pandas.io.parsers.TextFileReader`` | **[kept open, relabelled High priority / Needs astroid update]** Body snippet is fixed and bisected, but the thread carries five more and @FredStober's still fires on main: E1136 'Value dataframe is unsubscriptable' for DataFrame(...).fillna(0) under pandas 1.5.3 and 2.0.3, silent on 2.2.3 and 3.0.5. The root cause the reporters named is untouched: pd.read_csv(...) still infers to [NoneType x4, TextFileReader, Uninferable] on astroid 4.3.0, never DataFrame. Last comment on the thread postdates the fixing commit by three years, which was the tell. **Fixed by:** body snippet only: pylint 11807f0ae (Update astroid requirement to 2.11.0) then astroid 74710868d — Fix crash on Super.getattr for previously uninferable attributes. |
| **#4018** | disable=unexpected-keyword-arg doesn't work when placed on line where keyword is specified | Reproduces: the message is anchored to the call's opening line, so a disable comment on the offending argument line never covers it. The reporter's workaround - pragma on the myfun( line - still works. |
| **#3944** | Implicit namespace package is not linted if it is inside a regular package | Reproduces: a directory without __init__.py inside a regular package is skipped entirely by --recursive=y - exit 0, no output. Add __init__.py and the undefined-variable in that file is reported at once. |
| **#3758** | signature-mutators doesn't seem to work | Reproduces with --signature-mutators=unittest.mock.patch.object exactly as filed: the option is accepted and then has no effect on the decorated function's call site. |
| **#3756** | Cannot disable cell-var-from-loop on a splitted line when var was used before | Reproduces: with the loop variable referenced once before the lambda, a disable comment on the continuation line of a backslash-split lambda is ignored. Pylint 2.4.4 accepted it, per the reporter. |
| **#2559** | Inappropriate assignment-from-none error | Reproduces on an abc.ABCMeta class: a plain method returning None, meant to be overridden, makes every self.lock_name() assignment an assignment-from-none. No-self-use (R0201) is gone from pylint, so only the E1128 half of the report is still live. |
| **#2474** | __path__ mangling in a non namespace package | Reproduces: a package whose __init__ appends a subdirectory to __path__ still gives 'Unable to import module.myClass' and 'No name myClass in module module'. Runtime resolves it fine. |
| **#2392** | no-member false positive related to an import confusion | Built the reporter's two-file package. from mymodule import foobar binds the module-level FooBar() instance rather than the submodule, so foobar.FooBar() gives 'Instance of FooBar has no FooBar member'. __all__ is not consulted. |
| **#829** | Disable after module docstring has the scope of the whole file. | Reproduces, nine years on. A disable on the module docstring line silences the whole file; the same pragma one line lower is line-scoped. Verified both directions plus a no-pragma control that flags both lines. |

---

## Fixed — bisected to the commit (3)

No longer reproduces, and the fixing commit is named. Closable as completed.

| # | Title | Finding |
|---|---|---|
| **#10317** | `unbalanced-tuple-unpacking` false positive with `statistics.quantiles` | **[closed as completed]** No longer reproduces: statistics.quantiles unpacking into three names is 10.00/10 on main. **Fixed by:** pylint a0e601d03 (Bump astroid to 4.0.0rc0) then astroid 3db2bd943 — Add brain module for statistics inference. |
| **#10016** | Unreachable code in the next line when using `read_excel` function of `polars` module | **[closed as completed]** No longer reproduces on polars 1.x, with fastexcel installed as in the report: pl.read_excel() no longer makes the next line look unreachable. **Fixed by:** pylint 4f6c24120 — Fix false positive related to overload decorator + NoReturn (closes 10785), 2026-01-02. The only fix in either label landing in pylint's own checkers. |
| **#7680** | pylint crashed with a ``AstroidError`` (astroid.exceptions.ParentMissingError) | **[closed as completed]** The extracted sqlalchemy snippet no longer crashes on main; the original traceback came from a larger project, so this is a weak clean rather than a proof. **Fixed by:** pylint 7521eb1dc (Bump astroid to 3.2.0) then astroid a7f5d5ff4 — Prefer last same-named function in a class rather than first in igetattr(). |

---

## Never reproduced at the version filed (6)

Clean at the exact pylint/astroid/Python in the report, so nothing was fixed — something in the reporter's environment was doing the work.

| # | Title | Finding |
|---|---|---|
| **#10140** | pylint only catching `cyclic-import` in parallel mode | Never reproduced. At v3.3.2, -j1 and -j2 agree, both reporting the cyclic import. |
| **#9993** | Cannot find "dunder module" in package - False-positive `No name '__main__' in module 'foo' (no-name-in-module)` | Never reproduced. Clean at v3.2.7, the version filed against, with the src/foo + unittests layout rebuilt from the description. |
| **#9188** | Inconsistent behavior of `--recursive=y` depending on folder structure name | Never reproduced. At v3.0.2, the dataset/ and train/ layouts give byte-identical output. |
| **#7654** | Config file generated by --generate-toml-config option produces errors when later used | Never reproduced. At v2.15.4, --generate-toml-config round-trips into a working --rcfile. |
| **#3531** | no-member reported when accessing a @property of parent class | Never reproduced. pylint 2.5.0 will not build on any Python available here; checked at 2.6.0 on py3.10 with WTForms - clean. Reconstructed from the description. |
| **#1428** | Relative imports don't work if processed after empty package | Never reproduced. Filed against pylint 1.6.5, which will not install here; checked at 2.6.0 on py3.10 with the a/src + b/src/test tree rebuilt - clean. |

---

## Enhancement — nothing to reproduce (12)

Feature or scope requests; several are good first issues.

| # | Title | Finding |
|---|---|---|
| **#9407** | pyreverse tracking and drawing class data member relations in addition to instance data members (maybe enable/disable option). fixes attrs.org | Feature request: draw class-level data members alongside instance ones, behind an option. |
| **#9170** | Colorama >=0.4.5 not only required in Windows environment | Still unimplemented: pyproject.toml pins colorama>=0.4.5 only under sys_platform=='win32'. The request to enforce it everywhere is a one-line change plus a decision about adding a dependency for all platforms. |
| **#9018** | Determine if method is abstract using `__isabstractmethod__` instead of `abstractmethod` decorator | Use __isabstractmethod__ rather than looking for the abstractmethod decorator. |
| **#8654** | ``RuffChecker`` class to be able to create python plugins using ruff 's AST  | Proposal for a RuffChecker plugin base. High effort, needs a design decision before any code. |
| **#7438** | Features for refactoring automatically offending code (pylint autofix) | The pylint-autofix discussion. Needs design, not investigation. |
| **#7317** | Cache directory useless in CI (?), add a an incremental mode like mypy | Asks for a mypy-style incremental cache usable in CI. |
| **#5763** | feature suggestion for `is` compare between different types | Suggests flagging is between values of different types. Needs a decision on scope. |
| **#5471** | Warn if module dunders are below imports | Warn when module dunders sit below imports. Good first issue, still unimplemented. |
| **#5361** | False negatives `superfluous-parens` with more than one superfluous parenthesis | Confirmed the gap: if ((X)): draws one superfluous-parens, print((X)) draws none. C0325 only looks after keywords, so doubled parens elsewhere are invisible. A scope decision, not a bug. |
| **#5226** | Support an Option to Disable sys.path patching | Asks for an option to disable pylint's sys.path patching. |
| **#4912** | Separate check for possibly unused arguments if locals() is used | Still applicable. The local gets W0641 possibly-unused-variable, but both arguments get the flat W0613 unused-argument - there is no possibly-unused-argument counterpart for a function that returns locals(). |
| **#2095** | Add way to disable module caching for specific files | Asks for a way to disable module caching per file. Nineteen comments, high effort. |

---

## Needs the reporter's own code (15)

Tracebacks through packages that were never public, or reproducers living in someone's CI.

| # | Title | Finding |
|---|---|---|
| **#10474** | Crash (possibly caused by `win32more`) `Building error when trying to create ast representation of module 'src.ui.mainwindow'` | Not re-run: win32more is Windows-only and the report has no snippet that runs elsewhere. |
| **#10345** | Crash `TypeError: 'UninferableBase' object is not iterable` - [astroid-error] | Not re-run: the traceback comes from the reporter's own ft_core package on top of django. |
| **#10326** | Crash ``Building error when trying to create ast representation of module 'sympy.polys.numberfields.resolvent_lookup'`` | Not re-run: needs the reporter's app package; the sympy/minio half of the trace is not enough on its own. |
| **#9479** | Crashed while using pylint as a static test for a docker | Not re-run: the snippet imports the reporter's tables and utils modules. |
| **#8049** | Crash with AstroidError 'Could not find <FunctionDef.warning_logger' | Not re-run: the reporter says themselves they could not reduce it, and that linting the file alone does not crash. |
| **#7892** | Project plugin removed from sys.path | The issue body is pylint's own test code rather than a user scenario. Needs a real plugin layout before it can be judged. |
| **#7735** | False positive `ungrouped-imports` in match case | Not re-run: the snippet imports the reporter's app and something_else modules. |
| **#7519** | False-positive W0143:comparison-with-callable with PySide6 and `__feature__` | Not re-run: needs PySide6's __feature__ switch, which changes the generated API shape at import time. |
| **#7238** | Tensorflow: bad operand type for unary - false positive | Not re-run: tensorflow is a multi-gigabyte install; worth batching with any other tensorflow issue. |
| **#6042** | disable=redefined-builtin ignored in some scenarios | Not re-run: the reproducer lives in an external repository (kfsone/pylint-spurious-w0622) and the reporter only saw it on Linux CI workers. |
| **#4690** | False positive no-member on PonyORM | Could not reproduce from a reconstructed Pony entity and query. The reporter's case was one line inside a large project, and the issue carries no self-contained snippet - needs their code to go further. |
| **#4137** | False positive in 2.7.0: kazoo unpacking-non-sequence | Snippet is a fragment - the extracted code only shows a global statement. Needs the reporter's kazoo call site. |
| **#3620** | called code side effect | Not re-run: the snippet is a fragment of a flask + pyserial app. |
| **#2879** | pylint not reporting missing import false negative. | Not re-run: imports a venus module that is not on PyPI. |
| **#2555** | Pylint doesn't detect AttributeError when using PyQt5 | Not re-run as filed: the report is about pylint failing to flag a missing PyQt5 attribute, and the snippet stops mid-function. |

---

## No minimal case in the body (11)

Not re-run: nothing runnable in the issue. Some may be recoverable from the thread.

| # | Title | Finding |
|---|---|---|
| **#9937** | Non-deterministic output from the code similarity check | Similar-checker output order varies. Needs a seeded multi-run harness to pin down; related to #3843. |
| **#9317** | Incorrect Recommendation for unnecessary-lambda | The unnecessary-lambda documentation recommends a rewrite the reporter says is wrong. Labelled good first issue - a doc fix, once someone confirms the wording. |
| **#9175** | False positive circular dependency detection | Circular-dependency false positive with no snippet in the body. |
| **#7625** | Pylint disable working incorrectly | 'Pylint disable working incorrectly' - five comments, no minimal case in the body. |
| **#5168** | False positive cyclic-import | Another cyclic-import false positive, no snippet. Worth merging with #9175 if they turn out to be the same shape. |
| **#3843** | The similar checker will append the same stream in some weird reason | Claims the similar checker appends the same stream twice. Same area as #9937. |
| **#3298** | E0602 (undefined-variable) - False positive | undefined-variable false positive tied to the import system; the thread has eleven comments and no minimal case. |
| **#2977** | False positive: unsupported-assignment-operation | unsupported-assignment-operation false positive, inference-related, no snippet. |
| **#2724** | Pylint is painfully slow in script using gi library | Pylint slow on a gi script. Needs a GTK-enabled environment to time honestly. |
| **#2483** | docparams raise missing-type-doc without missing-param-doc for Google docstrings | missing-type-doc without missing-param-doc on Google-style docstrings. Testable, but the body does not carry the docstring that triggered it. |
| **#2188** | InconsistentMroError: Cannot create a consistent method resolution order for MROs | A crash with fifteen comments and no reduced case; labelled high effort. |

---

## Other platform (7)

macOS, Windows or PyPy-only behaviour this machine cannot reach.

| # | Title | Finding |
|---|---|---|
| **#9277** | Crash - on windows - pylint crashed with a ``AstroidError`` - UnicodeEncodeError: 'charmap' codec can't encode characters in position | Windows-only: a UnicodeEncodeError from the cp1252 console encoding. |
| **#9168** | Inconsistent behavior with circular import on MacOS | macOS-only circular-import behaviour; sibling of #8845 and #3068. |
| **#8845** | wrong-import-order fails on one system, passes in other | Two systems, different results, no reproducer. Same family as #9168 and #3068. |
| **#7527** | PyPy-specific: `ctypes.Structure` fields not ignored; `no-member` false positive | PyPy-only by the reporter's own statement - clean on CPython, which is all this machine runs. |
| **#5347** | Unable to create directory /Users/runner/Library/Caches/pylint | macOS CI runner could not create ~/Library/Caches/pylint. |
| **#5251** | "Unable to init server" warning with GTK import | Needs a GTK display environment; the warning comes from the library, not pylint. |
| **#3068** | Pylint behaves differently on Mac vs Linux | macOS-only divergence, no snippet. |

---

## Tracking / research (6)

2018-era 'investigate X' notes and open questions.

| # | Title | Finding |
|---|---|---|
| **#7263** | Checker plugin parallelization breaks algorithm | A long question thread about plugin parallelization, labelled Question and Documentation. Reads as a docs task now. |
| **#2249** | Investigate why the spellchecking checks are slow | Open question from 2018 about why spell-checking is slow. Still worth measuring, but it is a task, not a bug report. |
| **#2156** | Investigate if there is anything to learn from pytype | Tracking issue from 2018: learn from pytype. |
| **#2148** | Check if there is anything to learn from python-taint | Tracking issue from 2018: learn from python-taint. |
| **#2127** | Investigate if there's anything to learn from jedi | Tracking issue from 2018: learn from jedi. |
| **#2124** | Investigate if there is anything to learn from RuboCop/ESLint | Tracking issue from 2018: learn from RuboCop/ESLint. Nothing to reproduce; either convert to a discussion or close. |

---

## Obsolete (1)

The code the issue is about no longer exists.

| # | Title | Finding |
|---|---|---|
| **#3628** | Example in module docstring of epylint fails since 2.5.x | Obsolete: pylint.epylint no longer exists - the module was removed, so the docstring example the issue is about is gone with it. |

---

## Needs a decision, not an investigation (1)

Renames and policy calls.

| # | Title | Finding |
|---|---|---|
| **#7449** | Incorrect warning name | A message name the reporter considers wrong. A rename is a breaking change, so it needs a decision rather than a repro. |

---
