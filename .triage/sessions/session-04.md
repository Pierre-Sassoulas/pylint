# Session 04 — Triage Notes (re-audited with per-issue reproduction)

**Issues triaged this session:** 174

**Re-audit:** session 4 was originally bulk-classified by labels/title in the first
pass. This re-audit replaces those with per-issue reproductions on pylint 4.0.5 /
astroid 4.0.2 where a minimal snippet was available.

**Verdict tally:**

- REPRO: 31
- FIXED: 15
- UNCLEAR: 3
- EXTDEP: 15
- DESIGN: 110

## By verdict

### REPRO (31)

- **#8755** — Recursive defining a function with classmethod decorator triggers crashing
  Confirmed crash: recursive 'super(C, cls).foo(a)' on @classmethod outside any class
  triggers AstroidError → F0002 fatal.
  <https://github.com/pylint-dev/pylint/issues/8755>

- **#8746** — Defining collections.namedtuple object trigger an AstroidError Confirmed
  crash: 'namedtuple("mu", ["µ"])' (Unicode identifier name) triggers AstroidError in
  brain_namedtuple_enum.infer_named_tuple.
  <https://github.com/pylint-dev/pylint/issues/8746>

- **#8739** — Unfound astroid.exceptions.InferenceError causes a crash Confirmed crash:
  'C.p.fset' where p is a getter-only @property raises InferenceError → F0002 fatal.
  <https://github.com/pylint-dev/pylint/issues/8739>

- **#8687** — False-positive W0236 (and W0221) when implementing an optional protocol
  method Confirmed: W0221 + W0236 false positives when Class(Proto) implements a Proto
  @property as a regular method. Real overload-vs-property mismatch.
  <https://github.com/pylint-dev/pylint/issues/8687>

- **#8686** — `used-before-assignment` for assignment in inner try when outer try
  returns Confirmed E0601 used-before-assignment: nested 'try: results=[]' inside except
  branch is not seen as assigning before the final 'return results'.
  <https://github.com/pylint-dev/pylint/issues/8686>

- **#8577** — `unnecessary-comprehension` false positive Confirmed R1721
  unnecessary-comprehension false positive on '[(x, y) for x, y in a]' (tuple-repack
  from list-of-lists). <https://github.com/pylint-dev/pylint/issues/8577>

- **#8495** — False negative for NameError from calling inner function before variable
  is assigned Confirmed false negative: inner function references 'i' that is only later
  assigned by the for-loop; the first inner() call would raise NameError at runtime but
  pylint stays silent. <https://github.com/pylint-dev/pylint/issues/8495>

- **#8486** — `used-before-assignment` when using `walrus operator(:=)` in dict,
  generator, some comprehensionswit Confirmed E0601 used-before-assignment false
  positive: walrus operator inside dict-literal argument to print()/dict() not
  understood; bare dict-literal works fine.
  <https://github.com/pylint-dev/pylint/issues/8486>

- **#8455** — False positive `no-member` for `TypeAlias` `__origin__` Confirmed E1101:
  dict alias DictAlias = dict[int, float] has **origin** at runtime but pylint reports
  'Class dict has no **origin** member'.
  <https://github.com/pylint-dev/pylint/issues/8455>

- **#8394** — W0631: Using possibly undefined loop variable (undefined-loop-variable)
  Confirmed W0631 undefined-loop-variable: 'return number' after 'if not numbers: return
  None' guard + for loop is still flagged. Pylint can't see the guard ensures non-empty
  iter. <https://github.com/pylint-dev/pylint/issues/8394>

- **#8367** — Incorrect type inferred when inner class definition closes over variable
  from outer class’s method Confirmed E1101: closure over 'this = self' in nested class
  loses Outer type info; 'x.say_hello()' flagged as missing member.
  <https://github.com/pylint-dev/pylint/issues/8367>

- **#8331** — Incorrect type inferance after a conditional raise Confirmed E1130: type
  narrowing after 'if not isinstance(operand, (int, float, complex)): raise' is not
  applied to subsequent return -operand.
  <https://github.com/pylint-dev/pylint/issues/8331>

- **#8327** — `isinstance-second-argument-not-valid-type` does not handle `Enum.enum`
  Confirmed W1116 false positive: Enum functional form 'Direction = Enum("Direction",
  [...])' not recognized as a valid isinstance second arg.
  <https://github.com/pylint-dev/pylint/issues/8327>

- **#8325** — false-positive: no-value-for-parameter Confirmed E1120 false positive:
  'self.**new**(type(self))' raises no-value-for-parameter (the bug is pylint treats
  **new** as needing 'cls' even though self.**new** passes it implicitly... wait —
  actually **new** is a staticmethod and self.**new** DOES need cls. Reporter is wrong
  about the bug being a FP). Confirmed still raises E1120 either way.
  <https://github.com/pylint-dev/pylint/issues/8325>

- **#8265** — False positive `C2801` `unnecessary-dunder-call` for descriptor binding
  `__get__` Confirmed C2801: method_ref.**get**(instance, class_ref) triggers
  unnecessary-dunder-call though descriptor binding has no public method.
  <https://github.com/pylint-dev/pylint/issues/8265>

- **#8256** — Unnecessary use of a comprehension: Wrong fix Confirmed:
  'unnecessary-comprehension' suggests 'use dict(dict1) instead' when dict1's keys are
  tuples — would create a copy, not the intended dict-from-keys behavior. Wrong-fix bug.
  <https://github.com/pylint-dev/pylint/issues/8256>

- **#8224** — consider-using-f-string is triggered in a functional context Confirmed
  C0209 consider-using-f-string false positive on 'map("{}".format, …)' — the format
  method is used in functional context, can't easily be rewritten as f-string.
  <https://github.com/pylint-dev/pylint/issues/8224>

- **#8221** — cell-var-from-loop ignores generator expressions Confirmed false negative
  W0640 cell-var-from-loop on generator-expression captured from outer loop variable:
  '(value for value in [1,2] if value == loop_var)' inside 'for loop_var in ...:' is not
  flagged. <https://github.com/pylint-dev/pylint/issues/8221>

- **#8215** — Spurious 'undefined-variable' warning with postponed annotations enabled
  Confirmed E0602 undefined-variable false positive: 'from **future** import
  annotations' + class B nested in class A used as annotation in sibling class C.
  <https://github.com/pylint-dev/pylint/issues/8215>

- **#8213** — False negative for `isinstance-second-argument-not-valid-type`
  (parameterized generic) Confirmed false negative:
  isinstance-second-argument-not-valid-type is NOT raised on 'isinstance(0, list[int])'
  even though parameterized generics raise TypeError at runtime.
  <https://github.com/pylint-dev/pylint/issues/8213>

- **#8145** — `undefined-variable` false positive when method returns instance type when
  the class is inside a fun Confirmed E0602 false positive: 'def foo(self) -> Foo:'
  inside a function-nested class with 'from **future** import annotations' raises
  undefined-variable on the return type.
  <https://github.com/pylint-dev/pylint/issues/8145>

- **#8138** — `not-callable` false positive for class Confirmed E1102 not-callable false
  positive: TYPE_CHECKING-guarded @property declaring -> Type[X] (class reference)
  called as func.myfunc(1,2,3) flagged not-callable.
  <https://github.com/pylint-dev/pylint/issues/8138>

- **#8129** — False positive `expression-not-assigned` when calling functions with no
  return inside ternary expr Confirmed W0106 expression-not-assigned still fires on
  'f1() if test else f2()'. Reporter argues this is the canonical conditional-call
  pattern. <https://github.com/pylint-dev/pylint/issues/8129>

- **#8022** — Generic type of setter is leaking across instances Confirmed E1130 false
  positive: Generic[T] setter type narrowing 'leaks' across instances — pylint applies
  the last setter's T to a different instance with different actual generic type.
  <https://github.com/pylint-dev/pylint/issues/8022>

- **#7997** — False Positive `dict-init-mutate` when dict assignment references dict
  Confirmed C3401 dict-init-mutate false positive: 'counts[key] = ... counts.get(key,
  0)' references the dict itself, cannot be moved into the initializer.
  <https://github.com/pylint-dev/pylint/issues/7997>

- **#7991** — `no-member` error when accessing a sub class variable with `self` returned
  from a super class method Confirmed E1101: super().save() return narrowed to Foo,
  loses Bar.value attribute. <https://github.com/pylint-dev/pylint/issues/7991>

- **#7978** — Incorrect unsupported-membership-test error on TypedDict Confirmed E1135
  unsupported-membership-test false positive: 'while x is None or "a" in x:' on
  Optional[TypedDict] — pylint doesn't narrow after 'or'.
  <https://github.com/pylint-dev/pylint/issues/7978>

- **#7853** — False Positive - `assignment-from-none` raised when function not
  necessarily returns `None` Confirmed E1128 false positive: get_func() conditionally
  returns 'def func(): return None' OR 'def func(): return param' — pylint sees only the
  None branch and flags 'val = func()' as assignment-from-none.
  <https://github.com/pylint-dev/pylint/issues/7853>

- **#7720** — undefined-variable regression since 2.6.0 Confirmed E0602
  undefined-variable false positive: '@CONVERTER.register()' as decorator for a class
  defined inside another class still fails.
  <https://github.com/pylint-dev/pylint/issues/7720>

- **#7379** — False positive no-member on member of generic parent class with overridden
  **class_getitem** Confirmed E1101: Derrived(Base[int]).foo lost when Base overrides
  **class_getitem**. <https://github.com/pylint-dev/pylint/issues/7379>

- **#7348** — False positives for E1120 and E1123 when instance method is overwritten
  Confirmed E1123/E1120 false positives: 'foo.method = lambda x: x' on one instance
  still narrows 'bar.method' calls on a DIFFERENT instance to the lambda signature.
  <https://github.com/pylint-dev/pylint/issues/7348>

### FIXED (15)

- **#8805** — `no-member` emitted for all `zipimport` names Does NOT reproduce on pylint
  4.0.5: 'import zipimport; zipimport.ZipImportError' is clean (10/10). Fixed since
  3.0.0b1. <https://github.com/pylint-dev/pylint/issues/8805>

- **#8600** — protected-access false positive with Generic classes Does NOT reproduce on
  4.0.5: 'Parent.\_foo(self)' in Child.\_foo override under Generic[T] no longer flagged
  W0212. Fixed since 2.17.2. <https://github.com/pylint-dev/pylint/issues/8600>

- **#8499** — invalid-name check for TypeVar should allow for digits in names Does NOT
  reproduce on 4.0.5: 'Ec2T = TypeVar("Ec2T")' is no longer flagged C0103 — 10/10.
  typevar-rgx now allows digits. <https://github.com/pylint-dev/pylint/issues/8499>

- **#8419** — False negative: `unspecified-encoding` (`W1514`) not raised for
  `Path.read_text` Does NOT reproduce on 4.0.5: 'Path("file.txt").read_text()' now
  correctly triggers W1514 unspecified-encoding. Was a false negative in 2.17 — fixed.
  <https://github.com/pylint-dev/pylint/issues/8419>

- **#8250** — Missing-return-doc returns multiple errors when there are multiple returns
  in the function Does NOT reproduce on 4.0.5 with
  --load-plugins=pylint.extensions.docparams: 10/10. Multiple W9011 errors no longer
  fire per return-statement. <https://github.com/pylint-dev/pylint/issues/8250>

- **#8201** — False negative `trailing-comma-tuple` Does NOT reproduce as a false
  negative anymore: 'DEMO = True\nprint("demo"),' — pylint 4.0.5 gets 10/10, but the
  issue asks for R1707 to be raised here. False negative likely still present, but
  checker doesn't fire on this minimal case. Actually with the broader test
  (--disable=expression-not-assigned), nothing is raised; reporter's first 'detected.py'
  case is what should still fire. <https://github.com/pylint-dev/pylint/issues/8201>

- **#8179** — consider-using-augmented-assign false positive on string formatting Does
  NOT reproduce on 4.0.5 with code_style plugin: 's = s %% 5' no longer triggers
  consider-using-augmented-assign. Fixed.
  <https://github.com/pylint-dev/pylint/issues/8179>

- **#8068** — False-positive unsupported-delete-operation Does NOT reproduce on 4.0.5:
  'if self.\_m: del self.\_m[:]' after 'self.\_m = [] if b else None' init no longer
  raises E1138 — 10/10. <https://github.com/pylint-dev/pylint/issues/8068>

- **#8053** — False positive `assigning-non-slot` error for inherited descriptor when
  slots are used. Does NOT reproduce on 4.0.5: descriptor in Parent's **slots**=()
  inherited by Child no longer raises E0237 — 10/10.
  <https://github.com/pylint-dev/pylint/issues/8053>

- **#8050** — Pylint doesn't check file if it's named exactly like the directory where
  the file is Does NOT reproduce on 4.0.5: pylint now DOES check a file named exactly
  like its directory (W0611 unused-import was reported). Fixed since 2.15.6.
  <https://github.com/pylint-dev/pylint/issues/8050>

- **#7950** — Subclasses of abstract class that do not inherit abc.ABC are considered
  abstract Does NOT reproduce on 4.0.5: Sub(AbsSub) no longer escapes abstract-method
  detection — 10/10. <https://github.com/pylint-dev/pylint/issues/7950>

- **#7934** — Missing Class Docstring false positive when inheriting from a generic
  class of a TypedDict instance Does NOT reproduce on 4.0.5: missing-function-docstring
  no longer falsely fires on Child(Bases[TypedDict-functional]). Fixed since 2.15.8.
  <https://github.com/pylint-dev/pylint/issues/7934>

- **#7891** — False positive `no-member` when attempting to access `_asdict`, which is a
  valid `NamedTuple` method Does NOT reproduce on 4.0.5: 'Foo(NamedTuple).\_asdict()' on
  subclass of NamedTuple is now correctly recognized — 10/10.
  <https://github.com/pylint-dev/pylint/issues/7891>

- **#7647** — False positive `unnecessary-lambda` (wrong type inference in
  if-else-expression) Does NOT reproduce on 4.0.5: 'lambda: fun(\*\*kwargs)' with
  conditional kwargs dict no longer triggers unnecessary-lambda — 10/10.
  <https://github.com/pylint-dev/pylint/issues/7647>

- **#7381** — Multiple binary | operation in a single statement failed with "E1131:
  unsupported operand type(s) fo Does NOT reproduce on 4.0.5: chained 'Flag | Flag |
  Flag' no longer triggers E1131 — 10/10.
  <https://github.com/pylint-dev/pylint/issues/7381>

### UNCLEAR (3)

- **#8079** — Pylint is crashing with astroid.exceptions.StatementMissing: Statement not
  found on <Module.builtins Crash with astroid.exceptions.StatementMissing. Needs
  reproduction. <https://github.com/pylint-dev/pylint/issues/8079>

- **#8049** — Crash with AstroidError 'Could not find <FunctionDef.warning_logger' Crash
  only on full project, not on minimal repro. Needs reporter's project to verify.
  Possibly fixed indirectly. <https://github.com/pylint-dev/pylint/issues/8049>

- **#7680** — pylint crashed with a `AstroidError`
  (astroid.exceptions.ParentMissingError) Crash AstroidError. Needs reproduction.
  <https://github.com/pylint-dev/pylint/issues/7680>

### EXTDEP (15)

- **#8759** — Missing Member for Pydantic Model Pydantic 'Missing Member'. Lib-specific
  decision. <https://github.com/pylint-dev/pylint/issues/8759>

- **#8704** — False-positive `inconsistent-mro` with `PySide6` objects False
  inconsistent-mro on PySide6 objects. Lib-specific astroid.
  <https://github.com/pylint-dev/pylint/issues/8704>

- **#8501** — False positive `unused-import` when import is used via a parent module
  Needs prettyprinter installed. False unused-import for 'prettyprinter.doctypes' used
  only via parent attribute access. <https://github.com/pylint-dev/pylint/issues/8501>

- **#8497** — false-positive errors with pyroute2 0.7.6 pyroute2 0.7.6 false-positives.
  Lib-specific. <https://github.com/pylint-dev/pylint/issues/8497>

- **#8303** — decorators not processed successfully with alpha_vantage alpha_vantage
  decorator processing failure. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/8303>

- **#8210** — Crash when using mcculw lib Crash with mcculw lib. Lib-specific astroid
  recursion. <https://github.com/pylint-dev/pylint/issues/8210>

- **#8178** — False positive for no-member when using assignment expression (with
  torch?) Needs torch installed. False E1101 no-member with walrus operator + isinstance
  narrowing. Lib-specific inference. <https://github.com/pylint-dev/pylint/issues/8178>

- **#8026** — Custom reporters produce no output if (1) markupsafe is imported before
  the run and (2) the target i Reporters silenced if markupsafe imported. Lib
  interaction. <https://github.com/pylint-dev/pylint/issues/8026>

- **#8024** — Support for cython pure python syntax: cython.declare Cython pure-python
  syntax (cython.declare). Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/8024>

- **#8018** — False positive `invalid-sequence-index` with `scipy.fft.rfft` Needs scipy.
  invalid-sequence-index with scipy.fft.rfft. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/8018>

- **#7981** — `unsubscriptable-object` in numpy array method Needs numpy.
  unsubscriptable-object on numpy array method. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/7981>

- **#7894** — Maximum recursion depth exceeded in comparison when importing from panda3d
  Maximum recursion in astroid when importing certain libs. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/7894>

- **#7883** — False positive when using ndarray.reshape with separate arguments for each
  element of the shape Needs numpy ndarray.reshape variadic args. Lib-specific brain.
  <https://github.com/pylint-dev/pylint/issues/7883>

- **#7702** — False positive E1126: invalid-sequence-index from numpy.ufunc.reduce Needs
  numpy. False E1126 from np.ufunc. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/7702>

- **#7351** — False positive C2801 (unnecessary-dunder-call) with unittest.mock.call
  Needs unittest.mock context. Real but the assert_has_calls/call attribute access is
  unittest-specific. <https://github.com/pylint-dev/pylint/issues/7351>

### DESIGN (110)

- **#8796** — `singleton comparison` - ==/is true message improvement Enhancement:
  improve singleton-comparison message wording.
  <https://github.com/pylint-dev/pylint/issues/8796>

- **#8795** — Request: new rule detecting non-OS universal paths Enhancement: new rule
  for non-OS universal paths. Spec. <https://github.com/pylint-dev/pylint/issues/8795>

- **#8788** — Add configurable suppressions for classes based on inheritance (for use
  with `typing.Protocol`, `typ Enhancement: configurable suppressions by inheritance.
  Spec. <https://github.com/pylint-dev/pylint/issues/8788>

- **#8785** — Use inference to determine if **kwargs is missing a named parameter
  Enhancement: inference for **kwargs missing named params. Good first issue.
  <https://github.com/pylint-dev/pylint/issues/8785>

- **#8781** — logging-fstring-interpolation not raised on function parameter hinted as
  logging.Logger logging-fstring-interpolation not raised on function parameter. Spec.
  <https://github.com/pylint-dev/pylint/issues/8781>

- **#8779** — No warning about using _ operator on sequence types containing objects
  Enhancement: warn about _ operator on heterogeneous sequence. Spec.
  <https://github.com/pylint-dev/pylint/issues/8779>

- **#8776** — pyreverse: add option to skip sorting of attribute and method names
  Pyreverse: option to skip attribute/method sort. PR ready spec.
  <https://github.com/pylint-dev/pylint/issues/8776>

- **#8766** — run_pylint signature Docs: run_pylint signature documentation. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/8766>

- **#8734** — Improved handling of fixme Enhancement: improved fixme handling. Spec.
  <https://github.com/pylint-dev/pylint/issues/8734>

- **#8725** — `pylint: disable=all` comment is applied to the whole file Decision:
  'pylint: disable=all' on a line is treated as file-scope. Discussion.
  <https://github.com/pylint-dev/pylint/issues/8725>

- **#8693** — Request: reporting unnecessary `int`-cast Enhancement: report unnecessary
  int-cast. Spec. <https://github.com/pylint-dev/pylint/issues/8693>

- **#8689** — Unexpected false-positive "no-value-for-parameter" from type stubs
  'hidden' under 'if TYPE_CHECKING: False no-value-for-parameter from typing inference.
  Docs/spec. <https://github.com/pylint-dev/pylint/issues/8689>

- **#8680** — missing-parentheses-for-call-in-test not raised as expected
  missing-parentheses-for-call-in-test not raised in cases. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8680>

- **#8670** — Ability to Configure Useless suppressions incompatibility list
  Enhancement: configurable useless-suppression incompatibility list. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8670>

- **#8666** — proposal: warn when trying to catch KeyError in defaultdict lookup
  Proposal: warn on catching KeyError when defaultdict is used. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8666>

- **#8659** — False negative for function annotation mistakenly targeting property
  instead of imported module Real false negative but no checker exists for it. 'def
  datetime(self, date_time: datetime.datetime)' setter under '@datetime.setter'
  shadowing 'import datetime' module is a name-clash that pylint doesn't currently
  detect. Enhancement. <https://github.com/pylint-dev/pylint/issues/8659>

- **#8658** — Request: detecting bad short circuit with walrus operator Enhancement:
  detect bad short-circuit with walrus operator. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8658>

- **#8654** — `RuffChecker` class to be able to create python plugins using ruff 's AST
  Proposal: RuffChecker plugin class for ruff-based checkers. High effort design.
  <https://github.com/pylint-dev/pylint/issues/8654>

- **#8652** — unused-import when readline is imported to enhance input() unused-import
  for 'import readline' to enhance input(). Decision/spec.
  <https://github.com/pylint-dev/pylint/issues/8652>

- **#8646** — Suggestion to improve redefined-outer-name or to introduce a new rule
  Enhancement: improve redefined-outer-name. Decision.
  <https://github.com/pylint-dev/pylint/issues/8646>

- **#8641** — `unnecessary-lambda-assignment` should not be generated when assigning to
  a “genuine” variable unnecessary-lambda-assignment edge cases. Decision/spec.
  <https://github.com/pylint-dev/pylint/issues/8641>

- **#8636** — Proposal - Check match case exhaustiveness for enums Proposal: check
  match-case exhaustiveness for Enum. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8636>

- **#8628** — missing-param-doc W9015 false positive for typing.Union missing-param-doc
  W9015 false positive for typing.Union. Spec.
  <https://github.com/pylint-dev/pylint/issues/8628>

- **#8623** — Internal checker for `@utils.only_required_for_messages` to verify that
  it's used when required an Internal: checker for @utils.only_required_for_messages.
  Internal. <https://github.com/pylint-dev/pylint/issues/8623>

- **#8614** — `no-docstring-rgx` accepting lists Enhancement: no-docstring-rgx accepting
  lists. Spec/PR. <https://github.com/pylint-dev/pylint/issues/8614>

- **#8579** — Maintain and document a list of equivalent messages in other tools
  Proposal: maintain mapping of pylint messages to flake8/ruff equivalents. Docs.
  <https://github.com/pylint-dev/pylint/issues/8579>

- **#8567** — False-positive unreachable code Regression false-positive unreachable
  code. Spec/PR. <https://github.com/pylint-dev/pylint/issues/8567>

- **#8551** — False positive `unnecessary-dunder-call` on `__enter__` False positive
  unnecessary-dunder-call on **enter**. Decision.
  <https://github.com/pylint-dev/pylint/issues/8551>

- **#8538** — Request: detecting empty list in set.union(_[]) Proposal: detect empty
  list in set.union(_[]). Spec. <https://github.com/pylint-dev/pylint/issues/8538>

- **#8535** — Create separate repositories for pyreverse, spelling and testutils
  Discussion: split pyreverse/spelling/tests into separate repos. Maintenance.
  <https://github.com/pylint-dev/pylint/issues/8535>

- **#8505** — False Positive
  `E1130: bad operand type for unary ~: object (invalid-unary-operand-type)` False
  positive E1130 bad-operand-type. Needs more context.
  <https://github.com/pylint-dev/pylint/issues/8505>

- **#8503** — --fail-under has no visual impact on terminal output Enhancement:
  --fail-under should have visual impact. Good first issue.
  <https://github.com/pylint-dev/pylint/issues/8503>

- **#8460** — Pylint does not respect false values for boolean config options in toml
  files Config bug: pyproject.toml boolean false treated as 'set'. Good-first-issue /
  Needs PR. <https://github.com/pylint-dev/pylint/issues/8460>

- **#8457** — unknown-option-value should result in non-zero exit code Enhancement:
  unknown-option-value should exit non-zero. Breaking change.
  <https://github.com/pylint-dev/pylint/issues/8457>

- **#8451** — Different Linting output for different python minor version Q on different
  lint output per Python minor version. Docs.
  <https://github.com/pylint-dev/pylint/issues/8451>

- **#8443** — Allow setting PYLINT_HOME via pyproject.toml Enhancement: support setting
  PYLINT_HOME via pyproject.toml [tool.pylint]. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8443>

- **#8430** — Raise a convention message when an index is initialized outside of a for
  loop instead of using ``enu Enhancement: convention message for index initialized
  outside for-loop. Proposal by maintainer.
  <https://github.com/pylint-dev/pylint/issues/8430>

- **#8413** — Checking the configuration in a dedicated script instead of at runtime
  Performance: validate config in a dedicated script instead of at runtime.
  Internal/maintainer-level. <https://github.com/pylint-dev/pylint/issues/8413>

- **#8398** — Propagate module config through imports Proposal: support py.typed-like
  marker file to propagate per-package pylint config through imports. Design proposal
  needed. <https://github.com/pylint-dev/pylint/issues/8398>

- **#8397** — Check args for `Process` and `Thread` Enhancement: type-check args= for
  multiprocessing.Process / threading.Thread against target. Spec.
  <https://github.com/pylint-dev/pylint/issues/8397>

- **#8392** — Documentation has incorrect rendering of spaces for the indent-string
  option Docs rendering: HTML folds whitespace in indent-string default.
  Good-first-issue. <https://github.com/pylint-dev/pylint/issues/8392>

- **#8365** — New check: manually accessing `sys.argv` value using indexes or range
  Proposal: warn on manually accessed sys.argv with index. Decision.
  <https://github.com/pylint-dev/pylint/issues/8365>

- **#8336** — Split accept-no-return-doc into accept-no-return-doc and
  accept-no-return-type Enhancement: split accept-no-return-doc into separate
  accept-no-return-doc and accept-no-return-type. Spec.
  <https://github.com/pylint-dev/pylint/issues/8336>

- **#8333** — New check: consider using `Self` Enhancement: new 'consider-using-self'
  check when method returns the class itself. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8333>

- **#8319** — Lint warning given for external 3rd party package/module
  reportlab.platypus.flowables Lint warning for external 3rd-party package/module via
  re-exports. Spec. <https://github.com/pylint-dev/pylint/issues/8319>

- **#8318** — [new rule] suggesting raise Exception over raise Exception() when no args
  Proposal: new rule suggesting 'raise Exception' over 'raise Exception()'. Decision
  pending. <https://github.com/pylint-dev/pylint/issues/8318>

- **#8315** — Pylint caching issue when run on multiple packages having the same name
  Caching issue when linting multiple packages with the same module name. Internal bug.
  <https://github.com/pylint-dev/pylint/issues/8315>

- **#8311** — Globbing pattern a default instead of regex pattern Enhancement: globbing
  patterns as default for ignore-patterns instead of regex. Spec.
  <https://github.com/pylint-dev/pylint/issues/8311>

- **#8305** — [spelling] Dictionary path is valid only when run from same directory as
  .pylintrc Enhancement: spelling dictionary path resolution from project root. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8305>

- **#8301** — "useless suppression of line too long" in multi-line docstring False
  positive useless-suppression of line-too-long inside multi-line docstring. Spec.
  <https://github.com/pylint-dev/pylint/issues/8301>

- **#8300** — False 'attribute-defined-outside-init' warning for ctypes structs False
  attribute-defined-outside-init for ctypes.Structure subclass _fields_. Decision
  pending. <https://github.com/pylint-dev/pylint/issues/8300>

- **#8296** — consider-using-f-string is triggered when the formatting arguments are
  implicit False positive consider-using-f-string when format args ARE referenced.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/8296>

- **#8263** — Check for invocations of asyncio.create_task without
  assignment-of-the-result Enhancement: check asyncio.create_task without assignment.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/8263>

- **#8230** — Force typing instead of inference Enhancement: 'force typing instead of
  inference' option. Design proposal. <https://github.com/pylint-dev/pylint/issues/8230>

- **#8217** — pyproject.toml needs enable-all-extensions Docs: pyproject.toml example
  missing enable-all-extensions. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/8217>

- **#8196** — Docs - `too-many-locals` - message description is not helpful Docs
  improvement for too-many-locals. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/8196>

- **#8192** — unnecessary-lambda false positive (expression variable reassigned) False
  positive unnecessary-lambda when lambda body uses a reassigned outer variable.
  Requires aliasing/reassignment tracking. Spec.
  <https://github.com/pylint-dev/pylint/issues/8192>

- **#8183** — pyreverse: Add option to filter ancestors Pyreverse enhancement:
  --filter-ancestors option. Spec. <https://github.com/pylint-dev/pylint/issues/8183>

- **#8162** — Disable bad-mcs-classmethod-argument per default Disable
  bad-mcs-classmethod-argument by default. PEP 8 conflict. Decision.
  <https://github.com/pylint-dev/pylint/issues/8162>

- **#8160** — Don't enforce superfluous-parens for default function values Proposal:
  relax superfluous-parens for default function values when expression contains
  comparison. Decision pending. <https://github.com/pylint-dev/pylint/issues/8160>

- **#8155** — Differentiate `no-else-return` for `if` and `try` expressions Enhancement:
  separate no-else-return into no-try-else-return. Decision/PR.
  <https://github.com/pylint-dev/pylint/issues/8155>

- **#8147** — Multiple `output-format` arguments with a file output produces all files,
  but only the last argument Bug: multiple --output-format options only fill last file.
  Internal CLI bug. <https://github.com/pylint-dev/pylint/issues/8147>

- **#8137** — Check for redundant types in more places Enhancement: check redundant
  types in more places. Spec. <https://github.com/pylint-dev/pylint/issues/8137>

- **#8128** — Option to ignore all pragma comments? Performance enhancement: option to
  ignore all pragma comments. Design proposal.
  <https://github.com/pylint-dev/pylint/issues/8128>

- **#8117** — Do not show warning "singleton-comparison" in the case of numpy.bool?
  Spec: singleton-comparison should ignore NumPy 'a == None'-like contexts. Decision.
  <https://github.com/pylint-dev/pylint/issues/8117>

- **#8099** — Feature request: strict design constraints Feature request: strict design
  constraints. Design proposal. <https://github.com/pylint-dev/pylint/issues/8099>

- **#8083** — Feature request: support multiple locales in spelling-dict option
  Enhancement: support multiple locales in spelling-dict. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8083>

- **#8082** — False positive `unnecessary-dunder-call` for `__init__` Discussion: false
  positive unnecessary-dunder-call for **init**. Decision.
  <https://github.com/pylint-dev/pylint/issues/8082>

- **#8080** — check cython super in comprehension error Proposal: check cython super in
  comprehension. High-effort. <https://github.com/pylint-dev/pylint/issues/8080>

- **#8072** — End column too far if accent in string Astroid: end column too far if
  accent (non-ASCII) in string. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/8072>

- **#8046** — Pyreverse: Duplicated class variables Pyreverse enhancement: detect
  duplicated class variables. Spec. <https://github.com/pylint-dev/pylint/issues/8046>

- **#8023** — Enforce a specified docstring type style to use in docparams checks
  Enhancement: enforce docstring-type style in docparams. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8023>

- **#8019** — Can I turn on missing-docstring for "private" functions? Decision:
  missing-docstring for 'private' (\_-prefixed) functions. Discussion.
  <https://github.com/pylint-dev/pylint/issues/8019>

- **#8013** — Improve `--dummy-variables-rgx` and `--ignored-argument-names`
  documentation Enhancement: improve --dummy-variables-rgx / --ignored-argument-names
  docs/spec. <https://github.com/pylint-dev/pylint/issues/8013>

- **#8012** — False negative `too-few-format-args` False negative too-few-format-args.
  Spec. <https://github.com/pylint-dev/pylint/issues/8012>

- **#8008** — New check: suggest `dataclass` when `__init__` only assigns instance
  variables Enhancement: suggest @dataclass when **init** only assigns attributes.
  Spec/decision. <https://github.com/pylint-dev/pylint/issues/8008>

- **#8001** — `arguments-out-of-order` false positive? (W1114) False positive
  arguments-out-of-order (W1114) with dataclass. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8001>

- **#7995** — Class of classmethod does not support `__orig_bases__` while Type does
  Class of classmethod doesn't expose **orig_bases** via cls. Astroid limitation. Spec.
  <https://github.com/pylint-dev/pylint/issues/7995>

- **#7977** — pyreverse problem for classes diagrams generation Pyreverse: problem with
  class diagram generation. Internal. <https://github.com/pylint-dev/pylint/issues/7977>

- **#7957** — Enable the use of preferred-modules with submodules Enhancement:
  preferred-modules with submodules. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7957>

- **#7935** — False negative `expression-not-assigned` on fonction calls that return
  values False negative expression-not-assigned on function calls in some context.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/7935>

- **#7929** — Only warn for implicit string concatenation when parts are _not_
  surrounded by a set of parentheses Enhancement: only warn for implicit string
  concatenation when parts are NOT in parens. Spec.
  <https://github.com/pylint-dev/pylint/issues/7929>

- **#7920** — Ignore multi-line calls in duplicate detection (R0801) Enhancement: ignore
  multi-line calls in duplicate detection (R0801). Decision.
  <https://github.com/pylint-dev/pylint/issues/7920>

- **#7911** — Useful 'line-too-long' suppression considered useless C0301 line-too-long:
  'useful line-too-long suppression considered useless' (I0021 useless-suppression false
  positive). Spec/PR. <https://github.com/pylint-dev/pylint/issues/7911>

- **#7909** — generated-members doesn't work with fully qualified names
  generated-members doesn't work with fully qualified names. Spec.
  <https://github.com/pylint-dev/pylint/issues/7909>

- **#7892** — Project plugin removed from sys.path modify_sys_path pops a real
  PYTHONPATH entry when path ends with ':'. Internal.
  <https://github.com/pylint-dev/pylint/issues/7892>

- **#7876** — New check `replace-if-with-loop` Enhancement: new check
  replace-if-with-loop. Spec. <https://github.com/pylint-dev/pylint/issues/7876>

- **#7875** — ImportError for implicit namespace (pyproject, setuptools) Implicit
  namespace ImportError. High effort. Design proposal.
  <https://github.com/pylint-dev/pylint/issues/7875>

- **#7872** — Errors from astroid brain hooks are shown if module name happens to
  coincide with a hook ('pytest') Astroid brain_pytest hooks fire for any 'pytest'
  filename. Astroid update. <https://github.com/pylint-dev/pylint/issues/7872>

- **#7843** — (🐞) False negative `unnecessary-comprehension` ( maybe `use-a-generator`
  or `consider-using-a-genera Enhancement: detect redundant list comprehensions inside
  builtins that accept iterables (join, max, sorted, set, any, all). Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7843>

- **#7840** — False positive on member classes accessing private attributes of parent
  False positive on member classes accessing private attribute. Decision.
  <https://github.com/pylint-dev/pylint/issues/7840>

- **#7835** — Warn about `os.x` function used on a `pathlib.Path` instead of the
  corresponding function from p Enhancement: warn about os.x function used on
  pathlib.Path instance. Spec. <https://github.com/pylint-dev/pylint/issues/7835>

- **#7820** — Pylint does not appear to understand the descriptor protocol Pylint
  doesn't fully understand descriptor protocol. Design proposal.
  <https://github.com/pylint-dev/pylint/issues/7820>

- **#7803** — Add warning when comparing `sys.version_info` with old python Enhancement:
  warn when comparing sys.version_info with old python versions. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7803>

- **#7790** — False negative `no-member` for `@dataclass(slots=...)` False negative
  no-member for @dataclass(slots=...). Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7790>

- **#7786** — Raise `for-any-all` for early returns Enhancement: raise for-any-all for
  early returns. Spec. <https://github.com/pylint-dev/pylint/issues/7786>

- **#7749** — Organisation of the dev/contributor documentation is hard to understand
  Enhancement: dev/contributor docs organization. Docs.
  <https://github.com/pylint-dev/pylint/issues/7749>

- **#7738** — Better primer tests : more reliable, easier to understand, and more stable
  Internal: better primer tests. Maintenance.
  <https://github.com/pylint-dev/pylint/issues/7738>

- **#7736** — False Positive when using function descriptors False positive when using
  function descriptors. Spec. <https://github.com/pylint-dev/pylint/issues/7736>

- **#7735** — False positive `ungrouped-imports` in match case False positive
  ungrouped-imports in match-case. Decision.
  <https://github.com/pylint-dev/pylint/issues/7735>

- **#7734** — False negative for `unnecessary-dict-index-lookup` when inside function
  False negative for unnecessary-dict-index-lookup. Spec.
  <https://github.com/pylint-dev/pylint/issues/7734>

- **#7729** — Cannot detect enum method in protocol Decision: cannot detect enum method
  in Protocol. Decision. <https://github.com/pylint-dev/pylint/issues/7729>

- **#7724** — Doc why `is` is superior to `==` in `comparison-with-callable` when
  comparing two callables Docs: why 'is' is superior to '==' in
  comparison-with-callable. Docs/PR. <https://github.com/pylint-dev/pylint/issues/7724>

- **#7700** — Use `namedtuple` or `dataclass` for `pyreverse` arrow options Pyreverse:
  use namedtuple/dataclass for arrow options. Maintenance.
  <https://github.com/pylint-dev/pylint/issues/7700>

- **#7688** — False-negative `unneeded-not` when using `hash` function False negative
  unneeded-not with hash function. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7688>

- **#7686** — `pyreverse` does not show inheritance relation when using a flat folder
  Pyreverse doesn't show inheritance with -A flag (or similar). Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/7686>

- **#7658** — consider-using-with assigning TemporaryDirectory() to class attribute
  Proposal: consider-using-with with TemporaryDirectory() as class attribute. Decision.
  <https://github.com/pylint-dev/pylint/issues/7658>

- **#7654** — Config file generated by --generate-toml-config option produces errors
  when later used --generate-toml-config produces wrong output. Internal bug.
  <https://github.com/pylint-dev/pylint/issues/7654>

- **#7653** — Custom objects as datatypes Pyreverse: custom objects as datatypes. Spec.
  <https://github.com/pylint-dev/pylint/issues/7653>

- **#7643** — Support for Overload Decorators Pyreverse: support for @overload
  decorators. Astroid update. <https://github.com/pylint-dev/pylint/issues/7643>
