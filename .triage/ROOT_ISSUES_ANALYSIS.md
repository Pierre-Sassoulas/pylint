# High-leverage root issues — what single fixes would unblock the most open issues

This analysis combines all 1020 open triaged issues (181 REPRO + 197 EXTDEP + 598 DESIGN

- 32 FIXED + others) and identifies **root issues** whose resolution would cascade
  across many downstream bug reports.

Methodology:

1. For REPRO bugs, grouped by _underlying mechanism_ (not symptom) by scanning issue
   title + body + reproduction note for shared technical artifacts (astroid brain name,
   typing feature, control-flow component, decorator handling, etc.).
2. For EXTDEP bugs, grouped by upstream library — almost all EXTDEP issues are "astroid
   brain plugin doesn't model the library" rather than pylint bugs proper.
3. For each root, counted issues that would plausibly be resolved by a single
   coordinated fix (astroid brain release, control-flow rewrite, descriptor protocol
   update, …).

Counts are conservative — when an issue could plausibly be attributed to two roots, it
is counted under the more specific one. Companion data: `.triage/repro_roots.json`,
`.triage/repro_clusters.json`.

## Ranked root issues

| Rank | Root cause                                                                                                                                                                                                                              |              Issues it would unblock | Cost class                                 |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -----------------------------------: | ------------------------------------------ |
| 1    | Astroid brain plugins for the scientific / ORM / framework stack (numpy, pandas, sqlalchemy, pydantic, torch, pyside, django, tensorflow, scipy, matplotlib, attrs, sklearn, …)                                                         |                 **~95** REPRO+EXTDEP | upstream, but mostly per-library           |
| 2    | Control-flow rewrite — replace `NamesConsumer` all-or-nothing model with proper CFG-based reachability ([#4795](https://github.com/pylint-dev/pylint/issues/4795))                                                                      |                        **~40** REPRO | one large pylint internal change           |
| 3    | Decorator return-type / descriptor-protocol inference ([#7820](https://github.com/pylint-dev/pylint/issues/7820), [#2578](https://github.com/pylint-dev/pylint/issues/2578), [#4534](https://github.com/pylint-dev/pylint/issues/4534)) |                        **~18** REPRO | one focused astroid feature                |
| 4    | Generics inference — `Generic[T]` parameter tracking, `__class_getitem__`, `NewType`, `NamedTuple`, parameterised subscripting                                                                                                          |                        **~14** REPRO | one focused astroid feature                |
| 5    | Dataclass unification — `@dataclass(kw_only=True)`, `init=False`, generic dataclasses, dataclass inheritance, `field()`, pydantic dataclass compat                                                                                      |                        **~11** REPRO | one focused astroid brain                  |
| 6    | Enum / IntEnum / StrEnum modeling — class-body `from .. import` producing members, value-member resolution                                                                                                                              |                         **~7** REPRO | one focused astroid brain                  |
| 7    | PEP 695 (`type X = ...` + statement-scoped TypeVar + `__value__`)                                                                                                                                                                       | **~5** REPRO + already-closed #10995 | one astroid feature + 1 pylint scope tweak |
| 8    | Statement-scoped name resolution in astroid (`filter_stmts` / `scope_lookup` when a class member shadows a site-builtin or a builtin name)                                                                                              |                         **~5** REPRO | one astroid bug fix                        |

Roughly 75 % of all confirmed-reproducing bugs (and an even higher share of EXTDEP) are
attributable to one of these eight roots.

---

## Detailed breakdown

### 1. Brain plugins for the scientific / framework stack — ~95 issues

EXTDEP (197 issues total) is overwhelmingly astroid-brain work — 137/197 issue bodies
explicitly mention astroid or no-member-style symptoms. Distribution by upstream:

| Library                                        | EXTDEP issues |
| ---------------------------------------------- | ------------: |
| numpy                                          |            18 |
| pandas                                         |            12 |
| sqlalchemy                                     |            10 |
| pydantic                                       |             9 |
| django                                         |             6 |
| attrs                                          |             6 |
| pyside                                         |             5 |
| torch                                          |             5 |
| pytest                                         |             4 |
| tensorflow                                     |             4 |
| flask                                          |             4 |
| scipy                                          |             3 |
| matplotlib                                     |             3 |
| cython                                         |             3 |
| sklearn                                        |             2 |
| asyncio                                        |             2 |
| marshmallow                                    |             2 |
| (others)                                       |            ~5 |
| **Total EXTDEP attributable to brain plugins** |      **~103** |

Plus REPRO that fall into the same bucket:

- [#10806](https://github.com/pylint-dev/pylint/issues/10806) — `numpy.finfo.eps`
  (regressed at numpy 2.4.0)
- [#10166](https://github.com/pylint-dev/pylint/issues/10166) — pandas
  `DatetimeIndex.to_pydatetime`
- [#7296](https://github.com/pylint-dev/pylint/issues/7296) — `re.Pattern` members
- [#3728](https://github.com/pylint-dev/pylint/issues/3728) — `sys.stdin.buffer.peek()`

**The single highest-leverage thing pylint maintainers can do is coordinate brain-plugin
releases with the major libraries' release schedules** — numpy 2.x and pandas 3.x in
particular have generated steady streams of issues that disappear as soon as a matching
brain release ships.

### 2. Control-flow rewrite ([#4795](https://github.com/pylint-dev/pylint/issues/4795)) — ~40 issues

All 31 issues in the `control-flow` REPRO cluster trace to limitations in
`NamesConsumer` and the all-or-nothing per-variable consumed state. Examples:

- [#10847](https://github.com/pylint-dev/pylint/issues/10847) —
  `possibly-used-before-assignment` FN with type annotation
- [#10195](https://github.com/pylint-dev/pylint/issues/10195) — `used-before-assignment`
  FP
- [#9689](https://github.com/pylint-dev/pylint/issues/9689) — FP in try-while
- [#8686](https://github.com/pylint-dev/pylint/issues/8686) — `used-before-assignment`
  for assignment in inner try when outer returns
- [#8495](https://github.com/pylint-dev/pylint/issues/8495) — FN: calling inner function
  before var assigned
- [#8394](https://github.com/pylint-dev/pylint/issues/8394) — `undefined-loop-variable`
  (W0631)
- [#8221](https://github.com/pylint-dev/pylint/issues/8221) — `cell-var-from-loop`
  ignores genexprs
- [#7720](https://github.com/pylint-dev/pylint/issues/7720) — `undefined-variable`
  regression since 2.6.0
- [#7460](https://github.com/pylint-dev/pylint/issues/7460) — expected
  `undefined-variable` when deleted var used
- [#5955](https://github.com/pylint-dev/pylint/issues/5955) — multiple-target assignment
  FP
- [#841](https://github.com/pylint-dev/pylint/issues/841) — `redefined-outer-name` when
  using `del`
- … and ~20 more in the cluster.

Plus the 4 walrus issues ([#5735](https://github.com/pylint-dev/pylint/issues/5735),
[#7538](https://github.com/pylint-dev/pylint/issues/7538),
[#8486](https://github.com/pylint-dev/pylint/issues/8486),
[#10691](https://github.com/pylint-dev/pylint/issues/10691)) which all involve `:=`
interacting with the same flow machinery.

Plus several REPRO bugs in the `arguments` cluster that depend on knowing whether a
variable was definitely-assigned along all paths.

**The discussion in [#4795](https://github.com/pylint-dev/pylint/issues/4795) is the
right place to focus this work.** It is a large investment, but resolves the
second-largest unfixed surface.

### 3. Decorator return-type / descriptor protocol — ~18 issues

When a decorator changes a function's _type_ (e.g. wraps it in a descriptor, changes the
return type, or adds attributes), pylint largely ignores the change. The shared root is
that astroid does not run the descriptor protocol against bound vs unbound methods.

- [#7820](https://github.com/pylint-dev/pylint/issues/7820) — descriptor protocol
  meta-issue
- [#10848](https://github.com/pylint-dev/pylint/issues/10848) — `@` syntax decorator
  return type
- [#9505](https://github.com/pylint-dev/pylint/issues/9505) — decorator changing arg
  count
- [#7487](https://github.com/pylint-dev/pylint/issues/7487) — inner `@classmethod`
  no-member
- [#5784](https://github.com/pylint-dev/pylint/issues/5784) — decorator inner
  unexpected-keyword-arg
- [#5699](https://github.com/pylint-dev/pylint/issues/5699) — classmethod+property
  unsubscriptable
- [#3957](https://github.com/pylint-dev/pylint/issues/3957) — attributes added by
  decorator
- [#3586](https://github.com/pylint-dev/pylint/issues/3586) — function named "lazy"
  assignment-from-no-return
- [#2578](https://github.com/pylint-dev/pylint/issues/2578) — type changes in decorators
  (meta-issue)
- [#4803](https://github.com/pylint-dev/pylint/issues/4803) — classmethod+property
  unpacking-non-sequence
- [#2271](https://github.com/pylint-dev/pylint/issues/2271) — partial() class attribute
  `redundant-keyword-arg`
- [#3641](https://github.com/pylint-dev/pylint/issues/3641) — `undefined-variable` for
  decorators
- [#8265](https://github.com/pylint-dev/pylint/issues/8265) — `unnecessary-dunder-call`
  for `__get__` descriptor binding
- [#4534](https://github.com/pylint-dev/pylint/issues/4534) — `typing.cast()` ignored
  (related: trust the cast)
- [#4070](https://github.com/pylint-dev/pylint/issues/4070) — `NamedTuple._replace()`
- … plus 2 in REPRO `no-member` cluster and `cached_property` cases in DESIGN.

**Action:** scope an astroid milestone around the descriptor protocol + a generic
"decorator-changes-type" mechanism. This is one focused feature, not a rewrite.

### 4. Generics inference — ~14 issues

`Generic[T]`, `__class_getitem__`, `NewType`, `NamedTuple`, parameterised subscripting:

- [#10360](https://github.com/pylint-dev/pylint/issues/10360) — `__class_getitem__`
  E1136
- [#10186](https://github.com/pylint-dev/pylint/issues/10186) — `arguments-differ` on
  overloaded subclass
- [#10158](https://github.com/pylint-dev/pylint/issues/10158) — TypedDict
  `__required__`/`__optional__`
- [#10042](https://github.com/pylint-dev/pylint/issues/10042) — `typing.IO` not-callable
- [#10031](https://github.com/pylint-dev/pylint/issues/10031) — inheriting from
  `set[int]`
- [#9908](https://github.com/pylint-dev/pylint/issues/9908) — generic alias forward ref
- [#9319](https://github.com/pylint-dev/pylint/issues/9319) — `unnecessary-ellipsis` on
  Protocol
- [#9222](https://github.com/pylint-dev/pylint/issues/9222) — `duplicate-bases` with
  TypedDict
- [#8600](https://github.com/pylint-dev/pylint/issues/8600) — protected-access on
  Generic
- [#8213](https://github.com/pylint-dev/pylint/issues/8213) — `isinstance` parameterized
  generic
- [#8022](https://github.com/pylint-dev/pylint/issues/8022) — Generic setter type leaks
  across instances
- [#7978](https://github.com/pylint-dev/pylint/issues/7978) — TypedDict membership test
- [#7934](https://github.com/pylint-dev/pylint/issues/7934) — missing-docstring on
  Generic[TypedDict]
- [#7379](https://github.com/pylint-dev/pylint/issues/7379) — no-member generic parent
  `__class_getitem__`
- [#4944](https://github.com/pylint-dev/pylint/issues/4944) — `NewType` subscript
- [#4070](https://github.com/pylint-dev/pylint/issues/4070) — `NamedTuple._replace()`
- [#3162](https://github.com/pylint-dev/pylint/issues/3162) — `NewType` no-member
- [#2855](https://github.com/pylint-dev/pylint/issues/2855) —
  `ClassVar[Optional[Tuple]]` unpack
- [#2296](https://github.com/pylint-dev/pylint/issues/2296) — `NewType` not-iterable

**Action:** unified astroid model for generic-class parameterization (parameters survive
attribute lookup; `__class_getitem__` returns a parametrized variant).

### 5. Dataclass unification — ~11 issues

- [#10991](https://github.com/pylint-dev/pylint/issues/10991) — TypeVarTuple in
  dataclass hierarchy
- [#10519](https://github.com/pylint-dev/pylint/issues/10519) — crash inheriting generic
  dataclass with `__init_subclass__`
- [#10056](https://github.com/pylint-dev/pylint/issues/10056) — 2nd-order dataclass
  inheritance with `init=False`
- [#9972](https://github.com/pylint-dev/pylint/issues/9972) — wrapping
  `dataclasses.field`
- [#9488](https://github.com/pylint-dev/pylint/issues/9488) — Generic dataclass with ABC
  bounded TypeVar
- [#9389](https://github.com/pylint-dev/pylint/issues/9389) — dataclass with
  `init=False`
- [#9183](https://github.com/pylint-dev/pylint/issues/9183) — `__dataclass_fields__`
  member
- [#5810](https://github.com/pylint-dev/pylint/issues/5810) — dataclass E1134

Plus pydantic / attrs cases in EXTDEP (~15 more under root #1).

**Action:** consolidate the dataclass / attrs / pydantic brain into a single model with
shared parameterisation logic. Currently each lives in its own brain file.

### 6. Enum modeling — ~7 issues

- [#10951](https://github.com/pylint-dev/pylint/issues/10951) — `from .. import` inside
  IntEnum producing members
- [#10840](https://github.com/pylint-dev/pylint/issues/10840) — `invalid-envvar-value`
  StrEnum
- [#10609](https://github.com/pylint-dev/pylint/issues/10609) — subclassed Enums with
  args
- [#9905](https://github.com/pylint-dev/pylint/issues/9905) — overriding `Enum.value`
- [#9839](https://github.com/pylint-dev/pylint/issues/9839) — `__slots__` in IntEnum
  E0238
- [#8327](https://github.com/pylint-dev/pylint/issues/8327) — `Enum.enum` isinstance arg
- [#5091](https://github.com/pylint-dev/pylint/issues/5091) — `invalid-envvar-value`
  `builtins.str`

**Action:** single astroid `enum` brain refresh covering str/Int/auto and class-body
imports as member sources.

### 7. PEP 695 — ~5 issues

- [#10091](https://github.com/pylint-dev/pylint/issues/10091) —
  `TypeAliasType.__value__` no-member
- [#9884](https://github.com/pylint-dev/pylint/issues/9884) — `redefined-outer-name` on
  PEP 695 type-params
- [#9908](https://github.com/pylint-dev/pylint/issues/9908) — generic alias forward ref
  invalid-sequence-index
- [#8455](https://github.com/pylint-dev/pylint/issues/8455) — TypeAlias `__origin__`
  no-member
- [Plus already-closed #10995 and #9885 (dup pair)]

**Action:** astroid: model `TypeAliasType` properly (so `__value__` / `__origin__` are
available); pylint: treat statement-scoped type-parameters per PEP 695.

### 8. filter_stmts / scope_lookup on shadowed builtins — ~5 issues

- [#8079](https://github.com/pylint-dev/pylint/issues/8079) — site-builtins (`license`,
  `copyright`, `credits`) shadowed → astroid F0002 crash
- [#10994](https://github.com/pylint-dev/pylint/issues/10994) — `type` builtin
  overwritten → wrong inference
- [#7348](https://github.com/pylint-dev/pylint/issues/7348) — instance method
  overwritten → E1120/E1123
- [#6856](https://github.com/pylint-dev/pylint/issues/6856) — `repeated-keyword` on
  builtin functions
- [#2633](https://github.com/pylint-dev/pylint/issues/2633) — E0601 on global shadowing
- [#841](https://github.com/pylint-dev/pylint/issues/841) — `redefined-outer-name` when
  using `del`

**Action:** single astroid `filter_stmts.py` fix — handle the case where
`node.statement()` returns the synthetic Module-level entry for a site-builtin
(currently raises `StatementMissing`).

## Total open-issue cascade

| Root                                            | Issues unblocked |
| ----------------------------------------------- | ---------------: |
| 1. Brain plugins for scientific/framework stack |              ~95 |
| 2. Control-flow rewrite                         |              ~40 |
| 3. Decorator / descriptor protocol              |              ~18 |
| 4. Generics inference                           |              ~14 |
| 5. Dataclass unification                        |              ~11 |
| 6. Enum modeling                                |               ~7 |
| 7. PEP 695                                      |               ~5 |
| 8. filter_stmts shadowed-builtin                |               ~5 |
| **Sum**                                         |         **~195** |

Note: 195 > 181 because some REPRO issues plausibly resolve under more than one root
(e.g. #10991 is both dataclass and TypeVarTuple). EXTDEP issues are weighted toward
brain-plugin work. The combined ~195-issue cascade is over **half of the 378 open
REPRO+EXTDEP issues** — meaning eight focused workstreams could close more open bugs
than the total volume the project has been resolving per year for the last several
years.

## Recommendation

A **two-track plan** would maximize leverage:

- **Track A — Astroid brain modernization.** One coordinated release covering numpy 2.x
  / pandas 3.x / pydantic 2.x / sqlalchemy 2.x / generics / decorators / descriptor
  protocol / dataclass-unification / enum / PEP 695 / `filter_stmts` fix. Roots #1, #3,
  #4, #5, #6, #7, #8. Closes ~155 issues. Each sub-task is small in isolation; what's
  missing is the coordination.
- **Track B — Control-flow rewrite.** Land
  [#4795](https://github.com/pylint-dev/pylint/issues/4795). Single large pylint
  internal change. Closes ~40 issues. This is independent of Track A and can run in
  parallel.

The remaining ~180 REPRO+EXTDEP issues are long-tail (one-off checker FPs, niche library
brains, pyreverse, …) and benefit from the existing "small fixes per release" cadence.
