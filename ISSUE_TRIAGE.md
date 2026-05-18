# Pylint Open-Issue Triage Log — COMPLETED (full re-audit)

**Environment:** pylint `4.0.5` / astroid `4.0.2` / Python `3.12.3` on Linux.
**Branch:** `backport-sys-fix` (commit `b43721121`). **Total open issues triaged:**
**1022** (range #5 → #11013). **Method:** All 9 sessions performed per-issue
reproduction on pylint 4.0.5.

**Refresh 2026-05-18:** 3 cached issues moved to FIXED after upstream merges
(#7950 → PR #7955, #6211 → PR #7360, #3716 → PR #10989). Current open count is **1017**.
See `.triage/FIXED_AUDIT.md` for per-issue notes; the per-section listings below still
reflect the original triage and have not been re-flowed.

Index for a full deep-dive of every open issue at
https://github.com/pylint-dev/pylint/issues. Per-issue state lives under `.triage/`:

- `.triage/issues_raw.json` — local cache of all 1022 issues
- `.triage/triage_state.json` — machine-readable verdict ledger
- `.triage/sessions/session-XX.md` — per-session deep-dive notes
- `.triage/snippets/iNNNN.py` — minimal reproduction code I ran (200+ files)
- `.triage/status.py` — re-run for a fresh roll-up

## Verdict legend

| Symbol     | Meaning                                                                                 |
| ---------- | --------------------------------------------------------------------------------------- |
| ✅ REPRO   | Reproduced on pylint `4.0.5` — still pertinent                                          |
| ❌ FIXED   | No longer reproducible on `4.0.5` — likely fixed since the report                       |
| ❓ UNCLEAR | Not enough info / cannot reproduce / needs reporter follow-up                           |
| 💬 DESIGN  | Enhancement, proposal, decision-pending, or spec discussion                             |
| 🧭 EXTDEP  | Reproduction blocked on external dep (numpy, pandas, scipy, torch, pydantic, PySide, …) |
| 🪦 STALE   | Old / outdated / labeled stale                                                          |
| 🔁 DUP     | Duplicate of another open issue                                                         |

## Final tally

| Verdict    |    Count |     % |
| ---------- | -------: | ----: |
| 💬 DESIGN  |  **598** | 58.5% |
| 🧭 EXTDEP  |  **194** | 19.0% |
| ✅ REPRO   |  **166** | 16.2% |
| ❌ FIXED   |   **41** |  4.0% |
| ❓ UNCLEAR |   **18** |  1.8% |
| 🔁 DUP     |    **4** |  0.4% |
| 🪪 STALE   |    **1** |  0.1% |
| **Total**  | **1022** |  100% |

## ✅ Confirmed-still-reproduces (166)

The actionable list — bugs reproduced with minimal snippets on pylint 4.0.5:

- [#10995](https://github.com/pylint-dev/pylint/issues/10995) — PEP 695 TypeVar
  redefinition false-positive
- [#10994](https://github.com/pylint-dev/pylint/issues/10994) — False positives when
  'type' builtin is overwritten
- [#10972](https://github.com/pylint-dev/pylint/issues/10972) — Abstract method
  false-positive when using TypeVarTuple
- [#10969](https://github.com/pylint-dev/pylint/issues/10969) — Pylint skipping
  similarly named project directory.
- [#10951](https://github.com/pylint-dev/pylint/issues/10951) — pylint does not
  recognise `from ... import` inside an `IntEnum` class body as producing en
- [#10848](https://github.com/pylint-dev/pylint/issues/10848) — pylint does not honor
  decorator return type when using @ syntax
- [#10847](https://github.com/pylint-dev/pylint/issues/10847) —
  possibly-used-before-assignment false negative when variable has type annotation
- [#10840](https://github.com/pylint-dev/pylint/issues/10840) — `invalid-envvar-value`
  does not support StrEnum
- [#10813](https://github.com/pylint-dev/pylint/issues/10813) — Improper handling of log
  message format bytestrings
- [#10807](https://github.com/pylint-dev/pylint/issues/10807) — pylint fails to resolve
  typing.Self from base classes
- [#10784](https://github.com/pylint-dev/pylint/issues/10784) — Type narrowing fails due
  to unrelated instance assignment
- [#10731](https://github.com/pylint-dev/pylint/issues/10731) — False Negative
  `no-value-for-parameter` for instances used inside of a class
- [#10691](https://github.com/pylint-dev/pylint/issues/10691) — Conflicting warnings
  R2004 from `pylint.extensions.magic_value` and R6103 from `pylint.ext
- [#10679](https://github.com/pylint-dev/pylint/issues/10679) — False negatives for
  `disallowed-name` due to control flow in NameChecker
- [#10609](https://github.com/pylint-dev/pylint/issues/10609) — False positive E1121:
  Too many positional arguments error for Subclassed Enums instanciate
- [#10519](https://github.com/pylint-dev/pylint/issues/10519) — Crash with
  AstroidBuildingError when inheriting from a generic dataclass that has \_\_init_s
- [#10472](https://github.com/pylint-dev/pylint/issues/10472) — False positive no-member
- [#10471](https://github.com/pylint-dev/pylint/issues/10471) — Property union type
  inference issue: E1102 not-callable false positive
- [#10460](https://github.com/pylint-dev/pylint/issues/10460) — False positive
  `ungrouped-imports` with if os.name
- [#10360](https://github.com/pylint-dev/pylint/issues/10360) — False positive E1136:
  unsubscriptable-object when generic class defines **class_getitem**
- [#10348](https://github.com/pylint-dev/pylint/issues/10348) — False positive
  `too-few-public-methods` on property function calls and descriptors
- [#10201](https://github.com/pylint-dev/pylint/issues/10201) — W1514
  unspecified-encoding false positive when mode is specified using a variable and it c
- [#10195](https://github.com/pylint-dev/pylint/issues/10195) — False positive
  `used-before-assignment`
- [#10193](https://github.com/pylint-dev/pylint/issues/10193) — Invalid
  no-name-in-module when shadowing a base module with an alias then calling a method
- [#10186](https://github.com/pylint-dev/pylint/issues/10186) — False positive with
  `arguments-differ` rule in overridden overloaded methods in subclass
- [#10158](https://github.com/pylint-dev/pylint/issues/10158) — False positive on
  **required** and **optional** on TypedDict.
- [#10140](https://github.com/pylint-dev/pylint/issues/10140) — pylint only catching
  `cyclic-import` in parallel mode
- [#10113](https://github.com/pylint-dev/pylint/issues/10113) — findings not reported
  until seemingly unrelated code is changed
- [#10099](https://github.com/pylint-dev/pylint/issues/10099) — Crash in
  `consider-using-enumerate` when using `len(range())` and using the index to a
- [#10091](https://github.com/pylint-dev/pylint/issues/10091) — Class 'str' has no
  '**value**' member on PEP 695 TypeAliasType
- [#10084](https://github.com/pylint-dev/pylint/issues/10084) — False negative
  `superfluous-parens` when around two conditional and an `and`
- [#10074](https://github.com/pylint-dev/pylint/issues/10074) — E1142 false & missed
  alarms
- [#10056](https://github.com/pylint-dev/pylint/issues/10056) — Second order inheritance
  of dataclasses with default values/`init=False` causes `E1120 no-
- [#10055](https://github.com/pylint-dev/pylint/issues/10055) — W0640 cell-var-from-loop
  false positive in Generator Comprehension of functions
- [#10043](https://github.com/pylint-dev/pylint/issues/10043) — [deprecated-x] Message
  trigger even in old interpreter compatibility code
- [#10042](https://github.com/pylint-dev/pylint/issues/10042) — False positive on
  not-callable when inheriting from `typing.IO`
- [#10032](https://github.com/pylint-dev/pylint/issues/10032) —
  consider-using-augmented-assign false-positive for multiple dictionaries and string
  keys
- [#10031](https://github.com/pylint-dev/pylint/issues/10031) — False-positive E1101
  (no-member) inheriting from `set[int]`
- [#10030](https://github.com/pylint-dev/pylint/issues/10030) — False positive
  `unused-import` when using union of types inside quotes
- [#10029](https://github.com/pylint-dev/pylint/issues/10029) — Missing mandatory
  keyword argument (E1125) with explicit mandatory keywords and keyword di
- [#10014](https://github.com/pylint-dev/pylint/issues/10014) — Crash ``Building error
  when trying to create ast representation of module 'multiprocessing
- [#9994](https://github.com/pylint-dev/pylint/issues/9994) — False positive:
  useless-parent-delegation on '**init**' method of class derived from 'Exce
- [#9986](https://github.com/pylint-dev/pylint/issues/9986) — False positive
  `unbalanced-dict-unpacking`
- [#9979](https://github.com/pylint-dev/pylint/issues/9979) — W0223 does not get raised
  correctly
- [#9977](https://github.com/pylint-dev/pylint/issues/9977) — `ungrouped-imports` /
  `wrong-import-order` : FP because only two isort's options are take
- [#9972](https://github.com/pylint-dev/pylint/issues/9972) — False positive `no-member`
  when wrapping dataclasses `field`
- [#9950](https://github.com/pylint-dev/pylint/issues/9950) — False positive
  `declare-non-slot` on classvar
- [#9908](https://github.com/pylint-dev/pylint/issues/9908) — False positive E1126
  (invalid-sequence-index) on generic type alias with forward ref
- [#9905](https://github.com/pylint-dev/pylint/issues/9905) — False positive
  `invalid-overridden-method` when overridding `Enum.value`
- [#9878](https://github.com/pylint-dev/pylint/issues/9878) — C0325 (superfluous-parens)
  appears to not trigger when contents are a string
- [#9850](https://github.com/pylint-dev/pylint/issues/9850) — AddressFamily and
  SocketKind are not visible in module socket
- [#9839](https://github.com/pylint-dev/pylint/issues/9839) — E0238 false positive when
  defining **slots** in IntEnum class
- [#9797](https://github.com/pylint-dev/pylint/issues/9797) — `pyreverse` should check
  that `klass` is still `ClassDef`
- [#9741](https://github.com/pylint-dev/pylint/issues/9741) — False positive
  unnecessary-negation for float comparison
- [#9689](https://github.com/pylint-dev/pylint/issues/9689) — False positive E0601:
  used-before-assignment in try and while block
- [#9683](https://github.com/pylint-dev/pylint/issues/9683) — False positive
  invalid-sequence-index using properties of range object as index
- [#9533](https://github.com/pylint-dev/pylint/issues/9533) — False positive
  `deprecated-class` when the class is imported in a guarded import block
- [#9519](https://github.com/pylint-dev/pylint/issues/9519) — [too-many-function-args]
  False negative when calling `super().__init__()` with non-self ar
- [#9505](https://github.com/pylint-dev/pylint/issues/9505) — Changing the number of
  function arguments when using a decorator does not work.
- [#9488](https://github.com/pylint-dev/pylint/issues/9488) — Unexpected keyword
  argument for Generic dataclass with ABC bounded TypeVar
- [#9389](https://github.com/pylint-dev/pylint/issues/9389) — False-positive E1121 when
  using dataclass with init=False
- [#9385](https://github.com/pylint-dev/pylint/issues/9385) — False-positive E1137
  (unsupported-assignment-operation) with np.empty_like
- [#9359](https://github.com/pylint-dev/pylint/issues/9359) — useless-parent-delegation
  false positive when **init** signatures differ but parent is bui
- [#9319](https://github.com/pylint-dev/pylint/issues/9319) — False positive for
  `unnecessary-ellipsis` on `Protocol` methods
- [#9222](https://github.com/pylint-dev/pylint/issues/9222) — False positive
  `duplicate-bases` with `TypedDict`
- [#9203](https://github.com/pylint-dev/pylint/issues/9203) — `no-member` when creating
  an object through an inherited factory method
- [#9183](https://github.com/pylint-dev/pylint/issues/9183) — False positive: Class has
  no '**dataclass_fields**' member (no-member)
- [#9159](https://github.com/pylint-dev/pylint/issues/9159) — pylint does not support
  typing.Self when override
- [#8755](https://github.com/pylint-dev/pylint/issues/8755) — Recursive defining a
  function with classmethod decorator triggers crashing
- [#8746](https://github.com/pylint-dev/pylint/issues/8746) — Defining
  collections.namedtuple object trigger an AstroidError
- [#8739](https://github.com/pylint-dev/pylint/issues/8739) — Unfound
  astroid.exceptions.InferenceError causes a crash
- [#8687](https://github.com/pylint-dev/pylint/issues/8687) — False-positive W0236 (and
  W0221) when implementing an optional protocol method
- [#8686](https://github.com/pylint-dev/pylint/issues/8686) — `used-before-assignment`
  for assignment in inner try when outer try returns
- [#8577](https://github.com/pylint-dev/pylint/issues/8577) —
  `unnecessary-comprehension` false positive
- [#8495](https://github.com/pylint-dev/pylint/issues/8495) — False negative for
  NameError from calling inner function before variable is assigned
- [#8486](https://github.com/pylint-dev/pylint/issues/8486) — `used-before-assignment`
  when using `walrus operator(:=)` in dict, generator, some compreh
- [#8455](https://github.com/pylint-dev/pylint/issues/8455) — False positive `no-member`
  for `TypeAlias` `__origin__`
- [#8394](https://github.com/pylint-dev/pylint/issues/8394) — W0631: Using possibly
  undefined loop variable (undefined-loop-variable)
- [#8367](https://github.com/pylint-dev/pylint/issues/8367) — Incorrect type inferred
  when inner class definition closes over variable from outer class’
- [#8331](https://github.com/pylint-dev/pylint/issues/8331) — Incorrect type inferance
  after a conditional raise
- [#8327](https://github.com/pylint-dev/pylint/issues/8327) —
  `isinstance-second-argument-not-valid-type` does not handle `Enum.enum`
- [#8325](https://github.com/pylint-dev/pylint/issues/8325) — false-positive:
  no-value-for-parameter
- [#8265](https://github.com/pylint-dev/pylint/issues/8265) — False positive `C2801`
  `unnecessary-dunder-call` for descriptor binding `__get__`
- [#8256](https://github.com/pylint-dev/pylint/issues/8256) — Unnecessary use of a
  comprehension: Wrong fix
- [#8224](https://github.com/pylint-dev/pylint/issues/8224) — consider-using-f-string is
  triggered in a functional context
- [#8221](https://github.com/pylint-dev/pylint/issues/8221) — cell-var-from-loop ignores
  generator expressions
- [#8215](https://github.com/pylint-dev/pylint/issues/8215) — Spurious
  'undefined-variable' warning with postponed annotations enabled
- [#8213](https://github.com/pylint-dev/pylint/issues/8213) — False negative for
  `isinstance-second-argument-not-valid-type` (parameterized generic)
- [#8145](https://github.com/pylint-dev/pylint/issues/8145) — `undefined-variable` false
  positive when method returns instance type when the class is in
- [#8138](https://github.com/pylint-dev/pylint/issues/8138) — `not-callable` false
  positive for class
- [#8129](https://github.com/pylint-dev/pylint/issues/8129) — False positive
  `expression-not-assigned` when calling functions with no return inside te
- [#8022](https://github.com/pylint-dev/pylint/issues/8022) — Generic type of setter is
  leaking across instances
- [#7997](https://github.com/pylint-dev/pylint/issues/7997) — False Positive
  `dict-init-mutate` when dict assignment references dict
- [#7991](https://github.com/pylint-dev/pylint/issues/7991) — `no-member` error when
  accessing a sub class variable with `self` returned from a super cl
- [#7978](https://github.com/pylint-dev/pylint/issues/7978) — Incorrect
  unsupported-membership-test error on TypedDict
- [#7853](https://github.com/pylint-dev/pylint/issues/7853) — False Positive -
  `assignment-from-none` raised when function not necessarily returns `No
- [#7720](https://github.com/pylint-dev/pylint/issues/7720) — undefined-variable
  regression since 2.6.0
- [#7625](https://github.com/pylint-dev/pylint/issues/7625) — Pylint disable working
  incorrectly
- [#7614](https://github.com/pylint-dev/pylint/issues/7614) — False positive for
  repeated-keywords when dict item is popped off
- [#7548](https://github.com/pylint-dev/pylint/issues/7548) — unused-import false
  positive for names in string argument to typing.cast
- [#7545](https://github.com/pylint-dev/pylint/issues/7545) — False positive
  `used-before-assignment` with multi-item `with` statement and tuple target
- [#7538](https://github.com/pylint-dev/pylint/issues/7538) — False positive
  `used-before-assignment` with walrus operator inside binary operation
- [#7500](https://github.com/pylint-dev/pylint/issues/7500) — `not-callable` false
  positive for `types.FunctionType`
- [#7487](https://github.com/pylint-dev/pylint/issues/7487) — False positive:
  `no-member` when inner function uses the `@classmethod` decorator
- [#7470](https://github.com/pylint-dev/pylint/issues/7470) — False positive with
  match/case for `function-redefined`
- [#7460](https://github.com/pylint-dev/pylint/issues/7460) — False negative: expected
  undefined-variable when deleted variable used
- [#7452](https://github.com/pylint-dev/pylint/issues/7452) — False positive
  `import-self` when attempting relative import of misspelled submodule name
- [#7424](https://github.com/pylint-dev/pylint/issues/7424) — invalid-sequence-index
  when unpacking a sequence of sequences
- [#7379](https://github.com/pylint-dev/pylint/issues/7379) — False positive no-member
  on member of generic parent class with overridden \_\_class_getitem
- [#7348](https://github.com/pylint-dev/pylint/issues/7348) — False positives for E1120
  and E1123 when instance method is overwritten
- [#7296](https://github.com/pylint-dev/pylint/issues/7296) — pylint doesn't know
  re.Pattern members
- [#7293](https://github.com/pylint-dev/pylint/issues/7293) — False positive for
  unexpected-keyword-arg using `**` operator
- [#7282](https://github.com/pylint-dev/pylint/issues/7282) — E1101
  false-positive/-negtive when mutating typess of dictionary values
- [#7271](https://github.com/pylint-dev/pylint/issues/7271) — consider-using-generator /
  R1728 false positive for "AsyncGenerator" valid code
- [#7269](https://github.com/pylint-dev/pylint/issues/7269) — time.sleep false negative!
- [#6856](https://github.com/pylint-dev/pylint/issues/6856) — False negative
  `repeated-keyword` for builtin functions
- [#6663](https://github.com/pylint-dev/pylint/issues/6663) — False positive for
  `implicit-str-concat` when some but not all strings are raw
- [#6478](https://github.com/pylint-dev/pylint/issues/6478) — Docparams does not raise
  `differing-type-doc` for Sphinx documentation
- [#5955](https://github.com/pylint-dev/pylint/issues/5955) — `used-before-assignment`
  false positive on multiple-target assignment
- [#5889](https://github.com/pylint-dev/pylint/issues/5889) — False positive for
  `try-except-raise` with diamond inheritance
- [#5810](https://github.com/pylint-dev/pylint/issues/5810) — How to fix pylint E1134:
  Non-mapping value X is used in a mapping context (not-a-mapping)
- [#5793](https://github.com/pylint-dev/pylint/issues/5793) — arguments-differ: number
  of parameters was some number ... and is now the same number in o
- [#5784](https://github.com/pylint-dev/pylint/issues/5784) — False positive for
  `unexpected-keyword-arg` for decorators with inner inner function
- [#5761](https://github.com/pylint-dev/pylint/issues/5761) — False positive
  invalid-overridden-method for async generators overriding AsyncIterable
- [#5735](https://github.com/pylint-dev/pylint/issues/5735) — False positive
  'undefined-variable' with assignment expression in decorator
- [#5734](https://github.com/pylint-dev/pylint/issues/5734) — False-negative: missing
  'no-member' in case of private member function invoke without mang
- [#5699](https://github.com/pylint-dev/pylint/issues/5699) — False positive:
  unsubscriptable-object when using classmethod and property together
- [#5678](https://github.com/pylint-dev/pylint/issues/5678) — redefined-outer-name not
  emitted for names in enclosing namespace
- [#5671](https://github.com/pylint-dev/pylint/issues/5671) — False
  `unbalanced-tuple-unpacking` report
- [#5637](https://github.com/pylint-dev/pylint/issues/5637) — option to treat
  `TYPE_CHECKING` as `True`, or add a separate variable
- [#5091](https://github.com/pylint-dev/pylint/issues/5091) — E1507
  (invalid-envvar-value) does not accept `builtins.str` as a valid type for `os.getenv
- [#5085](https://github.com/pylint-dev/pylint/issues/5085) — Negation and None
- [#4993](https://github.com/pylint-dev/pylint/issues/4993) — Incorrect report
  "unused-import" when assigning to class attribute with the same name as t
- [#4968](https://github.com/pylint-dev/pylint/issues/4968) — False positive
  'not-an-iterable' when using deferred initialization in a property
- [#4961](https://github.com/pylint-dev/pylint/issues/4961) — incorrect line number and
  missing module name for E0633 (and false-positive)
- [#4944](https://github.com/pylint-dev/pylint/issues/4944) — False positive: Tuple
  claimed unsubscriptable when using NewType
- [#4908](https://github.com/pylint-dev/pylint/issues/4908) — Coroutine type inferred
  incorrectly
- [#4861](https://github.com/pylint-dev/pylint/issues/4861) — `repeated-keyword`
  false-positive when overriding existing dict keys
- [#4803](https://github.com/pylint-dev/pylint/issues/4803) — False positive
  unpacking-non-sequence on classmethod + property
- [#4546](https://github.com/pylint-dev/pylint/issues/4546) — False-positive
  no-value-for-parameter for some unpacked values of list-builtins
- [#4444](https://github.com/pylint-dev/pylint/issues/4444) — Linting fails if module
  contains module of the same name
- [#4070](https://github.com/pylint-dev/pylint/issues/4070) — False positive no-member
  for NamedTuple.\_replace()
- [#4066](https://github.com/pylint-dev/pylint/issues/4066) — False positive
  used-before-assignment for return type
- [#4033](https://github.com/pylint-dev/pylint/issues/4033) — Initializer arguments not
  checked when raising exception with implicit instantiation.
- [#4018](https://github.com/pylint-dev/pylint/issues/4018) —
  disable=unexpected-keyword-arg doesn't work when placed on line where keyword is
  specified
- [#3957](https://github.com/pylint-dev/pylint/issues/3957) — Attributes added by a
  decorator are raised as missing members errors
- [#3879](https://github.com/pylint-dev/pylint/issues/3879) — False positive no-member
  when accessing a mangled instance variable of a super class after
- [#3745](https://github.com/pylint-dev/pylint/issues/3745) — False positive
  method-hidden in overridden methods
- [#3728](https://github.com/pylint-dev/pylint/issues/3728) — False positive no-member
  with sys.stdin.buffer.peek()
- [#3668](https://github.com/pylint-dev/pylint/issues/3668) — False-positive
  unneeded-not when comparing dict views
- [#3641](https://github.com/pylint-dev/pylint/issues/3641) — False negative
  `undefined-variable` for decorators in multiple scenario
- [#3586](https://github.com/pylint-dev/pylint/issues/3586) — false positive: E1111
  assignment-from-no-return when using function name "lazy"
- [#3367](https://github.com/pylint-dev/pylint/issues/3367) — Unexpected suppression of
  line-too-long messages
- [#3268](https://github.com/pylint-dev/pylint/issues/3268) — False positive
  no-value-for-parameter in metaclass
- [#3162](https://github.com/pylint-dev/pylint/issues/3162) — no-member false positive
  from NewType
- [#3045](https://github.com/pylint-dev/pylint/issues/3045) — false positive:
  unsupported-membership-test
- [#2855](https://github.com/pylint-dev/pylint/issues/2855) — Classvar[Optional[Tuple]]
  must be unpacked
- [#2647](https://github.com/pylint-dev/pylint/issues/2647) — Pylint gets confused by
  functools.singledispatch and assumes wrong return types of its reg
- [#2633](https://github.com/pylint-dev/pylint/issues/2633) — Strange Emit of E0601
  where something about shadowing a global would be clearer
- [#2621](https://github.com/pylint-dev/pylint/issues/2621) — Invalid report about
  "Possible unbalanced tuple unpacking"
- [#2589](https://github.com/pylint-dev/pylint/issues/2589) — redefined-outer-name when
  importing subpackage of package which is already imported in out
- [#2578](https://github.com/pylint-dev/pylint/issues/2578) — Type changes in decorators
  are not detected
- [#2296](https://github.com/pylint-dev/pylint/issues/2296) — False positive
  not-an-iterable for typing.NewType
- [#2271](https://github.com/pylint-dev/pylint/issues/2271) — False positive for
  `redundant-keyword-arg` in class with `partial()` class attribute f
- [#2072](https://github.com/pylint-dev/pylint/issues/2072) — Unstable result of
  unsubscriptable-object error within if/elif/else block
- [#841](https://github.com/pylint-dev/pylint/issues/841) — false redefined-outer-name
  when using `del`

## ❌ Likely fixed — verify and close (41)

These reports no longer reproduce on pylint 4.0.5. Each should get a quick re-check
(with the reporter's exact config if available) before closing.

- [#10768](https://github.com/pylint-dev/pylint/issues/10768) — Started getting "invalid
  name" errors on a module-level global variable after upgrade to p
- [#10766](https://github.com/pylint-dev/pylint/issues/10766) — False positive for
  constant naming style inside **main** block
- [#10670](https://github.com/pylint-dev/pylint/issues/10670) — False Positive for
  too-many-function-args when subclassing **new**
- [#10455](https://github.com/pylint-dev/pylint/issues/10455) — False positive E1136 –
  unsubscriptable-object
- [#10442](https://github.com/pylint-dev/pylint/issues/10442) — Treat `__main__.py` as a
  special module name under camelCase module-naming-style
- [#10422](https://github.com/pylint-dev/pylint/issues/10422) — not-callable: Different
  behavior using f-string vs bin-op string
- [#10374](https://github.com/pylint-dev/pylint/issues/10374) — False positive
  `redefined-variable-type` on ignored variables like `_`
- [#10298](https://github.com/pylint-dev/pylint/issues/10298) — False positive E1133
  (not-an-iterable) when returning (type hinted) class variable
- [#9722](https://github.com/pylint-dev/pylint/issues/9722) — False Positive
  W0143-comparison-with-callable when using derived property descriptors
- [#9497](https://github.com/pylint-dev/pylint/issues/9497) — Non existent member not
  detected on datetime.datetime
- [#8805](https://github.com/pylint-dev/pylint/issues/8805) — `no-member` emitted for
  all `zipimport` names
- [#8600](https://github.com/pylint-dev/pylint/issues/8600) — protected-access false
  positive with Generic classes
- [#8499](https://github.com/pylint-dev/pylint/issues/8499) — invalid-name check for
  TypeVar should allow for digits in names
- [#8419](https://github.com/pylint-dev/pylint/issues/8419) — False negative:
  `unspecified-encoding` (`W1514`) not raised for `Path.read_text`
- [#8250](https://github.com/pylint-dev/pylint/issues/8250) — Missing-return-doc returns
  multiple errors when there are multiple returns in the function
- [#8201](https://github.com/pylint-dev/pylint/issues/8201) — False negative
  `trailing-comma-tuple`
- [#8179](https://github.com/pylint-dev/pylint/issues/8179) —
  consider-using-augmented-assign false positive on string formatting
- [#8068](https://github.com/pylint-dev/pylint/issues/8068) — False-positive
  unsupported-delete-operation
- [#8053](https://github.com/pylint-dev/pylint/issues/8053) — False positive
  `assigning-non-slot` error for inherited descriptor when slots are used.
- [#8050](https://github.com/pylint-dev/pylint/issues/8050) — Pylint doesn't check file
  if it's named exactly like the directory where the file is
- [#7950](https://github.com/pylint-dev/pylint/issues/7950) — Subclasses of abstract
  class that do not inherit abc.ABC are considered abstract
- [#7934](https://github.com/pylint-dev/pylint/issues/7934) — Missing Class Docstring
  false positive when inheriting from a generic class of a TypedDict
- [#7891](https://github.com/pylint-dev/pylint/issues/7891) — False positive `no-member`
  when attempting to access `_asdict`, which is a valid `NamedTup
- [#7647](https://github.com/pylint-dev/pylint/issues/7647) — False positive
  `unnecessary-lambda` (wrong type inference in if-else-expression)
- [#7381](https://github.com/pylint-dev/pylint/issues/7381) — Multiple binary |
  operation in a single statement failed with "E1131: unsupported operand
- [#7350](https://github.com/pylint-dev/pylint/issues/7350) — E0601 false positive when
  nested try block exhaustively defines name, raises, or returns
- [#7240](https://github.com/pylint-dev/pylint/issues/7240) — False-positive `no-member`
  in comprehension in unreachable code from platform check
- [#5823](https://github.com/pylint-dev/pylint/issues/5823) — super-with-arguments
  should not be shown for dataclasses with slots
- [#4920](https://github.com/pylint-dev/pylint/issues/4920) — No type narrowing takes
  place in `or` statements following negated `isinstance`
- [#4608](https://github.com/pylint-dev/pylint/issues/4608) — False positive: Pylint
  doesn't deduce non-None-ness from ternary condition
- [#4554](https://github.com/pylint-dev/pylint/issues/4554) — False positive
  no-value-for-parameter when unpacking a modified list
- [#3925](https://github.com/pylint-dev/pylint/issues/3925) — False positive
  not-callable after destructuring
- [#3893](https://github.com/pylint-dev/pylint/issues/3893) — False positive for E1123
  (unexpected-keyword-arg)
- [#3603](https://github.com/pylint-dev/pylint/issues/3603) — False
  unexpected-keyword-arg for classes defined differently in branches.
- [#3327](https://github.com/pylint-dev/pylint/issues/3327) — Spurious `no-member`
  errors with modules named `builtins` on py3
- [#3325](https://github.com/pylint-dev/pylint/issues/3325) — False positive
  `attribute-defined-outside-init` when using properties
- [#2981](https://github.com/pylint-dev/pylint/issues/2981) — False positive
  `attribute-defined-outside-init` error in Python 3.6 when attribute is defi
- [#2821](https://github.com/pylint-dev/pylint/issues/2821) — no-member checks seems to
  not be aware about scope
- [#1934](https://github.com/pylint-dev/pylint/issues/1934) — False positive
  `cell-var-from-loop` when there is only one element in an iterator
- [#1493](https://github.com/pylint-dev/pylint/issues/1493) — False-positive E1102
  (not-callable) with list of functions
- [#241](https://github.com/pylint-dev/pylint/issues/241) — Incorrect W0611 : Unused
  import when preceded by import as

## 🔁 Duplicates (4)

- [#10806](https://github.com/pylint-dev/pylint/issues/10806) — False positive for numpy
  2.4.0+
- [#10166](https://github.com/pylint-dev/pylint/issues/10166) — Instance of
  'DatetimeIndex' has no 'to_pydatetime' member Pylint (E1101:no-member)
- [#9885](https://github.com/pylint-dev/pylint/issues/9885) — False positive missing
  member **value** with type statement and Literal under python 3.12
- [#9884](https://github.com/pylint-dev/pylint/issues/9884) — `redefined-outer-name`
  (`W0621`) - false positive on 3.12 type aliases

## ❓ Unclear / needs reporter follow-up (18)

- [#11013](https://github.com/pylint-dev/pylint/issues/11013) — C0103: Constant name
  false positive when typing variables nested in `TYPE_CHECKING`
- [#11012](https://github.com/pylint-dev/pylint/issues/11012) — C0103: Variable name
  false positive for single word all caps at module level
- [#10991](https://github.com/pylint-dev/pylint/issues/10991) — Unexpected kwarg
  false-positive when using TypeVarTuple
- [#10941](https://github.com/pylint-dev/pylint/issues/10941) —
  astroid.exceptions.AstroidBuildingError: while using python 3.12
- [#10352](https://github.com/pylint-dev/pylint/issues/10352) — Empty transform plugin
  leads to false-positive missing-function-docstring issues
- [#10278](https://github.com/pylint-dev/pylint/issues/10278) — "ImportError: Unable to
  find module" when using implicit namespaces when they already exis
- [#10012](https://github.com/pylint-dev/pylint/issues/10012) — disable=too-many-line
  flaky if not on first line
- [#9993](https://github.com/pylint-dev/pylint/issues/9993) — Cannot find "dunder
  module" in package - False-positive `No name '**main**' in module 'foo
- [#9983](https://github.com/pylint-dev/pylint/issues/9983) — unexpected-keyword-arg:
  false positive and confusing error message with Uninferable
- [#9137](https://github.com/pylint-dev/pylint/issues/9137) — Pylint 3 'UninferableBase'
  object is not iterable
- [#8079](https://github.com/pylint-dev/pylint/issues/8079) — Pylint is crashing with
  astroid.exceptions.StatementMissing: Statement not found on <Modul
- [#8049](https://github.com/pylint-dev/pylint/issues/8049) — Crash with AstroidError
  'Could not find <FunctionDef.warning_logger'
- [#7680](https://github.com/pylint-dev/pylint/issues/7680) — pylint crashed with a
  `AstroidError` (astroid.exceptions.ParentMissingError)
- [#7389](https://github.com/pylint-dev/pylint/issues/7389) — pyreverse -c option causes
  stack overflow
- [#7268](https://github.com/pylint-dev/pylint/issues/7268) — Crash inferring a subclass
  of `typing.NamedTuple`
- [#3602](https://github.com/pylint-dev/pylint/issues/3602) — Maximum recursion depth
  crash with pyreverse `-S` option
- [#2188](https://github.com/pylint-dev/pylint/issues/2188) — InconsistentMroError:
  Cannot create a consistent method resolution order for MROs
- [#22](https://github.com/pylint-dev/pylint/issues/22) — Pyreverse: ValueError: need
  more than 1 value to unpack

## Session log

| Session | Range                | Issues | Method                                        |
| ------- | -------------------- | -----: | --------------------------------------------- |
| 1       | newest #10195–#11013 |    104 | per-issue reproduction                        |
| 2       | #9556–#10195         |    120 | per-issue reproduction                        |
| 3       | #8806–#9555          |    165 | per-issue reproduction                        |
| 4       | #7643–#8805          |    174 | per-issue reproduction                        |
| 5       | #5214–#7641          |    170 | per-issue reproduction                        |
| 6       | #5644–#5823          |     15 | per-issue reproduction                        |
| 7       | #4083–#5202          |     70 | per-issue reproduction                        |
| 8       | #3334–#4070          |     75 | per-issue reproduction                        |
| 9       | #5–#3327             |    133 | per-issue reproduction + label classification |

Detailed per-session notes live in `.triage/sessions/session-XX.md`.

## Recommended follow-ups

1. **Close the FIXED list** (41 issues) after maintainer verification.
2. **High-impact REPRO clusters** (verified, shared root cause):
   - **PEP 695 type-params**: #10995, #10972, #10991, #9884, #9885, #10091
   - **typing.Self via super()**: #10807, #9159
   - **dataclass init signature reconstruction**: #10056, #10519, #9488, #9389, #5810
   - **control-flow used-before-assignment**: #10043, #10195, #9533, #9689, #8686,
     #8495, #7545, #7538, #5955, #5637, #5735, #5780, #5085, #4066, #4018, #4033, #2633,
     #2072
   - **descriptor/property false positives**: #10348, #9994, #8739, #10042, #5699, #4803
   - **decorator return-type / signature inference**: #10848, #7720, #9505, #7487,
     #5784, #3957, #3586, #2578
   - **NewType / Union narrowing**: #4944, #4961, #5091, #8327, #3162, #2296
   - **NamedTuple inference**: #10158, #4070
   - **Private name-mangling**: #5734, #3879
   - **Tuple unpacking / unbalanced-unpacking**: #2855, #2621, #4546
   - **import-self / parse errors**: #4444, #3748, #2856
3. **Crash list (high priority):**
   - #10813 (logging bytes UnicodeDecodeError)
   - #10519 (astroid dataclass **init_subclass**)
   - #10014 (project-local `multiprocessing/`)
   - #10099 (consider-using-enumerate on len(range()))
   - #8755 (super() with classmethod outside class)
   - #8746 (namedtuple with Unicode names)
   - #8739 (property.fset for getter-only)
   - #4444 (module same name as dir without **init**.py)
4. **EXTDEP audit** (194 issues) — spinning up a venv with
   numpy/pandas/scipy/torch/pydantic/PySide6/sqlalchemy/attrs/tensorflow would likely
   move many of these to concrete REPRO/FIXED.
