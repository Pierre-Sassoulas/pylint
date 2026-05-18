# Local branch prioritization

Snapshot date: 2026-05-18 (refresh). Audited from `pierre@pylint` local clone vs `origin/main` at `d523e3e89` ("Replace `MSG_STATE_*` int constants with `MessageDisableScope` enum"). Eight merges have landed since the 2026-05-18 morning snapshot at `628f3a759`; landed-since-snapshot work is called out per-tier.

## Landed since last snapshot (origin/main `628f3a759` → `d523e3e89`)

| Commit | PR | Closes | Local branch (now mergeable into main, archive/delete) |
|---|---|---|---|
| `d523e3e89` | — | refactor | `enum-for-scope-control` (MSG_STATE_* enum part) |
| `7667457f5` | — | refactor | `tighten-confidence-nullable` |
| `52efad31a` | #11015 | #11015 (FP E0203 bare type annotation) | _no local_ |
| `9f08fc7bb` | #7955 | #7950 (abstract-method FN) | `takeover-7955` |
| `c0aa7e58e` | #7360 | #6211 (NumPy default-param doc) | `takeover-7360` (head on adam-grant-hendry fork) |
| `31095a23f` | — | col_offset=0 preserve | `add-message-falsey-value-fix` |
| `166f071ed` | #11014 | #11014 (FP inconsistent-return-statements + NoReturn) | _no local_ |
| `0e9a3fc57` | — | doc clarification | _no local_ (closes #10680 in docs) |
| `3d7ac126f` | #10989 | #3716 (NamedTuple dangerous-default-value FN) | _no local_ |

Triage-state impact: #7950, #6211, #3716 moved REPRO/DESIGN → FIXED. Verdict tally is now DESIGN 596 / EXTDEP 197 / REPRO 180 / FIXED 32 / UNCLEAR 9 / DUP 2 / STALE 1, over 1017 still-open issues.

## Method

- For every non-system local branch, tested rebaseability with `git merge-tree --merge-base=$(git merge-base origin/main $b) origin/main $b`.
- Rebased the conflict-free branches locally (no pushes).
- Cross-referenced each branch's target issue against `.triage/issues_raw.json` to know which are still OPEN.
- Categorized into tiers by recency, scope size, conflict count, and whether the target issue is still open.

Numbers below are post-rebase (commits ahead of `origin/main`).

## TIER 0 — Live open PRs (active work)

Branches that already have an open PR by Pierre on pylint-dev/pylint. Local copies track the live PR head; resume work there directly. Banded by ship-readiness.

### P0 — Ready (not draft, recent activity) → push for merge

These are out of draft and saw activity in the last ~2 months. Each blocks little new work but lands real user-visible value.

| PR | Title | Updated | Local branch | Head ref |
|---|---|---|---|---|
| #10881 | Fix quadratic perf/memory in duplicate-code | 2026-04-24 | _no local_ | `Pierre-Sassoulas:symilar-performance` |
| #10894 | Add `module`/`filepath` params to `add_message` | 2026-03-08 | _no local_ | `pylint-dev:add-message-module-file` |
| #7611 | Generalize `chained-comparison` (taken over from areveny) | 2026-05-18 | `takeover-7611` | `areveny:release-chained-comparison` |
| _(py3.15)_ | Add preliminary support for Python 3.15 (takeover) | 2026-05-18 | `takeover-py315-support` | (no upstream PR yet — open one) |

**Why P0:** non-draft = author thinks it's review-ready. #10881 is a user-facing performance fix; #10894 is an API extension that downstream checkers can consume. #7611 is a graph-based impossible-comparison / chained-comparison-all-equal rewrite on top of areveny's stalled PR — local branch has heavy recent activity (test coverage to 100%, codecov-flag cleanup, docs). The py3.15-support local branch is one commit (`c508e26e3`) ahead of main with the new-version scaffolding; needs a PR opened upstream.

**Landed since previous snapshot:** #7360 (closed #6211 — `takeover-7360` is now archivable).

### P1 — Active feature drafts (recent, major scope) → finalize

Drafts touched in the last ~2 months with substantial work behind them. Need a final polish pass and a "mark ready for review" flip.

| PR | Title | Updated | Local branch | Head ref |
|---|---|---|---|---|
| #10425 | Misleading scientific/engineering/underscore notations | 2026-04-26 | `scientific-notation-formatting` | `Pierre-Sassoulas:scientific-notation-formatting` |
| #10551 | Re-implement mccabe (supply-chain) | 2026-04-19 | `vendored-mccabe` | `pylint-dev:vendored-mccabe` |
| #10880 | Attribute duplicate-code messages correctly | 2026-03-07 | _no local_ | `pylint-dev:fix-2368` |

**Why P1:** these are the meatiest in-flight features. Landing #10551 unblocks `match-case-too-complex`. #10880 is a logical follow-up after #10881. #10425 has 69 commits and a coherent architecture — the long tail of edge cases is what's left.

### P2 — Recent infra drafts → land when convenient

Internal/dev infra. Lower stakes, less time-sensitive.

| PR | Title | Updated | Local branch | Head ref |
|---|---|---|---|---|
| #10893 | Benchmark CI comment workflow | 2026-05-07 | _no local_ | `pylint-dev:benchmark-ci-comment` |
| #10914 | [primer] Show changed messages as diffs | 2026-04-26 | _no local_ | `Pierre-Sassoulas:primer-message-smarter-diff` |

### P3 — Stale, needs a decision (rebase + finish, or close)

No activity in 6+ months (or, for #9072, a long-running draft despite recent rebase). Each one is sunk cost — the right move may be to close.

| PR | Title | Updated | Local branch | Head ref |
|---|---|---|---|---|
| #10176 | New check: unguarded-typing-import (not draft, but stale) | 2025-10-11 | _no local_ | `Pierre-Sassoulas:used-only-for-typechecking` |
| #10568 | Add `:ref:` script for docs | 2025-10-12 | `check-message-reference` | `pylint-dev:check-message-reference` |
| #9072 | `pylint` equivalent to `pylint .` (long-running draft) | 2026-04-19 | `pylint-default-to-current-dir` | `Pierre-Sassoulas:pylint-default-to-current-dir` |

**Why P3:** #10176 is the only non-draft here — it's apparently ready but stuck; either rebase and merge, or there's unaddressed review feedback you've lost track of. #10568 has been dormant for 7 months. #9072 has been a draft for *years* — at some point the "pylint as `pylint .`" decision needs an explicit yes/no, since the lingering draft signals indecision.

### Recommended order

1. **#10881** then **#10894** — clear the non-draft backlog first
2. **#7611** — heavy local polish already done; finish review + ship
3. **py3.15-support** — open the upstream PR while the diff is small (one commit)
4. **#10551** — small enough to finish and unblocks `match-case-too-complex`
5. **#10880** — pair this with #10881 if duplicate-code is on your mind anyway
6. **#10425** — biggest feature; once polished, flip it ready
7. **#10893**, **#10914** — opportunistic when context-switching
8. **#10176**, **#10568**, **#9072** — block out an hour to triage these three: rebase + merge, or close with a comment

## TIER 1 — High value, no PR yet, near-mergeable

Clean rebase, focused diff, clear scope. Open PRs from these next.

| Branch | Why | Action |
|---|---|---|
| `copilot/fix-10519` | 40-line regression test for **open** #10519 | Polish commit msg, open PR |
| `enforce-the-confidence-in-add-message` | tiny test enforcing confidence in `add_message` | Open PR |
| `copilot-instruction` | trims outdated "python 3.8" copilot instructions (-41 lines) | Open PR |
| `add-tests-for-message-control` | 211 lines of new message-control tests | Polish (commit name `ruff noqaé` is messy) |
| `false-negative-chained-comparison` | 2026-05 active, better chained-comparison message | Decide direction, push to pierre |

## TIER 2 — Aligned with active #3512 / #5462 conf-upgrade plan

Substantial duplication — four branches attacking the conf-upgrade script.

| Branch | Status | Diff |
|---|---|---|
| `upgrade-breaking-change-data-structure` | clean rebase | 8 files, +620/-170 (data structure + #10711 regression test) |
| `configuration-upgrader-script` | clean rebase | 6 files, +161/-13 (base impl) |
| `conf-upgrade-script` | 1 conflict | 12 files, +637/-170 (more advanced) |
| `wip-upgrade` | 1 conflict | 15 files, +561 (newest, has whatsnew fragments) |

**Recommendation:** pick `wip-upgrade` as canonical (most complete + recent), salvage anything unique from the others, then archive the rest. This is the prerequisite for landing #3512 per `.triage/issue_3512_plan.md`.

## TIER 3 — 2025 work, no PR yet (conflicts but fixable)

| Branch | Notes |
|---|---|
| `vendoring-in-small-steps` | Alternative approach to PR #10551 (mccabe vendoring done in smaller steps). Pierre's live PR uses the optimized approach — this is only worth resurrecting if you want to break that PR into smaller pieces. |
| `match-case-too-complex` | Depends on PR #10551 landing; rebase on top once mccabe vendoring is merged. |
| `fix-element-of-a-list-inside-list` | small (34 lines), 1 conflict |
| `docstring-using-node`, `enable-error-checking-in-doc-tests`, `deprecated-module-partial` | small clean rebases, all WIP |
| `codegen-bot/simplify-complex-conditionals` | 6/7 lines — codegen output, marginal value |
| `files` | "files" option, 157 lines, 2 conflicts |

## TIER 4 — Issue still open but branch stale, low-cost regression tests

For OPEN issues, these tiny test-only branches could be polished into PRs.

| Branch | Issue | Diff |
|---|---|---|
| `issue-3339` | #3339 open | +20 functional test |
| `issue-2072` | #2072 open | +30 functional test |
| `false-negative-consider-using-any-or-all` | open | 13 lines WIP |
| `false-negative-consider-using-enumerate` | open | 21 lines WIP |

Note: `issue-8419` is already covered by `regression-tests-fixed-issues` — delete it.

## TIER 5 — Stale, recommend deletion

Old refactor experiments / WIPs (no specific issue or issue closed):

- `fix-implicit-abstract-class`, `decorator-spelling-checker`
- 2024 WIPs: `crash-consider-using-enumerate`, `litteral-dict`, `feature-print-filepaths`, `autofix-with-fixit`, `better-message-for-use-implicit-booleaness-not-len`, `document-deleted-messages`, `spelling-checker-refactor-initialization`
- 2022-2023 experiments: `change-primer-datastructure`, `better-primer-diff`, `refactor-primer-stash`, `remove-ini-support`, `remove-isort`, `all-options`, `uniformize-message-use-implicit-booleaness`, `move-pragma-to-message`, `optimized-message-store`, `use-x-literal`, `primer-equivalent-message`, `ruff-for-pylint`, `make-invalid-name-oddity-explicit`, `fix-ignored-unused-variable-configuration`, `fix-inconsistent-circular-import-with-multiple-jobs`, `more-useless-comprehension`, `pylint-default-to-current-dir`, `relative-path-for-spelling-dict`, `add-number-of-duplicated-line-in-msg`, `remove-return-in-generator`, `fix-panda-numpy-false-positive`

Special case:

- `fix-5083` — #5083 still **open** but 9 conflicts on a 2022 branch. Faster to start over than salvage.

## Branch relationships (ordering hints)

Audited by comparing pairwise ancestry, commit subjects, and the actual files touched (`git diff $(merge-base)..branch`). These relationships aren't visible from branch listings alone.

### Logical dependency (not a git stack — needs manual rebase)

| Depends on | Dependent | Note |
|---|---|---|
| `vendored-mccabe` (or whichever mccabe-vendoring branch you pick) | `match-case-too-complex` | `match-case-too-complex` modifies `pylint/extensions/mccabe.py` assuming the vendored version exists. Currently they're parallel — land vendoring first, then rebase. |

### Parallel re-implementations (NOT stacks — pick canonical, archive rest)

These four conf-upgrade branches all chase the same goal but each rewrote the data structure from scratch. The directory each one creates is the easiest way to tell them apart:

| Branch | Module path | Era |
|---|---|---|
| `configuration-upgrader-script` | single file `_breaking_changes.py` | earliest prototype |
| `upgrade-breaking-change-data-structure` | subpackage `_breaking_changes/` with `typing.py`, `condition.py`, `solution.py` | data-structure refactor |
| `conf-upgrade-script` | subpackage `_breaking_changes/` with `intention.py`, `config_file.py` (no solution/typing) | next iteration |
| `wip-upgrade` | **renamed module** `_pylint_upgrade_conf/` with `check_config_upgrade.py`, `upgrade.py` | most recent rename |

The directory rename in `wip-upgrade` confirms it's the latest direction. The mccabe situation is now resolved by PR #10551 (head: `vendored-mccabe` on pylint-dev) — `vendoring-in-small-steps` is the gradual-approach alternative, unused unless you want to break the PR up.

### Independent — no consolidation needed

`false-negative-chained-comparison` (touches `refactoring_checker.py` + test), `false-negative-consider-using-any-or-all` (test only), `false-negative-consider-using-enumerate` (test only) all touch disjoint files. Treat each as its own PR.

## Suggested next moves (in order)

1. **Archive landed-and-merged branches** in one sweep: `takeover-7955`, `takeover-7360`, `tighten-confidence-nullable`, `fix-numpy-default-param-doc`, `add-message-falsey-value-fix`, `add-assert-does-not-add-messages`, `enum-for-scope-control` (MSG_STATE_* int part — keep the branch only if the scope-string follow-up is still planned).
2. **Open upstream PR for `takeover-py315-support`** while it's a single commit — easier to review and trigger CI now than after rebases pile up.
3. **Triage TIER 0**: PR #10568 (`check-message-reference`) has been dormant since Oct 2025 — rebase and ping reviewers, or close. Same question for #9072 (`pylint-default-to-current-dir`) which has been a draft for years.
4. **Open small PRs** from TIER 1 (the copilot fix, confidence test, copilot-instructions cleanup, message-control tests). Low-risk wins.
5. **Pick a canonical conf-upgrade branch** (recommend `wip-upgrade`), merge unique work from the other three, archive the rest. Unblocks #3512.
6. **Delete TIER 5** in a single sweep once you confirm you don't need any of it as reference.

## Conflicting branches — prioritized by recovery effort vs value

Conflict counts come from `git merge-tree`; the actual rebase may surface more (intermediate commits) or fewer (auto-resolved renames) — treat as an effort estimate. `maintenance/4.0.x` and `backport-sys-fix` are upstream-maintenance branches and excluded.

### CONFLICT-TIER A — Worth resolving (recent + open issue / active plan)

Resolve the conflicts on these by hand; they map to ongoing work.

| Branch | Conflicts | Date | Reason |
|---|---|---|---|
| `wip-upgrade` | 1 | 2025-10 | Canonical conf-upgrade branch candidate; unblocks #3512 via #5462 (open) |
| `conf-upgrade-script` | 1 | 2025-12 | Same effort as `wip-upgrade`; salvage anything unique then drop |
| `vendoring-in-small-steps` | 1 | 2025-09 | Alternative gradual approach to PR #10551; only useful if you want to split the PR |
| `match-case-too-complex` | 3 | 2025-09 | Depends on PR #10551 landing first |

### CONFLICT-TIER B — Recent but lower stakes

Worth a second look only if the topic is still on the roadmap.

| Branch | Conflicts | Date | Reason |
|---|---|---|---|
| `fix-element-of-a-list-inside-list` | 1 | 2025-05 | 34 lines WIP; recent enough to be salvageable |
| `codegen-bot/simplify-complex-conditionals` | 1 | 2025-05 | 7 lines codegen output; only finish if you trust the suggestions |
| `files` | 2 | 2025-04 | "files" option, 157 lines — decide if you want this feature |

### CONFLICT-TIER C — Stale but target issue still open → start over

Branch is too old to salvage cheaply; faster to write a fresh patch.

| Branch | Conflicts | Date | Issue |
|---|---|---|---|
| `fix-5083` | 9 | 2022-06 | #5083 open — 4-year-old 13-file diff, rewrite from scratch |
| `make-invalid-name-oddity-explicit` | 1 | 2023-02 | no specific issue; pre-emptive cleanup, low priority |

### CONFLICT-TIER D — Stale, obsolete approach → delete

Recommend `git branch -D` once you've eyeballed the list.

2024 stale WIPs (no clear issue, dormant 1+ year):

- `crash-consider-using-enumerate` (1)
- `litteral-dict` (1)
- `feature-print-filepaths` (2)
- `autofix-with-fixit` (4)
- `better-message-for-use-implicit-booleaness-not-len` (1)
- `document-deleted-messages` (1)

2022-2023 abandoned experiments (3+ years dormant):

- `more-useless-comprehension` (1)
- `pylint-default-to-current-dir` (1)
- `remove-ini-support` (2)
- `all-options` (1)
- `add-number-of-duplicated-line-in-msg` (1)
- `remove-isort` (2)
- `refactor-primer-stash` (2)
- `uniformize-message-use-implicit-booleaness` (17) — biggest conflict count of all; clearly abandoned
- `ruff-for-pylint` (2)
- `remove-return-in-generator` (3)
- `fix-implicit-abstract-class` (1, 2021)
- `fix-panda-numpy-false-positive` (2) — superseded by [[numpy-2x-brain-plan]]
- `decorator-spelling-checker` (1)
- `change-primer-datastructure` (3, 2022)
- `better-primer-diff` (2, 2022)

### Conflict-resolution order (if you want to power through)

1. `wip-upgrade` (1 conflict) — most strategic value (#3512 prerequisite)
2. `conf-upgrade-script` (1 conflict) — same family, salvage uniques
3. Stop and re-evaluate. mccabe and scientific-notation work continues on the live PRs (#10551, #10425); no local rebase needed for those.

## Rebase status reference

Conflict-free rebases applied locally (none pushed):

`add-tests-for-message-control`, `check-message-reference`, `configuration-upgrader-script`, `copilot/fix-10519`, `copilot-instruction`, `deprecated-module-partial`, `docstring-using-node`, `enable-error-checking-in-doc-tests`, `enforce-the-confidence-in-add-message`, `false-negative-chained-comparison`, `false-negative-consider-using-any-or-all`, `false-negative-consider-using-enumerate`, `fix-ignored-unused-variable-configuration`, `fix-inconsistent-circular-import-with-multiple-jobs`, `issue-2072`, `issue-3339`, `issue-8419`, `move-pragma-to-message`, `optimized-message-store`, `primer-equivalent-message`, `relative-path-for-spelling-dict`, `spelling-checker-refactor-initialization`, `upgrade-breaking-change-data-structure`, `use-x-literal`.
