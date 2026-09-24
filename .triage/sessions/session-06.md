# Session 06 — Triage Notes (re-audited with per-issue reproduction)

**Issues triaged this session:** 15

**Re-audit:** session 6 was originally bulk-classified. This pass replaces those with
per-issue reproductions on pylint 4.0.5 / astroid 4.0.2.

**Verdict tally:**

- REPRO: 5
- FIXED: 1
- EXTDEP: 2
- DESIGN: 7

## By verdict

### REPRO (5)

- **#5810** — How to fix pylint E1134: Non-mapping value X is used in a mapping context
  (not-a-mapping) Confirmed E1134 false positive: dataclass with **post_init** doing
  'self.f_four = One(\*\*self.f_four)' where f_four is dict before being replaced by One
  instance — pylint treats f_four as One type from the annotation.
  <https://github.com/pylint-dev/pylint/issues/5810>

- **#5793** — arguments-differ: number of parameters was some number ... and is now the
  same number in overridden Confirmed W0221 message wording bug: 'Number of parameters
  was 2 in ... and is now 2 in overriding ...' — the count is the same; the real issue
  (kw-only conversion) isn't communicated.
  <https://github.com/pylint-dev/pylint/issues/5793>

- **#5784** — False positive for `unexpected-keyword-arg` for decorators with inner
  inner function Confirmed E1123 false positive: 'example_func(6, print_me="hello")'
  decorated with example_decorator (top-level wrapper) — pylint still flags print_me as
  unexpected kwarg. <https://github.com/pylint-dev/pylint/issues/5784>

- **#5761** — False positive invalid-overridden-method for async generators overriding
  AsyncIterable Confirmed W0236 false positive: async generator (uses yield) overriding
  a Protocol method returning AsyncIterable[str] flagged invalid-overridden-method.
  pylint should detect 'yield' to recognize async-generator vs coroutine.
  <https://github.com/pylint-dev/pylint/issues/5761>

- **#5735** — False positive 'undefined-variable' with assignment expression in
  decorator Confirmed E0602: walrus 'foo := preprocess(string)' inside list
  comprehension that is itself inside a decorator argument; the inner 'foo' references
  after walrus are flagged undefined. <https://github.com/pylint-dev/pylint/issues/5735>

### FIXED (1)

- **#5823** — super-with-arguments should not be shown for dataclasses with slots Does
  NOT reproduce on 4.0.5: @dataclass(slots=True) subclass with super().greet() no longer
  triggers R1725 super-with-arguments suggestion — 10/10.
  <https://github.com/pylint-dev/pylint/issues/5823>

### EXTDEP (2)

- **#5794** — False positive `undefined-variable` when using class reference of sibling
  class Needs full project (pySim repo) to reproduce E0602 on ApplicationLabel
  sibling-class reference inside class body. Complex inheritance.
  <https://github.com/pylint-dev/pylint/issues/5794>

- **#5655** — False positive `no-name-in-module` in Matplotlib component Needs
  Matplotlib. no-name-in-module FP. Lib-specific.
  <https://github.com/pylint-dev/pylint/issues/5655>

### DESIGN (7)

- **#5814** — Check for circular comparisons and other comparison improvements
  Enhancement: detect circular comparisons that simplify to False (current R1716 only
  suggests simplification, not the impossibility). Spec.
  <https://github.com/pylint-dev/pylint/issues/5814>

- **#5806** — Emit a message for reliance on variable annotations never initialized in
  `__init__` or `__new__` Enhancement: emit message for declared-but-never-initialized
  instance annotations. Decision pending. (Confirmed FN still present.)
  <https://github.com/pylint-dev/pylint/issues/5806>

- **#5780** — False negative `used-before-assignment` after name defined and used in
  except False negative: 'print(msg)' AFTER the except block isn't flagged
  used-before-assignment when msg is also used INSIDE the except block. Reporter's
  snippet confirmed clean (10/10) — FN persists. Spec/PR.
  <https://github.com/pylint-dev/pylint/issues/5780>

- **#5763** — feature suggestion for `is` compare between different types Proposal: warn
  on 'is' comparison between different types (always False). Decision/spec.
  <https://github.com/pylint-dev/pylint/issues/5763>

- **#5701** — Should `pylint` be equivalent to `pylint .` ? Decision: should 'pylint'
  (no args) be equivalent to 'pylint .'? Maintainer discussion.
  <https://github.com/pylint-dev/pylint/issues/5701>

- **#5695** — Performance improvement with reusing checks for attribute validity
  Performance: cache visit_attribute results. Internal optimization.
  <https://github.com/pylint-dev/pylint/issues/5695>

- **#5644** — Pylint is not using a src/ folder Maintenance: pylint itself doesn't use a
  src/ folder. Internal. <https://github.com/pylint-dev/pylint/issues/5644>
