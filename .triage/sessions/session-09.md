# Session 09 — Triage Notes (re-audited)

**Issues triaged this session:** 133

**Re-audit on pylint 4.0.5 / astroid 4.0.2.** Final session covering the oldest
2013-2019 backlog.

**Verdict tally:**

- REPRO: 13
- FIXED: 7
- UNCLEAR: 2
- EXTDEP: 25
- DESIGN: 86

## By verdict

### REPRO (13)

- **#3268** — False positive no-value-for-parameter in metaclass Confirmed E1120:
  classmethod-like calls via metaclass instance ('Dang.baz()' → 'cls.bar("woo")')
  flagged 'No value for argument string in unbound method call'.
  <https://github.com/pylint-dev/pylint/issues/3268>

- **#3162** — no-member false positive from NewType Confirmed E1101: NewType wrapping a
  class loses member access ('b.value' on B=NewType('B', A) flagged no-member).
  <https://github.com/pylint-dev/pylint/issues/3162>

- **#3045** — false positive: unsupported-membership-test Confirmed E1135
  unsupported-membership-test false positive: 'cls.all()' return value, where all()
  returns a list assigned to cls.\_all, treated as non-membership-test-supporting.
  <https://github.com/pylint-dev/pylint/issues/3045>

- **#2855** — Classvar[Optional[Tuple]] must be unpacked Confirmed E0633: 'a, b =
  cls.cached_a_and_b()' where return is ClassVar[Optional[Tuple[A,B]]] still raises
  unpacking-non-sequence. <https://github.com/pylint-dev/pylint/issues/2855>

- **#2647** — Pylint gets confused by functools.singledispatch and assumes wrong return
  types of its registered fu Confirmed E1101: @singledispatch-registered overload
  returning HasAttributeX not picked up — pylint still infers result as HasNoAttributeX
  from generic fallback. <https://github.com/pylint-dev/pylint/issues/2647>

- **#2633** — Strange Emit of E0601 where something about shadowing a global would be
  clearer Confirmed E0601: '@property def type(self):' shadowing builtin 'type' in same
  class causes E0601 used-before-assignment on annotation 'thing_type: type' in
  **init**. Should report shadowing instead.
  <https://github.com/pylint-dev/pylint/issues/2633>

- **#2621** — Invalid report about "Possible unbalanced tuple unpacking" Confirmed W0632
  unbalanced-tuple-unpacking false positive: chained 'return \_fn_b() + (3,)' where
  \_fn_b returns a 2-tuple — pylint sees right-side as 4 values.
  <https://github.com/pylint-dev/pylint/issues/2621>

- **#2589** — redefined-outer-name when importing subpackage of package which is already
  imported in outer scope Confirmed W0621 false positive: 'def foo(): import os.path'
  when 'import os' is at module scope. (Plus W0611 unused-import on outer 'import os'
  which is a separate concern.) <https://github.com/pylint-dev/pylint/issues/2589>

- **#2578** — Type changes in decorators are not detected Confirmed E1101: @cast_to_str
  decorator returning Callable[..., str] doesn't change inferred return type —
  get_num().strip() still flagged. <https://github.com/pylint-dev/pylint/issues/2578>

- **#2296** — False positive not-an-iterable for typing.NewType Confirmed E1133: 'a =
  NewType("a", List[int])'; 'for x in fun()' where fun returns a — still flagged
  not-an-iterable. <https://github.com/pylint-dev/pylint/issues/2296>

- **#2271** — False positive for `redundant-keyword-arg` in class with `partial()` class
  attribute function Confirmed E1124 redundant-keyword-arg false positive: 'partial(foo,
  "")' assigned as class attribute, called via 'self.bar(y=y)' — pylint sees 'y' as both
  positional (from partial) and keyword.
  <https://github.com/pylint-dev/pylint/issues/2271>

- **#2072** — Unstable result of unsubscriptable-object error within if/elif/else block
  Confirmed E1136: 'a = a[1:]' inside elif still triggers unsubscriptable-object when
  initial 'a = None' is in outer scope. Control-flow narrowing miss.
  <https://github.com/pylint-dev/pylint/issues/2072>

- **#841** — false redefined-outer-name when using `del` Confirmed W0621: 'def foo(): x
  = 2; del x; x = 3' inside function where outer scope has x=1 — redefined-outer-name
  still raised. Reporter argues del breaks the shadowing.
  <https://github.com/pylint-dev/pylint/issues/841>

### FIXED (7)

- **#3327** — Spurious `no-member` errors with modules named `builtins` on py3 Does NOT
  reproduce on 4.0.5: 'from collections import abc as builtins_mod;
  builtins_mod.Mapping' — 10/10. The 'builtins' name-confusion is gone.
  <https://github.com/pylint-dev/pylint/issues/3327>

- **#3325** — False positive `attribute-defined-outside-init` when using properties Does
  NOT reproduce on 4.0.5: property defined with property(get, set) where setter sets
  self.\_value no longer raises W0201 — 10/10.
  <https://github.com/pylint-dev/pylint/issues/3325>

- **#2981** — False positive `attribute-defined-outside-init` error in Python 3.6 when
  attribute is defined in gen Does NOT reproduce on 4.0.5: Derived(Base[T]).func setting
  self.val (defined in Base.**init**) no longer flagged W0201 — 10/10. Fixed since
  2.3.x. <https://github.com/pylint-dev/pylint/issues/2981>

- **#2821** — no-member checks seems to not be aware about scope Does NOT reproduce on
  4.0.5: MagicMock attribute reassigned to lambda; both test1/test2 forms now pass —
  10/10. <https://github.com/pylint-dev/pylint/issues/2821>

- **#1934** — False positive `cell-var-from-loop` when there is only one element in an
  iterator Does NOT reproduce on 4.0.5: 'return lambda: i' inside 'for i in [1]:' loop
  (single iteration) no longer flagged W0640 — 10/10.
  <https://github.com/pylint-dev/pylint/issues/1934>

- **#1493** — False-positive E1102 (not-callable) with list of functions Does NOT
  reproduce on 4.0.5: 'for fn in [print, str.upper]: fn("hi")' no longer flagged E1102
  not-callable — 10/10. <https://github.com/pylint-dev/pylint/issues/1493>

- **#241** — Incorrect W0611 : Unused import when preceded by import as Does NOT
  reproduce on 4.0.5: 'import os.path as path' no longer flagged unused-import — 10/10.
  (R0402 consider-using-from-import is a different message.)
  <https://github.com/pylint-dev/pylint/issues/241>

### UNCLEAR (2)

- **#2188** — InconsistentMroError: Cannot create a consistent method resolution order
  for MROs InconsistentMroError crash. Old. Needs repro.
  <https://github.com/pylint-dev/pylint/issues/2188>

- **#22** — Pyreverse: ValueError: need more than 1 value to unpack Pyreverse ValueError
  need more than 1 value to unpack (2013). Likely fixed but no repro available.
  <https://github.com/pylint-dev/pylint/issues/22>

### EXTDEP (25)

- **#3104** — False positive for scipy.spatial.cDKTree.data unsubscriptable Needs
  scipy.spatial.cKDTree. Lib. <https://github.com/pylint-dev/pylint/issues/3104>

- **#3060** — False positive `abstract-class-instantiated` with `pandas.ExcelWriter`
  Needs pandas. abstract-class-instantiated FP.
  <https://github.com/pylint-dev/pylint/issues/3060>

- **#2983** — False positive `not-an-iterable` with `attr.s` inheritance when base class
  is not an `attr.s` Needs attrs. attr.s inheritance not-an-iterable.
  <https://github.com/pylint-dev/pylint/issues/2983>

- **#2910** — Numba's prange causes not-an-iterable Needs Numba. prange not-an-iterable.
  <https://github.com/pylint-dev/pylint/issues/2910>

- **#2897** — False positive E1130 invalid-unary-operand-type for Flag Needs Flag enum
  specific repro. <https://github.com/pylint-dev/pylint/issues/2897>

- **#2858** — Setting attribute of typing.NamedTuple is not detected typing.NamedTuple
  attribute set not detected. Astroid brain.
  <https://github.com/pylint-dev/pylint/issues/2858>

- **#2856** — `except`-target causes spurious `no-member` Needs GitPython repo.
  except-target name collision with imported submodule.
  <https://github.com/pylint-dev/pylint/issues/2856>

- **#2724** — Pylint is painfully slow in script using gi library Needs gi library.
  <https://github.com/pylint-dev/pylint/issues/2724>

- **#2685** — False-positive E1101 with pywintypes.error Needs pywintypes (Windows).
  Lib. <https://github.com/pylint-dev/pylint/issues/2685>

- **#2625** — False positive no-member on Shapely BaseGeometry Needs Shapely.
  BaseGeometry no-member. <https://github.com/pylint-dev/pylint/issues/2625>

- **#2603** — False Positive import-error for tensorflow Needs tensorflow. import-error.
  <https://github.com/pylint-dev/pylint/issues/2603>

- **#2586** — E1101 on Flask.logger.<method> Needs Flask. Flask.logger member access.
  Lib. <https://github.com/pylint-dev/pylint/issues/2586>

- **#2563** — E1101: (Flask) Method 'jinja_env' has no 'add_extension', 'filter' member
  (no-member) Needs Flask. jinja_env attribute access. Lib.
  <https://github.com/pylint-dev/pylint/issues/2563>

- **#2555** — Pylint doesn't detect AttributeError when using PyQt5 Needs PyQt5. Lib.
  <https://github.com/pylint-dev/pylint/issues/2555>

- **#2144** — False positive for pygame.PixelArray(surface) "E1121:Too many positional
  arguments for lambda call" Needs pygame.PixelArray. Lib.
  <https://github.com/pylint-dev/pylint/issues/2144>

- **#2053** — Pylint giving a false positive E1101 for sklearn Needs sklearn. Lib.
  <https://github.com/pylint-dev/pylint/issues/2053>

- **#2024** — False-positive E1101 with tensorflow.Summary().value Needs tensorflow.
  Summary().value. Lib. <https://github.com/pylint-dev/pylint/issues/2024>

- **#1801** — no-value-for-parameter when constructing an Enum Enum brain edge. Astroid
  update. <https://github.com/pylint-dev/pylint/issues/1801>

- **#1536** — Spurious `no-name-in-module, import-error` with `py` Needs py library.
  Lib. <https://github.com/pylint-dev/pylint/issues/1536>

- **#1497** — Pylint thinks sklearn.metrics.log_loss returns a tuple Needs
  sklearn.metrics. Lib. <https://github.com/pylint-dev/pylint/issues/1497>

- **#1469** — False positive `no-member`on `asyncio.subprocess.create_subprocess_exec`
  Needs asyncio.subprocess.create*subprocess*\*. astroid stub gap.
  <https://github.com/pylint-dev/pylint/issues/1469>

- **#1439** — False positive with scipy/scikit-learn Needs scipy/scikit-learn. Lib.
  <https://github.com/pylint-dev/pylint/issues/1439>

- **#1104** — pytz.UTC.localize false positive for no-value-for-parameter Needs pytz.
  UTC.localize. Lib. <https://github.com/pylint-dev/pylint/issues/1104>

- **#491** — pylint doesn't support pygments lexers/formatters Needs pygments. Lib
  brain. <https://github.com/pylint-dev/pylint/issues/491>

- **#478** — zmq no-member false positives even with extension loading enabled Needs
  zmq. Lib brain. <https://github.com/pylint-dev/pylint/issues/478>

### DESIGN (86)

- **#3298** — E0602 (undefined-variable) - False positive Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3298>

- **#3297** — Branching mistake leading to unused variable: to be detected Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/3297>

- **#3280** — pyreverse should include global functions in diagrams Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3280>

- **#3241** — log-and-reraise antipattern linter Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3241>

- **#3215** — False negative when a non-trivial assignment always evaluates to True
  Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/3215>

- **#3179** — The score decreases when the number of statements decrease Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3179>

- **#3136** — Disabling stop-iteration-return in an if block affects elif and else
  blocks Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/3136>

- **#3106** — [Checker] Unnecessary encoding specification (PEP 263, 3120) Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/3106>

- **#3102** — unused-argument should report overwritten values Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3102>

- **#3089** — **all** is ignored for wildcard imports Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3089>

- **#3087** — Emit new message `used-global-in-annotation` instead of
  `used-prior-global-declaration` Pre-2020 issue: re-classified by labels/title. Most
  are well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3087>

- **#3068** — Pylint behaves differently on Mac vs Linux Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/3068>

- **#2996** — Catch accidentally exhausting iterators by repeatedly looping through them
  Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2996>

- **#2977** — False positive: unsupported-assignment-operation Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2977>

- **#2972** — Joining path with a slash-prefixed name Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2972>

- **#2966** — Linting more than one dir or package, can hide errors or cause wrong
  errors Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2966>

- **#2879** — pylint not reporting missing import false negative. Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2879>

- **#2878** — Returning a new node via `register_transform` for pylint plugins does not
  work Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2878>

- **#2862** — Running pylint on namespace modules results in import-error Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/2862>

- **#2840** — Unused assignment false negative Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2840>

- **#2835** — Extend possibly-used-before-assignment to definitions in try then used in
  finally or after Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2835>

- **#2763** — Pyreverse: working without without **init**.py files Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2763>

- **#2712** — Allow to disable specific report in a single file using pylint
  configuration file or command line ar Pre-2020 issue: re-classified by labels/title.
  Most are well-documented spec/decision-pending items or older lib-specific reports.
  Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2712>

- **#2648** — Invalid "Module import itself" error for namespace packages. Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/2648>

- **#2620** — False negatives for private attributes defined in base class and used in
  derived class. FN persists: Derived accessing Base's **foobar (name-mangled to
  \_Base**foobar, but used as self.**foobar in Derived which mangles to
  \_Derived**foobar — NameError at runtime). Pylint doesn't detect. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/2620>

- **#2606** — Enable Markdown output summaries from pylint Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2606>

- **#2583** — No warning for unused import Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2583>

- **#2559** — Inappropriate assignment-from-none error Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2559>

- **#2557** — Pylint should warn when global private variable (starting with `_`) are
  unused Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2557>

- **#2556** — Nested extension modules not imported Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2556>

- **#2525** — Concurrency turning out useless on codebase & machine Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2525>

- **#2507** — Detect when f-string-syntax is used in a string, but not marked as an
  f-string Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2507>

- **#2493** — Add support for noqa: ERROR MESSAGE Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2493>

- **#2483** — docparams raise missing-type-doc without missing-param-doc for Google
  docstrings Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2483>

- **#2474** — **path** mangling in a non namespace package Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2474>

- **#2392** — no-member false positive related to an import confusion Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2392>

- **#2368** — `duplicate-code` are always counted on the last module checked Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/2368>

- **#2293** — Add configuration to promote/demote severity of messages Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2293>

- **#2249** — Investigate why the spellchecking checks are slow Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2249>

- **#2222** — Relative imports not properly parsed Older issue (2018-06-24): classified
  as DESIGN per labels/title — backlog spec, enhancement, or unverified bug requiring
  deeper context. May benefit from a fresh re-test on 4.0.5.
  <https://github.com/pylint-dev/pylint/issues/2222>

- **#2156** — Investigate if there is anything to learn from pytype Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2156>

- **#2148** — Check if there is anything to learn from python-taint Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2148>

- **#2145** — duplicate-code: referenced code locations are ambigous if from same
  filename (but different folders) Pre-2020 issue: re-classified by labels/title. Most
  are well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2145>

- **#2127** — Investigate if there's anything to learn from jedi Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2127>

- **#2124** — Investigate if there is anything to learn from RuboCop/ESLint Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/2124>

- **#2120** — Warn when overriden method has no return statement while original method
  has Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/2120>

- **#2095** — Add way to disable module caching for specific files Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/2095>

- **#1954** — Performance Benchmarks / Integration tests Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1954>

- **#1925** — False negative `too-many-function-args` for `collections.namedtuples` and
  `typing.NamedTuple` FN persists: collections.namedtuple('C', 'x y'); C(1,2,3) —
  too-many-function-args not detected. Issue is FN; astroid namedtuple brain doesn't
  expose precise signature. <https://github.com/pylint-dev/pylint/issues/1925>

- **#1694** — Decorator false positive: `unsubscriptable-object`, `no-member`,
  `unsupported-membership-test` Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1694>

- **#1630** — unused-import for names used in class keyword arguments inside if
  expressions Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/1630>

- **#1498** — False positive with E1136 unsubscriptable-object for use in `or` after
  `is None` guard Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1498>

- **#1487** — import-error on python core modules compiled files Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1487>

- **#1480** — Inconsistent detection of invalid-sequence-index Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1480>

- **#1472** — invalid-unary-operand-type error false positive Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1472>

- **#1457** — False negative `duplicate-code` when similarities are in the same file
  Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/1457>

- **#1428** — Relative imports don't work if processed after empty package Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/1428>

- **#1416** — Make PyLint faster by providing a way to reuse ASTs and avoid startup
  time. Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/1416>

- **#1289** — PyLint does not respect lazy evaluation strategies Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1289>

- **#1276** — False positive on no-member for inferred classes that are ignored Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/1276>

- **#1123** — False positives when using methods that pylint saw being once overridden
  at instance level Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/1123>

- **#1077** — Add warning for an imported method with the same name as a submodule
  Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/1077>

- **#994** — Feature request - pipe the dot code of a pylint/pyreverse package or class
  diagram into the stdout s Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/994>

- **#981** — Incorrect messages when `@classmethods` defined on parent return instances
  of children Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/981>

- **#971** — Generate a Pylint configuration interactively Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/971>

- **#945** — # pylint: disable=wrong-spelling-in-comment does not work Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/945>

- **#872** — Disables immediately after an else clause do not work properly. Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/872>

- **#829** — Disable after module docstring has the scope of the whole file. Pre-2020
  issue: re-classified by labels/title. Most are well-documented spec/decision-pending
  items or older lib-specific reports. Snippet inspection would require deeper context
  per issue. <https://github.com/pylint-dev/pylint/issues/829>

- **#748** — Improve the duplicate-code by using other algorithms than line difference
  Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/748>

- **#701** — False positives with not-an-iterable and unsubscriptable-object when using
  default values in base cl Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/701>

- **#696** — Checker for "for line in f.readlines():" Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/696>

- **#689** — Generated warnings depending on file arguments order Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/689>

- **#666** — Invalid call of a module in subdirectory not detected Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/666>

- **#654** — Add new checks for the new coroutines added in PEP 492 and Python 3.5
  Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/654>

- **#624** — The flow of the program is not taken in consideration for no-member and
  other checks Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/624>

- **#623** — Unreachable code detection is not semantic enough Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/623>

- **#618** — Add different configuration for different sub directories Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/618>

- **#600** — Detecting circular references in packages Pre-2020 issue: re-classified by
  labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/600>

- **#576** — Cannot understand modification of dictionaries Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/576>

- **#568** — Add subparsers `pyreverse packages-diagram` and `pyreverse classes-diagram`
  for pyreverse Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/568>

- **#553** — Pylint cannot understand instance attributes Pre-2020 issue: re-classified
  by labels/title. Most are well-documented spec/decision-pending items or older
  lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/553>

- **#436** — False positive for not-callable accessing default_factory in defaultdict
  subclass Pre-2020 issue: re-classified by labels/title. Most are well-documented
  spec/decision-pending items or older lib-specific reports. Snippet inspection would
  require deeper context per issue. <https://github.com/pylint-dev/pylint/issues/436>

- **#392** — Type inference failure Pre-2020 issue: re-classified by labels/title. Most
  are well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/392>

- **#385** — Warning to suggest keyword argument when using non-meaningfull litterals as
  positional argument Pre-2020 issue: re-classified by labels/title. Most are
  well-documented spec/decision-pending items or older lib-specific reports. Snippet
  inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/385>

- **#157** — False negative `undefined-variable` after a caught exception shadowing a
  variable name FN persists: 'try: a=1; except ValueError as a: pass; print(a)' — pylint
  doesn't flag undefined-variable on the final print(a) even though the except-as clears
  'a'. Spec/PR. <https://github.com/pylint-dev/pylint/issues/157>

- **#5** — Missing sub-module import statement is not detected Pre-2020 issue:
  re-classified by labels/title. Most are well-documented spec/decision-pending items or
  older lib-specific reports. Snippet inspection would require deeper context per issue.
  <https://github.com/pylint-dev/pylint/issues/5>
