# Session 02 — 2026-05-12 — Triage Notes

**Scope:** Next 120 issues (mostly 2024 reports through #9556). **Verdict tally for this
session:**

- REPRO: 34
- FIXED: 1
- UNCLEAR: 3
- EXTDEP: 30
- DESIGN: 49
- DUP: 3
- STALE: 0

## By verdict

### REPRO (34)

- **#10195** — False positive `used-before-assignment` Confirmed E0601
  used-before-assignment on 'v' — control-flow analysis treats the early 'if x not in
  ["A"]:' as not narrowing later 'elif x == "A":'. Reporter says it should at minimum be
  downgraded to possibly-used-before-assignment.
  <https://github.com/pylint-dev/pylint/issues/10195>

- **#10193** — Invalid no-name-in-module when shadowing a base module with an alias then
  calling a method named for Confirmed E0611 'No name utils in module my_module.utils'
  triggered by combination of 'import my_module.utils as my_module' AND calling method
  named 'format' on the alias. Specific to .format() method name shadowing.
  <https://github.com/pylint-dev/pylint/issues/10193>

- **#10186** — False positive with `arguments-differ` rule in overridden overloaded
  methods in subclass Confirmed W0221 arguments-differ false positive on overloaded
  @staticmethod overrides — pylint compares only the first @overload signature of the
  base class, not the full overload set.
  <https://github.com/pylint-dev/pylint/issues/10186>

- **#10158** — False positive on **required** and **optional** on TypedDict. Confirmed
  E1101: TypedDict.**required_keys** / **optional_keys** flagged as unknown members.
  Should be supported by astroid TypedDict brain.
  <https://github.com/pylint-dev/pylint/issues/10158>

- **#10140** — pylint only catching `cyclic-import` in parallel mode Confirmed by
  reporter: cyclic-import only fires under -j0 or -j>=2, not -j1. Internal: serial
  codepath misses the cycle detector.
  <https://github.com/pylint-dev/pylint/issues/10140>

- **#10113** — findings not reported until seemingly unrelated code is changed Confirmed
  false negative: f() body's unnecessary-negation is not reported, blocked by an
  upstream inference involving subprocess.Popen.communicate. Reporter notes the missing
  finding is broader than C0117. <https://github.com/pylint-dev/pylint/issues/10113>

- **#10099** — Crash in `consider-using-enumerate` when using `len(range())` and using
  the index to access an e Crash in consider-using-enumerate when 'len(range(...))' used
  with nested list indexing. Already labeled 'Needs PR'.
  <https://github.com/pylint-dev/pylint/issues/10099>

- **#10091** — Class 'str' has no '**value**' member on PEP 695 TypeAliasType Confirmed
  E1101 on 'X.**value**' where X is a PEP 695 'type X = ...' TypeAliasType. astroid
  doesn't model TypeAliasType's **value** attribute.
  <https://github.com/pylint-dev/pylint/issues/10091>

- **#10084** — False negative `superfluous-parens` when around two conditional and an
  `and` Confirmed false negative C0325 (superfluous-parens) on 'if (a and b):' patterns.
  Other comparison checkers fire (R1727, R0124, R0133), but superfluous-parens does not.
  <https://github.com/pylint-dev/pylint/issues/10084>

- **#10074** — E1142 false & missed alarms Confirmed E1142: false alarm on line with
  'await x' inside a generator-expression returning awaits, AND missing alarm on '[x
  async for x in agen()]' inside a sync function. Mixed-case
  awaitable/async-comprehension scope detection bug.
  <https://github.com/pylint-dev/pylint/issues/10074>

- **#10056** — Second order inheritance of dataclasses with default values/`init=False`
  causes `E1120 no-value-for- Confirmed E1120 'no-value-for-parameter' on @dataclass
  three-level inheritance where intermediate level has 'field(default=..., init=False)'.
  astroid dataclass init signature reconstruction.
  <https://github.com/pylint-dev/pylint/issues/10056>

- **#10055** — W0640 cell-var-from-loop false positive in Generator Comprehension of
  functions Confirmed W0640 cell-var-from-loop FP on '(lambda: print(i) for i in
  range(10))' generator expression. The lambda _is_ the generator's element so each i
  binding is correct. <https://github.com/pylint-dev/pylint/issues/10055>

- **#10043** — [deprecated-x] Message trigger even in old interpreter compatibility code
  Confirmed W4904 deprecated-class triggered inside 'if sys.version_info >= (3, 12): ...
  else: ...' compatibility blocks. pylint should not warn the older branch when guarded.
  <https://github.com/pylint-dev/pylint/issues/10043>

- **#10042** — False positive on not-callable when inheriting from `typing.IO` Confirmed
  E1102 not-callable on subclass-of-typing.IO[T] when instantiated as Z[str]() while
  X[str]()/Y[str]() with plain typing.Generic work. typing.IO ClassVar inference issue.
  <https://github.com/pylint-dev/pylint/issues/10042>

- **#10032** — consider-using-augmented-assign false-positive for multiple dictionaries
  and string keys Confirmed R6104 consider-using-augmented-assign false positive on
  'accumulated_values[key] = accumulated_values[previous] + values[key]' where LHS
  dict-key and RHS first-term dict-key differ.
  <https://github.com/pylint-dev/pylint/issues/10032>

- **#10031** — False-positive E1101 (no-member) inheriting from `set[int]` Confirmed
  E1101: subclass of 'set[int]' loses inferred attributes. astroid
  generic-builtin-subclass inheritance gap.
  <https://github.com/pylint-dev/pylint/issues/10031>

- **#10030** — False positive `unused-import` when using union of types inside quotes
  Confirmed W0611: 'List[int] | None' inside a quoted forward annotation is not parsed
  as a usage, so 'from typing import List' is flagged unused.
  <https://github.com/pylint-dev/pylint/issues/10030>

- **#10029** — Missing mandatory keyword argument (E1125) with explicit mandatory
  keywords and keyword dictionary Confirmed E1125: passing **someargs that contains 'c'
  and 'd' to fun(\*, c, d, **kwargs) still raises missing-kwoa. Checker assumes literal
  kwargs only. <https://github.com/pylint-dev/pylint/issues/10029>

- **#10014** — Crash
  ``Building error when trying to create ast representation of module 'multiprocessing.process'`
  Confirmed crash pattern: project has its own 'multiprocessing/' directory shadowing
  stdlib multiprocessing → astroid brain_multiprocessing transform raises TypeError.
  Astroid brain bug. <https://github.com/pylint-dev/pylint/issues/10014>

- **#9994** — False positive: useless-parent-delegation on '**init**' method of class
  derived from 'Exception' Confirmed W0246 useless-parent-delegation false positive on
  Exception subclass **init** that calls super().**init**() — Exception's **init**
  accepts varargs so a no-arg override IS a behavior change.
  <https://github.com/pylint-dev/pylint/issues/9994>

- **#9986** — False positive `unbalanced-dict-unpacking` Confirmed W0644
  unbalanced-dict-unpacking false positive: even after 'if len(self.data) == 1:'
  narrowing the unpack of a single (k,v) tuple still warns.
  <https://github.com/pylint-dev/pylint/issues/9986>

- **#9979** — W0223 does not get raised correctly Confirmed false negative W0223:
  'abstract-method' is not raised on Derived(Base) when Base inherits 'abc.ABC'
  directly. Raising it only when class uses metaclass=ABCMeta explicitly.
  <https://github.com/pylint-dev/pylint/issues/9979>

- **#9977** — `ungrouped-imports` / `wrong-import-order` : FP because only two isort's
  options are taken into acc Confirmed ungrouped-imports/wrong-import-order false
  positive: pylint only consults isort's 'known_first_party'/'known_third_party'
  sections, ignoring custom sections (known_platforms, known_frameworks, …).
  <https://github.com/pylint-dev/pylint/issues/9977>

- **#9972** — False positive `no-member` when wrapping dataclasses `field` Confirmed
  false positive E1101: wrapping dataclasses.field() in a helper that returns it (return
  field(\*\*kw)) makes pylint see attribute as Field instead of the annotated type.
  <https://github.com/pylint-dev/pylint/issues/9972>

- **#9950** — False positive `declare-non-slot` on classvar Confirmed E0245
  declare-non-slot false positive: 'x: ClassVar[int]' (no default) is treated as slot
  violation, while 'y: ClassVar[int] = 2' and 'z = 3' are not.
  <https://github.com/pylint-dev/pylint/issues/9950>

- **#9908** — False positive E1126 (invalid-sequence-index) on generic type alias with
  forward ref Confirmed E1126 false positive: 'Alias2: TypeAlias = "list[T]"' (string
  form) triggers invalid-sequence-index, while non-string form 'list[T]' does not.
  <https://github.com/pylint-dev/pylint/issues/9908>

- **#9905** — False positive `invalid-overridden-method` when overridding `Enum.value`
  Confirmed W0236 false positive: overriding enum.Enum.value (a DynamicClassAttribute)
  with @property triggers invalid-overridden-method.
  <https://github.com/pylint-dev/pylint/issues/9905>

- **#9878** — C0325 (superfluous-parens) appears to not trigger when contents are a
  string Confirmed false negative C0325: 'if x == ("option2"):' and 'if x in
  ("option4"):' do NOT trigger superfluous-parens (single-string in parens). Only
  kw-then-paren form triggers. <https://github.com/pylint-dev/pylint/issues/9878>

- **#9850** — AddressFamily and SocketKind are not visible in module socket Confirmed
  E0611: 'from socket import AddressFamily, SocketKind' is flagged even though they're
  real socket attributes (defined dynamically by socket module). astroid stub gap.
  <https://github.com/pylint-dev/pylint/issues/9850>

- **#9839** — E0238 false positive when defining **slots** in IntEnum class Confirmed
  E0238 invalid-slots false positive: '**slots** = ()' inside an IntEnum body is flagged
  invalid although it is valid (empty tuple is acceptable **slots**).
  <https://github.com/pylint-dev/pylint/issues/9839>

- **#9797** — `pyreverse` should check that `klass` is still `ClassDef` Pyreverse
  failure mode: 'klass.root().name' when klass is Uninferable raises TypeError.
  Code-reference identified; needs guard.
  <https://github.com/pylint-dev/pylint/issues/9797>

- **#9741** — False positive unnecessary-negation for float comparison Confirmed C0117
  unnecessary-negation false positive: for floats, 'not a < b' is NOT equivalent to 'b
  <= a' under NaN. Checker doesn't consider float semantics.
  <https://github.com/pylint-dev/pylint/issues/9741>

- **#9689** — False positive E0601: used-before-assignment in try and while block
  Confirmed E0601 used-before-assignment false positive: 'nonlocal a' inside a
  try/except or while block fails to mark 'a' as resolvable; works fine for for/range
  loops. <https://github.com/pylint-dev/pylint/issues/9689>

- **#9683** — False positive invalid-sequence-index using properties of range object as
  index Confirmed E1126: l[r.start], l[r.stop] (range object's int properties) trigger
  invalid-sequence-index. astroid doesn't expose range's start/stop/step as int.
  <https://github.com/pylint-dev/pylint/issues/9683>

### FIXED (1)

- **#9722** — False Positive W0143-comparison-with-callable when using derived property
  descriptors Does NOT reproduce on pylint 4.0.5: comparison-with-callable on
  multi-level property descriptor subclass (my_prop2 < my_prop < property) now correctly
  identifies the descriptor as non-callable.
  <https://github.com/pylint-dev/pylint/issues/9722>

### UNCLEAR (3)

- **#10012** — disable=too-many-line flaky if not on first line Reported flaky
  'too-many-lines' if disable not on first line. No minimal repro; happens only
  occasionally in CI on pylint 2.14 and 3.2.x. Likely already addressed in 4.0.x.
  <https://github.com/pylint-dev/pylint/issues/10012>

- **#9993** — Cannot find "dunder module" in package - False-positive `No name
  '**main**' in module 'foo' (no-name Cryptic title; needs the reporter's package layout
  to evaluate. <https://github.com/pylint-dev/pylint/issues/9993>

- **#9983** — unexpected-keyword-arg: false positive and confusing error message with
  Uninferable Confusing message 'Uninferable_factory' when \*\*kwargs dict key is
  Uninferable. Real but no minimal snippet, refers to external repo.
  <https://github.com/pylint-dev/pylint/issues/9983>

### EXTDEP (30)

- **#10181** — Pylint crash when importing `pyarrow.flight` Needs pyarrow.flight
  installed. Crash in basic_checker.is_terminating_func when inferring through pyarrow's
  import chain. <https://github.com/pylint-dev/pylint/issues/10181>

- **#10147** — bug and false-positive: pylint blows up with implicit namespaces
  submodules with relative imports in Needs src/ implicit-namespace project repro under
  jobs>=2. Long-running discussion; possibly related to fix b43721121 (sys.path handling
  for parallel). Worth re-testing post-fix.
  <https://github.com/pylint-dev/pylint/issues/10147>

- **#10144** — False positive for E1133(not-an-iterable) with pydantic `model_fields`
  class method Needs pydantic. E1133 not-an-iterable on model_fields. Pydantic v2
  lib-specific brain gap. <https://github.com/pylint-dev/pylint/issues/10144>

- **#10137** — recursion error on windows when running pylint with a path to an
  `__init__.py` file with a lambda an Windows-specific recursion error on
  path-to-egg-installed module. Perf+OS specific.
  <https://github.com/pylint-dev/pylint/issues/10137>

- **#10096** — pylint complains on import of "_" from ibis Needs ibis package. False
  E0611 on 'from ibis import _' — astroid doesn't enumerate ibis dynamic exports.
  <https://github.com/pylint-dev/pylint/issues/10096>

- **#10090** — py313: AttributeError: 'black.parsing.ASTSafetyError' object has no
  attribute '**dict**'. Did you me macOS / py3.13 specific crash via
  black.parsing.ASTSafetyError. Needs reproduction.
  <https://github.com/pylint-dev/pylint/issues/10090>

- **#10087** — False positives on container attributes Pydantic v2 Needs pydantic v2.
  False positives on container attributes of pydantic models. Lib-specific brain gap.
  <https://github.com/pylint-dev/pylint/issues/10087>

- **#10082** — E1136/E1137 false positives Needs the user's library setup to repro
  E1136/E1137 false positives. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/10082>

- **#10080** — generator causing false positive using-constant-test Tested with default
  checks — does not raise W0125 on the snippet here. May depend on py-version or
  extension. Lib/version-specific. The 'bad-builtin' message firing here is incidental.
  <https://github.com/pylint-dev/pylint/issues/10080>

- **#10050** — unsupported-assignment-operation false positive False positive
  'unsupported-assignment-operation' — no minimal snippet in body, needs reporter
  sample. <https://github.com/pylint-dev/pylint/issues/10050>

- **#10025** — Rerunning pylint on the same code can produce inconsistent `import-self`
  warnings Non-deterministic 'import-self' on a top-level script named 'pack' under
  scripts/ with sibling 'pack' package. Specific to ordering of module name resolution.
  <https://github.com/pylint-dev/pylint/issues/10025>

- **#10016** — Unreachable code in the next line when using `read_excel` function of
  `polars` module Needs pandas/openpyxl. Unreachable code reported after pd.read_excel
  call. Lib-specific astroid brain gap.
  <https://github.com/pylint-dev/pylint/issues/10016>

- **#9989** — [Regression] Misidentified return type of `numpy.mgrid` Needs numpy 2.1.1.
  numpy.mgrid no-member regression — astroid numpy brain returns 'tuple' for mgrid since
  2.1.1. <https://github.com/pylint-dev/pylint/issues/9989>

- **#9973** — no-member false positive with super() with huggingface's
  transformers.Trainer Needs HuggingFace transformers. super().method() resolves to
  wrong Trainer class — astroid can't traverse transformers' meta-import setup.
  <https://github.com/pylint-dev/pylint/issues/9973>

- **#9968** — False positive unsubscriptable-object for Pydantic model with dict Field
  Needs langchain-core + pydantic v2. False E1135/E1136 on a dict-typed Pydantic Field —
  pydantic brain gap. <https://github.com/pylint-dev/pylint/issues/9968>

- **#9956** — False-positive E1101 (no-member) for `numpy.dtypes.StringDType` Needs
  numpy 2.1+. E1101 on np.dtypes.StringDType — astroid numpy brain missing 2.1
  additions. <https://github.com/pylint-dev/pylint/issues/9956>

- **#9874** — False positive: `duplicate-bases` when using advanced-alchemy repository
  classes Needs advanced-alchemy lib. False positive 'duplicate-bases'. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/9874>

- **#9846** — False positives with imported variable that shadows class Needs two-module
  setup; pylint confused by class+variable same name across modules. Likely real but
  path-dependent. <https://github.com/pylint-dev/pylint/issues/9846>

- **#9843** — False positive `unused-argument` in `dataclass` `__new__` False
  unused-argument on dataclass **new**. Needs reproduction.
  <https://github.com/pylint-dev/pylint/issues/9843>

- **#9834** — False positive: pylint does not honour disable-statement when a line is
  continued with backslash Disable not honored. Needs reporter's project to reproduce.
  High effort. <https://github.com/pylint-dev/pylint/issues/9834>

- **#9813** — False positive `not-async-context-manager` with Pydantic `PrivateAttr`
  Needs pydantic v2. Not-async-context-manager FP on Pydantic
  PrivateAttr(default_factory=asyncio.Lock).
  <https://github.com/pylint-dev/pylint/issues/9813>

- **#9809** — False positive for optional class attribute Optional class-attribute FP —
  title alone, no minimal snippet shown above. Needs deeper read.
  <https://github.com/pylint-dev/pylint/issues/9809>

- **#9804** — False positive `arguments-differ` on `__post_init__` method in dataclass
  inheritence False positive arguments-differ on dataclass **post_init**. Needs snippet.
  <https://github.com/pylint-dev/pylint/issues/9804>

- **#9762** — E1101: Module 'orjson' has no 'dumps' member (no-member) Needs orjson
  installed. E1101 on orjson.dumps — astroid brain gap for orjson C extension.
  <https://github.com/pylint-dev/pylint/issues/9762>

- **#9757** — no-value-for-parameter false positive with
  sqlalchemy.ext.hybrid.hybrid_method Needs sqlalchemy. no-value-for-parameter FP on
  @hybrid_property. Lib-specific. <https://github.com/pylint-dev/pylint/issues/9757>

- **#9681** — Infinite recursion of Pyreverse when numpy.array is in class Needs numpy.
  Pyreverse infinite recursion when numpy.array is a class attribute. Lib-specific
  recursion. <https://github.com/pylint-dev/pylint/issues/9681>

- **#9666** — pylint: disable=invalid-name pragma gets ignored when using ctypes
  Structure ctypes Structure with class-level pragma disable=invalid-name not honored on
  _fields_ items. Needs ctypes setup to verify.
  <https://github.com/pylint-dev/pylint/issues/9666>

- **#9590** — Incorrect 'unsubscriptable-object' reported Lib-specific
  'unsubscriptable-object'. Needs library context to repro.
  <https://github.com/pylint-dev/pylint/issues/9590>

- **#9585** — Cannot import 'rti.connextdds' due to 'invalid syntax (rti.connextdds,
  line 18332)' (syntax-error) Cannot import rti.connextdds — astroid syntax error
  parsing the C extension stubs. Needs lib.
  <https://github.com/pylint-dev/pylint/issues/9585>

- **#9566** — OpenCV vs Pylint - E0611:no-name-in-module - OpenCV (cv2)
  no-name-in-module. C-extension/.pyi astroid gap. Library-specific.
  <https://github.com/pylint-dev/pylint/issues/9566>

### DESIGN (49)

- **#10187** — Spellchecker doesn't ignore labels and types in autodoc docstrings
  Enhancement: spelling checker should ignore sphinx/autodoc directives ':arg',
  ':rtype', ':returns', and the type names in ':arg <type> <name>:' positions.
  <https://github.com/pylint-dev/pylint/issues/10187>

- **#10172** — Ignore common tools' pragmas in `line-too-long` (`# type: ignore`,
  `# noqa: RUF001`, ``pragma: Enhancement (maintainer): ignore inline pragmas (# type:
  ignore, # noqa, # pragma: no cover, # pylint: disable=) when computing line-too-long.
  Specification effort. <https://github.com/pylint-dev/pylint/issues/10172>

- **#10164** — Generated mermaid files do not implement the --module-names option of
  pyreverse. Enhancement: pyreverse mermaid output ignores --module-names option.
  Internal feature gap. <https://github.com/pylint-dev/pylint/issues/10164>

- **#10143** — List of rules requiring file traversal User Q: which checks need
  full-codebase traversal vs single-file? Doc/design discussion.
  <https://github.com/pylint-dev/pylint/issues/10143>

- **#10093** — typing.Annotated should be considered a dangerous default Proposal: treat
  typing.Annotated[...] in function default args as dangerous-default. Spec needed
  (since Annotated is rarely mutable).
  <https://github.com/pylint-dev/pylint/issues/10093>

- **#10092** — Question: Is there a reason that `invalid-envvar-default` only checks
  `os.getenv`, not `os.environ.g Q/Enhancement: invalid-envvar-default only checks
  os.getenv defaults, should it also cover os.environ.get? Good-first-issue.
  <https://github.com/pylint-dev/pylint/issues/10092>

- **#10054** — Should we remove `abstract-method`? Maintainer proposal to remove the
  'abstract-method' check (16 comments). Decision pending.
  <https://github.com/pylint-dev/pylint/issues/10054>

- **#10052** — [consider-using-any-or-all] No suggestion when the loop condition already
  contain any / all or is 'l Proposal: consider-using-any-or-all should also suggest
  when the loop condition has a side-effect-free form. Discussion.
  <https://github.com/pylint-dev/pylint/issues/10052>

- **#10041** — Crash handler does not attempt to create directory for crash reports
  Proposal: pylint's crash-report writer should mkdir ~/.cache/pylint/ when missing
  instead of falling back to stderr. <https://github.com/pylint-dev/pylint/issues/10041>

- **#9980** — Add auto-completion for command line Enhancement: add shell completion for
  pylint CLI. Spec needed. <https://github.com/pylint-dev/pylint/issues/9980>

- **#9974** — Document how to configure the location of site packages in pylint Docs
  request: how to point pylint at a different venv's site-packages. Docs gap.
  <https://github.com/pylint-dev/pylint/issues/9974>

- **#9955** — Alter fallback when `source-root` based package path discovery when a
  source root containing the mod Source-roots fallback design discussion when project
  source-root doesn't contain the file being linted (e.g. tests/ vs src/).
  <https://github.com/pylint-dev/pylint/issues/9955>

- **#9943** — Guarantee a deterministic order when processing files for directory
  arguments. Enhancement: deterministic file-processing order in multiprocessing mode.
  Internal. <https://github.com/pylint-dev/pylint/issues/9943>

- **#9941** — False negative used-before-assignment when the variable is used again in
  try/except False negative used-before-assignment when var is used as default argument
  of nested function. Discussion. <https://github.com/pylint-dev/pylint/issues/9941>

- **#9937** — Non-deterministic output from the code similarity check Non-deterministic
  similarity-check output. Needs investigation; likely dict-ordering related.
  <https://github.com/pylint-dev/pylint/issues/9937>

- **#9935** — Possible false-negative for `unused-argument` when function always raises
  False negative unused-argument when function aliased. Discussion.
  <https://github.com/pylint-dev/pylint/issues/9935>

- **#9930** — Add option to list configuration values optionally with origins
  Enhancement: --list-options with source-of-value (rcfile vs cli vs default). Internal
  feature. <https://github.com/pylint-dev/pylint/issues/9930>

- **#9928** — Emit no-member for `__annotations__` for py-version < 3.10 Enhancement:
  emit no-member for **annotations** when py-version < 3.10. Spec needed.
  <https://github.com/pylint-dev/pylint/issues/9928>

- **#9924** — Document how to only run pre-push with the pre-commit integration Docs
  request: how to run pylint only on pre-push (not pre-commit) under pre-commit
  framework. <https://github.com/pylint-dev/pylint/issues/9924>

- **#9923** — Spurious W3301: min(value, min(iterable)) does not do the same thing as
  min(value, iterable) Spurious W3301 min(value, min(iterable)). Documentation/spec.
  <https://github.com/pylint-dev/pylint/issues/9923>

- **#9915** — pylint treats `package.module` same as `package/module.py` in terms of
  search Enhancement: pylint treats 'package.module' (dotted) the same as
  'package/module.py' (path) in some discovery, causing surprises with namespace
  packages. Spec. <https://github.com/pylint-dev/pylint/issues/9915>

- **#9889** — Behavior of --prefer-stubs Design proposal for --prefer-stubs behavior.
  Internal spec. <https://github.com/pylint-dev/pylint/issues/9889>

- **#9873** — Add a checker for superfluous `import a` statements when there is already
  `import a.b` Enhancement: warn on superfluous 'import a' when 'import a.b' already
  imports the parent. Spec needed. <https://github.com/pylint-dev/pylint/issues/9873>

- **#9863** — Unexpected behavior when dealing with Protocol generics Generic Protocol
  handling discussion. Needs spec. <https://github.com/pylint-dev/pylint/issues/9863>

- **#9862** — missing-docstring for constants and types Enhancement: require docstrings
  for module-level constants/TypeAlias declarations. Spec.
  <https://github.com/pylint-dev/pylint/issues/9862>

- **#9861** — Pylint ignores disable=invalid-name under certain conditions
  Specification: scope of '# pylint: disable=invalid-name' on attribute-assignment line
  when the receiving class is imported. Related to #10199.
  <https://github.com/pylint-dev/pylint/issues/9861>

- **#9859** — [used-before-assignment] False negative when nested in if statements
  Decision: possibly-used-before-assignment should also fire when both assignment
  branches and usage are nested behind equivalent if guards. Spec.
  <https://github.com/pylint-dev/pylint/issues/9859>

- **#9833** — Dynamic `__getattr__` still leads to `no-member` if inference is ambiguous
  Spec: dynamic **getattr** still warns no-member when inference fails. Design needed
  for how aggressive to be. <https://github.com/pylint-dev/pylint/issues/9833>

- **#9818** — `from __future__ import annotations` is 3.7+ Enhancement: 'from **future**
  import annotations' is 3.7+, so py-version<3.7 check should fire when used. Niche.
  <https://github.com/pylint-dev/pylint/issues/9818>

- **#9807** — Report global object redefinition Enhancement: warn on global-object
  redefinition. Spec. <https://github.com/pylint-dev/pylint/issues/9807>

- **#9805** — [pyreverse] Dunder methods in diagrams Enhancement: pyreverse should
  optionally include dunder methods in diagrams. WIP.
  <https://github.com/pylint-dev/pylint/issues/9805>

- **#9798** — FN `attribute-defined-outside-init` with `setattr()` False negative
  attribute-defined-outside-init when assignment uses setattr(). Hacktoberfest, Needs
  PR. <https://github.com/pylint-dev/pylint/issues/9798>

- **#9783** — Brains should be dynamically registered Performance enhancement:
  lazy/dynamic brain registration to avoid running e.g. numpy brain transforms on
  non-numpy code (1.4M unneeded calls). Big speedup potential.
  <https://github.com/pylint-dev/pylint/issues/9783>

- **#9766** — `missing-function-docstring` when overriding methods of generic classes
  with undefined type paramete Spec: missing-function-docstring on overriding generic
  methods. Discussion. <https://github.com/pylint-dev/pylint/issues/9766>

- **#9758** — How to satisfy `unexpected-keyword-arg` in derived class override method
  that creates an instance vi Doc question: how to override a method in a derived class
  without triggering unexpected-keyword-arg. Docs gap.
  <https://github.com/pylint-dev/pylint/issues/9758>

- **#9745** — Pylint is not smart enough when analyzes functions returning coroutine.
  Proposal: more inference for functions returning Callables/closures. High-effort.
  <https://github.com/pylint-dev/pylint/issues/9745>

- **#9692** — Pylint does not discover a NoReturn method in certain cases to avoid
  "inconsistent-return-statements Enhancement: NoReturn discovery for
  instance-method-on-arg patterns (test cases 4a/4b/4d). Has many related issues. Good
  first issue. <https://github.com/pylint-dev/pylint/issues/9692>

- **#9688** — Can't update functional test refs Maintenance: tooling to update
  functional test refs broken. Internal.
  <https://github.com/pylint-dev/pylint/issues/9688>

- **#9673** — line-too-long false positive on long comment in function with
  disable=line-too-long if comment is af False positive line-too-long on long comment
  within function. Specifics not clear from title alone.
  <https://github.com/pylint-dev/pylint/issues/9673>

- **#9662** — False positive: possibly-used-before-assignment doesn't understand and-ed
  contions Spec: possibly-used-before-assignment with conjoined try/except branches.
  High-effort design proposal. <https://github.com/pylint-dev/pylint/issues/9662>

- **#9642** — [used-before-assignment] False negative for name defined inside loop that
  never runs False negative used-before-assignment for name defined inside dict/list
  comprehension. Spec. <https://github.com/pylint-dev/pylint/issues/9642>

- **#9641** — False positive: unused-variable + undefined-variable when using :=
  operator in stacked decorators False positive on decorator-defined symbols
  (used-before-assignment / undefined-variable). Discussion.
  <https://github.com/pylint-dev/pylint/issues/9641>

- **#9633** — undefined-variable/possibly-used-before-assignment/used-before-assignment
  false positives for global Bundled used-before-assignment/undefined-variable
  false-positive design ticket. Spec. <https://github.com/pylint-dev/pylint/issues/9633>

- **#9624** — [unsupported-binary-operation] should become .pyi-conscious Enhancement:
  unsupported-binary-operation should consult .pyi sibling. PR needed.
  <https://github.com/pylint-dev/pylint/issues/9624>

- **#9622** — Inside a sys.version_info guard, unexpected-keyword-arg returns error for
  version-specific keyword a Control-flow: unexpected-keyword-arg inside
  sys.version_info guard should consider version-specific return types. Astroid update
  needed. <https://github.com/pylint-dev/pylint/issues/9622>

- **#9598** — Allow CheckerTestCase to assertDoesNotAddMessages() to check that a
  specific message has not been ad Enhancement:
  CheckerTestCase.assertDoesNotAddMessages() helper for internal tests.
  <https://github.com/pylint-dev/pylint/issues/9598>

- **#9574** — Using typeshed stubs instead of dependencies Proposal: read typeshed stubs
  in lieu of installed package code. Large-scale design.
  <https://github.com/pylint-dev/pylint/issues/9574>

- **#9559** — Pyreverse unable to detect relative imports Pyreverse doesn't follow
  relative imports. Internal feature. <https://github.com/pylint-dev/pylint/issues/9559>

- **#9556** — using-constant-test triggers on a built-in exception property
  using-constant-test on builtin exception property — needs more context.
  <https://github.com/pylint-dev/pylint/issues/9556>

### DUP (3)

- **#10166** — Instance of 'DatetimeIndex' has no 'to_pydatetime' member Pylint
  (E1101:no-member) Duplicate of #10796 — same pandas DatetimeIndex no-member family of
  false positives. <https://github.com/pylint-dev/pylint/issues/10166>

- **#9885** — False positive missing member **value** with type statement and Literal
  under python 3.12 Duplicate of #10091 — same E1101 on TypeAliasType.**value**.
  <https://github.com/pylint-dev/pylint/issues/9885>

- **#9884** — `redefined-outer-name` (`W0621`) - false positive on 3.12 type aliases
  Duplicate of #10995 — same redefined-outer-name false positive on PEP 695 type-params.
  <https://github.com/pylint-dev/pylint/issues/9884>
