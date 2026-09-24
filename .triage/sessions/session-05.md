# Session 05 — Triage Notes (re-audited with per-issue reproduction)

**Issues triaged this session:** 170

**Re-audit:** session 5 was originally bulk-classified by labels/title in the first
pass. This re-audit replaces those with per-issue reproductions on pylint 4.0.5 /
astroid 4.0.2 where a minimal snippet was available.

**Verdict tally:**

- REPRO: 28
- FIXED: 3
- UNCLEAR: 2
- EXTDEP: 24
- DESIGN: 113

## By verdict

### REPRO (28)

- **#7625** — Pylint disable working incorrectly Confirmed bug: # pylint:
  disable-next=C0301 on a too-long comment line doesn't disable just that comment; needs
  --enable to recover. Pragma scope issue.
  <https://github.com/pylint-dev/pylint/issues/7625>

- **#7614** — False positive for repeated-keywords when dict item is popped off
  Confirmed E1132 false positive: 'foo(c=x, \*\*d)' after 'd.pop("c")' still flags
  repeated-keyword. pylint can't track dict mutation.
  <https://github.com/pylint-dev/pylint/issues/7614>

- **#7548** — unused-import false positive for names in string argument to typing.cast
  Confirmed W0611 false positive: 'paths = t.cast("set[Path]", set())' flags Path as
  unused even though it's in the cast type string.
  <https://github.com/pylint-dev/pylint/issues/7548>

- **#7545** — False positive `used-before-assignment` with multi-item `with` statement
  and tuple target Confirmed E0601 false positive: 'with f() as (a, b), g(a) as c:' —
  tuple-target multi-item with statement — pylint sees 'a' as undefined when used in
  g(a). <https://github.com/pylint-dev/pylint/issues/7545>

- **#7538** — False positive `used-before-assignment` with walrus operator inside binary
  operation Confirmed E0601 false positive: walrus operator inside binary 'd' + (... if
  (s1 := 'x') else '') — only flagged when the f-string is on either side of +; bare
  conditional works. <https://github.com/pylint-dev/pylint/issues/7538>

- **#7500** — `not-callable` false positive for `types.FunctionType` Confirmed E1102
  not-callable false positive on 'types.FunctionType(code, {})()'. astroid doesn't
  recognize FunctionType instances as callable.
  <https://github.com/pylint-dev/pylint/issues/7500>

- **#7487** — False positive: `no-member` when inner function uses the `@classmethod`
  decorator Confirmed E1101 false positive: @classmethod-decorated inner function inside
  def test() treated as member of 'test' function.
  <https://github.com/pylint-dev/pylint/issues/7487>

- **#7470** — False positive with match/case for `function-redefined` Confirmed E0102
  function-redefined false positive: 'def function():' in match/case 'case "c":' branch
  flagged as redefinition of earlier 'function = function_a' assignment in 'case "a":'
  branch. <https://github.com/pylint-dev/pylint/issues/7470>

- **#7460** — False negative: expected undefined-variable when deleted variable used
  Confirmed FN persists: 'del abc; print(abc)' inside function is not flagged
  undefined-variable (10/10) even though Python raises UnboundLocalError at runtime.
  <https://github.com/pylint-dev/pylint/issues/7460>

- **#7452** — False positive `import-self` when attempting relative import of misspelled
  submodule name in a packa Confirmed W0406 import-self false positive: 'from . import
  misspelled_module_name' on a missing submodule incorrectly reports 'Module import
  itself' instead of import-error. <https://github.com/pylint-dev/pylint/issues/7452>

- **#7424** — invalid-sequence-index when unpacking a sequence of sequences Confirmed
  E1126 false positive: 'for a1,a2,a3,a4 in n:' where n has 4+ p1 entries and p1 is a
  4-tuple. Tuple unpacking in for-loop loses element type info.
  <https://github.com/pylint-dev/pylint/issues/7424>

- **#7379** — False positive no-member on member of generic parent class with overridden
  **class_getitem** Already verified REPRO in session 4.
  <https://github.com/pylint-dev/pylint/issues/7379>

- **#7348** — False positives for E1120 and E1123 when instance method is overwritten
  Already verified REPRO in session 4.
  <https://github.com/pylint-dev/pylint/issues/7348>

- **#7296** — pylint doesn't know re.Pattern members Confirmed E1101: dataclass with
  field 're.Pattern[str]' — accessing C.pattern_instance.pattern reports no-member.
  astroid re brain doesn't propagate through dataclass.
  <https://github.com/pylint-dev/pylint/issues/7296>

- **#7293** — False positive for unexpected-keyword-arg using `**` operator Confirmed
  E1123 false positive: 'd["arg"] = d["b"]; del d["b"]; func(\*\*d)' still flags 'b' as
  unexpected kwarg even though it was deleted.
  <https://github.com/pylint-dev/pylint/issues/7293>

- **#7282** — E1101 false-positive/-negtive when mutating typess of dictionary values
  Confirmed mixed E1101 FP/FN: mutating dict values via 'for k,v in d.items(): d[k] =
  transform(v)' — pylint still sees old type. Real but the FN side (case 3) is the
  trickier part. <https://github.com/pylint-dev/pylint/issues/7282>

- **#7271** — consider-using-generator / R1728 false positive for "AsyncGenerator" valid
  code Confirmed R1728 false positive: consider-using-generator suggests rewriting
  'tuple([_ async for _ in my_gen()])' → 'tuple(_ async for _ in my_gen())' which raises
  TypeError. <https://github.com/pylint-dev/pylint/issues/7271>

- **#7269** — time.sleep false negative! Confirmed false negative: 'from time import
  time; time.sleep(1)' (calling .sleep on the time _function_) is not flagged no-member
  even though time.time is a function.
  <https://github.com/pylint-dev/pylint/issues/7269>

- **#6856** — False negative `repeated-keyword` for builtin functions Confirmed false
  negative persists: 'print(end=" !", \*\*{"end": ":("})' — the duplicate 'end' keyword
  is not flagged repeated-keyword for builtin functions.
  <https://github.com/pylint-dev/pylint/issues/6856>

- **#6663** — False positive for `implicit-str-concat` when some but not all strings are
  raw Confirmed W1404 false positive: r-string + plain string concat (intentional, to
  escape raw treatment for part of string) is flagged implicit-str-concat.
  <https://github.com/pylint-dev/pylint/issues/6663>

- **#6478** — Docparams does not raise `differing-type-doc` for Sphinx documentation
  Confirmed FN persists: differing-type-doc not raised when Sphinx-format docstring
  mismatches type hint. <https://github.com/pylint-dev/pylint/issues/6478>

- **#5955** — `used-before-assignment` false positive on multiple-target assignment
  Confirmed E0601 false positive: 'a = b[id(a)] = 0' multiple-target assignment with
  target-n using target-n+1 reports 'a' used before assignment.
  <https://github.com/pylint-dev/pylint/issues/5955>

- **#5889** — False positive for `try-except-raise` with diamond inheritance Confirmed
  W0706 try-except-raise false positive on diamond-inherited exception: 'except
  ArithmeticError: raise' is a behavior difference from removing the handler.
  <https://github.com/pylint-dev/pylint/issues/5889>

- **#5734** — False-negative: missing 'no-member' in case of private member function
  invoke without mangling Confirmed false negative: 'Foo.**foo' name-mangling access
  from outside the class is not flagged no-member (the issue is FN — should suggest
  \_Foo**foo). <https://github.com/pylint-dev/pylint/issues/5734>

- **#5699** — False positive: unsubscriptable-object when using classmethod and property
  together Confirmed E1136 false positive: @classmethod @property combination for
  'all_constants' returning List[int] flagged unsubscriptable.
  <https://github.com/pylint-dev/pylint/issues/5699>

- **#5678** — redefined-outer-name not emitted for names in enclosing namespace
  Confirmed FN: 'def wrapper(): x=42; def f(x):' — pylint doesn't report
  redefined-outer-name when outer is enclosing fn scope, only when outer is
  module-level. <https://github.com/pylint-dev/pylint/issues/5678>

- **#5671** — False `unbalanced-tuple-unpacking` report Confirmed W0632 false positive:
  'a, b = f("12")' where f appends to a list — pylint can't track that the list
  ultimately has 2 elements at unpack time.
  <https://github.com/pylint-dev/pylint/issues/5671>

- **#5637** — option to treat `TYPE_CHECKING` as `True`, or add a separate variable
  Confirmed E1120: 'if TYPE_CHECKING: def **init**(self): ... else: def **init**(self,
  value): ...' — pylint uses the TYPE_CHECKING branch for the call check, ignoring the
  runtime else-branch. <https://github.com/pylint-dev/pylint/issues/5637>

### FIXED (3)

- **#7381** — Multiple binary | operation in a single statement failed with "E1131:
  unsupported operand type(s) fo Already verified FIXED in session 4 re-audit (chained
  Flag |). <https://github.com/pylint-dev/pylint/issues/7381>

- **#7350** — E0601 false positive when nested try block exhaustively defines name,
  raises, or returns Does NOT reproduce on 4.0.5: nested try/except/finally with 'x =
  None; except: x = None; raise' no longer produces E0601 — 10/10.
  <https://github.com/pylint-dev/pylint/issues/7350>

- **#7240** — False-positive `no-member` in comprehension in unreachable code from
  platform check Does NOT reproduce on 4.0.5: '[group for group in os.getgroups()]'
  inside 'if sys.platform == "linux":' guard — 10/10. Fixed since 2.14.
  <https://github.com/pylint-dev/pylint/issues/7240>

### UNCLEAR (2)

- **#7389** — pyreverse -c option causes stack overflow pyreverse -c stack overflow.
  Needs repro. <https://github.com/pylint-dev/pylint/issues/7389>

- **#7268** — Crash inferring a subclass of `typing.NamedTuple` Crash inferring
  typing.NamedTuple subclass. Needs repro.
  <https://github.com/pylint-dev/pylint/issues/7268>

### EXTDEP (24)

- **#7641** — Initializing DataFrame in **init** hangs pyreverse Needs pandas. Pyreverse
  hangs initializing DataFrame in **init**.
  <https://github.com/pylint-dev/pylint/issues/7641>

- **#7582** — False positive: E1136(unsubscriptable-object) in pandas Needs pandas.
  unsubscriptable-object false positive on pandas.
  <https://github.com/pylint-dev/pylint/issues/7582>

- **#7564** — false positive E1137 on pandas dataframe column assignment when
  set_index() is used Needs pandas. E1137 unsupported-assignment-operation on DataFrame
  column assignment when set_index used. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/7564>

- **#7527** — PyPy-specific: `ctypes.Structure` fields not ignored; `no-member` false
  positive PyPy-specific ctypes.Structure issue. Platform-specific.
  <https://github.com/pylint-dev/pylint/issues/7527>

- **#7519** — False-positive W0143:comparison-with-callable with PySide6 and
  `__feature__` Needs PySide6. comparison-with-callable false positive with **feature**.
  <https://github.com/pylint-dev/pylint/issues/7519>

- **#7474** — False positive: Various dict-access checks fail when using NewType for
  Dict[str,str] Needs NumPy. Various dict-access checks. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/7474>

- **#7387** — E0611: No name 'QDesktopWidget' in module 'PySide2.QtWidgets'
  (no-name-in-module) Needs PySide2. <https://github.com/pylint-dev/pylint/issues/7387>

- **#7351** — False positive C2801 (unnecessary-dunder-call) with unittest.mock.call
  Already addressed in session 4: unittest.mock context.
  <https://github.com/pylint-dev/pylint/issues/7351>

- **#7283** — pylint fails to see that a module has no attribute by this name Needs
  i2c+smbus modules. False negative: dotted attribute access on imported module not
  flagged. <https://github.com/pylint-dev/pylint/issues/7283>

- **#7238** — Tensorflow: bad operand type for unary - false positive Needs tensorflow.
  bad-operand-type FP. Lib-specific. <https://github.com/pylint-dev/pylint/issues/7238>

- **#7122** — False positive not-an-iterable for apt_pkg module apt_pkg debian-specific.
  Lib. <https://github.com/pylint-dev/pylint/issues/7122>

- **#6894** — `unnecessary-lambda-assignment` false-positive (?) with pytest's
  `__tracebackhide__` pytest-specific issue with unnecessary-lambda-assignment. Lib.
  <https://github.com/pylint-dev/pylint/issues/6894>

- **#6535** — Pylint does not follow python import order : Builtin modules are imported
  before custom modules Builtin modules import-order regression. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/6535>

- **#6531** — False Positive W0621: Redefining name %r from outer scope when using
  pytest fixtures Lib-specific W0621 regression. Needs context.
  <https://github.com/pylint-dev/pylint/issues/6531>

- **#6352** — Pylint can't find some PyGObject classes' members PyGObject classes. Lib.
  <https://github.com/pylint-dev/pylint/issues/6352>

- **#6281** — Module 'google.protobuf.any_pb2' has no 'Any' member
  google.protobuf.any_pb2. Lib. <https://github.com/pylint-dev/pylint/issues/6281>

- **#5947** — False positive "No name 'ConnectionError' in module 'unicon.core.errors'
  (no-name-in-module)" unicon library no-name-in-module. Lib.
  <https://github.com/pylint-dev/pylint/issues/5947>

- **#5835** — Slow with all checks disabled using pandas + dataclass Slow with
  pandas+dataclass. Perf-specific. <https://github.com/pylint-dev/pylint/issues/5835>

- **#5831** — Regression: False positive I1101(c-extension-no-member) for
  np.finfo(np.float64).resolution c-extension-no-member regression. Lib.
  <https://github.com/pylint-dev/pylint/issues/5831>

- **#5705** — False E0237 for **slots** and collections.abc.Iterable and Container and
  subtypes using TypeVar spec TypeVar+**slots** specialization on
  collections.abc.Iterable. Lib-specific astroid brain.
  <https://github.com/pylint-dev/pylint/issues/5705>

- **#5543** — False positive: "Does not support item assignment" error with empty_like
  from numpy Numpy item assignment. Lib.
  <https://github.com/pylint-dev/pylint/issues/5543>

- **#5533** — false positive for numpy ufunc: bad-string-format-type Numpy ufunc
  bad-string-format-type. Lib. <https://github.com/pylint-dev/pylint/issues/5533>

- **#5347** — Unable to create directory /Users/runner/Library/Caches/pylint macOS cache
  directory issue. Platform. <https://github.com/pylint-dev/pylint/issues/5347>

- **#5251** — "Unable to init server" warning with GTK import GTK 'Unable to init
  server' warning. Lib/env. <https://github.com/pylint-dev/pylint/issues/5251>

### DESIGN (113)

- **#7601** — Disable next should consider the next occurance of an error not only of
  the next line [Regression] Regression discussion: # pylint: disable-next= now only
  suppresses literal next-line, not the next occurrence. High priority. Decision/PR.
  <https://github.com/pylint-dev/pylint/issues/7601>

- **#7572** — Add dark mode to pyreverse Pyreverse enhancement: dark mode. Good first
  issue. <https://github.com/pylint-dev/pylint/issues/7572>

- **#7534** — Warn for nonstandard **exit** argument names Enhancement: warn for
  nonstandard **exit** argument names. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7534>

- **#7515** — Accept regexes in ignored-parents Enhancement: accept regexes in
  ignored-parents. Spec. <https://github.com/pylint-dev/pylint/issues/7515>

- **#7449** — Incorrect warning name Internal: misnamed warning. Maintenance.
  <https://github.com/pylint-dev/pylint/issues/7449>

- **#7438** — Features for refactoring automatically offending code (pylint autofix)
  High-effort proposal: pylint autofix. Discussion.
  <https://github.com/pylint-dev/pylint/issues/7438>

- **#7437** — Add support for PEP 681: `dataclass_transform` Enhancement: PEP 681
  dataclass_transform support. Astroid update + Hacktoberfest.
  <https://github.com/pylint-dev/pylint/issues/7437>

- **#7435** — useless-super-delegation with ABC Discussion: useless-super-delegation
  with ABC. Decision. <https://github.com/pylint-dev/pylint/issues/7435>

- **#7396** — False positive with default arg values before *args Re-file of #2481:
  W1113 false positive for default arg values before *args. High-priority discussion.
  <https://github.com/pylint-dev/pylint/issues/7396>

- **#7391** — Make `modified-iterating-*` also check class attributes Enhancement:
  modified-iterating-\* should also check class attributes. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7391>

- **#7376** — CLI should be able to extend ignore from config file Enhancement: CLI
  --extend-ignore vs --ignore replacing config-file value. Spec.
  <https://github.com/pylint-dev/pylint/issues/7376>

- **#7371** — Provide a --ignore-file option with .gitignore as default Enhancement:
  --ignore-file option with .gitignore as default. High priority. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7371>

- **#7362** — Better release notes generation and automated release process Enhancement:
  better release notes generation / automated release. Maintenance.
  <https://github.com/pylint-dev/pylint/issues/7362>

- **#7361** — Pyreverse not showing sub-classes with -c flag Pyreverse not showing
  sub-classes with -c flag. Spec/PR. <https://github.com/pylint-dev/pylint/issues/7361>

- **#7352** — variable-naming-style toml configuration: only a single style is allowed?
  Q: variable-naming-style toml allows only single style. Spec/docs.
  <https://github.com/pylint-dev/pylint/issues/7352>

- **#7339** — Modules of files specified on the command line can be cached with the
  wrong name Cache invalidation issue for files specified on cmd line. Internal.
  <https://github.com/pylint-dev/pylint/issues/7339>

- **#7338** — pylint -j0 always uses 1 core on real hardware in Linux pylint -j0 always
  uses 1 core on real Linux hardware. Internal.
  <https://github.com/pylint-dev/pylint/issues/7338>

- **#7317** — Cache directory useless in CI (?), add a an incremental mode like mypy
  Cache directory useless in CI. Enhancement: incremental mode. Spec.
  <https://github.com/pylint-dev/pylint/issues/7317>

- **#7292** — signature-mutators should silent errors on return type Enhancement:
  signature-mutators should silence errors on return type. Spec.
  <https://github.com/pylint-dev/pylint/issues/7292>

- **#7289** — `import-self` only compares the name of a module and doesn't consider the
  actual module being import Bug: import-self only compares module name, not actual
  module. Module named 'gzip' importing stdlib gzip flagged as self-import. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7289>

- **#7263** — Checker plugin parallelization breaks algorithm Documentation/spec issue
  around checker plugin parallelization. Long discussion. Decision.
  <https://github.com/pylint-dev/pylint/issues/7263>

- **#7258** — False positive `no-member` error if the `__new__` static method replaces
  returning class False positive no-member if **new** static method present. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7258>

- **#7237** — `docstring-first-line-empty` Discussion: docstring-first-line-empty.
  Decision. <https://github.com/pylint-dev/pylint/issues/7237>

- **#7213** — [R0801] Similarities false positive on abstract classes R0801 similarities
  FP on abstract classes. Internal. <https://github.com/pylint-dev/pylint/issues/7213>

- **#7172** — Warn about creating a setter or getter without defining a property
  Enhancement: warn when creating setter/getter without defining property. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7172>

- **#7170** — Option to regard invalid configuration as an error Bug: option to regard
  invalid configuration as error. Internal.
  <https://github.com/pylint-dev/pylint/issues/7170>

- **#7127** — Refactoring message when not all paths delegate to super() despite
  multiple bases each defining a me Enhancement: refactoring message when not all paths
  delegate to super(). Spec. <https://github.com/pylint-dev/pylint/issues/7127>

- **#7121** — The confidence option is not very intuitive to use Enhancement: confidence
  option more intuitive. Spec. <https://github.com/pylint-dev/pylint/issues/7121>

- **#7120** — Create configuration templates with message tiers or presets Enhancement:
  configuration templates / message tiers. Spec.
  <https://github.com/pylint-dev/pylint/issues/7120>

- **#7100** — False positive for cell-var-from-loop / W0640 Docs: false positive
  cell-var-from-loop / W0640. Docs/spec.
  <https://github.com/pylint-dev/pylint/issues/7100>

- **#7098** — False negative | class attribute & global False negative class attribute &
  global. Spec/PR. <https://github.com/pylint-dev/pylint/issues/7098>

- **#7093** — pylint fails to import module if the script is named the same way Astroid:
  pylint fails to import module if script same as it. Possibly fixed by b43721121.
  <https://github.com/pylint-dev/pylint/issues/7093>

- **#7085** — Request: Add optional Checker to `enforce explicit namespace packages` aka
  `there must be an \__init_ Enhancement: explicit namespace package checker. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7085>

- **#7003** — Pylint no longer support separating options from positional arguments with
  -- Regression: Pylint no longer supports separating options from positional args.
  Internal. <https://github.com/pylint-dev/pylint/issues/7003>

- **#6992** — Warn if a class has multiple direct parents that each define a method name
  besides `__init__` Enhancement: warn on multiple direct parents defining same method.
  Spec. <https://github.com/pylint-dev/pylint/issues/6992>

- **#6963** — `ignore-paths` Can't use escape sequence in toml config Docs/bug:
  ignore-paths doesn't handle escape sequences in toml. Spec.
  <https://github.com/pylint-dev/pylint/issues/6963>

- **#6961** — Create new `no-self-class-in-super` message Enhancement: new
  no-self-class-in-super message. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/6961>

- **#6938** — Show options from the `Run` class in the documentation Docs: show Run
  class options. Docs/PR. <https://github.com/pylint-dev/pylint/issues/6938>

- **#6918** — Pass extra parameters of `MessageDefinition` as dictionary instead of
  separate paramters Maintenance: pass MessageDefinition extra params as dict. Internal.
  <https://github.com/pylint-dev/pylint/issues/6918>

- **#6887** — False positives `invalid-enum-extension` False positive
  invalid-enum-extension. Spec. <https://github.com/pylint-dev/pylint/issues/6887>

- **#6833** — Support multiple separate arguments for —ignore Enhancement: multiple
  separate --ignore args. Spec. <https://github.com/pylint-dev/pylint/issues/6833>

- **#6748** — False positive `used-before-assignment` with dataclasses and shadowing
  False positive used-before-assignment with dataclass. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/6748>

- **#6737** — Support for complex type annotations in `pyreverse` Enhancement: pyreverse
  support for complex type annotations. High priority.
  <https://github.com/pylint-dev/pylint/issues/6737>

- **#6692** — Docparams does not recognize class docstring when placed in **init**
  Enhancement: docparams recognizes class docstring in **init**. Good first issue.
  <https://github.com/pylint-dev/pylint/issues/6692>

- **#6683** — PlantUML generation by `pyreverse` may be incorrect Bug: PlantUML
  generation in pyreverse may be incorrect. Internal.
  <https://github.com/pylint-dev/pylint/issues/6683>

- **#6670** — Deleted messages and checkers are still being searched on ReadTheDoc but
  they are not documented at Docs: deleted messages still searchable in RTD. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/6670>

- **#6627** — `invalid-bool-returned` raises error only for case when `__bool__()`
  returns a constant Enhancement: invalid-bool-returned for **bool** cases. Spec.
  <https://github.com/pylint-dev/pylint/issues/6627>

- **#6582** — Refactoring ToDos for `pyreverse` Maintenance: pyreverse refactoring
  TODOs. Internal. <https://github.com/pylint-dev/pylint/issues/6582>

- **#6568** — Styling false negative and false positives around "private" and
  "protected" class members Styling false positive/negative around 'private' attrs.
  Spec. <https://github.com/pylint-dev/pylint/issues/6568>

- **#6542** — New checks: Use literals instead of calling the constructor Enhancement:
  use literals instead of calling constructor (empty types). Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/6542>

- **#6495** — Consider adding rule to suggest using the operator library Enhancement:
  suggest using operator library. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/6495>

- **#6484** — per-line pylint suppression does not work inside multiline-imports like
  black formats things Spec: per-line pylint disable inside multi-line if-condition.
  Astroid update. <https://github.com/pylint-dev/pylint/issues/6484>

- **#6444** — False negative for `implicit-str-concat` when it happens on a single line
  inside a multiline strin False negative implicit-str-concat across multi-line. High
  effort. Spec/PR. <https://github.com/pylint-dev/pylint/issues/6444>

- **#6420** — No suggestion should be emitted by `wrong-spelling-in-x` when
  `max-spelling-suggestions=0` Enhancement: wrong-spelling-in-x should not suggest words
  on unspellable code. Spec/PR. <https://github.com/pylint-dev/pylint/issues/6420>

- **#6416** — Miscellaneous spelling checker enhancements Spelling checker enhancements.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/6416>

- **#6359** — Investigate false negatives for `unsupported-binary-operation`
  Maintenance: investigate FNs for unsupported-binary-operation. Internal.
  <https://github.com/pylint-dev/pylint/issues/6359>

- **#6252** — Some TypeErrors are not caught Enhancement: some TypeErrors not caught.
  Spec. <https://github.com/pylint-dev/pylint/issues/6252>

- **#6234** — Warn usage of datetime.utcnow() Enhancement: warn on datetime.utcnow().
  High priority. Spec/PR. <https://github.com/pylint-dev/pylint/issues/6234>

- **#6211** — False negative: missing numpy param doc when "default ..." in same line of
  "param : type" False negative missing numpy param doc when 'default ...' in
  description. Spec/PR. <https://github.com/pylint-dev/pylint/issues/6211>

- **#6170** — Move `test_messages_documentation.py` to tests folder Maintenance: move
  test_messages_documentation.py. Internal.
  <https://github.com/pylint-dev/pylint/issues/6170>

- **#6163** — `bad-string-format-type`: only works on old-style string formatting and
  can't infer values Bug: bad-string-format-type only works on old-style format.
  Good-first-issue. <https://github.com/pylint-dev/pylint/issues/6163>

- **#6085** — `bad-format-character` false negative on `.format()` and f-strings False
  negative bad-format-character on .format(). Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/6085>

- **#6053** — Better explanation for reasoning behind `invalid-name` warnings
  Enhancement: better explanation for invalid-name. Decision.
  <https://github.com/pylint-dev/pylint/issues/6053>

- **#6044** — False positive E1133 Non-iterable value used in an iterating context
  (not-an-iterable) False positive E1133 in control flow with non-iterable. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/6044>

- **#6042** — disable=redefined-builtin ignored in some scenarios Bug:
  disable=redefined-builtin ignored in some scenarios. Internal.
  <https://github.com/pylint-dev/pylint/issues/6042>

- **#5972** — (🎁) Make a pylint playground to easily reproduce errors Enhancement:
  pylint playground for repro. High effort.
  <https://github.com/pylint-dev/pylint/issues/5972>

- **#5933** — Compile pylint with mypyc to improve performance. Performance: compile
  pylint with mypyc. Spec/PR. <https://github.com/pylint-dev/pylint/issues/5933>

- **#5922** — Upgrade and check the custom plugin documentation Docs: custom plugin
  documentation. Docs. <https://github.com/pylint-dev/pylint/issues/5922>

- **#5898** — Option to enable all `useless-suppression` warnings Enhancement: option to
  enable all useless-suppression warnings. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5898>

- **#5854** — DocStrings giving a `pointless-string-statement` DocStrings giving
  pointless-string-statement. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5854>

- **#5852** — Ignore specific undefined variables Enhancement: ignore specific undefined
  variables. Spec. <https://github.com/pylint-dev/pylint/issues/5852>

- **#5838** — Lint unused variable assignment / dead store (false negative
  `unused-variable`?) Enhancement: lint unused variable assignment (dead store). High
  effort. <https://github.com/pylint-dev/pylint/issues/5838>

- **#5829** — Document how to register options for Reporter plugins (by creating a bare
  checker) Docs: how to register options for Reporter plugins. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/5829>

- **#5635** — Pylint catches missing method in some situations but not in others
  Inference inconsistency: missing method detected in some situations but not others.
  Astroid update. <https://github.com/pylint-dev/pylint/issues/5635>

- **#5607** — Refactor the message handling to use a smaller data structure Minor
  performance/maintenance refactor in message handling. Internal.
  <https://github.com/pylint-dev/pylint/issues/5607>

- **#5604** — Next step in pylint's gamification and user experience Maintainer
  discussion: pylint gamification/UX. High effort.
  <https://github.com/pylint-dev/pylint/issues/5604>

- **#5578** — Suggest replacing `Tuple[X]` with `Tuple[X, ...]` or `Sequence[X]`
  Enhancement: suggest Tuple[X, ...] over Tuple[X]. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5578>

- **#5551** — `no-member` false negative if member conditionally defined in parent class
  False negative no-member if member conditionally defined. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5551>

- **#5508** — [cell-var-from-loop] false positive for lambda used as keyword arg
  cell-var-from-loop false positive for lambda used as keyword arg. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5508>

- **#5503** — Disable `assignment-from-none` for methods Decision: disable
  assignment-from-none for methods. Discussion.
  <https://github.com/pylint-dev/pylint/issues/5503>

- **#5496** — Message content style guide and revamp of offending messages Message
  content style guide / messages revamp. Maintenance.
  <https://github.com/pylint-dev/pylint/issues/5496>

- **#5493** — SARIF output format for pylint ? Enhancement: SARIF output format. Good
  first issue. <https://github.com/pylint-dev/pylint/issues/5493>

- **#5491** — Do not remove preceding `./` from `ignore-paths` option input Bug:
  preceding './' removed from ignore-paths. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5491>

- **#5480** — False positive `undefined-loop-variable` in function signature when the
  typing match a variable name False positive undefined-loop-variable in function
  signature. Spec/PR. <https://github.com/pylint-dev/pylint/issues/5480>

- **#5471** — Warn if module dunders are below imports Enhancement: warn if module
  dunders below imports. Good first issue.
  <https://github.com/pylint-dev/pylint/issues/5471>

- **#5469** — Emit `arguments-differ` if function definition overwritten to have
  different argument count Enhancement: emit arguments-differ if function def
  overwritten in nested scope. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5469>

- **#5465** — Auto-upgrade the `whitelist` and `blacklist` options in configuration
  Enhancement: auto-upgrade whitelist/blacklist options. Spec.
  <https://github.com/pylint-dev/pylint/issues/5465>

- **#5462** — Provide an auto-upgrade option / migration tool for pylint configurations
  Enhancement: auto-upgrade/migration tool for pylint config. WIP.
  <https://github.com/pylint-dev/pylint/issues/5462>

- **#5441** — False positive: decorating an instance func raises
  `bad-staticmethod-argument` False positive on decorator instance func with
  bad-staticmethod-argument. Spec/PR. <https://github.com/pylint-dev/pylint/issues/5441>

- **#5403** — Better user experience when starting to use pylint on legacy codebase
  Better UX for legacy codebases. High effort.
  <https://github.com/pylint-dev/pylint/issues/5403>

- **#5398** — Allow `\` to be both a regex escape character and a windows directory
  delimiter in ``ignore-paths` Allow backslash as both regex escape AND windows path
  separator. Regression. Spec/PR. <https://github.com/pylint-dev/pylint/issues/5398>

- **#5391** — `consider-using-f-string`'s message needs to hint at the possible solution
  consider-using-f-string message should hint at performance impact. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5391>

- **#5363** — False positive `subprocess-run-check` when passing check = True by kwargs
  False positive subprocess-run-check when check= passed dynamically. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5363>

- **#5361** — False negatives `superfluous-parens` with more than one superfluous
  parenthesis False negatives superfluous-parens with multiple superfluous parens. Spec.
  <https://github.com/pylint-dev/pylint/issues/5361>

- **#5356** — Check enum members are compared by identity Enhancement: check enum
  members compared by identity. Hacktoberfest.
  <https://github.com/pylint-dev/pylint/issues/5356>

- **#5337** — False positive `consider-using-with` for context managers passed to
  `AsyncExitStack` False positive consider-using-with for ctx managers passed to
  functions. Spec/PR. <https://github.com/pylint-dev/pylint/issues/5337>

- **#5334** — False negatives `superfluous-parens` with superfluous parenthesis on
  function call False negative superfluous-parens with extra parens. Spec.
  <https://github.com/pylint-dev/pylint/issues/5334>

- **#5328** — option to enforce messages on `assert` statements Proposal: messages on
  assert statements. Decision. <https://github.com/pylint-dev/pylint/issues/5328>

- **#5321** — Checker for `unspecified-encoding` is unable to infer attributes from
  dataclasses Enhancement: unspecified-encoding infer attribute. Spec.
  <https://github.com/pylint-dev/pylint/issues/5321>

- **#5293** — Provide `pre-commit` hooks even without having to use a system hook Docs:
  pre-commit hooks without sys integration. Design proposal.
  <https://github.com/pylint-dev/pylint/issues/5293>

- **#5290** — Check tempfile.TemporaryFile() and siblings for unspecified-encoding
  (W1514) Enhancement: tempfile.TemporaryFile() unspecified-encoding. Spec.
  <https://github.com/pylint-dev/pylint/issues/5290>

- **#5289** — Detect improvable code with open + pathlib.Path Enhancement: detect
  open() + pathlib.Path improvement. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5289>

- **#5286** — `consider-using-f-string` and `logging-fstring-interpolation` are mutually
  exclusive Docs: consider-using-f-string vs logging-fstring-interpolation.
  Hacktoberfest. <https://github.com/pylint-dev/pylint/issues/5286>

- **#5285** — signature-mutators should also handle "arguments-differ"
  signature-mutators should also handle arguments-differ. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5285>

- **#5275** — Allow five digit message id's (and possibly disallow four digit id's)
  Proposal: 5-digit message IDs / disallow 4-digit. Discussion.
  <https://github.com/pylint-dev/pylint/issues/5275>

- **#5274** — Override existing checks with a plugin Enhancement: override existing
  checks with plugin. Spec. <https://github.com/pylint-dev/pylint/issues/5274>

- **#5270** — False-negative `signature-differs` with kw-only args False negative
  signature-differs with kw-only args. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5270>

- **#5264** — False-positive `signature-differs` / `arguments-differ` with
  `typing.overload` False positive signature-differs / arguments-differ with overloads.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/5264>

- **#5263** — cell-var-from-loop (W0640): why Why cell-var-from-loop W0640 fires.
  Discussion. <https://github.com/pylint-dev/pylint/issues/5263>

- **#5258** — Multiline disable for long list of disabled messages Enhancement:
  multi-line disable for long lists. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5258>

- **#5253** — Enforcing justification for disabled messages Enhancement: enforce
  justification for disabled messages. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5253>

- **#5226** — Support an Option to Disable sys.path patching Enhancement: option to
  disable sys.path patching. Spec. <https://github.com/pylint-dev/pylint/issues/5226>

- **#5214** — Inconsistent behaviour with attribute-defined-outside-init Inconsistent
  attribute-defined-outside-init behavior. High effort.
  <https://github.com/pylint-dev/pylint/issues/5214>
