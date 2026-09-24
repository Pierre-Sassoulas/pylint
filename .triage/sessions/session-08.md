# Session 08 — Triage Notes (re-audited)

**Issues triaged this session:** 75

**Re-audit on pylint 4.0.5 / astroid 4.0.2.**

**Verdict tally:**

- REPRO: 12
- FIXED: 3
- UNCLEAR: 1
- EXTDEP: 20
- DESIGN: 39

## By verdict

### REPRO (12)

- **#4070** — False positive no-member for NamedTuple.\_replace() Confirmed E1101:
  'self.\_replace(...)' on NamedTuple subclass not recognized. astroid NamedTuple brain
  doesn't expose \_replace via subclass.
  <https://github.com/pylint-dev/pylint/issues/4070>

- **#4066** — False positive used-before-assignment for return type Confirmed E0601
  false positive: 'def foo(self) -> bool:' inside class with later 'def bool(self) ->
  bool' method — return annotation 'bool' confused with sibling method.
  <https://github.com/pylint-dev/pylint/issues/4066>

- **#4033** — Initializer arguments not checked when raising exception with implicit
  instantiation. Confirmed: 'raise Bang' (without instantiation) still doesn't check
  **init** args. False negative for implicit exception instantiation.
  <https://github.com/pylint-dev/pylint/issues/4033>

- **#4018** — disable=unexpected-keyword-arg doesn't work when placed on line where
  keyword is specified Confirmed: 'c=3 # pylint: disable=unexpected-keyword-arg' on the
  kwarg line doesn't suppress E1123 (raised on the open-paren line). Plus I0021
  useless-suppression false positive. <https://github.com/pylint-dev/pylint/issues/4018>

- **#3957** — Attributes added by a decorator are raised as missing members errors
  Confirmed E1101: @functools.wraps decorator returning a NamedTuple-wrapped instance
  loses inferred type — 'mod.init' and 'mod.apply' flagged no-member.
  <https://github.com/pylint-dev/pylint/issues/3957>

- **#3879** — False positive no-member when accessing a mangled instance variable of a
  super class after calling t Confirmed E1101: 'TestSub().\_Test\_\_test' (private
  name-mangling access from outside) flagged no-member even though attribute exists at
  runtime. <https://github.com/pylint-dev/pylint/issues/3879>

- **#3745** — False positive method-hidden in overridden methods Confirmed E0202
  method-hidden false positive: Extended.func defined while Base.**init** sets
  self.func=func — but Extended overrides **init** to NOT call super, so no actual
  conflict. <https://github.com/pylint-dev/pylint/issues/3745>

- **#3728** — False positive no-member with sys.stdin.buffer.peek() Confirmed E1101:
  'sys.stdin.buffer.peek(16)' flagged no-member. astroid wrongly types stdin.buffer as
  BufferedWriter instead of BufferedReader.
  <https://github.com/pylint-dev/pylint/issues/3728>

- **#3668** — False-positive unneeded-not when comparing dict views Confirmed C0117
  unneeded-not false positive: 'not {}.items() <= {}.items()' rewriting to '>' changes
  meaning for set-like dict views. <https://github.com/pylint-dev/pylint/issues/3668>

- **#3641** — False negative `undefined-variable` for decorators in multiple scenario
  Confirmed but with different message: '@x.getter' in subclass B(A) where x is property
  on A — pylint flags W0236 invalid-overridden-method instead of expected
  undefined-variable. Either way the bug surfaces.
  <https://github.com/pylint-dev/pylint/issues/3641>

- **#3586** — false positive: E1111 assignment-from-no-return when using function name
  "lazy" Confirmed E1111 false positive: function named 'lazy' as decorator triggers
  assignment-from-no-return; renaming the function (e.g. 'lazy2') fixes it. astroid
  name-based heuristic confuses 'lazy' specifically.
  <https://github.com/pylint-dev/pylint/issues/3586>

- **#3367** — Unexpected suppression of line-too-long messages Confirmed I0021
  useless-suppression false positive: '# pylint: disable=line-too-long' on a short line
  raises useless-suppression even when intentional.
  <https://github.com/pylint-dev/pylint/issues/3367>

### FIXED (3)

- **#3925** — False positive not-callable after destructuring Does NOT reproduce on
  4.0.5: 'self.f1, self.f2 = f or (None, None)' destructuring no longer triggers E1102 —
  10/10. Fixed since 2.6. <https://github.com/pylint-dev/pylint/issues/3925>

- **#3893** — False positive for E1123 (unexpected-keyword-arg) Does NOT reproduce on
  4.0.5: 'for g in [PV1Axis, Wind]: if g == Wind: g(..., delimiter=...)' no longer flags
  E1123 — 10/10. Fixed since 2.6. <https://github.com/pylint-dev/pylint/issues/3893>

- **#3603** — False unexpected-keyword-arg for classes defined differently in branches.
  Does NOT reproduce on 4.0.5: 'if str is bytes: class C(a)\nelse: class C(a, b)\nC(1,
  b=2)' no longer raises E1123 — 10/10. Fixed since 2.6.
  <https://github.com/pylint-dev/pylint/issues/3603>

### UNCLEAR (1)

- **#3602** — Maximum recursion depth crash with pyreverse `-S` option Pyreverse -S
  stack overflow. No minimal repro. <https://github.com/pylint-dev/pylint/issues/3602>

### EXTDEP (20)

- **#4047** — Inference information are lost depending on code structure Needs
  temppathlib. control-flow narrowing test.
  <https://github.com/pylint-dev/pylint/issues/4047>

- **#3984** — False positive import-error Needs the empty **init**.py + a.py / b.py
  layout. Real but env-specific. <https://github.com/pylint-dev/pylint/issues/3984>

- **#3955** — SQLAlchemy Declared Attribute: comparison-with-callable Needs SQLAlchemy.
  comparison-with-callable on declared_attr. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/3955>

- **#3933** — W0406: Module import itself (import-self) in **init**.py Needs
  settings/**init**.py + base.py + local.py layout. False import-self with try/except
  ImportError pattern. <https://github.com/pylint-dev/pylint/issues/3933>

- **#3911** — false positive unused-argument overriding
  rest_framework.generics.RetrieveUpdateAPIView.update metho Needs rest_framework.
  unused-argument FP on generics. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/3911>

- **#3903** — Recognize variable references in DataFrame.query as such Needs pandas.
  DataFrame.query reference recognition. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/3903>

- **#3832** — false positive E1137 with optional list Optional[List] iter pattern.
  Complex control-flow analysis. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3832>

- **#3804** — SQLAlchemy @hybrid_property.expression has "no-self-argument" Needs
  SQLAlchemy hybrid_property.expression. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/3804>

- **#3801** — Function on attrs object mistaken for bound method Needs attrs lib.
  <https://github.com/pylint-dev/pylint/issues/3801>

- **#3744** — false positive [E1101(no-member)] Module 'scipy.special' has no 'erfinv'
  member Needs scipy.special. Lib. <https://github.com/pylint-dev/pylint/issues/3744>

- **#3734** — pandas MultiIndex levels is unsubscriptable? Needs pandas.
  MultiIndex.levels unsubscriptable. Lib.
  <https://github.com/pylint-dev/pylint/issues/3734>

- **#3662** — kwargs used by decorator being flagged as unused. Needs Marshmallow lib.
  <https://github.com/pylint-dev/pylint/issues/3662>

- **#3637** — Incorrect 'unsubscriptable-object' reported Needs statsmodels.
  Lib-specific unsubscriptable-object.
  <https://github.com/pylint-dev/pylint/issues/3637>

- **#3556** — syntax-error incorectly detected inside a type-comment with python 3.8
  Needs SQLAlchemy. type-comment syntax-error in Python 3.8 with sqlalchemy-stubs.
  Astroid update. <https://github.com/pylint-dev/pylint/issues/3556>

- **#3531** — no-member reported when accessing a @property of parent class @property of
  parent class. Needs reporter context.
  <https://github.com/pylint-dev/pylint/issues/3531>

- **#3492** — False positive on arguments of constructor created by "attrs" Needs attrs
  lib. <https://github.com/pylint-dev/pylint/issues/3492>

- **#3488** — Typing: Value 'Queue' is unsubscriptablepylint(unsubscriptable-object)
  Lib-specific Queue unsubscriptable. Needs repro context.
  <https://github.com/pylint-dev/pylint/issues/3488>

- **#3484** — using-constant-test triggers on a property when using unknown property
  decorators Needs cached_property lib for unknown property decorator.
  <https://github.com/pylint-dev/pylint/issues/3484>

- **#3348** — Importing FMT_BINARY from plistlib yields no-name-in-module plistlib
  FMT_BINARY. Stdlib brain. <https://github.com/pylint-dev/pylint/issues/3348>

- **#3334** — Incorrect E1101 (no-member) using SQLAlchemy @hybrid_property Needs
  SQLAlchemy. @hybrid_property. Lib. <https://github.com/pylint-dev/pylint/issues/3334>

### DESIGN (39)

- **#4048** — False-negative E1101 no-member for function parameter FN persists:
  no-member not raised when accessing attribute on a parameter with default=True (bool
  literal). Hard to do safely. <https://github.com/pylint-dev/pylint/issues/4048>

- **#4043** — spelling: ignore lines via regex (copyright headers) Enhancement: spelling
  extension ignore lines via regex (copyright headers). Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4043>

- **#4002** — Raising len-as-conditions when using len on function returning generators
  or list comprehensions Enhancement: len-as-conditions for
  generator/comprehension-returning functions. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/4002>

- **#3995** — Take the `FORCE_COLOR` and `NO_COLOR` environnement variables into account
  Enhancement: respect FORCE_COLOR / NO_COLOR env vars. Spec.
  <https://github.com/pylint-dev/pylint/issues/3995>

- **#3945** — Inline disable comments conflicts with `--disable=W` CLI argument Bug:
  inline disable comment with --disable=W CLI arg interaction. Internal.
  <https://github.com/pylint-dev/pylint/issues/3945>

- **#3944** — Implicit namespace package is not linted if it is inside a regular package
  Implicit namespace package not linted if inside regular dir. Astroid + import system.
  <https://github.com/pylint-dev/pylint/issues/3944>

- **#3888** — Block level disable comments depend on function formatting Bug:
  block-level disable scope depends on function formatting. Internal pragma scoping
  issue. <https://github.com/pylint-dev/pylint/issues/3888>

- **#3857** — f-string-without-interpolation false negative (concatenation) False
  negative f-string-without-interpolation on concatenation 'f"foo" f"{x}"' — still not
  flagged. Spec/PR. <https://github.com/pylint-dev/pylint/issues/3857>

- **#3853** — Have a way to require type annotations Enhancement: way to require type
  annotations. High priority spec. <https://github.com/pylint-dev/pylint/issues/3853>

- **#3843** — The similar checker will append the same stream in some weird reason
  Similar checker streams append weird. Internal investigation.
  <https://github.com/pylint-dev/pylint/issues/3843>

- **#3808** — False positive `unnecessary-lambda` for function that are not pure (like
  datetime or timedelta) False positive unnecessary-lambda for impure functions
  (datetime/random). Spec/PR. <https://github.com/pylint-dev/pylint/issues/3808>

- **#3767** — Add different configuration for different files Enhancement: per-file
  config. High effort spec. <https://github.com/pylint-dev/pylint/issues/3767>

- **#3758** — signature-mutators doesn't seem to work Bug: signature-mutators doesn't
  seem to work. Internal. <https://github.com/pylint-dev/pylint/issues/3758>

- **#3757** — False positive `syntax-error` for badly placed type annotations Bug:
  syntax-error inside type-comment with Python 3.8. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/3757>

- **#3756** — Cannot disable cell-var-from-loop on a splitted line when var was used
  before Bug: cell-var-from-loop disable on splitted line. Spec.
  <https://github.com/pylint-dev/pylint/issues/3756>

- **#3748** — `import-self` false positive when importing non-existing module from
  current package False positive import-self when importing non-existing module (should
  be import-error). Spec/PR. <https://github.com/pylint-dev/pylint/issues/3748>

- **#3732** — do not report too-few-public-methods for `attr.s`, `attr.dataclass`,
  `typing.NamedTuple` and similar Enhancement: don't report too-few-public-methods for
  attrs/dataclass. Hacktoberfest, high priority.
  <https://github.com/pylint-dev/pylint/issues/3732>

- **#3717** — Make floating point numbers look like numbers, not abbreviations
  Enhancement: friendlier float number representation. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3717>

- **#3716** — False negative `dangerous-default-value` when `typing.NamedTuple` uses
  mutable defaults False negative dangerous-default-value with typing.NamedTuple.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/3716>

- **#3705** — False positive `no-self-use` when a method defines a sub-class that itself
  does not use `self` in a False positive no-self-use when method defines inner class.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/3705>

- **#3693** — Could we define and add an IDE mode for Python checkers ? Enhancement: IDE
  mode for checkers. Docs/design proposal.
  <https://github.com/pylint-dev/pylint/issues/3693>

- **#3678** — Feature request: Check use of deprecated exception classes like IOError
  Enhancement: detect use of deprecated exception classes. Hacktoberfest.
  <https://github.com/pylint-dev/pylint/issues/3678>

- **#3663** — package.**path** has incorrect type for namespace packages Bug:
  package.**path** has incorrect type for namespace packages. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/3663>

- **#3656** — False negative `bare-except` if the except re-raises Enhancement:
  bare-except should fire even if except re-raises. Decision.
  <https://github.com/pylint-dev/pylint/issues/3656>

- **#3628** — Example in module docstring of epylint fails since 2.5.x Bug: epylint
  module docstring example fails since 2.5.x. Internal.
  <https://github.com/pylint-dev/pylint/issues/3628>

- **#3620** — called code side effect Bug: 'called code side effect' — vague. Internal
  investigation. <https://github.com/pylint-dev/pylint/issues/3620>

- **#3609** — relative imports of modules in namespace packages (without **init**.py)
  Bug: relative imports in namespace packages (no **init**). Import system.
  <https://github.com/pylint-dev/pylint/issues/3609>

- **#3587** — import-self / no-member not emitted for modules named after stdlib modules
  import-self / no-member not emitted for modules named after stdlib. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3587>

- **#3512** — Disable certain messages by default Maintenance: disable certain messages
  by default. Decision. <https://github.com/pylint-dev/pylint/issues/3512>

- **#3506** — False negative for uninitialized variable usage in negative comprehensions
  False negative used-before-assignment in negative comprehensions: '[x for x in
  range(10) if y % 2 == 0 for y in range(x)]' — semantic order. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3506>

- **#3502** — no need to complain 'attribute-defined-outside-init' when base class not
  in same file as sub class False positive attribute-defined-outside-init when base
  class assigned in init. Hacktoberfest.
  <https://github.com/pylint-dev/pylint/issues/3502>

- **#3471** — Redeclared names without usage rule Enhancement: redeclared names without
  usage rule. Hacktoberfest. <https://github.com/pylint-dev/pylint/issues/3471>

- **#3436** — Per-file enable does not work for C (convention) messages Bug: per-file
  enable doesn't work for C messages. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3436>

- **#3420** — False warning when combining parameters in numpy style doctring False
  warning combining parameters in numpy docstring. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3420>

- **#3418** — Warn when code makes use of field named with "unused*" or "ignored*"
  prefix. Enhancement: warn on use of fields named 'unused*\*' or 'ignored*\*'. Spec.
  <https://github.com/pylint-dev/pylint/issues/3418>

- **#3408** — Autoformatter integration: Stop no line-too-long errors that your
  formatter cannot fix, etc. Enhancement: autoformatter integration for line-too-long.
  High effort. <https://github.com/pylint-dev/pylint/issues/3408>

- **#3390** — Support pragma rule "parameters" for narrower disables Enhancement: pragma
  rule for narrower disable scopes (parameter-level). Spec.
  <https://github.com/pylint-dev/pylint/issues/3390>

- **#3339** — Attributes set in metaclass reported `no-member` False positive no-member
  for attrs set in metaclass. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/3339>

- **#3338** — Make the verbose mode more talkative Enhancement: more verbose --verbose
  output. Spec. <https://github.com/pylint-dev/pylint/issues/3338>
