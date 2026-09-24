# Session 03 — Triage Notes

**Issues triaged this session:** 165

**Verdict tally:**

- REPRO: 12
- FIXED: 1
- UNCLEAR: 1
- EXTDEP: 35
- DESIGN: 116

## By verdict

### REPRO (12)

- **#9533** — False positive `deprecated-class` when the class is imported in a guarded
  import block Confirmed: deprecated-class W4904 fires inside 'if sys.version_info >
  (2,):' guarded import block. Mirrors #10043.
  <https://github.com/pylint-dev/pylint/issues/9533>

- **#9519** — [too-many-function-args] False negative when calling `super().__init__()`
  with non-self argument Confirmed false negative: super().**init**(txt) in a class
  where the MRO ultimately resolves to object.**init**() (takes no args) is not flagged
  too-many-function-args. <https://github.com/pylint-dev/pylint/issues/9519>

- **#9505** — Changing the number of function arguments when using a decorator does not
  work. Confirmed via reporter: decorator with Concatenate[…, P] adds new positional arg
  but pylint doesn't pick up the new signature; E1121 too-many-function-args false
  positive. <https://github.com/pylint-dev/pylint/issues/9505>

- **#9488** — Unexpected keyword argument for Generic dataclass with ABC bounded TypeVar
  Confirmed E1123 unexpected-keyword-arg: @dataclass with Generic[_T] where \_T has
  'bound=Base|AbstractBase' (Union bound). pylint loses 'field' kwarg through the bound
  resolution. <https://github.com/pylint-dev/pylint/issues/9488>

- **#9389** — False-positive E1121 when using dataclass with init=False Confirmed E1121
  false positive: dataclass A with init=False inherited by B(A) — B('a','b') flagged
  'too many positional args' even though it is valid.
  <https://github.com/pylint-dev/pylint/issues/9389>

- **#9385** — False-positive E1137 (unsupported-assignment-operation) with np.empty_like
  Per reporter: 'from numpy import empty_like' results in E1137
  unsupported-assignment-operation while 'np.empty_like([1])' (qualified) does not.
  Lib-specific astroid inference asymmetry.
  <https://github.com/pylint-dev/pylint/issues/9385>

- **#9359** — useless-parent-delegation false positive when **init** signatures differ
  but parent is built-in type Confirmed W0246 useless-parent-delegation false positive:
  child of list/dict that takes no args in **init** while parent takes optional args is
  flagged useless. <https://github.com/pylint-dev/pylint/issues/9359>

- **#9319** — False positive for `unnecessary-ellipsis` on `Protocol` methods Confirmed
  W2301 unnecessary-ellipsis false positive on Protocol method body. The '...' is
  required for type-checkers like pyright to infer non-implementation.
  <https://github.com/pylint-dev/pylint/issues/9319>

- **#9222** — False positive `duplicate-bases` with `TypedDict` Confirmed E0241
  duplicate-bases false positive on 'class ABCD(ABC):' where ABC inherits multiple
  TypedDicts qualified via 'typing.TypedDict'. Works fine with unqualified TypedDict
  import. <https://github.com/pylint-dev/pylint/issues/9222>

- **#9203** — `no-member` when creating an object through an inherited factory method
  Confirmed E1101: Child.from_dict() through inherited factory loses subclass
  attributes. astroid factory-classmethod inference gap.
  <https://github.com/pylint-dev/pylint/issues/9203>

- **#9183** — False positive: Class has no '**dataclass_fields**' member (no-member)
  Confirmed E1101: '**dataclass_fields**' attribute on a @dataclass is not modeled by
  astroid dataclass brain. <https://github.com/pylint-dev/pylint/issues/9183>

- **#9159** — pylint does not support typing.Self when override Confirmed E1101 false
  positive: super(B, cls).f1() with @classmethod and typing.Self return type doesn't
  narrow back to B. Mirror of #10807. <https://github.com/pylint-dev/pylint/issues/9159>

### FIXED (1)

- **#9497** — Non existent member not detected on datetime.datetime Does NOT reproduce
  on pylint 4.0.5: 'datetime.datetime.not_a_member' correctly raises E1101 no-member
  now. <https://github.com/pylint-dev/pylint/issues/9497>

### UNCLEAR (1)

- **#9137** — Pylint 3 'UninferableBase' object is not iterable Crash 'UninferableBase
  not iterable'. Needs reproduction. <https://github.com/pylint-dev/pylint/issues/9137>

### EXTDEP (35)

- **#9549** — False positive unsubscriptable-object Needs sqlalchemy 2.x with
  Mapped[Type] declarations and ForeignKey forward refs. False E1136
  unsubscriptable-object on Mapped[T] triggered by a later relationship() with forward
  reference. <https://github.com/pylint-dev/pylint/issues/9549>

- **#9518** — False positive for missing-kwoa (E1125) on inherited dataclasses with
  kw_only=True False E1125 missing-kwoa on inherited @dataclass(kw_only=True). Astroid
  dataclass init reconstruction with kw_only.
  <https://github.com/pylint-dev/pylint/issues/9518>

- **#9479** — Crashed while using pylint as a static test for a docker Crash on docker
  test setup. No minimal repro. <https://github.com/pylint-dev/pylint/issues/9479>

- **#9472** — False positive singleton-comparison with sqlalchemy's filter Needs
  sqlalchemy. singleton-comparison on filter(field == None) style — sqlalchemy idiom
  that pylint flags. <https://github.com/pylint-dev/pylint/issues/9472>

- **#9470** — False positive on E1101: no-member when using "random.choices" False E1101
  random.choice([fn1, fn2]) result called — needs more context.
  <https://github.com/pylint-dev/pylint/issues/9470>

- **#9439** — False positive not-an-iterable on partial async iterator Partial async
  iterator false positive. Snippet may not exercise the bug. Needs more context.
  <https://github.com/pylint-dev/pylint/issues/9439>

- **#9426** — False positive: import-error and no-name-in-module when importing from
  python-docx import-error/no-name-in-module FP on specific import pattern. Needs
  reporter setup. <https://github.com/pylint-dev/pylint/issues/9426>

- **#9425** — false positive: no-member when importing from matplotlib.cm no-member on
  matplotlib.cm. Lib-specific astroid.
  <https://github.com/pylint-dev/pylint/issues/9425>

- **#9424** — False positive: overriding a generic `ParamSpec` method triggers
  `arguments-differ` (W0221) Generic ParamSpec method override FP. Needs typing-rich
  repro. <https://github.com/pylint-dev/pylint/issues/9424>

- **#9421** — `unexpected-keyword-arg` (E1123) and `missing-kwoa` (E1125) false
  positives with changing dict E1123/E1125 false positives — needs deeper repro.
  <https://github.com/pylint-dev/pylint/issues/9421>

- **#9410** — Pylint incorrectly resolving type vs instances Needs marshmallow.
  Type-vs-instance Union annotation breaks not-callable / no-value-for-parameter
  inference. <https://github.com/pylint-dev/pylint/issues/9410>

- **#9340** — Dictionary is unsubscriptable false positive when using `random.sample`
  Dict unsubscriptable false positive with random.choice. Needs more detail.
  <https://github.com/pylint-dev/pylint/issues/9340>

- **#9332** — cv2.error recognised as exception on Linux, not macOS cv2.error recognized
  as exception on Linux but not macOS. Lib + platform specific.
  <https://github.com/pylint-dev/pylint/issues/9332>

- **#9311** — False Positive E1136: PyTorch nn.Parameter.repeat (Value is
  unsubscriptable) Needs PyTorch. False E1136 on nn.Parameter.repeat. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/9311>

- **#9277** — Crash - on windows - pylint crashed with a `AstroidError` -
  UnicodeEncodeError: 'charmap' codec ca Windows crash with AstroidError. No minimal
  repro. <https://github.com/pylint-dev/pylint/issues/9277>

- **#9262** — E0401 (import-error): False positive with relative import from file in
  another module E0401 import-error false positive with relative import in specific
  layout. Needs repro. <https://github.com/pylint-dev/pylint/issues/9262>

- **#9224** — `source-roots` + jobs > 1: occasional `no-member` false positives
  source-roots + jobs>1 occasional no-member FP. Needs reproduction. May be addressed by
  b43721121. <https://github.com/pylint-dev/pylint/issues/9224>

- **#9218** — Pylint complains functions in torch.linalg not callable. Needs torch.
  not-callable on torch.linalg functions. Lib-specific brain.
  <https://github.com/pylint-dev/pylint/issues/9218>

- **#9216** — E1102 should not fire on fields in mock objects that have been given a
  return_value. E1102 false positive on mock attributes. Needs context.
  <https://github.com/pylint-dev/pylint/issues/9216>

- **#9208** — load plugin regression since pip 23.1 Plugin loading regression since pip
  23.1. Needs reproduction. <https://github.com/pylint-dev/pylint/issues/9208>

- **#9207** — W0611: Unused import enum (unused-import) when checking a file called
  signal.py W0611 unused-import enum FP. Needs more detail.
  <https://github.com/pylint-dev/pylint/issues/9207>

- **#9190** — RecursionError escapes when calculating MRO RecursionError in MRO
  calculation for Django+TYPE_CHECKING pattern. Needs Django+methodtools setup.
  <https://github.com/pylint-dev/pylint/issues/9190>

- **#9188** — Inconsistent behavior of `--recursive=y` depending on folder structure
  name --recursive=y inconsistent behavior. Needs reproduction.
  <https://github.com/pylint-dev/pylint/issues/9188>

- **#9175** — False positive circular dependency detection False positive circular
  dependency. Needs project. <https://github.com/pylint-dev/pylint/issues/9175>

- **#9170** — Colorama >=0.4.5 not only required in Windows environment Colorama
  dependency not just Windows. Crash on import. Internal.
  <https://github.com/pylint-dev/pylint/issues/9170>

- **#9168** — Inconsistent behavior with circular import on MacOS Inconsistent
  circular-import behavior on macOS. Platform-specific.
  <https://github.com/pylint-dev/pylint/issues/9168>

- **#9151** — False positive no-member when calling class method on Annotated type
  no-member calling classmethod on Annotated type. Needs more context.
  <https://github.com/pylint-dev/pylint/issues/9151>

- **#9090** — Pydantic Field(alias=) is not recognized by Pylint, warns E1123
  unexpected-keyword-arg Pydantic Field(alias=) not recognized. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/9090>

- **#9077** — E0401: Unable to import 'apsw' (import-error) apsw import-error.
  Library-specific. <https://github.com/pylint-dev/pylint/issues/9077>

- **#9013** — E0110 False positive when using attrs.field attrs.field E0110 false
  positive. Lib-specific. <https://github.com/pylint-dev/pylint/issues/9013>

- **#8980** — `no-name-in-module` not recognizing package with same base namespace
  no-name-in-module package shadow. Needs reproduction.
  <https://github.com/pylint-dev/pylint/issues/8980>

- **#8975** — Crash `'Deprecated' object has no attribute '__dict__'` with
  `unsafe-load-any-extension` Crash with 'Deprecated' object — needs lib-specific repro.
  <https://github.com/pylint-dev/pylint/issues/8975>

- **#8965** — False positive with pylxd module "has no member" pylxd library 'has no
  member'. Lib-specific. <https://github.com/pylint-dev/pylint/issues/8965>

- **#8894** — false positive `no-member` warnings in pydantic 2.0 pydantic 2.0 false
  no-member. Lib-specific. <https://github.com/pylint-dev/pylint/issues/8894>

- **#8845** — wrong-import-order fails on one system, passes in other wrong-import-order
  inconsistent across systems. Needs reproduction.
  <https://github.com/pylint-dev/pylint/issues/8845>

### DESIGN (116)

- **#9541** — "no-member" not triggered for C-extension member but
  "--unsafe-load-any-extension=y" Q: PyQt6/sip-generated stubs not consulted by pylint
  when --unsafe-load-any-extension=y. Documentation/feature gap for C-ext stubs.
  <https://github.com/pylint-dev/pylint/issues/9541>

- **#9539** — Add a specifier for alerts that are linked to a library Enhancement: tag
  checker messages with which library/version they apply to (pylint-ml use case). Spec.
  <https://github.com/pylint-dev/pylint/issues/9539>

- **#9530** — Detect useless f-strings Proposal: detect useless f-strings (f-string with
  single variable, no formatting). Discussion.
  <https://github.com/pylint-dev/pylint/issues/9530>

- **#9522** — PyLint reports "no assignment is done" but variable is changed in the
  scope of the procedure Docs Q: global-statement reports 'no assignment is done' even
  when subscript assignment happens. Spec/docs.
  <https://github.com/pylint-dev/pylint/issues/9522>

- **#9517** — Missing timeout for requests.Session object? Enhancement: extend
  missing-timeout/W3101 to requests.Session.get/post/etc. Feature.
  <https://github.com/pylint-dev/pylint/issues/9517>

- **#9509** — Detect useless copy/deepcopy Enhancement: detect useless copy/deepcopy on
  immutable objects. Discussion. <https://github.com/pylint-dev/pylint/issues/9509>

- **#9507** — Document the setting of the `sys/PYTHONPATH` in our doc and on a popular
  stackoverflow answer Docs: how pylint resolves PYTHONPATH/sys.path. Docs gap.
  <https://github.com/pylint-dev/pylint/issues/9507>

- **#9501** — Add a dynamic URL to the message documentation in the message descriptions
  from checkers Enhancement: dynamic URL to message docs in --output messages. Feature.
  <https://github.com/pylint-dev/pylint/issues/9501>

- **#9499** — Check "**slots**" and "@dataclass" attributes Enhancement: check **slots**
  vs @dataclass attribute consistency. Discussion.
  <https://github.com/pylint-dev/pylint/issues/9499>

- **#9490** — Cannot disable 'cyclic-import' warning Spec: # pylint:
  disable=cyclic-import is module-level only; doesn't work at line/scope. By-design or
  docs gap. <https://github.com/pylint-dev/pylint/issues/9490>

- **#9487** — spelling of Sphinx parameter descriptions Q on Sphinx parameter spelling.
  Docs. <https://github.com/pylint-dev/pylint/issues/9487>

- **#9480** — False positive assignment-from-no-return on generator with nested yield
  expression Generator+yield assignment-from-no-return; needs more info.
  <https://github.com/pylint-dev/pylint/issues/9480>

- **#9471** — Suggest flattening nested idempotent function applications Enhancement:
  suggest flattening nested idempotent function applications. Spec.
  <https://github.com/pylint-dev/pylint/issues/9471>

- **#9464** — False positive with return guard False positive with return guard — title
  only, needs investigation. <https://github.com/pylint-dev/pylint/issues/9464>

- **#9460** — False positive for E0601 when variable first assigned in assignment
  expression in `if` clause of a c False E0601 with walrus assignment in if-condition.
  Title says 'first assigned in assignment-expression'. Spec.
  <https://github.com/pylint-dev/pylint/issues/9460>

- **#9456** — allow-any-import-level seems to have no effect Q on allow-any-import-level
  option. Docs. <https://github.com/pylint-dev/pylint/issues/9456>

- **#9445** — "colorized" ignored when called without shell?d Q on colorized output not
  honored when stdout not a tty. Docs/feature.
  <https://github.com/pylint-dev/pylint/issues/9445>

- **#9441** — Abstract base class defined separately to concrete implementation: pylint
  complains method args are Q on abstract-base-class linting when concrete
  implementations are in separate modules. Discussion.
  <https://github.com/pylint-dev/pylint/issues/9441>

- **#9440** — Respect warnings disablement or provide .pylintrc file controls Spec:
  pylint should respect warnings module disablement, or .pylintrc warning-level control.
  <https://github.com/pylint-dev/pylint/issues/9440>

- **#9434** — `too-few-public-methods` doesn't count dunder methods if inherited
  Decision: too-few-public-methods should count dunder methods if inherited. Spec.
  <https://github.com/pylint-dev/pylint/issues/9434>

- **#9422** — [Enhancement] `newline` argument for `csv.reader()` Enhancement: 'newline'
  kwarg awareness in csv.reader recommendation. Spec.
  <https://github.com/pylint-dev/pylint/issues/9422>

- **#9418** — too-many-try-statements should exclude `pass` statements if required by
  Python Enhancement: too-many-try-statements should exclude 'pass' statements
  (early-exit / placeholder pattern). <https://github.com/pylint-dev/pylint/issues/9418>

- **#9417** — unused-argument in .pyi stub file Enhancement: ignore unused-argument
  inside .pyi stub files. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9417>

- **#9416** — protected-access false positive in class method of child class False
  protected-access in class method of child class. Spec.
  <https://github.com/pylint-dev/pylint/issues/9416>

- **#9408** — [duplicate-code] unclear how to disable the message for select
  occurrences, while keeping the option Docs: how to disable duplicate-code for specific
  sections. Doc gap. <https://github.com/pylint-dev/pylint/issues/9408>

- **#9407** — pyreverse tracking and drawing class data member relations in addition to
  instance data members (may Pyreverse feature: track class data member relations
  recursively. <https://github.com/pylint-dev/pylint/issues/9407>

- **#9405** — False negative: no-member in conditional branch False negative no-member
  in conditional branch. Spec. <https://github.com/pylint-dev/pylint/issues/9405>

- **#9379** — [used-before-assignment] False negative for for/if/else/continue pattern
  False negative used-before-assignment in for/if/else/continue patterns. Spec.
  <https://github.com/pylint-dev/pylint/issues/9379>

- **#9369** — Wrong report "instance of _ has not _ member" (E1101) no-member when
  **setattr**/**getattr** used at runtime to forward attrs. Common pattern, design
  discussion needed. <https://github.com/pylint-dev/pylint/issues/9369>

- **#9360** — False positive with consider-iterating-dictionary Docs: when
  consider-iterating-dictionary is/isn't appropriate. Doc gap.
  <https://github.com/pylint-dev/pylint/issues/9360>

- **#9356** — unused-private-member/W0238 about privates or mangling? Spec:
  unused-private-member W0238 semantics around name-mangling. Docs/decision.
  <https://github.com/pylint-dev/pylint/issues/9356>

- **#9354** — unpacking-non-sequence false positive when RHS is a function from pyi
  Enhancement: unpacking-non-sequence should consult .pyi stub for RHS function return
  type. Spec. <https://github.com/pylint-dev/pylint/issues/9354>

- **#9352** — Add ability to mark decorator inline as signature-mutator (via a comment?)
  Enhancement: inline marker for signature-mutator decorators. Spec.
  <https://github.com/pylint-dev/pylint/issues/9352>

- **#9349** — False negative `attribute-defined-outside-init` with class definition in
  other file False negative attribute-defined-outside-init with class decorator. Spec.
  <https://github.com/pylint-dev/pylint/issues/9349>

- **#9320** — Allow navigating messages by shorthands Enhancement: allow message
  shorthands in CLI navigation. Spec. <https://github.com/pylint-dev/pylint/issues/9320>

- **#9317** — Incorrect Recommendation for unnecessary-lambda Docs: unnecessary-lambda
  recommendation incorrect for some cases. Doc fix.
  <https://github.com/pylint-dev/pylint/issues/9317>

- **#9315** — W4701(modified-iterating-list) not reported for glob.glob() list W4701
  modified-iterating-list not raised for glob.glob() result. Specification.
  <https://github.com/pylint-dev/pylint/issues/9315>

- **#9306** — False positive `unnecessary-lambda` when the lambda refers to a
  not-yet-defined symbol False positive unnecessary-lambda when lambda references
  enclosing var. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9306>

- **#9294** — False positive `unnecessary-direct-lambda-call` / `C3002` with assignment
  expression False positive unnecessary-direct-lambda-call C3002 with
  assignment-expression. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9294>

- **#9282** — False positive import warnings when `jobs != 1` False positive import
  warnings when -j>=2 with namespace packages. Likely related to recently fixed
  b43721121 (sys.path/parallel). <https://github.com/pylint-dev/pylint/issues/9282>

- **#9274** — no-else-return / R1705 instructs users to use error-prone construction
  Docs: no-else-return recommendation can lead to error-prone code. Discussion.
  <https://github.com/pylint-dev/pylint/issues/9274>

- **#9270** — Two tests fails with `pydantic` installed Maintenance: 2 tests fail with
  pydantic installed. Internal. <https://github.com/pylint-dev/pylint/issues/9270>

- **#9259** — Incorrect inference of types when using match/case on a caught exception
  match/case type narrowing of caught exception not modeled. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/9259>

- **#9258** — False positive `W0612` / `unused-variable` with dataclasses Dataclass
  dunder-method-only field W0612 unused-variable. astroid brain dataclass.
  <https://github.com/pylint-dev/pylint/issues/9258>

- **#9252** — Incorrect type detected when @contextmanager uses a subgenerator Incorrect
  inference when @contextmanager wraps a sub-generator yield. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/9252>

- **#9250** — Assignments to class attributes inside `__init__()` are not inferred
  Astroid enhancement: class attribute assignments inside **init**() should be tracked.
  Astroid update. <https://github.com/pylint-dev/pylint/issues/9250>

- **#9239** — False Positive on E1121 for Usage of Self False positive E1121 on usage of
  typing.Self. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9239>

- **#9238** — False positive `import-error` with distutils.errors False positive
  import-error on distutils.errors. Stdlib in py3.12+ removal — relevant for older
  py-version. <https://github.com/pylint-dev/pylint/issues/9238>

- **#9237** — Pyreverse produces a class diagram even when there are no classes in the
  source code Pyreverse produces diagram even with no class definitions. Internal bug.
  <https://github.com/pylint-dev/pylint/issues/9237>

- **#9226** — False positive `useless-super-delegation` when only passing different
  arguments False positive useless-super-delegation when passing modified args. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/9226>

- **#9225** — False positive `super-init-not-called` for subclasses of subclasses of
  subclasses of typing.Protocol False positive super-init-not-called in subclass of
  subclass. Spec. <https://github.com/pylint-dev/pylint/issues/9225>

- **#9223** — False positive for unused-import when only usage is inside of forward
  references False positive unused-import when only usage is inside docstring. Spec.
  <https://github.com/pylint-dev/pylint/issues/9223>

- **#9219** — Race condition in primer cloned project caching Internal primer race
  condition. Maintenance. <https://github.com/pylint-dev/pylint/issues/9219>

- **#9215** — Docstrings on functions matching "no-docstring-rgx" are not linted
  Docstrings on functions matching no-docstring-rgx still need docstrings. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/9215>

- **#9194** — False positive on W0143, comparing a property to a something that is not a
  callable False positive W0143 comparison-with-callable on property. Spec.
  <https://github.com/pylint-dev/pylint/issues/9194>

- **#9192** — False negative for `modified-iterating-list` when list variable is not
  defined inline False negative modified-iterating-list when list variable is os.walk
  return. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9192>

- **#9187** — --recursive option does not find .py files in sub-directories of packages
  --recursive doesn't find .py files in sub-directories of source-root. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/9187>

- **#9184** — Link to or list of the checker's options from a message's doc if the
  message can be affected by an o Docs: link from message page to checker option docs.
  Feature. <https://github.com/pylint-dev/pylint/issues/9184>

- **#9181** — False positive. `cast` gives `not-a-mapping` error False positive
  not-a-mapping on typing.cast result. Spec.
  <https://github.com/pylint-dev/pylint/issues/9181>

- **#9179** — False positive unsubscriptable-object with MutableMapping / pygtrie False
  positive unsubscriptable-object with MutableMapping. Spec.
  <https://github.com/pylint-dev/pylint/issues/9179>

- **#9174** — Better docs required for 2 'design' checkers Docs request: better docs for
  2 'design' checkers. <https://github.com/pylint-dev/pylint/issues/9174>

- **#9169** — Pylint treats tabs like spaces Pylint treats tabs like spaces. Spec.
  <https://github.com/pylint-dev/pylint/issues/9169>

- **#9162** — R1732(consider-using-with): Regression on `contextlib.ExitStack` R1732
  consider-using-with regression with contextlib.ExitStack. Spec.
  <https://github.com/pylint-dev/pylint/issues/9162>

- **#9161** — Pylint 3.0.1 | invalid-field-call | false positive (another) False
  positive invalid-field-call. Spec. <https://github.com/pylint-dev/pylint/issues/9161>

- **#9160** — import-private-name false positive False positive import-private-name.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/9160>

- **#9157** — attribute-defined-outside-init false positive for attribute defined on
  subclass after verifying clas False positive attribute-defined-outside-init on certain
  attr patterns. Spec. <https://github.com/pylint-dev/pylint/issues/9157>

- **#9153** — `no-member` check does not honor `sys.version_info` Spec: no-member
  doesn't honor sys.version_info guards. Related to deprecated-class issues
  #10043/#9533. <https://github.com/pylint-dev/pylint/issues/9153>

- **#9143** — Add pylint-junit reporter class Enhancement: add pylint-junit reporter
  class. Help-wanted. <https://github.com/pylint-dev/pylint/issues/9143>

- **#9134** — Pylint false report for used-before-assignment used-before-assignment
  false positive. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9134>

- **#9130** — Pylint 3.0.1 | invalid-field-call | false positive False positive
  invalid-field-call. Spec. <https://github.com/pylint-dev/pylint/issues/9130>

- **#9126** — used-before-assignment false positive False positive
  used-before-assignment. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9126>

- **#9125** — Usability improvment for `use-a-generator` in test assertion Enhancement:
  use-a-generator usability improvement in test assertions.
  <https://github.com/pylint-dev/pylint/issues/9125>

- **#9118** — Floating point logging format gives false error False positive
  logging-format-interpolation on floats. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/9118>

- **#9115** — Possible used-before-assignment false positive on type hinting identical
  to func names in class Possible used-before-assignment false positive on type hinting
  (no value). Spec/decision. <https://github.com/pylint-dev/pylint/issues/9115>

- **#9096** — `super-init-not-called` false positive in `.pyi` files .pyi false positive
  super-init-not-called. Spec/PR. <https://github.com/pylint-dev/pylint/issues/9096>

- **#9095** — False positive: unpacking-non-sequence after return False positive
  unpacking-non-sequence after return. Spec.
  <https://github.com/pylint-dev/pylint/issues/9095>

- **#9087** — False positive E1121 when using multiple inheritance and overriding class
  names False E1121 multiple inheritance + overload. Spec.
  <https://github.com/pylint-dev/pylint/issues/9087>

- **#9080** — Ellipsis in Protocol methods not recognized in 'assignment-from-no-return'
  on methods of dataclass m Ellipsis in Protocol methods false positive
  assignment-from-no-return. Spec. <https://github.com/pylint-dev/pylint/issues/9080>

- **#9063** — Add randomization to test suite to find test isolation problems
  Maintenance: add randomization to test suite. Internal.
  <https://github.com/pylint-dev/pylint/issues/9063>

- **#9058** — Do not raise `too-many-instance-attributes` on dataclasses or with a
  higher threshold Proposal: exempt dataclasses from too-many-instance-attributes. High
  priority discussion. <https://github.com/pylint-dev/pylint/issues/9058>

- **#9054** — Undeserved unexpected-line-ending-format on Windows Windows:
  unexpected-line-ending-format false positive. Platform-specific.
  <https://github.com/pylint-dev/pylint/issues/9054>

- **#9053** — docstyle doesn't work with --from-stdin docstyle extension doesn't work
  with --from-stdin. Internal. <https://github.com/pylint-dev/pylint/issues/9053>

- **#9052** — [pyreverse] Filtering out specific classes from diagrams Pyreverse Q:
  filtering classes from diagrams. Docs.
  <https://github.com/pylint-dev/pylint/issues/9052>

- **#9051** — E1131: unsupported operand type(s) for | (unsupported-binary-operation)
  Enhancement: E1131 unsupported-binary-operation with TypedDict. Spec.
  <https://github.com/pylint-dev/pylint/issues/9051>

- **#9040** — False positive with dataclasses when inheriting and using defaulted fields
  Dataclass inheritance + defaults: well-known false positive. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/9040>

- **#9018** — Determine if method is abstract using `__isabstractmethod__` instead of
  `abstractmethod` decorator Proposal: use **isabstractmethod** to detect abstract
  methods. Spec. <https://github.com/pylint-dev/pylint/issues/9018>

- **#9009** — False positive `access-member-before-definition` (E0203) if member is
  defined in parent class in dif False positive E0203 access-member-before-definition.
  Spec. <https://github.com/pylint-dev/pylint/issues/9009>

- **#8987** — False positive `protected-access` and `unused-private-member` with
  Singleton Pattern False positives protected-access and unused-private-member. Spec.
  <https://github.com/pylint-dev/pylint/issues/8987>

- **#8986** — `invalid-name` and `arguments-renamed` not triggered by constructor
  arguments in derived class invalid-name / arguments-renamed not triggered by
  const-typing-keyword override. Spec.
  <https://github.com/pylint-dev/pylint/issues/8986>

- **#8979** — unspecified-encoding should not be raised when PYTHONUTF8=1 Enhancement:
  unspecified-encoding should not fire when PYTHONUTF8=1. Spec/decision.
  <https://github.com/pylint-dev/pylint/issues/8979>

- **#8978** — False positive unnecessary-dunder-call for **iadd** False positive
  unnecessary-dunder-call for **iadd**. Spec.
  <https://github.com/pylint-dev/pylint/issues/8978>

- **#8972** — spelling-private-dict-file should be looked up relative to pylintrc file
  instead of current folder spelling-private-dict-file path resolution. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8972>

- **#8969** — Extend consider-using-f-string to string concatenations Enhancement:
  extend consider-using-f-string to concatenations. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8969>

- **#8968** — W1404: implicit-str-concat is not working with f strings W1404
  implicit-str-concat not detecting f-string concats. Astroid update.
  <https://github.com/pylint-dev/pylint/issues/8968>

- **#8955** — Weird redefined-variable-type warning for IntEnum redefined-variable-type
  warning for IntEnum. Spec. <https://github.com/pylint-dev/pylint/issues/8955>

- **#8944** — Way to avoid duplicated parameter types with docparams Enhancement:
  docparams - avoid duplicated parameter types with type hints. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8944>

- **#8939** — False positive invalid-overridden-method with decorator False positive
  invalid-overridden-method with custom decorator. Spec.
  <https://github.com/pylint-dev/pylint/issues/8939>

- **#8923** — False negative `redefined-outer-name` when an import aliased to `_` is
  redefined in a function False negative redefined-outer-name with import alias.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/8923>

- **#8913** — Potential lazy regex in default value if badly edited in the future +
  useless part Docs: lazy regex defaults can be edited badly. Docs.
  <https://github.com/pylint-dev/pylint/issues/8913>

- **#8912** — Fix all_options.rst Docs: fix all_options.rst issues. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/8912>

- **#8911** — unknown-option-value not emitted for config files under --jobs
  unknown-option-value not emitted under --jobs!=1. Internal.
  <https://github.com/pylint-dev/pylint/issues/8911>

- **#8909** — False-positive unreachable code for error-emitting generator
  False-positive unreachable code for generator with raise. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8909>

- **#8908** — `E1101 (no-member)` for wrong class with for partially implemented
  abstract `classmethod`? E1101 no-member for wrong class with partially implemented.
  Spec. <https://github.com/pylint-dev/pylint/issues/8908>

- **#8900** — False positive attribute-defined-outside-init when setting variant field
  False positive attribute-defined-outside-init when setting via descriptor. Spec.
  <https://github.com/pylint-dev/pylint/issues/8900>

- **#8890** — False positive: unneeded not False positive 'unneeded not'. Spec.
  <https://github.com/pylint-dev/pylint/issues/8890>

- **#8885** — Unignorable "invalid-name" when accessing "private" members Unignorable
  invalid-name on private members. Spec.
  <https://github.com/pylint-dev/pylint/issues/8885>

- **#8882** — Improve similarities checker by considering relative indentation of code
  blocks rather than absolute Enhancement: similarities checker — consider relative
  indentation. Design proposal. <https://github.com/pylint-dev/pylint/issues/8882>

- **#8880** — Redefined outer name not detected across modules when parallelization used
  redefined-outer-name not detected across modules under parallel. Spec.
  <https://github.com/pylint-dev/pylint/issues/8880>

- **#8879** — Issues with `invalid-name` Issues with invalid-name. Spec.
  <https://github.com/pylint-dev/pylint/issues/8879>

- **#8876** — False positive `E1101` when inheriting from tuple and using sorted
  function inside **new** dunder False positive E1101 inheriting from tuple + indexing.
  Spec. <https://github.com/pylint-dev/pylint/issues/8876>

- **#8870** — missing await and/or unused coroutine Enhancement: missing-await /
  unused-coroutine checker. Spec/PR. <https://github.com/pylint-dev/pylint/issues/8870>

- **#8869** — R6003 does not apply to "quick" top-level type definition R6003 doesn't
  apply to quick top-level type def. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8869>

- **#8865** — False positive `R0903: Too few public methods (0/1)` when using generics
  and shim imports False R0903 too-few-public-methods using NewType. Spec.
  <https://github.com/pylint-dev/pylint/issues/8865>

- **#8848** — Option to warn when logging format string is not a string literal
  Proposal: warn when logging format string is not a literal. Spec.
  <https://github.com/pylint-dev/pylint/issues/8848>

- **#8831** — unused-import false positive when using type union in annotations False
  positive unused-import with type union in annotation. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/8831>

- **#8806** — `disable=too-many-statements` sometimes not working
  disable=too-many-statements sometimes not working. Spec.
  <https://github.com/pylint-dev/pylint/issues/8806>
