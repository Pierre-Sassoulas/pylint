# Session 07 — Triage Notes (re-audited)

**Issues triaged this session:** 70

**Re-audit on pylint 4.0.5 / astroid 4.0.2.**

**Verdict tally:**

- REPRO: 11
- FIXED: 3
- EXTDEP: 17
- DESIGN: 39

## By verdict

### REPRO (11)

- **#5091** — E1507 (invalid-envvar-value) does not accept `builtins.str` as a valid
  type for `os.getenv` argument Confirmed E1507 false positive: os.getenv(self.name)
  where self.name is annotated as str — invalid-envvar-value fires.
  <https://github.com/pylint-dev/pylint/issues/5091>

- **#5085** — Negation and None Confirmed E1130 false positive: property with 'if
  self.**val is None: self.**val = 42; return self.**val' — pylint doesn't narrow **val
  to int after assignment, flags unary minus.
  <https://github.com/pylint-dev/pylint/issues/5085>

- **#4993** — Incorrect report "unused-import" when assigning to class attribute with
  the same name as the importe Confirmed W0611 false positive: 'import gettext' used in
  'translation: gettext.NullTranslations' annotation but shadowed by '@property gettext'
  on the same class — pylint marks the import unused.
  <https://github.com/pylint-dev/pylint/issues/4993>

- **#4968** — False positive 'not-an-iterable' when using deferred initialization in a
  property Confirmed E1133 false positive: 'getattr(obj, "names")' where names is a
  property doing deferred init returning a list. pylint can't see through
  getattr+property+deferred-init. <https://github.com/pylint-dev/pylint/issues/4968>

- **#4961** — incorrect line number and missing module name for E0633 (and
  false-positive) Confirmed E0633 false positive AND misleading message: 'a, b =
  NewType_wrapped_tuple' raises 'unpacking-non-sequence defined at line 10 of
  <empty module name>'. <https://github.com/pylint-dev/pylint/issues/4961>

- **#4944** — False positive: Tuple claimed unsubscriptable when using NewType Confirmed
  E1136: NewType('T', tuple[float,float]) — instance treated as unsubscriptable. astroid
  doesn't model NewType-wrapped tuples.
  <https://github.com/pylint-dev/pylint/issues/4944>

- **#4908** — Coroutine type inferred incorrectly Confirmed E1101 false positive: 'g =
  f(); g.send(None)' where f is async — coroutine type not modeled, g inferred as bytes.
  <https://github.com/pylint-dev/pylint/issues/4908>

- **#4861** — `repeated-keyword` false-positive when overriding existing dict keys
  Confirmed E1132 false positive: 'dict(kwargs, that=3)' merges dict (overriding),
  passed as 'my_func(\*\*new_kwargs)' — pylint sees both 'that' values in original
  kwargs and override. <https://github.com/pylint-dev/pylint/issues/4861>

- **#4803** — False positive unpacking-non-sequence on classmethod + property Confirmed
  E0633 false positive: @classmethod @property returning tuple, unpacked as 'x, y =
  E.p'. astroid doesn't track tuple type through chained classmethod+property.
  <https://github.com/pylint-dev/pylint/issues/4803>

- **#4546** — False-positive no-value-for-parameter for some unpacked values of
  list-builtins Confirmed E1120 false positive: 'list(returns_implicit_tuple(1))' loses
  the implicit-tuple's element count; 'foo(\*args)' flagged no-value-for-parameter. The
  non-list-wrapped variant works. <https://github.com/pylint-dev/pylint/issues/4546>

- **#4444** — Linting fails if module contains module of the same name Confirmed
  F0010/parse-error: 'pylint a/' where a/ contains a.py (same name as dir) without
  **init**.py fails with 'Unable to load file a/**init**.py'.
  <https://github.com/pylint-dev/pylint/issues/4444>

### FIXED (3)

- **#4920** — No type narrowing takes place in `or` statements following negated
  `isinstance` Does NOT reproduce on 4.0.5: 'if not isinstance(exc, X) or exc.status !=
  404:' no longer raises E1101 — 10/10. Fixed since 2.9.6.
  <https://github.com/pylint-dev/pylint/issues/4920>

- **#4608** — False positive: Pylint doesn't deduce non-None-ness from ternary condition
  Does NOT reproduce on 4.0.5: '-x if x is not None else None' no longer raises E1130 —
  10/10. Fixed since 2.8. <https://github.com/pylint-dev/pylint/issues/4608>

- **#4554** — False positive no-value-for-parameter when unpacking a modified list Does
  NOT reproduce on 4.0.5: 'a = []; a.extend([...]); os.path.join(\*a)' no longer raises
  E1120 — 10/10. Fixed since 2.8. <https://github.com/pylint-dev/pylint/issues/4554>

### EXTDEP (17)

- **#5168** — False positive cyclic-import Needs zhmccli project. cyclic-import
  regression from 2.10→2.11. Real but project-specific.
  <https://github.com/pylint-dev/pylint/issues/5168>

- **#5061** — false positive no-member on connexion.exceptions.\* connexion lib
  no-member. Lib. <https://github.com/pylint-dev/pylint/issues/5061>

- **#4917** — Variable created in context manager is detected as object of context
  variable class Needs reporter's project. context-manager variable type confusion.
  <https://github.com/pylint-dev/pylint/issues/4917>

- **#4911** — Field lookup fails for `geoip2.records.Country.iso_code` geoip2 records
  field lookup. Lib. <https://github.com/pylint-dev/pylint/issues/4911>

- **#4899** — Instance of 'Field' has no 'append' member Lib-specific 'Field has no
  append member'. Needs reporter context.
  <https://github.com/pylint-dev/pylint/issues/4899>

- **#4739** — False positive: Tuple is unsuscriptable since pylint 2.9.3 Tuple
  unsuscriptable since 2.9.3. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/4739>

- **#4694** — Regression on rest_framework : Value 'serializer.data' is unsubscriptable
  django rest_framework serializer.data. Lib.
  <https://github.com/pylint-dev/pylint/issues/4694>

- **#4693** — False positive no-member after `assert isinstance` Needs Authl/disposition
  module. False E1101 after assert isinstance. Real lib-specific.
  <https://github.com/pylint-dev/pylint/issues/4693>

- **#4690** — False positive no-member on PonyORM PonyORM. Lib.
  <https://github.com/pylint-dev/pylint/issues/4690>

- **#4667** — no-member on argparse result on Python 3.9 (only) argparse on python 3.9
  only. Needs reproduction. <https://github.com/pylint-dev/pylint/issues/4667>

- **#4609** — False positive `no-name-in-module` with `tensorflow==2.5.0` tensorflow
  2.5.x no-name-in-module. Lib. <https://github.com/pylint-dev/pylint/issues/4609>

- **#4584** — False positive 'requests.packages' has no 'urllib3' member (no-member)
  requests.packages.urllib3. Lib. <https://github.com/pylint-dev/pylint/issues/4584>

- **#4577** — False positives on `pandas.io.parsers.TextFileReader` pandas
  TextFileReader. Lib. <https://github.com/pylint-dev/pylint/issues/4577>

- **#4386** — Improper `too-many-function-args` for decorated function Decorated
  function too-many-function-args. Needs more context.
  <https://github.com/pylint-dev/pylint/issues/4386>

- **#4278** — no-member errors for flask-wtf form flask-wtf form no-member. Lib.
  <https://github.com/pylint-dev/pylint/issues/4278>

- **#4137** — False positive in 2.7.0: kazoo unpacking-non-sequence kazoo
  unpacking-non-sequence regression. Lib.
  <https://github.com/pylint-dev/pylint/issues/4137>

- **#4083** — Sequence index is not an int, slice, or instance with **index** (with
  scipy.fft) Needs scipy.fft. invalid-sequence-index. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/4083>

### DESIGN (39)

- **#5202** — Suggest limit checks instead of bool `in range` with step 1/-1
  Enhancement: suggest 'lo <= x < hi' over 'x in range(lo, hi)' for boolean checks.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/5202>

- **#5197** — Catch `undefined-variable` for variables with only type assignment and
  `NamedExpr` calls Enhancement: catch undefined-variable for type-only declarations
  with NamedExpr that's never reached. Control-flow.
  <https://github.com/pylint-dev/pylint/issues/5197>

- **#5159** — Add dataclass tests Maintenance: add dataclass tests. Internal.
  <https://github.com/pylint-dev/pylint/issues/5159>

- **#5156** — Refactor so `Pylinter` do not need to be a `BaseChecker` anymore
  Maintenance: refactor Pylinter inheritance. Internal.
  <https://github.com/pylint-dev/pylint/issues/5156>

- **#5092** — Improve error message of the `spelling-dict` option Docs: improve
  spelling-dict error message. Docs/PR.
  <https://github.com/pylint-dev/pylint/issues/5092>

- **#5086** — Setting command line options by environment variables Enhancement: set CLI
  options via env vars. Spec. <https://github.com/pylint-dev/pylint/issues/5086>

- **#5083** — False negative `useless-parent-delegation` when using the old style
  super/parent lookup FN persists: useless-parent-delegation not raised on old-style
  'Parent.**init**(self, ...)' delegation. Hacktoberfest spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5083>

- **#5047** — warning for variable that can be marked as `Final` Enhancement: warn when
  variable could be Final. High effort. Spec.
  <https://github.com/pylint-dev/pylint/issues/5047>

- **#5038** — Improve docs for `py-version` Docs: improve py-version docs. Docs.
  <https://github.com/pylint-dev/pylint/issues/5038>

- **#4933** — Extends `use-set-for-membership` for all hashable classes Enhancement:
  extend use-set-for-membership to all hashable classes. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4933>

- **#4921** — Cython support Cython support. High effort, design proposal.
  <https://github.com/pylint-dev/pylint/issues/4921>

- **#4916** — Raise a warning when a docstring is inherited but the type was changed in
  the child class Enhancement: warn when docstring inherited but type changed. Spec.
  <https://github.com/pylint-dev/pylint/issues/4916>

- **#4914** — Limiting String Constant Values Enhancement: limit string constant values.
  Hacktoberfest. <https://github.com/pylint-dev/pylint/issues/4914>

- **#4912** — Separate check for possibly unused arguments if locals() is used False
  positive when arguments referenced via locals(). Spec.
  <https://github.com/pylint-dev/pylint/issues/4912>

- **#4906** — Warn against unicode identifier normalization Enhancement: warn unicode
  identifier normalization. Hacktoberfest.
  <https://github.com/pylint-dev/pylint/issues/4906>

- **#4813** — Take type annotation into account when inference fails Enhancement: take
  type annotation into account when inference fails. Design proposal.
  <https://github.com/pylint-dev/pylint/issues/4813>

- **#4807** — bare-except (W0702) tricks developers into writing bugs Discussion:
  bare-except W0702 'tricks developers into bugs'. Decision.
  <https://github.com/pylint-dev/pylint/issues/4807>

- **#4795** — Discussion around a proper implementation of control-flow in pylint
  Discussion: proper control-flow implementation. Design proposal.
  <https://github.com/pylint-dev/pylint/issues/4795>

- **#4772** — Do not emit `raising-bad-type` if raising a function that always raise
  Enhancement: don't emit raising-bad-type for function-returning-exception. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4772>

- **#4725** — Checker for `unguarded-next-called-without-default` for `next` called
  without catching ``StopIte Enhancement: unguarded-next-called-without-default.
  Spec/PR. <https://github.com/pylint-dev/pylint/issues/4725>

- **#4697** — Using classes "defined as generic in stubs but not at runtime" as base
  class triggers inherit-non-cl False positive for stub-only generics. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4697>

- **#4659** — Dangerous default argument should include "Stateful" default arguments as
  well Enhancement: dangerous-default-value should include stateful defaults. Spec.
  <https://github.com/pylint-dev/pylint/issues/4659>

- **#4617** — Create an `--enforce-docstring-style` option Enhancement:
  --enforce-docstring-style option. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4617>

- **#4586** — Please consider warning on keyword arguments before positional unpacking
  arguments Enhancement: warn keyword args before positional. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4586>

- **#4563** — Provide a way to define name to be ignored via `good-method-names` and
  `good-property-names` Enhancement: name ignore via good-method-names regex. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4563>

- **#4556** — False negative `unexpected-keyword-arg` for `datetime.now` False negative
  unexpected-keyword-arg for datetime.now. Astroid brain.
  <https://github.com/pylint-dev/pylint/issues/4556>

- **#4542** — Add check for unused module-level private and protected functions
  Enhancement: unused private module-level functions. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4542>

- **#4534** — Casted type from `typing.cast()` is ignored (`no-member`) Enhancement:
  respect typing.cast() result type. Astroid brain. High effort.
  <https://github.com/pylint-dev/pylint/issues/4534>

- **#4452** — Detecting OOP principles (SOLID) violations Enhancement: SOLID violation
  detection. Hacktoberfest, broad scope.
  <https://github.com/pylint-dev/pylint/issues/4452>

- **#4437** — Pylint takes the isort configuration into account only if it's directly
  available in its launch dire Enhancement: pylint takes isort config only if installed.
  Spec. <https://github.com/pylint-dev/pylint/issues/4437>

- **#4355** — New checker for casting sets to lists Enhancement: new checker for casting
  sets to lists. Spec/PR. <https://github.com/pylint-dev/pylint/issues/4355>

- **#4352** — too-few-public-methods: warn only for the parent class Enhancement:
  too-few-public-methods only warn on parent. Spec.
  <https://github.com/pylint-dev/pylint/issues/4352>

- **#4322** — Github actions for pylint available in github actions marketplace
  Enhancement: GitHub Actions for pylint in marketplace. Hacktoberfest.
  <https://github.com/pylint-dev/pylint/issues/4322>

- **#4320** — Have spellchecker ignore black/flake8/bandit directives Enhancement:
  spellchecker ignore tool directives. Spec.
  <https://github.com/pylint-dev/pylint/issues/4320>

- **#4300** — Imports from module using PEP 562's **getattr** should not raise E0611
  Astroid enhancement: PEP 562 **getattr** imports shouldn't raise no-name-in-module.
  High effort. <https://github.com/pylint-dev/pylint/issues/4300>

- **#4197** — Create an allow list for class that can have a few public methods
  Enhancement: allow list for too-few-public-methods exceptions. Spec.
  <https://github.com/pylint-dev/pylint/issues/4197>

- **#4167** — Cannot use --never-returning-functions for some functions Bug:
  --never-returning-functions doesn't work for some functions. Astroid brain.
  <https://github.com/pylint-dev/pylint/issues/4167>

- **#4146** — Checker to replace 'any/all(not condition)' by 'not any/all(condition)'
  when 'not condition' is slow Enhancement: refactor 'any/all(not condition)' → 'not
  any/all(condition)'. Spec/PR. <https://github.com/pylint-dev/pylint/issues/4146>

- **#4121** — False positive: unsupported-membership-test with Singleton False positive
  unsupported-membership-test with Singleton. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/4121>
