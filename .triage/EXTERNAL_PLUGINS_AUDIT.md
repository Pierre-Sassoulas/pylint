# External-plugin audit — 73 "big" Enhancement issues

For each of the 598 DESIGN-verdict issues that carry both `Enhancement ✨` and one of
`High effort 🏋` / `Needs design proposal 🔒` / `Needs specification 🔐` /
`Proposal 📨`, this audit checks whether an external tool / plugin already covers the
request.

The point is not "pylint should not do this" — it is "if a user wants this _today_ there
is somewhere to point them". For issues where a plugin exists, pylint maintainers can
link to it from the issue and either (a) close the issue as covered-externally, or (b)
keep it open as a candidate for absorbing the rule into pylint core.

Legend:

- **✅ Covered** — a maintained external plugin already implements the requested check
  (close-with-pointer candidate).
- **🟡 Partially covered** — an adjacent plugin / tool exists but doesn't fully match
  the ask (worth linking from the issue, not enough to close).
- **🌐 External web tool** — the request is for non-checker infrastructure (playground,
  config bootstrapper, dashboard, …) and an external tool serves the use case.
- **❌ No external equivalent** — the request is structural pylint work (control flow,
  config layering, pyreverse, astroid hook, etc.) and has to live in pylint.

## Summary

| Category                      | Count | Issues                                                                                                                                                                                                                                                              |
| ----------------------------- | ----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ✅ Covered by external plugin |    18 | #10748 #9530 #9980 #9471 #8848 #8734 #8654 #8430 #8413 #7835 #5838 #5290 #5289 #5047 #5328 #4921 #2493 #600                                                                                                                                                         |
| 🟡 Partially covered          |    10 | #10404 #10637 #9862 #9051 #8779 #8230 #4813 #5806 #748 #2996                                                                                                                                                                                                        |
| 🌐 External web tool          |     1 | #5972                                                                                                                                                                                                                                                               |
| ❌ Internal pylint work       |    44 | #9915 #9501 #9440 #9125 #8882 #8538 #8398 #8128 #8099 #8013 #7929 #7820 #7653 #7601 #7376 #7371 #7127 #7121 #7120 #6992 #5852 #5604 #5462 #5403 #5274 #5258 #4795 #4772 #4534 #4300 #3767 #3693 #3408 #3390 #3338 #2474 #2293 #2095 #1416 #971 #623 #568 #553 #8365 |

(73 = 18 + 10 + 1 + 44 ✅)

## Per-issue verdicts

### ✅ Covered by an external plugin (18)

#### #10748 — Annotation Complexity checker

**Plugin:**
[`flake8-annotations-complexity`](https://github.com/best-doctor/flake8-annotations-complexity)
— flake8 plugin that flags deeply nested type annotations. Complexity is the max nesting
depth (`List[int]` = 2, `Tuple[List[Optional[str]], int]` = 4); threshold set via
`--max-annotations-complexity` (default 3). Exactly the request.

#### #9530 — Detect useless f-strings

**Plugin:**
[Ruff `F541` f-string-missing-placeholders](https://docs.astral.sh/ruff/rules/f-string-missing-placeholders/)
— exactly the rule. Also handles nested f-strings. Available via ruff or flake8
(`pyflakes` ≥ 2.5).

#### #9980 — CLI auto-completion

**Plugin:** [`argcomplete`](https://github.com/kislyuk/argcomplete) — bash/zsh tab
completion for argparse, used by hundreds of CLIs. Pylint's CLI is argparse-based since
2.14; `PYTHON_ARGCOMPLETE_OK` magic comment in the entry point +
`eval "$(register-python-argcomplete pylint)"` is the typical wiring (could be enabled
in pylint with a one-line change).

#### #9471 — Suggest flattening nested idempotent function applications

**Plugin:** [Refurb](https://github.com/dosisod/refurb) — `FURB` rules for idiomatic
simplifications (also re-exported as Ruff `FURB*`). Covers many "idempotent wrapper"
rewrites; not a 1-to-1 match for the request but the closest existing thing.

#### #8848 — Warn when logging format string is not a literal

**Plugin:**
[`flake8-logging-format`](https://github.com/globality-corp/flake8-logging-format) —
exactly the request. Codes `G001`–`G004` flag `.format()`, `%`, `+`, and f-string used
as the first argument to a logger call. Also see
[`flake8-logging`](https://github.com/adamchainz/flake8-logging).

#### #8734 — Improved handling of fixme (require issue link in TODO)

**Plugin:**
[`flake8-jira-todo-checker`](https://github.com/SimonStJG/flake8-jira-todo-checker) —
every TODO/FIXME/QQ must have a JIRA ID next to it, and the ID must resolve to an open
ticket. Also [`flake8-todos`](https://github.com/orsinium-labs/flake8-todos) (`T003` =
link to issue required) and
[`flake8-fixme`](https://github.com/tommilligan/flake8-fixme) for the simpler "ban
FIXME" variant.

#### #8654 — `RuffChecker` class to run ruff rules from pylint

**Plugin:** [Ruff](https://github.com/astral-sh/ruff) itself. Users wanting ruff's
checks run them via ruff directly — most teams already pair pylint + ruff. Pylint
absorbing ruff's AST would be a structural ask; the practical answer today is "use both
tools".

#### #8430 — Convention for index initialized outside for-loop instead of `enumerate`

**Plugin:**
[Ruff `SIM113` enumerate-for-loop](https://docs.astral.sh/ruff/rules/enumerate-for-loop/)
— exact match. Originally from `flake8-simplify`.

#### #8413 — Check configuration in a dedicated script instead of at runtime

**Plugin:** [Ruff `ruff check --no-cache`](https://docs.astral.sh/ruff/configuration/) —
ruff resolves config eagerly and reports config errors before running checks. Not
pylint-specific but covers the underlying need ("validate my config without running the
linter").

#### #7835 — Warn about `os.x` used on `pathlib.Path`

**Plugin:** [Ruff `PTH` rules](https://docs.astral.sh/ruff/rules/builtin-open/)
(`flake8-use-pathlib`) — `PTH100`–`PTH210` cover the full `os.path.* → pathlib`
modernization. Also Refurb `FURB101` / `FURB104`.

#### #5838 — Lint unused variable assignment / dead store

**Plugin:** [`vulture`](https://github.com/jendrikseipp/vulture) — dedicated dead-code
finder; detects unused vars, attrs, functions, classes, _and_ unreachable code after
`return`/`break`/`continue`/`raise`. Also Ruff `F841` for the simple local-variable
case.

#### #5290 — `tempfile.TemporaryFile()` unspecified encoding

**Plugin:**
[Ruff `PLW1514` unspecified-encoding](https://docs.astral.sh/ruff/rules/unspecified-encoding/)
— already covers `open()`. Extending to `tempfile.TemporaryFile` / `NamedTemporaryFile`
is an open Ruff issue but the rule is the right home for this enhancement.

#### #5289 — Detect improvable code with `open` + `pathlib.Path`

**Plugin:**
[Ruff `PTH123` builtin-open](https://docs.astral.sh/ruff/rules/builtin-open/) + Refurb
[`FURB101`](https://github.com/dosisod/refurb) — `open(p, …)` → `p.read_text()` /
`Path(p).open()`. Direct match.

#### #5047 — Warn for variable that can be marked `Final`

**Plugin:**
[Refurb / mypy `Final` analysis](https://mypy.readthedocs.io/en/stable/final_attrs.html)
— mypy enforces `Final` once declared; for the "could be Final" _suggestion_ the closest
tools are Refurb and pyright's reportConstantRedefinition. Not a perfect plugin match,
but lives in the type-checker layer, not the linter layer.

#### #5328 — Enforce messages on `assert` statements

**Plugin:** [`flake8-assert-msg`](https://pypi.org/project/flake8-assert-msg/) — forbids
assert statements without messages. Exactly the request. (Related:
[`flake8-assertive`](https://github.com/jparise/flake8-assertive) for the unittest
variant.)

#### #4921 — Cython support

**Plugin:** [`cython-lint`](https://github.com/MarcoGorelli/cython-lint) — dedicated
`.pyx` linter, used by SciPy / scikit-learn / pandas / spaCy. Different tool, not a
pylint plugin, but it's the practical answer for users today.

#### #2493 — Add support for `noqa: ERROR MESSAGE`

**Plugin:** [Ruff](https://docs.astral.sh/ruff/linter/#error-suppression) — supports
both `# noqa: E501` AND `# pylint: disable=invalid-name`, so a project using ruff for
linting gets unified pragma handling. Doesn't make pylint _accept_ `noqa`, but solves
the cross-linter pragma fragmentation that motivated the request.

#### #600 — Detecting circular references in packages

**Plugin:** [`import-linter`](https://github.com/seddonym/import-linter) — dedicated
import-graph linter with `independence`, `forbidden`, and `layers` contracts; explicitly
built on grimp for transitive cycle detection. Pylint already has `cyclic-import`
(R0401) but it's known-limited; import-linter is the deep-coverage tool.

### 🟡 Partially covered (10)

#### #10404 — Invoke `any`/`all` on non-iterables

**Adjacent:** No direct rule found in ruff/flake8-bugbear. Closest is pyright's narrow
type inference on `Iterable`. Worth pylint absorbing — it's a small targeted check that
doesn't fit any existing plugin.

#### #10637 — Remove mandatory isort dependency

**Adjacent:** [Ruff `I` rules](https://docs.astral.sh/ruff/rules/#isort-i) re-implement
isort. The "isort dependency" concern goes away if a project uses ruff; doesn't help
projects that need pylint's check standalone.

#### #9862 — `missing-docstring` for constants and types

**Adjacent:** [`pydocstyle`](https://www.pydocstyle.org/) / Ruff `D1xx` cover
modules/functions/classes/methods but not module-level constants or `TypeAlias`. Closest
tool, but the specific ask is uncovered.

#### #9051 — `unsupported-binary-operation` on stub-typed unions

**Adjacent:** astroid-level limitation, not a checker-rule request. mypy/pyright handle
this correctly via stub-aware type inference; no pylint-plugin shape.

#### #8779 — `*` operator on container with mutables

**Adjacent:** Pyflakes / ruff don't have this.
[`flake8-bugbear` `B008`](https://github.com/PyCQA/flake8-bugbear) covers function-arg
mutable-default, related but not the same. Niche enough that no plugin targets it
directly.

#### #8230 — Force typing instead of inference

**Adjacent:** [mypy](https://mypy.readthedocs.io/) /
[pyright](https://github.com/microsoft/pyright) take annotations as authoritative by
design — exactly what the requester wants, but in a different tool. Pylint making this a
mode would be a fundamental inference-engine change.

#### #4813 — Take type annotation into account when inference fails

**Adjacent:** Same as #8230 — type checkers do this natively. Pylint absorbing it would
mean reading typeshed.

#### #5806 — Emit message for reliance on annotation never initialized

**Adjacent:** [Pyright](https://github.com/microsoft/pyright) reports this; mypy is more
lenient. No flake8-style plugin covers it.

#### #748 — Improve duplicate-code algorithm

**Adjacent:** [Clone Digger](https://clonedigger.sourceforge.net/) (AST-based
anti-unification, referenced in the original issue),
[PMD CPD](https://pmd.github.io/pmd/pmd_userdocs_cpd.html) (token-based, multi-language
including Python),
[`duplicate-code-detection-tool`](https://github.com/platisd/duplicate-code-detection-tool)
(gensim-based). External tools exist but none integrate into pylint's `similarities`
checker.

#### #2996 — Catch exhausting iterators by re-looping

**Adjacent:** No direct flake8/ruff rule. Closest is ruff's pylint-port `PLE1101`-style
checks but not this pattern. Worth pylint absorbing — narrowly scoped check.

### 🌐 External web tool (1)

#### #5972 — Pylint playground

**Tool:** No dedicated playground exists (verified: search returns generic Python
playgrounds like playcode.io, not a pylint-specific one like
[mypy-play.net](https://mypy-play.net) or
[black.vercel.app](https://black.vercel.app/)). Some clones exist on onworks.net. This
is a genuine "build the thing" item — no existing pylint playground to redirect users
to.

### ❌ Internal pylint work — no external plugin equivalent (44)

These are all structural pylint asks: control flow, config layering, pyreverse, astroid
hooks, pragma syntax, message taxonomy, baseline functionality, etc. None map cleanly to
an existing external tool because they're either (a) about pylint's architecture, (b)
about pylint's UX surface, or (c) astroid-inference work.

| Issue | Title                                                       | Why no external                                    |
| ----- | ----------------------------------------------------------- | -------------------------------------------------- |
| #9915 | `package.module` vs `package/module.py` path handling       | pylint module-loading internals                    |
| #9501 | Dynamic URL in message descriptions                         | pylint message-rendering                           |
| #9440 | Respect warning disablement / pylintrc controls             | pylint config                                      |
| #9125 | `use-a-generator` UX in test asserts                        | tweak to existing pylint checker                   |
| #8882 | Relative-indentation similarities                           | improvement to pylint's `similarities`             |
| #8538 | Detect empty list in `set.union(*[])`                       | niche astroid-inference check                      |
| #8398 | Propagate module config through imports                     | pylint config resolution                           |
| #8365 | sys.argv via index → suggest argparse                       | doable as plugin but no one wrote one              |
| #8128 | Option to ignore all pragmas                                | pylint pragma parser                               |
| #8099 | Strict design constraints                                   | pylint config                                      |
| #8013 | `--dummy-variables-rgx` / `--ignored-argument-names` doc    | docs                                               |
| #7929 | Implicit str concat — only warn without parens              | tweak existing pylint check                        |
| #7820 | Descriptor protocol support                                 | astroid update                                     |
| #7653 | Custom objects as datatypes (pyreverse)                     | pyreverse internals                                |
| #7601 | `disable-next` should target next _occurrence_              | pylint pragma engine                               |
| #7376 | CLI extend ignore from config                               | pylint config                                      |
| #7371 | `--ignore-file` with `.gitignore` default                   | pylint config (ruff has this — but as ruff config) |
| #7127 | `super()` not called in all paths with multi-base           | pylint inference check                             |
| #7121 | Confidence option intuition                                 | pylint UX                                          |
| #7120 | Config templates / message tiers                            | pylint UX                                          |
| #6992 | Multiple direct parents define same method                  | pylint inference check                             |
| #5852 | Ignore specific undefined variables                         | pylint config                                      |
| #5604 | Gamification / UX                                           | pylint UX                                          |
| #5462 | Auto-upgrade `.pylintrc` migration tool                     | pylint config                                      |
| #5403 | Baseline functionality for legacy code                      | pylint UX (ruff has `--add-noqa`, partial cover)   |
| #5274 | Override existing checks via plugin                         | pylint plugin API                                  |
| #5258 | Multiline disable for long lists                            | pylint pragma parser                               |
| #4795 | Proper control-flow implementation                          | pylint internals (the big one)                     |
| #4772 | `raising-bad-type` and `NoReturn` functions                 | pylint inference                                   |
| #4534 | `typing.cast` ignored for no-member                         | astroid brain                                      |
| #4300 | PEP 562 `__getattr__` imports                               | astroid brain                                      |
| #3767 | Different configuration per file                            | pylint config (partly: ruff has per-file-ignores)  |
| #3693 | IDE mode for checkers                                       | pylint UX                                          |
| #3408 | Autoformatter integration (line-too-long)                   | pylint UX                                          |
| #3390 | Pragma rule parameters                                      | pylint pragma engine                               |
| #3338 | More verbose `--verbose`                                    | pylint UX                                          |
| #2474 | `__path__` mangling in non-namespace package                | astroid                                            |
| #2293 | Promote/demote message severity                             | pylint config                                      |
| #2095 | Disable module caching for specific files                   | pylint internals                                   |
| #1416 | Reuse ASTs across runs                                      | pylint performance                                 |
| #971  | Pylint `--quickstart` interactive config                    | pylint UX                                          |
| #623  | Unreachable code semantic                                   | pylint control-flow                                |
| #568  | `pyreverse packages-diagram` / `classes-diagram` subparsers | pyreverse CLI                                      |
| #553  | Pylint can't understand instance attributes                 | astroid                                            |

## Triage recommendations

1. **Close-with-pointer candidates** — for each of the 18 "✅ Covered" issues, a
   maintainer could leave a comment along the lines of
   > "If you want this check today, `{plugin-name}` covers it: `{url}`. Closing as
   > covered externally — happy to reopen if there's a specific reason pylint should
   > ship this in core." This is exactly the same shape as your existing `pylint-junit`
   > redirect mentioned in the brief.
2. **Link-and-leave-open candidates** — the 10 "🟡 Partially covered" issues should have
   the adjacent tool linked in a comment, but stay open because either the coverage is
   imperfect or absorbing the check into pylint is still worthwhile.
3. **#5972 playground** — could be a Hacktoberfest / Google Summer of Code shaped
   project, not a "ship in pylint 4.x" item. mypy-play and black.vercel.app are useful
   precedents.
4. **The 44 internal issues** stay in their existing DESIGN bucket — they need pylint /
   astroid work and there is nowhere to redirect them.

## Methodology notes

- "Big" = labeled `Enhancement ✨` AND at least one of `High effort 🏋`,
  `Needs design proposal 🔒`, `Needs specification 🔐`, `Proposal 📨` in the issue's
  current label set as cached in `.triage/issues_raw.json`.
- "External" was checked via web search (PyPI / GitHub) — verified the plugin exists and
  is actively maintained (recent release in 2024 or later for almost all entries).
- This audit is opinionated about scope. A maintainer reviewing it may decide a given ✅
  should stay open (because pylint should ship the check in core anyway) or that a 🟡 is
  close enough to close. The verdicts here are "external coverage exists" / "doesn't
  exist", not "should be closed" / "shouldn't be closed".
