# REPRO cluster audit — 181 confirmed-reproducing bugs

All 181 open issues with verdict REPRO in `.triage/triage_state.json`, partitioned into
mutually-exclusive primary clusters by subsystem. The clustering is heuristic (based on
issue title, labels, and reproduction notes) — each issue lands in exactly one bucket,
even if it cross-cuts. The goal is to surface where the biggest unfixed surface lives,
not to formally categorize every bug.

Companion to `FIXED_AUDIT.md` (fixed issues + regression tests), `DUP_AUDIT.md` (4 dup
pairs), `UNCLEAR_AUDIT.md` (9 unclear), and `EXTERNAL_PLUGINS_AUDIT.md` (73 big
enhancements covered externally).

## Summary

| Cluster                                                                                 |   Count | Notes |
| --------------------------------------------------------------------------------------- | ------: | ----- |
| **Crashes (F0002 astroid-error / AstroidBuildingError / RecursionError)**               |      10 |       |
| **Typing / generics / PEP 695**                                                         |      31 |       |
| **Control flow (used-before-assignment, possibly-used-before-assignment, unreachable)** |      31 |       |
| **Refactor / "consider-using" / "unnecessary-_" / "useless-_" suggestions**             |      20 |       |
| **Function-signature checks (E1120 / E1121 / E1123 / arguments-differ / unpacking)**    |      17 |       |
| **no-member / no-name-in-module / unsubscriptable-object**                              |      15 |       |
| **Dataclasses / pydantic / attrs**                                                      |       8 |       |
| **Decorators**                                                                          |       8 |       |
| **Enum / IntEnum / StrEnum**                                                            |       6 |       |
| **Import system / namespace packages / cyclic-import**                                  |       5 |       |
| **Naming / redefined-outer-name / shadow-builtin**                                      |       6 |       |
| **Walrus / assignment expression**                                                      |       4 |       |
| **Astroid inference (other)**                                                           |       3 |       |
| **Design metrics (too-many-_ / too-few-_)**                                             |       2 |       |
| **Abstract classes (W0223 / abstract-method)**                                          |       2 |       |
| **Exceptions (raising-bad-type / assignment-from-none)**                                |       2 |       |
| **Unused / dead**                                                                       |       1 |       |
| **PyReverse**                                                                           |       1 |       |
| **Pragma / disable / fixme**                                                            |       1 |       |
| **Match / case (PEP 634)**                                                              |       1 |       |
| **Docs / docparams**                                                                    |       1 |       |
| **Config / pylintrc / CLI**                                                             |       1 |       |
| **Other (one-off checker FPs)**                                                         |       5 |       |
| **Total**                                                                               | **181** |       |

## Top-line takeaways

- **Typing (31) + no-member (15) + dataclasses (8) + decorators (8) = 62 issues** —
  roughly a third of all confirmed-reproducing bugs are inference-engine / astroid-brain
  work. Many would resolve together with a single astroid release if the brain plugin
  maintainers got coordinated time.
- **Control flow (31)** is the second-largest cluster and tracks the long-pending design
  discussion in [#4795](https://github.com/pylint-dev/pylint/issues/4795). Until that
  lands, individual fixes are mostly point-patches.
- **Refactor suggestions (20)** are all in `RefactoringChecker` family and are good
  first-issue territory — each is a single-rule edge case.
- **Crashes (10)** are the highest-priority cluster. Worth their own milestone.
- **Arguments (17)** mostly need argument-resolution + unpacking-inference fixes.

## Per-cluster issue lists

### Crashes (F0002 astroid-error / AstroidBuildingError / RecursionError) (10)

Actionable: each issue here is a pylint crash on user code. Highest priority for any
release. Includes the funkwhale site-builtin shadowing pattern
([#8079](https://github.com/pylint-dev/pylint/issues/8079)).

- [#10813](https://github.com/pylint-dev/pylint/issues/10813) — Improper handling of log
  message format bytestrings
- [#10519](https://github.com/pylint-dev/pylint/issues/10519) — Crash with
  AstroidBuildingError when inheriting from a generic dataclass that has
  **init_subclass**
- [#10099](https://github.com/pylint-dev/pylint/issues/10099) — Crash in
  `consider-using-enumerate` when using `len(range())` and using the index to access an
  element of a list inside and element of a list
- [#10014](https://github.com/pylint-dev/pylint/issues/10014) — Crash
  `Building error when trying to create ast representation of module 'multiprocessing.process'`
- [#8755](https://github.com/pylint-dev/pylint/issues/8755) — Recursive defining a
  function with classmethod decorator triggers crashing
- [#8746](https://github.com/pylint-dev/pylint/issues/8746) — Defining
  collections.namedtuple object trigger an AstroidError
- [#8739](https://github.com/pylint-dev/pylint/issues/8739) — Unfound
  astroid.exceptions.InferenceError causes a crash
- [#8079](https://github.com/pylint-dev/pylint/issues/8079) — Pylint is crashing with
  astroid.exceptions.StatementMissing: Statement not found on <Module.builtins l.0
- [#3602](https://github.com/pylint-dev/pylint/issues/3602) — Maximum recursion depth
  crash with pyreverse `-S` option
- [#22](https://github.com/pylint-dev/pylint/issues/22) — Pyreverse: ValueError: need
  more than 1 value to unpack

### Typing / generics / PEP 695 (31)

False positives and negatives in pylint's handling of `typing.*`, PEP 695 generics,
`TypeVar` / `ParamSpec` / `TypeAliasType` / `TypeGuard`, `Self`, `Protocol`,
`@overload`, `Literal`, `TypedDict`, etc. The largest cluster — most of these need
astroid brain updates rather than pylint checker changes.

- [#10972](https://github.com/pylint-dev/pylint/issues/10972) — Abstract method
  false-positive when using TypeVarTuple
- [#10807](https://github.com/pylint-dev/pylint/issues/10807) — pylint fails to resolve
  typing.Self from base classes
- [#10784](https://github.com/pylint-dev/pylint/issues/10784) — Type narrowing fails due
  to unrelated instance assignment
- [#10360](https://github.com/pylint-dev/pylint/issues/10360) — False positive E1136:
  unsubscriptable-object when generic class defines **class_getitem**
- [#10186](https://github.com/pylint-dev/pylint/issues/10186) — False positive with
  `arguments-differ` rule in overridden overloaded methods in subclass
- [#10158](https://github.com/pylint-dev/pylint/issues/10158) — False positive on
  **required** and **optional** on TypedDict.
- [#10091](https://github.com/pylint-dev/pylint/issues/10091) — Class 'str' has no
  '**value**' member on PEP 695 TypeAliasType
- [#10042](https://github.com/pylint-dev/pylint/issues/10042) — False positive on
  not-callable when inheriting from `typing.IO`
- [#10031](https://github.com/pylint-dev/pylint/issues/10031) — False-positive E1101
  (no-member) inheriting from `set[int]`
- [#9908](https://github.com/pylint-dev/pylint/issues/9908) — False positive E1126
  (invalid-sequence-index) on generic type alias with forward ref
- [#9884](https://github.com/pylint-dev/pylint/issues/9884) — `redefined-outer-name`
  (`W0621`) - false positive on 3.12 type aliases
- [#9319](https://github.com/pylint-dev/pylint/issues/9319) — False positive for
  `unnecessary-ellipsis` on `Protocol` methods
- [#9222](https://github.com/pylint-dev/pylint/issues/9222) — False positive
  `duplicate-bases` with `TypedDict`
- [#9159](https://github.com/pylint-dev/pylint/issues/9159) — pylint does not support
  typing.Self when override
- [#8687](https://github.com/pylint-dev/pylint/issues/8687) — False-positive W0236 (and
  W0221) when implementing an optional protocol method
- [#8600](https://github.com/pylint-dev/pylint/issues/8600) — protected-access false
  positive with Generic classes
- [#8499](https://github.com/pylint-dev/pylint/issues/8499) — invalid-name check for
  TypeVar should allow for digits in names
- [#8455](https://github.com/pylint-dev/pylint/issues/8455) — False positive `no-member`
  for `TypeAlias` `__origin__`
- [#8331](https://github.com/pylint-dev/pylint/issues/8331) — Incorrect type inferance
  after a conditional raise
- [#8213](https://github.com/pylint-dev/pylint/issues/8213) — False negative for
  `isinstance-second-argument-not-valid-type` (parameterized generic)
- [#8022](https://github.com/pylint-dev/pylint/issues/8022) — Generic type of setter is
  leaking across instances
- [#7978](https://github.com/pylint-dev/pylint/issues/7978) — Incorrect
  unsupported-membership-test error on TypedDict
- [#7934](https://github.com/pylint-dev/pylint/issues/7934) — Missing Class Docstring
  false positive when inheriting from a generic class of a TypedDict instance
- [#7548](https://github.com/pylint-dev/pylint/issues/7548) — unused-import false
  positive for names in string argument to typing.cast
- [#7379](https://github.com/pylint-dev/pylint/issues/7379) — False positive no-member
  on member of generic parent class with overridden **class_getitem**
- [#5761](https://github.com/pylint-dev/pylint/issues/5761) — False positive
  invalid-overridden-method for async generators overriding AsyncIterable
- [#4944](https://github.com/pylint-dev/pylint/issues/4944) — False positive: Tuple
  claimed unsubscriptable when using NewType
- [#4070](https://github.com/pylint-dev/pylint/issues/4070) — False positive no-member
  for NamedTuple.\_replace()
- [#2855](https://github.com/pylint-dev/pylint/issues/2855) — Classvar[Optional[Tuple]]
  must be unpacked
- [#2647](https://github.com/pylint-dev/pylint/issues/2647) — Pylint gets confused by
  functools.singledispatch and assumes wrong return types of its registered functions.
- [#2296](https://github.com/pylint-dev/pylint/issues/2296) — False positive
  not-an-iterable for typing.NewType

### Control flow (used-before-assignment, possibly-used-before-assignment, unreachable) (31)

False positives / negatives in the variable checker's `NamesConsumer` machinery and the
unreachable-code analysis. Related design discussion:
[#4795](https://github.com/pylint-dev/pylint/issues/4795).

- [#10847](https://github.com/pylint-dev/pylint/issues/10847) —
  possibly-used-before-assignment false negative when variable has type annotation
- [#10471](https://github.com/pylint-dev/pylint/issues/10471) — Property union type
  inference issue: E1102 not-callable false positive
- [#10460](https://github.com/pylint-dev/pylint/issues/10460) — False positive
  `ungrouped-imports` with if os.name
- [#10195](https://github.com/pylint-dev/pylint/issues/10195) — False positive
  `used-before-assignment`
- [#10055](https://github.com/pylint-dev/pylint/issues/10055) — W0640 cell-var-from-loop
  false positive in Generator Comprehension of functions
- [#10043](https://github.com/pylint-dev/pylint/issues/10043) — [deprecated-x] Message
  trigger even in old interpreter compatibility code
- [#9689](https://github.com/pylint-dev/pylint/issues/9689) — False positive E0601:
  used-before-assignment in try and while block
- [#8686](https://github.com/pylint-dev/pylint/issues/8686) — `used-before-assignment`
  for assignment in inner try when outer try returns
- [#8495](https://github.com/pylint-dev/pylint/issues/8495) — False negative for
  NameError from calling inner function before variable is assigned
- [#8394](https://github.com/pylint-dev/pylint/issues/8394) — W0631: Using possibly
  undefined loop variable (undefined-loop-variable)
- [#8221](https://github.com/pylint-dev/pylint/issues/8221) — cell-var-from-loop ignores
  generator expressions
- [#8215](https://github.com/pylint-dev/pylint/issues/8215) — Spurious
  'undefined-variable' warning with postponed annotations enabled
- [#8145](https://github.com/pylint-dev/pylint/issues/8145) — `undefined-variable` false
  positive when method returns instance type when the class is inside a function
- [#7720](https://github.com/pylint-dev/pylint/issues/7720) — undefined-variable
  regression since 2.6.0
- [#7614](https://github.com/pylint-dev/pylint/issues/7614) — False positive for
  repeated-keywords when dict item is popped off
- [#7545](https://github.com/pylint-dev/pylint/issues/7545) — False positive
  `used-before-assignment` with multi-item `with` statement and tuple target
- [#7460](https://github.com/pylint-dev/pylint/issues/7460) — False negative: expected
  undefined-variable when deleted variable used
- [#7293](https://github.com/pylint-dev/pylint/issues/7293) — False positive for
  unexpected-keyword-arg using `**` operator
- [#7282](https://github.com/pylint-dev/pylint/issues/7282) — E1101
  false-positive/-negtive when mutating typess of dictionary values
- [#5955](https://github.com/pylint-dev/pylint/issues/5955) — `used-before-assignment`
  false positive on multiple-target assignment
- [#5671](https://github.com/pylint-dev/pylint/issues/5671) — False
  `unbalanced-tuple-unpacking` report
- [#5085](https://github.com/pylint-dev/pylint/issues/5085) — Negation and None
- [#4968](https://github.com/pylint-dev/pylint/issues/4968) — False positive
  'not-an-iterable' when using deferred initialization in a property
- [#4066](https://github.com/pylint-dev/pylint/issues/4066) — False positive
  used-before-assignment for return type
- [#3745](https://github.com/pylint-dev/pylint/issues/3745) — False positive
  method-hidden in overridden methods
- [#3641](https://github.com/pylint-dev/pylint/issues/3641) — False negative
  `undefined-variable` for decorators in multiple scenario
- [#3045](https://github.com/pylint-dev/pylint/issues/3045) — false positive:
  unsupported-membership-test
- [#2633](https://github.com/pylint-dev/pylint/issues/2633) — Strange Emit of E0601
  where something about shadowing a global would be clearer
- [#2621](https://github.com/pylint-dev/pylint/issues/2621) — Invalid report about
  "Possible unbalanced tuple unpacking"
- [#2072](https://github.com/pylint-dev/pylint/issues/2072) — Unstable result of
  unsubscriptable-object error within if/elif/else block
- [#841](https://github.com/pylint-dev/pylint/issues/841) — false redefined-outer-name
  when using `del`

### Refactor / "consider-using" / "unnecessary-_" / "useless-_" suggestions (20)

Issues against the suggest-refactor checkers — wrong fixes proposed, missed cases, edge
cases not covered. Touches `RefactoringChecker`, `ImplicitBooleanityChecker`, and the
consider-using-\* family.

- [#10113](https://github.com/pylint-dev/pylint/issues/10113) — findings not reported
  until seemingly unrelated code is changed
- [#10084](https://github.com/pylint-dev/pylint/issues/10084) — False negative
  `superfluous-parens` when around two conditional and an `and`
- [#10032](https://github.com/pylint-dev/pylint/issues/10032) —
  consider-using-augmented-assign false-positive for multiple dictionaries and string
  keys
- [#9994](https://github.com/pylint-dev/pylint/issues/9994) — False positive:
  useless-parent-delegation on '**init**' method of class derived from 'Exception'
- [#9878](https://github.com/pylint-dev/pylint/issues/9878) — C0325 (superfluous-parens)
  appears to not trigger when contents are a string
- [#9741](https://github.com/pylint-dev/pylint/issues/9741) — False positive
  unnecessary-negation for float comparison
- [#9359](https://github.com/pylint-dev/pylint/issues/9359) — useless-parent-delegation
  false positive when **init** signatures differ but parent is built-in type
- [#8577](https://github.com/pylint-dev/pylint/issues/8577) —
  `unnecessary-comprehension` false positive
- [#8265](https://github.com/pylint-dev/pylint/issues/8265) — False positive `C2801`
  `unnecessary-dunder-call` for descriptor binding `__get__`
- [#8256](https://github.com/pylint-dev/pylint/issues/8256) — Unnecessary use of a
  comprehension: Wrong fix
- [#8224](https://github.com/pylint-dev/pylint/issues/8224) — consider-using-f-string is
  triggered in a functional context
- [#8201](https://github.com/pylint-dev/pylint/issues/8201) — False negative
  `trailing-comma-tuple`
- [#8129](https://github.com/pylint-dev/pylint/issues/8129) — False positive
  `expression-not-assigned` when calling functions with no return inside ternary
  expression
- [#7997](https://github.com/pylint-dev/pylint/issues/7997) — False Positive
  `dict-init-mutate` when dict assignment references dict
- [#7271](https://github.com/pylint-dev/pylint/issues/7271) — consider-using-generator /
  R1728 false positive for "AsyncGenerator" valid code
- [#6663](https://github.com/pylint-dev/pylint/issues/6663) — False positive for
  `implicit-str-concat` when some but not all strings are raw
- [#5889](https://github.com/pylint-dev/pylint/issues/5889) — False positive for
  `try-except-raise` with diamond inheritance
- [#3668](https://github.com/pylint-dev/pylint/issues/3668) — False-positive
  unneeded-not when comparing dict views
- [#3367](https://github.com/pylint-dev/pylint/issues/3367) — Unexpected suppression of
  line-too-long messages
- [#241](https://github.com/pylint-dev/pylint/issues/241) — Incorrect W0611 : Unused
  import when preceded by import as

### Function-signature checks (E1120 / E1121 / E1123 / arguments-differ / unpacking) (17)

Issues in argument-arity, keyword-argument, unpacking and
`arguments-differ`/`arguments-renamed` reporting. Includes `repeated-keyword`,
`unbalanced-dict-unpacking`, `unpacking-non-sequence`, `invalid-sequence-index`.

- [#10731](https://github.com/pylint-dev/pylint/issues/10731) — False Negative
  `no-value-for-parameter` for instances used inside of a class
- [#10029](https://github.com/pylint-dev/pylint/issues/10029) — Missing mandatory
  keyword argument (E1125) with explicit mandatory keywords and keyword dictionary
- [#9986](https://github.com/pylint-dev/pylint/issues/9986) — False positive
  `unbalanced-dict-unpacking`
- [#9683](https://github.com/pylint-dev/pylint/issues/9683) — False positive
  invalid-sequence-index using properties of range object as index
- [#8325](https://github.com/pylint-dev/pylint/issues/8325) — false-positive:
  no-value-for-parameter
- [#7424](https://github.com/pylint-dev/pylint/issues/7424) — invalid-sequence-index
  when unpacking a sequence of sequences
- [#7348](https://github.com/pylint-dev/pylint/issues/7348) — False positives for E1120
  and E1123 when instance method is overwritten
- [#6856](https://github.com/pylint-dev/pylint/issues/6856) — False negative
  `repeated-keyword` for builtin functions
- [#5793](https://github.com/pylint-dev/pylint/issues/5793) — arguments-differ: number
  of parameters was some number ... and is now the same number in overridden ...
- [#5637](https://github.com/pylint-dev/pylint/issues/5637) — option to treat
  `TYPE_CHECKING` as `True`, or add a separate variable
- [#4961](https://github.com/pylint-dev/pylint/issues/4961) — incorrect line number and
  missing module name for E0633 (and false-positive)
- [#4861](https://github.com/pylint-dev/pylint/issues/4861) — `repeated-keyword`
  false-positive when overriding existing dict keys
- [#4803](https://github.com/pylint-dev/pylint/issues/4803) — False positive
  unpacking-non-sequence on classmethod + property
- [#4546](https://github.com/pylint-dev/pylint/issues/4546) — False-positive
  no-value-for-parameter for some unpacked values of list-builtins
- [#4018](https://github.com/pylint-dev/pylint/issues/4018) —
  disable=unexpected-keyword-arg doesn't work when placed on line where keyword is
  specified
- [#3268](https://github.com/pylint-dev/pylint/issues/3268) — False positive
  no-value-for-parameter in metaclass
- [#2271](https://github.com/pylint-dev/pylint/issues/2271) — False positive for
  `redundant-keyword-arg` in class with `partial()` class attribute function

### no-member / no-name-in-module / unsubscriptable-object (15)

False E1101 / E0611 / E1136 reporting. Usually a missing astroid brain or a missing
inference fallback.

- [#10994](https://github.com/pylint-dev/pylint/issues/10994) — False positives when
  'type' builtin is overwritten
- [#10806](https://github.com/pylint-dev/pylint/issues/10806) — False positive for numpy
  2.4.0+
- [#10472](https://github.com/pylint-dev/pylint/issues/10472) — False positive no-member
- [#10193](https://github.com/pylint-dev/pylint/issues/10193) — Invalid
  no-name-in-module when shadowing a base module with an alias then calling a method
  named format on that alias
- [#10166](https://github.com/pylint-dev/pylint/issues/10166) — Instance of
  'DatetimeIndex' has no 'to_pydatetime' member Pylint (E1101:no-member)
- [#9203](https://github.com/pylint-dev/pylint/issues/9203) — `no-member` when creating
  an object through an inherited factory method
- [#8367](https://github.com/pylint-dev/pylint/issues/8367) — Incorrect type inferred
  when inner class definition closes over variable from outer class’s method
- [#7991](https://github.com/pylint-dev/pylint/issues/7991) — `no-member` error when
  accessing a sub class variable with `self` returned from a super class method
- [#7269](https://github.com/pylint-dev/pylint/issues/7269) — time.sleep false negative!
- [#5734](https://github.com/pylint-dev/pylint/issues/5734) — False-negative: missing
  'no-member' in case of private member function invoke without mangling
- [#5091](https://github.com/pylint-dev/pylint/issues/5091) — E1507
  (invalid-envvar-value) does not accept `builtins.str` as a valid type for `os.getenv`
  argument
- [#4908](https://github.com/pylint-dev/pylint/issues/4908) — Coroutine type inferred
  incorrectly
- [#3879](https://github.com/pylint-dev/pylint/issues/3879) — False positive no-member
  when accessing a mangled instance variable of a super class after calling the
  constructor of the super class
- [#3728](https://github.com/pylint-dev/pylint/issues/3728) — False positive no-member
  with sys.stdin.buffer.peek()
- [#3162](https://github.com/pylint-dev/pylint/issues/3162) — no-member false positive
  from NewType

### Dataclasses / pydantic / attrs (8)

Inference and checker issues around `@dataclass`, `kw_only`, `pydantic.BaseModel`,
`attrs` classes. Usually astroid brain work.

- [#10991](https://github.com/pylint-dev/pylint/issues/10991) — Unexpected kwarg
  false-positive when using TypeVarTuple
- [#10056](https://github.com/pylint-dev/pylint/issues/10056) — Second order inheritance
  of dataclasses with default values/`init=False` causes `E1120 no-value-for-parameter`
- [#9972](https://github.com/pylint-dev/pylint/issues/9972) — False positive `no-member`
  when wrapping dataclasses `field`
- [#9488](https://github.com/pylint-dev/pylint/issues/9488) — Unexpected keyword
  argument for Generic dataclass with ABC bounded TypeVar
- [#9389](https://github.com/pylint-dev/pylint/issues/9389) — False-positive E1121 when
  using dataclass with init=False
- [#9183](https://github.com/pylint-dev/pylint/issues/9183) — False positive: Class has
  no '**dataclass_fields**' member (no-member)
- [#7296](https://github.com/pylint-dev/pylint/issues/7296) — pylint doesn't know
  re.Pattern members
- [#5810](https://github.com/pylint-dev/pylint/issues/5810) — How to fix pylint E1134:
  Non-mapping value X is used in a mapping context (not-a-mapping)

### Decorators (8)

Issues where a decorator changes a function/class signature or type and pylint loses
track. Includes `@property`-like descriptors, `@cached_property`, `@functools.wraps`,
etc.

- [#10848](https://github.com/pylint-dev/pylint/issues/10848) — pylint does not honor
  decorator return type when using @ syntax
- [#9505](https://github.com/pylint-dev/pylint/issues/9505) — Changing the number of
  function arguments when using a decorator does not work.
- [#7487](https://github.com/pylint-dev/pylint/issues/7487) — False positive:
  `no-member` when inner function uses the `@classmethod` decorator
- [#5784](https://github.com/pylint-dev/pylint/issues/5784) — False positive for
  `unexpected-keyword-arg` for decorators with inner inner function
- [#5699](https://github.com/pylint-dev/pylint/issues/5699) — False positive:
  unsubscriptable-object when using classmethod and property together
- [#3957](https://github.com/pylint-dev/pylint/issues/3957) — Attributes added by a
  decorator are raised as missing members errors
- [#3586](https://github.com/pylint-dev/pylint/issues/3586) — false positive: E1111
  assignment-from-no-return when using function name "lazy"
- [#2578](https://github.com/pylint-dev/pylint/issues/2578) — Type changes in decorators
  are not detected

### Enum / IntEnum / StrEnum (6)

Enum handling — `from ... import` inside class body, `auto()`, `StrEnum`,
`_member_names_`, etc.

- [#10951](https://github.com/pylint-dev/pylint/issues/10951) — pylint does not
  recognise `from ... import` inside an `IntEnum` class body as producing enum members.
  It infers the members as `int` instead of `LogLevel`, causing a spurious
  `E1101: Instance of 'int' has no 'value' member (no-member)` error.
- [#10840](https://github.com/pylint-dev/pylint/issues/10840) — `invalid-envvar-value`
  does not support StrEnum
- [#10609](https://github.com/pylint-dev/pylint/issues/10609) — False positive E1121:
  Too many positional arguments error for Subclassed Enums instanciated with functional
  API
- [#9905](https://github.com/pylint-dev/pylint/issues/9905) — False positive
  `invalid-overridden-method` when overridding `Enum.value`
- [#9839](https://github.com/pylint-dev/pylint/issues/9839) — E0238 false positive when
  defining **slots** in IntEnum class
- [#8327](https://github.com/pylint-dev/pylint/issues/8327) —
  `isinstance-second-argument-not-valid-type` does not handle `Enum.enum`

### Import system / namespace packages / cyclic-import (5)

Issues in how pylint discovers and loads modules — namespace packages, `package.module`
vs `package/module.py`, ungrouped-imports, wrong-import-order, cyclic-import edge cases.

- [#10969](https://github.com/pylint-dev/pylint/issues/10969) — Pylint skipping
  similarly named project directory.
- [#10140](https://github.com/pylint-dev/pylint/issues/10140) — pylint only catching
  `cyclic-import` in parallel mode
- [#9977](https://github.com/pylint-dev/pylint/issues/9977) — `ungrouped-imports` /
  `wrong-import-order` : FP because only two isort's options are taken into account
- [#7452](https://github.com/pylint-dev/pylint/issues/7452) — False positive
  `import-self` when attempting relative import of misspelled submodule name in a
  package.
- [#4444](https://github.com/pylint-dev/pylint/issues/4444) — Linting fails if module
  contains module of the same name

### Naming / redefined-outer-name / shadow-builtin (6)

False positives / negatives in name shadowing checks. Often interacts with control flow.

- [#10768](https://github.com/pylint-dev/pylint/issues/10768) — Started getting "invalid
  name" errors on a module-level global variable after upgrade to pylint 4.0.4
- [#10766](https://github.com/pylint-dev/pylint/issues/10766) — False positive for
  constant naming style inside **main** block
- [#10679](https://github.com/pylint-dev/pylint/issues/10679) — False negatives for
  `disallowed-name` due to control flow in NameChecker
- [#5678](https://github.com/pylint-dev/pylint/issues/5678) — redefined-outer-name not
  emitted for names in enclosing namespace
- [#4993](https://github.com/pylint-dev/pylint/issues/4993) — Incorrect report
  "unused-import" when assigning to class attribute with the same name as the imported
  module.
- [#2589](https://github.com/pylint-dev/pylint/issues/2589) — redefined-outer-name when
  importing subpackage of package which is already imported in outer scope

### Walrus / assignment expression (4)

Bugs specific to `:=` — interaction with control flow, comprehensions, conditional
expressions.

- [#10691](https://github.com/pylint-dev/pylint/issues/10691) — Conflicting warnings
  R2004 from `pylint.extensions.magic_value` and R6103 from
  `pylint.extensions.code_style`
- [#8486](https://github.com/pylint-dev/pylint/issues/8486) — `used-before-assignment`
  when using `walrus operator(:=)` in dict, generator, some comprehensionswith function
- [#7538](https://github.com/pylint-dev/pylint/issues/7538) — False positive
  `used-before-assignment` with walrus operator inside binary operation
- [#5735](https://github.com/pylint-dev/pylint/issues/5735) — False positive
  'undefined-variable' with assignment expression in decorator

### Astroid inference (other) (3)

Inference issues that don't fall under a more specific cluster — typically need an
astroid brain fix.

- [#9850](https://github.com/pylint-dev/pylint/issues/9850) — AddressFamily and
  SocketKind are not visible in module socket
- [#9385](https://github.com/pylint-dev/pylint/issues/9385) — False-positive E1137
  (unsupported-assignment-operation) with np.empty_like
- [#7500](https://github.com/pylint-dev/pylint/issues/7500) — `not-callable` false
  positive for `types.FunctionType`

### Design metrics (too-many-_ / too-few-_) (2)

Issues in the design-constraint checkers.

- [#10348](https://github.com/pylint-dev/pylint/issues/10348) — False positive
  `too-few-public-methods` on property function calls and descriptors
- [#9519](https://github.com/pylint-dev/pylint/issues/9519) — [too-many-function-args]
  False negative when calling `super().__init__()` with non-self argument

### Abstract classes (W0223 / abstract-method) (2)

Issues in the abstract-method checker — false positives from non-`abc.ABC` bases, missed
abstract overrides.

- [#9979](https://github.com/pylint-dev/pylint/issues/9979) — W0223 does not get raised
  correctly
- [#7950](https://github.com/pylint-dev/pylint/issues/7950) — Subclasses of abstract
  class that do not inherit abc.ABC are considered abstract

### Exceptions (raising-bad-type / assignment-from-none) (2)

Issues around how pylint handles `raise` statements and exception classes.

- [#7853](https://github.com/pylint-dev/pylint/issues/7853) — False Positive -
  `assignment-from-none` raised when function not necessarily returns `None`
- [#4033](https://github.com/pylint-dev/pylint/issues/4033) — Initializer arguments not
  checked when raising exception with implicit instantiation.

### Unused / dead (1)

Issues in `unused-variable` / `unused-import` / dead-store reporting.

- [#10030](https://github.com/pylint-dev/pylint/issues/10030) — False positive
  `unused-import` when using union of types inside quotes

### PyReverse (1)

pyreverse-specific issues.

- [#9797](https://github.com/pylint-dev/pylint/issues/9797) — `pyreverse` should check
  that `klass` is still `ClassDef`

### Pragma / disable / fixme (1)

Issues in pragma parsing and rule-disable semantics.

- [#7625](https://github.com/pylint-dev/pylint/issues/7625) — Pylint disable working
  incorrectly

### Match / case (PEP 634) (1)

Issues with structural pattern matching.

- [#7470](https://github.com/pylint-dev/pylint/issues/7470) — False positive with
  match/case for `function-redefined`

### Docs / docparams (1)

Issues with the doc-string / `docparams` extension.

- [#6478](https://github.com/pylint-dev/pylint/issues/6478) — Docparams does not raise
  `differing-type-doc` for Sphinx documentation

### Config / pylintrc / CLI (1)

Configuration resolution issues.

- [#3325](https://github.com/pylint-dev/pylint/issues/3325) — False positive
  `attribute-defined-outside-init` when using properties

### Other (one-off checker FPs) (5)

Single-issue checker bugs that don't cluster with anything else.

- [#10201](https://github.com/pylint-dev/pylint/issues/10201) — W1514
  unspecified-encoding false positive when mode is specified using a variable and it can
  be 'b' (binary mode)
- [#10074](https://github.com/pylint-dev/pylint/issues/10074) — E1142 false & missed
  alarms
- [#9950](https://github.com/pylint-dev/pylint/issues/9950) — False positive
  `declare-non-slot` on classvar
- [#9533](https://github.com/pylint-dev/pylint/issues/9533) — False positive
  `deprecated-class` when the class is imported in a guarded import block
- [#8138](https://github.com/pylint-dev/pylint/issues/8138) — `not-callable` false
  positive for class

## Methodology

- **REPRO** = verdict in `.triage/triage_state.json` after 9 full triage sessions. Means
  the bug was reproduced on pylint 4.0.5 / astroid 4.0.2 / Python 3.12.3.
- **Clustering** = priority-ordered keyword + label matching against the issue title and
  the reproduction note. Order: crash > pyreverse > enum > dataclasses > match-case >
  walrus > typing > control-flow > decorators > arguments > no-member > imports >
  refactor > naming > closures > pragma > config > performance > docs > duplicate-code >
  design > unused > abstract > exceptions > astroid-inference > other. Source: same
  script that produced `.triage/repro_clusters.json`.
- **No "should this stay open" verdict per issue.** Every entry is already REPRO; this
  audit is purely about _grouping_, not re-triaging.
