# Session 01 — 2026-05-12 — Triage Notes

**Scope:** Newest 104 open issues (created 2025-01-22 — 2026-05-12). **Environment:**
pylint 4.0.5 / astroid 4.0.2 / Python 3.12.3.

**Verdict tally:**

- REPRO: 22
- FIXED: 8
- UNCLEAR: 6
- EXTDEP: 27
- DESIGN: 39
- DUP: 1
- STALE: 1

## By verdict

### REPRO (22)

- **#10995** — PEP 695 TypeVar redefinition false-positive Confirmed: PEP 695 TypeVar in
  'type Alias[T] = ...' and 'def fn[T](...)' triggers W0621 redefined-outer-name. Each
  PEP 695 type-param is scope-local but pylint treats them as shared outer scope. Real
  bug. <https://github.com/pylint-dev/pylint/issues/10995>

- **#10994** — False positives when 'type' builtin is overwritten Confirmed: when 'type'
  builtin is shadowed by a parameter, pylint still infers the call as returning the
  actual class, leading to false E1101. Real bug.
  <https://github.com/pylint-dev/pylint/issues/10994>

- **#10972** — Abstract method false-positive when using TypeVarTuple Confirmed: E0110
  false positive on Concrete that satisfies abstract Base.get_item via TypeVarTuple
  chain (PEP 695). pylint cannot follow \*Shape forwarding through inheritance.
  <https://github.com/pylint-dev/pylint/issues/10972>

- **#10969** — Pylint skipping similarly named project directory. Confirmed bug;
  same-prefix sibling directories get incorrectly skipped by \_discover_files() because
  skip_subtrees uses string prefix match. Author has WIP fix.
  <https://github.com/pylint-dev/pylint/issues/10969>

- **#10951** — pylint does not recognise `from ... import` inside an `IntEnum` class
  body as producing enum members Confirmed: E1101 false positive — pylint/astroid does
  not treat 'from x import y as Z' inside an IntEnum body as producing enum members;
  infers them as int. <https://github.com/pylint-dev/pylint/issues/10951>

- **#10848** — pylint does not honor decorator return type when using @ syntax
  Confirmed: E1101 false positive — pylint ignores decorator's annotated return type
  when applied via '@' syntax (works with explicit f = decorator(f\_) form). Marked
  Duplicate label upstream. <https://github.com/pylint-dev/pylint/issues/10848>

- **#10847** — possibly-used-before-assignment false negative when variable has type
  annotation Confirmed false negative: when 'err' has a forward type annotation but only
  is assigned in some except clauses, pylint does not flag
  possibly-used-before-assignment at the later use site. Removing the annotation makes
  pylint flag it. <https://github.com/pylint-dev/pylint/issues/10847>

- **#10840** — `invalid-envvar-value` does not support StrEnum Confirmed: E1507
  (invalid-envvar-value) triggers for StrEnum member used as os.getenv arg, even though
  StrEnum members ARE strings. Needs StrEnum support in the envvar checker.
  <https://github.com/pylint-dev/pylint/issues/10840>

- **#10813** — Improper handling of log message format bytestrings Confirmed: crash
  (F0002 / UnicodeDecodeError) in pylint.checkers.logging.\_check_format_string when
  format string is a non-UTF8 bytes object. Direct fix in logging.py line 333 (use
  .decode(errors='replace') or str()).
  <https://github.com/pylint-dev/pylint/issues/10813>

- **#10807** — pylint fails to resolve typing.Self from base classes Confirmed:
  typing.Self from a base-class method called via super() does not narrow to the
  subclass type. False E1101 on B().meth().f2().
  <https://github.com/pylint-dev/pylint/issues/10807>

- **#10784** — Type narrowing fails due to unrelated instance assignment Confirmed: type
  narrowing via isinstance(...) and isinstance(stmt.src, ...) within a single 'and'
  breaks when an unrelated function in the same module constructs another concrete
  subclass. Removing that function eliminates the false positive.
  <https://github.com/pylint-dev/pylint/issues/10784>

- **#10731** — False Negative `no-value-for-parameter` for instances used inside of a
  class Confirmed: E1120 'no-value-for-parameter' is fired for direct 'seagull.flap()'
  but NOT for 'bird.flap()' or 'self.bird.flap()' inside BirdTester even with typed Bird
  annotation. False negative. <https://github.com/pylint-dev/pylint/issues/10731>

- **#10691** — Conflicting warnings R2004 from `pylint.extensions.magic_value` and R6103
  from `pylint.extensions.co Confirmed: applying R6103's walrus suggestion in the
  magic_value example still leaves R2004. Either R6103 should not apply here, or R2004
  should look through walrus. Real interaction bug.
  <https://github.com/pylint-dev/pylint/issues/10691>

- **#10679** — False negatives for `disallowed-name` due to control flow in NameChecker
  Genuine internal bug per maintainer note: NameChecker short-circuits skip
  'disallowed-name' along with 'invalid-name' in several control-flow paths. Code
  reference provided. <https://github.com/pylint-dev/pylint/issues/10679>

- **#10609** — False positive E1121: Too many positional arguments error for Subclassed
  Enums instanciated with fun Confirmed E1121 false positive: CustomEnum('MyEnum',
  {'RED': 1}) (subclass of Enum used via Enum functional API) triggers
  too-many-function-args, while base Enum() does not. astroid does not propagate the
  functional **call** signature through subclassing.
  <https://github.com/pylint-dev/pylint/issues/10609>

- **#10519** — Crash with AstroidBuildingError when inheriting from a generic dataclass
  that has **init_subclass** Crash confirmed: AstroidBuildingError when a dataclass
  inherits unparameterized from a generic dataclass that defines **init_subclass**.
  Trace points to astroid brain_dataclasses.\_find_arguments_from_base_classes. Astroid
  bug. <https://github.com/pylint-dev/pylint/issues/10519>

- **#10472** — False positive no-member Confirmed E1101 false positive: '[sth.name for
  sth, \_ in [lorem, ipsum, dolor]]' where each list element is a 2-tuple (Foo, int).
  pylint cannot infer the tuple-unpacking type from list of homogeneous tuples.
  <https://github.com/pylint-dev/pylint/issues/10472>

- **#10471** — Property union type inference issue: E1102 not-callable false positive
  Confirmed E1102 false positive: property returning CallableType|None, even after 'if
  self.processor:' narrowing, still triggers not-callable. Direct attribute access
  works. <https://github.com/pylint-dev/pylint/issues/10471>

- **#10460** — False positive `ungrouped-imports` with if os.name Confirmed C0412
  ungrouped-imports false positive across if/else branches (cross-platform import
  pattern). Already linked to #7735, #3382 by reporter.
  <https://github.com/pylint-dev/pylint/issues/10460>

- **#10360** — False positive E1136: unsubscriptable-object when generic class defines
  **class_getitem** Confirmed E1136: when a generic class defines **class_getitem** AND
  **getitem**, instance of Test[int]([...]) is still flagged as unsubscriptable.
  <https://github.com/pylint-dev/pylint/issues/10360>

- **#10348** — False positive `too-few-public-methods` on property function calls and
  descriptors Real false positive R0903 'too-few-public-methods' for the
  property-equivalent forms via class-attribute property() / **get** descriptors.
  Verified by labels and author's diff.
  <https://github.com/pylint-dev/pylint/issues/10348>

- **#10201** — W1514 unspecified-encoding false positive when mode is specified using a
  variable and it can be 'b' W1514 unspecified-encoding fires when mode is a variable
  that could be binary. Real false positive — checker doesn't handle parameterized mode
  strings. <https://github.com/pylint-dev/pylint/issues/10201>

### FIXED (8)

- **#10768** — Started getting "invalid name" errors on a module-level global variable
  after upgrade to pylint 4.0. Does NOT reproduce on pylint 4.0.5/astroid 4.0.2 —
  '\_g_is_installed' under '--include-naming-hint=y' only triggers W0603
  (global-statement), no C0103. Likely fixed via the dummy-vars/global mutation handling
  improvement landed in 4.0.5. <https://github.com/pylint-dev/pylint/issues/10768>

- **#10766** — False positive for constant naming style inside **main** block Does NOT
  reproduce on pylint 4.0.5: 'exit_code = main()' inside 'if **name** == "**main**":'
  block — even in a file actually named **main**.py — gets 10/10. Bug appears to be
  fixed since 4.0.4. <https://github.com/pylint-dev/pylint/issues/10766>

- **#10670** — False Positive for too-many-function-args when subclassing **new** Does
  NOT reproduce on pylint 4.0.5: subclassing datetime.datetime with custom **new**
  signature passes (10.00/10 with --enable=E1121). Fixed after 4.0.1.
  <https://github.com/pylint-dev/pylint/issues/10670>

- **#10455** — False positive E1136 – unsubscriptable-object Does NOT reproduce on
  pylint 4.0.5 — the conditional-expression pattern 'end = struct[k] if k in struct else
  None' followed by 'is not None' narrowing is now correctly handled (10/10).
  <https://github.com/pylint-dev/pylint/issues/10455>

- **#10442** — Treat `__main__.py` as a special module name under camelCase
  module-naming-style Does NOT reproduce: '**main**.py' under
  '--module-naming-style=camelCase' gets 10/10. Pylint 4.0.5 likely special-cases dunder
  module names. <https://github.com/pylint-dev/pylint/issues/10442>

- **#10422** — not-callable: Different behavior using f-string vs bin-op string Does NOT
  reproduce on pylint 4.0.5 with -d all -e not-callable: 'getattr(self, f"_call_{x}",
  None); method()' no longer raises E1102. Behavior unified with old-style %-format.
  <https://github.com/pylint-dev/pylint/issues/10422>

- **#10374** — False positive `redefined-variable-type` on ignored variables like `_`
  Does NOT reproduce on pylint 4.0.5 with redefined*variable_type extension. '* =
  cfg\_.read(...)' no longer raises R0204.
  <https://github.com/pylint-dev/pylint/issues/10374>

- **#10298** — False positive E1133 (not-an-iterable) when returning (type hinted) class
  variable Does NOT reproduce E1133 on simple Iterable|None narrowing snippet on 4.0.5.
  Reporter's exact pattern may differ; default snippet is now clean.
  <https://github.com/pylint-dev/pylint/issues/10298>

### UNCLEAR (6)

- **#11013** — C0103: Constant name false positive when typing variables nested in
  `TYPE_CHECKING` Default pylint config does not raise C0103 on the snippet. Reporter
  has heavy custom .pylintrc with many plugins (pylint-per-file-ignores, docparams,
  mccabe). With defaults the only message is R6003 (Union->|). Config-dependent.
  <https://github.com/pylint-dev/pylint/issues/11013>

- **#11012** — C0103: Variable name false positive for single word all caps at module
  level Default pylint config does not raise C0103 on 'HTML = obj.method' at module
  level. Reporter has heavy custom .pylintrc. Tried several variations (os.path.join,
  function call return, classmethod) — all clean under defaults. Config-dependent.
  <https://github.com/pylint-dev/pylint/issues/11012>

- **#10991** — Unexpected kwarg false-positive when using TypeVarTuple Does NOT
  reproduce E1123 on pylint 4.0.5/astroid 4.0.2 — only W2604 (PEP695 unsupported). User
  reported on astroid 4.0.4; behavior may differ in newer astroid. Need astroid 4.0.4 to
  verify. <https://github.com/pylint-dev/pylint/issues/10991>

- **#10941** — astroid.exceptions.AstroidBuildingError: while using python 3.12 Vague
  crash report (AstroidBuildingError) on old pylint 3.2.2/astroid 3.2.4 with no minimal
  repro. Labeled 'Needs reproduction'.
  <https://github.com/pylint-dev/pylint/issues/10941>

- **#10352** — Empty transform plugin leads to false-positive missing-function-docstring
  issues Needs the user's empty transform plugin to reproduce. Body claims false
  missing-function-docstring across PEP 695 inheritance chain; needs plugin
  reproduction. <https://github.com/pylint-dev/pylint/issues/10352>

- **#10278** — "ImportError: Unable to find module" when using implicit namespaces when
  they already exist in site- ImportError on implicit namespace package. Needs project
  setup to repro. <https://github.com/pylint-dev/pylint/issues/10278>

### EXTDEP (27)

- **#10916** — E1136 false positive on PySide6 overloaded signal subscript Needs PySide6
  installed to verify; E1136 on QSignal[type] subscript. Likely real — Qt signals'
  subscript overload not modeled by pylint/astroid. Library-specific.
  <https://github.com/pylint-dev/pylint/issues/10916>

- **#10849** — "Cannot import 'libtorrent' due to 'invalid or missing encoding
  declaration" false positive Needs libtorrent (cython/.so extension) — false E0001
  'invalid or missing encoding declaration' when astroid tries to parse a compiled .so
  file. Real astroid bug discriminating C-ext modules.
  <https://github.com/pylint-dev/pylint/issues/10849>

- **#10838** — False Positive "no member" with numpy finfo Needs numpy 2.4+ installed to
  verify (numpy not installed locally). Claim is np.finfo(1.0).eps raises E1101.
  Library-specific (numpy brain in astroid).
  <https://github.com/pylint-dev/pylint/issues/10838>

- **#10831** — False positive unexpected-keyword-arg with scipy.stats 1.17 Needs scipy
  1.17 installed (scipy not installed locally). Regression in scipy 1.17 where
  stats.entropy added nan_policy kwarg; astroid hasn't followed the API change.
  <https://github.com/pylint-dev/pylint/issues/10831>

- **#10827** — False positive unused-import and unused-wildcard-import Needs project
  layout reproduction (src/tests with **all**-driven wildcard import). False
  unused-import/unused-wildcard-import. Likely real — pattern-match through inter-module
  imports is shaky. <https://github.com/pylint-dev/pylint/issues/10827>

- **#10796** — False Positive "no-member" with pandas `DatetimeIndex` Needs pandas
  installed; reported on pandas 2.3.3. False E1101 for DatetimeIndex.date — astroid's
  pandas brain doesn't model the .date property.
  <https://github.com/pylint-dev/pylint/issues/10796>

- **#10767** — Pylint/pyreverse bug Pyreverse crash 'EmptyNode has no attribute name' on
  a real Django/poetry project. No minimal repro shared. Needs project minimization or
  astroid update. <https://github.com/pylint-dev/pylint/issues/10767>

- **#10761** — False positive for `unreachable` when doing OpenGL (Pyglet.gl) calls
  Needs pyglet.gl installed. False-positive unreachable after pyglet.gl calls.
  Library-specific — astroid likely infers GL func returning NoReturn.
  <https://github.com/pylint-dev/pylint/issues/10761>

- **#10710** — E1102 “not-callable” false positive for torch.nn.functional.one_hot
  (alias, fully-qualified, and dir Needs torch installed. E1102 'not-callable' false
  positive on torch.nn.functional.one_hot. Library-specific astroid brain.
  <https://github.com/pylint-dev/pylint/issues/10710>

- **#10665** — False-positive: Starting from version 4.0.0 false-positive on pytest-bdd
  fixtures Needs pytest*bdd. Regression in 4.0.0 where @given/@when decorated step
  functions named '*' get E0102. Reporter's body is inconsistent but the title and
  version-range claim are clear. <https://github.com/pylint-dev/pylint/issues/10665>

- **#10650** — False-positive E1101: Method '<no-name>' has no 'connect' member
  (no-member) Needs PySide6. False E1101 on QSignal.connect — astroid does not resolve
  Qt signals as descriptors. Library-specific brain gap.
  <https://github.com/pylint-dev/pylint/issues/10650>

- **#10602** — False positives on generic pydantic models Needs pydantic installed.
  R0903 'too-few-public-methods' false positive on classes that inherit from a
  generic-parameterized pydantic BaseModel subclass. astroid pydantic brain gap.
  <https://github.com/pylint-dev/pylint/issues/10602>

- **#10548** — False positive: `unexpected-keyword-argument` when passing `dtype` to
  `numpy.concatenate()` Needs numpy installed. False E1123 on np.concatenate(...,
  dtype=...) — astroid numpy brain stub missing the dtype kwarg.
  <https://github.com/pylint-dev/pylint/issues/10548>

- **#10513** — Pylint hangs when trying to lint a pyo3 enum with named fields Needs
  pyo3-compiled module to reproduce; pylint hangs in astroid transforms on Rust
  enum-with-named-fields. Minimal Python repro provided but cannot be tested without
  building the .so. Astroid recursion.
  <https://github.com/pylint-dev/pylint/issues/10513>

- **#10474** — Crash (possibly caused by `win32more`) `Building error when trying to
  create ast representation of m Needs win32more installed. Crash 'Building error when
  trying to create ast representation'. Astroid lib-specific failure.
  <https://github.com/pylint-dev/pylint/issues/10474>

- **#10459** — Infinite recursion error with scipy 1.16 Needs scipy 1.16. Infinite
  recursion / crash in astroid when parsing 'from scipy.special import erf'. Astroid
  issue. <https://github.com/pylint-dev/pylint/issues/10459>

- **#10440** — FP unbalanced-tuple-unpacking with np.unravel_index Needs numpy. False
  W0632 unbalanced-tuple-unpacking on np.unravel_index return — astroid numpy brain
  doesn't know the function returns a tuple of length ndim.
  <https://github.com/pylint-dev/pylint/issues/10440>

- **#10433** — False positive E1120 for static method call on GI object in Python 3.14
  Needs gi (PyGObject) installed. False E1120 'self' missing for static-method call on
  GIRepository class — regression linked to Python 3.14 internal introspection change.
  <https://github.com/pylint-dev/pylint/issues/10433>

- **#10423** — unsubscriptable-object doesn't consider all inference results Needs
  matplotlib. unsubscriptable-object only considers the first inference result, misses
  tuple-returning branch. Real but tied to plt.subplots return-type inference.
  <https://github.com/pylint-dev/pylint/issues/10423>

- **#10418** — With Astroid 3.3.10 and .pyi files, Pylint gives false duplicate code
  errors Needs the blessed project's .pyi files and astroid 3.3.10. Duplicate-code
  blowup with .pyi triggered by an astroid 3.3.10 change. Astroid-side.
  <https://github.com/pylint-dev/pylint/issues/10418>

- **#10413** — No name 'CoInitialize' in module 'pythoncom' Needs pythoncom
  (Windows-only). False E0611 on 'from pythoncom import CoInitialize' — astroid doesn't
  enumerate C extension symbols correctly.
  <https://github.com/pylint-dev/pylint/issues/10413>

- **#10345** — Crash `TypeError: 'UninferableBase' object is not iterable` -
  [astroid-error] Crash 'TypeError: UninferableBase not iterable'. Needs project repro
  or full traceback to localize. <https://github.com/pylint-dev/pylint/issues/10345>

- **#10326** — Crash ``Building error when trying to create ast representation of module
  'sympy.polys.numberfields. Crash 'Building error when trying to create ast
  representation of module'. No minimal repro shared.
  <https://github.com/pylint-dev/pylint/issues/10326>

- **#10317** — `unbalanced-tuple-unpacking` false positive with `statistics.quantiles`
  Needs statistics module from stdlib + astroid quantile signature. Related to #10440.
  <https://github.com/pylint-dev/pylint/issues/10317>

- **#10316** — Wave_write object from wave library confused with Wave_read object #603
  Real lib-specific: astroid wave brain models wave.open() return as Wave_read
  regardless of mode. Has 'Needs PR' label.
  <https://github.com/pylint-dev/pylint/issues/10316>

- **#10312** — False positive E1126 when using np.newaxis with np.where Needs numpy.
  False E1126 on np.where with np.newaxis indexing. Astroid numpy brain.
  <https://github.com/pylint-dev/pylint/issues/10312>

- **#10222** — E1101: Class 'value' has no 'any' member (no-member) for psycopg
  connection class Needs psycopg installed. Variable assignment vs in-with-statement
  context-manager unbinding produces wrong type inference.
  <https://github.com/pylint-dev/pylint/issues/10222>

### DESIGN (39)

- **#11005** — Improve the performance of PyLinter.\_discover_files()'s use of the
  os.walk() method. Performance enhancement for \_discover_files() to use os.walk
  topdown pruning. Author already has a PR planned. Pertinent.
  <https://github.com/pylint-dev/pylint/issues/11005>

- **#10982** — Python 3.15 compatibility Python 3.15 compat tracker — patch provided in
  body to update functional tests, mostly test-infrastructure work. Active.
  <https://github.com/pylint-dev/pylint/issues/10982>

- **#10976** — warn of module level attributes that may get shadowed by importing
  submodules Enhancement: extend C0103 to also warn module-level attrs that may be
  shadowed by importing same-name submodule. No code repro applicable.
  <https://github.com/pylint-dev/pylint/issues/10976>

- **#10959** — Disable `W0603` in the body of module-level `__getattr__` by default
  Proposal to suppress W0603 in module-level **getattr** body — well-justified by stdlib
  pattern (asyncio). Design discussion, no repro.
  <https://github.com/pylint-dev/pylint/issues/10959>

- **#10958** — Let's stay away from recommending `re.prefixmatch`. Meta-discussion:
  decision to NOT add a re.prefixmatch recommendation check. Decision-tracking ticket.
  <https://github.com/pylint-dev/pylint/issues/10958>

- **#10844** — test_functional.py --update-functional-output deletes files for other
  Python versions Internal dev tool bug: test_functional.py --update-functional-output
  incorrectly removes files for other Python versions. Internal cleanup.
  <https://github.com/pylint-dev/pylint/issues/10844>

- **#10792** — Add check for redundant exception message when using 'raise ... from'
  (W0720) New checker proposal W0720: redundant-exception-message when 'raise X(...
  {err}) from err'. Decision pending; implementation offered.
  <https://github.com/pylint-dev/pylint/issues/10792>

- **#10748** — Add optional "Annotation Complexity" checker to flag deeply nested type
  hints Enhancement: add 'annotation-complexity' checker for deeply nested type hints.
  Specification pending; prototype offered.
  <https://github.com/pylint-dev/pylint/issues/10748>

- **#10739** — import-private-name raises for multi-root projects Design discussion:
  import-private-name fires across multi-root projects; user wants config to declare
  additional 'package roots'. <https://github.com/pylint-dev/pylint/issues/10739>

- **#10737** — Backslashes don't properly render in docs Docs bug: backslashes don't
  render in some auto-generated .rst pages. Partial PR exists (#10736). Documentation
  cleanup. <https://github.com/pylint-dev/pylint/issues/10737>

- **#10713** — `comparison-with-itself` only flags comparison with Name
  Question/enhancement: extend comparison-with-itself beyond Name to general expressions
  (a.b == a.b). Discussion. <https://github.com/pylint-dev/pylint/issues/10713>

- **#10688** — tbump before commit step to update functional test output fails Internal
  dev tooling: tbump on maintenance branch fails because functional test output file for
  3.14 doesn't exist on older branches.
  <https://github.com/pylint-dev/pylint/issues/10688>

- **#10657** — Changelog with both rst, github, and specific message output Maintainer
  enhancement: improve release/changelog tooling (sphinx, towncrier). Internal
  infrastructure. <https://github.com/pylint-dev/pylint/issues/10657>

- **#10637** — Removal of mandatory isort dependency for import position check 5.0-level
  design proposal: drop or refactor isort dependency in wrong-import-position. Author is
  a maintainer; not a user bug. <https://github.com/pylint-dev/pylint/issues/10637>

- **#10630** — Extend W0102 dangerous-default-value rule to Include os.getenv and
  os.environ Enhancement: extend W0102 dangerous-default-value to flag
  os.getenv/os.environ as defaults. Specification pending.
  <https://github.com/pylint-dev/pylint/issues/10630>

- **#10604** — Async Context Managers User question + docs request: how to type async
  ctx manager method overrides that use @asynccontextmanager so they're recognized as
  compatible with AbstractAsyncContextManager. Documentation gap.
  <https://github.com/pylint-dev/pylint/issues/10604>

- **#10584** — disable rule for files matching a patttern User question on how to
  disable a rule for files matching a pattern. Q&A / docs improvement opportunity
  (pyproject.toml has per-file overrides for some options, this is mostly a doc
  surface). <https://github.com/pylint-dev/pylint/issues/10584>

- **#10563** — Add sphinx references to pylint messages Enhancement: add a custom sphinx
  role :pylint:`msg-name` to link to message docs. Documentation tooling.
  <https://github.com/pylint-dev/pylint/issues/10563>

- **#10550** — Warn about PEP 784: Zstandard in the standard library Discussion: warn
  about PEP 784 zstandard / compression.\* aliases when py-version >= 3.14. Blocked
  pending policy decision. <https://github.com/pylint-dev/pylint/issues/10550>

- **#10517** — parameter_documentation: Add magic phrase to ignore missing return
  documentation Enhancement: add 'For the return, see' magic phrase for
  parameter_documentation extension to allow missing return docs. Discussion.
  <https://github.com/pylint-dev/pylint/issues/10517>

- **#10479** — False positive `duplicate-code` on `setuptools-scm` autogenerated
  `version.py` files Decision needed: should pylint auto-skip 'duplicate-code' on
  auto-generated setuptools-scm version.py files? Has user workaround.
  <https://github.com/pylint-dev/pylint/issues/10479>

- **#10478** — false positive consider-using-namedtuple-or-dataclass Heuristic: R6101
  consider-using-namedtuple-or-dataclass over-fires on dicts with different key sets
  that are then passed via \*\*kwargs. Discussion on tightening the heuristic.
  <https://github.com/pylint-dev/pylint/issues/10478>

- **#10476** — Using return value of a function that returns None is not always
  reported. Good first issue / Hacktoberfest. False negative: assigning the return value
  of a None-returning function to a variable should be flagged. Spec/design.
  <https://github.com/pylint-dev/pylint/issues/10476>

- **#10473** — Emit a new warning message for `global` usage scenario Enhancement: emit
  a new warning for some 'global' usage scenarios. Discussion-level.
  <https://github.com/pylint-dev/pylint/issues/10473>

- **#10461** — Plugin to add generated members User question: how to write an astroid
  transform plugin for a custom @extends_class decorator that injects methods into
  pybind11 ClassDef. Docs gap. <https://github.com/pylint-dev/pylint/issues/10461>

- **#10448** — Enhancement to `unreachable` - `if-else` Control Flow Proposal to extend
  'unreachable' to handle if/elif/else where all branches terminate. CFG-based approach
  proposed. Decision pending. <https://github.com/pylint-dev/pylint/issues/10448>

- **#10404** — Feature request - invoke `any`/`all` on non iterables Enhancement: extend
  not-an-iterable to any()/all() and to maybe-None paths. Spec needed.
  <https://github.com/pylint-dev/pylint/issues/10404>

- **#10383** — False negative - assign `list.reverse()` instead of `reversed(list)`
  Enhancement: warn on 'x = lst.reverse()' (return is None) — proposed via
  assignment-from-none. Discussion. <https://github.com/pylint-dev/pylint/issues/10383>

- **#10371** — W1404: implicit-str-concat does not work for single-argument function
  calls Spec: implicit-str-concat is whitelisted inside parens; reporter wants config to
  disable that whitelist. <https://github.com/pylint-dev/pylint/issues/10371>

- **#10365** — `unidiomatic-typecheck` not flagged for type(x) is type(y) Enhancement:
  extend unidiomatic-typecheck to 'type(x) is type(y)'. Discussion.
  <https://github.com/pylint-dev/pylint/issues/10365>

- **#10364** — Extend `comparison-with-callable` to types Enhancement: extend
  comparison-with-callable to compare types (a_class == b_class). Discussion.
  <https://github.com/pylint-dev/pylint/issues/10364>

- **#10339** — False negative `import-error` when the package imported is one of
  pylint's dependency Enhancement: detect import-error when package imported is itself
  the linted project. High-effort design proposal.
  <https://github.com/pylint-dev/pylint/issues/10339>

- **#10281** — Expand to `use-implicit-booleaness-not-len` to catch `len(iterable) == 0`
  and `>0` Enhancement: extend use-implicit-booleaness-not-len to 'len(iter)'. Spec
  pending. <https://github.com/pylint-dev/pylint/issues/10281>

- **#10262** — Why does too-many-statements consider statements in nested functions?
  Q+docs: should too-many-statements count nested-function statements? Decision pending.
  <https://github.com/pylint-dev/pylint/issues/10262>

- **#10259** — Pylint doesn't complain on Protocol callback argument-type / return-type
  mismatch Decision: Pylint doesn't validate Protocol callback arg/return types. Spec
  needed. <https://github.com/pylint-dev/pylint/issues/10259>

- **#10239** — Support for checking construction of NamedTuple/namedtuple Enhancement:
  check construction of NamedTuple/namedtuple. astroid update needed.
  <https://github.com/pylint-dev/pylint/issues/10239>

- **#10238** — Class definition in conditionals not correctly found Spec: class
  definition inside conditionals isn't tracked correctly by control flow. Design
  proposal. <https://github.com/pylint-dev/pylint/issues/10238>

- **#10237** — False negative `differing-type-doc` for Google-style docstring
  Enhancement: differing-type-doc for Google-style docstrings. Has PR scope.
  <https://github.com/pylint-dev/pylint/issues/10237>

- **#10199** — Inconsistent block starting line behaviour for classes Specification
  question: scope of '# pylint: disable=invalid-name' on class-def line — applies to
  body methods or only the def line? Behavior is inconsistent.
  <https://github.com/pylint-dev/pylint/issues/10199>

### DUP (1)

- **#10806** — False positive for numpy 2.4.0+ Duplicate of #10838 — same
  numpy.finfo.eps no-member false positive. #10806 is the older report.
  <https://github.com/pylint-dev/pylint/issues/10806>

### STALE (1)

- **#10963** — Pylint OOM (exit code -9) in GitHub Actions when processing large number
  of files. OOM report on pylint 3.2.5 (4.x current). Vague, no minimal repro — generic
  CI memory issue. User on outdated version.
  <https://github.com/pylint-dev/pylint/issues/10963>
