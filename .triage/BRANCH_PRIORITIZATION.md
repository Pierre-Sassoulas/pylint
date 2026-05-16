# Local branch prioritization

Snapshot date: 2026-05-16. Audited from `pierre@pylint` local clone vs `origin/main` at `371933bfb` ("Fix pylint skipping similarly named project directory (#10970)").

## Method

- For every non-system local branch, tested rebaseability with `git merge-tree --merge-base=$(git merge-base origin/main $b) origin/main $b`.
- Rebased the 28 conflict-free branches locally (no pushes).
- Cross-referenced each branch's target issue against `.triage/issues_raw.json` to know which are still OPEN.
- Categorized into tiers by recency, scope size, conflict count, and whether the target issue is still open.

Numbers below are post-rebase (commits ahead of `origin/main`).

## Deleted (already in main)

| Branch | Note |
|---|---|
| ~~`fix-changelog-9167`~~ | tip == origin/main after rebase; deleted |
| ~~`disable-benchmark-in-ci`~~ | tip == origin/main after rebase; deleted |
| ~~`backport-10929-to-maintenance/4.0.x`~~ | fully behind origin/main; deleted, stale worktree pruned |

## TIER 1 — High value, near-mergeable

Clean rebase, focused diff, clear scope. Open PRs from these next.

| Branch | Why | Action |
|---|---|---|
| `copilot/fix-10519` | 40-line regression test for **open** #10519 | Polish commit msg, open PR |
| `enforce-the-confidence-in-add-message` | tiny test enforcing confidence in `add_message` | Open PR |
| `copilot-instruction` | trims outdated "python 3.8" copilot instructions (-41 lines) | Open PR |
| `check-message-reference` | script + pre-commit hook to add msg-ref to docs (412 lines) | Open PR (dev infra) |
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

## TIER 3 — 2025 work worth keeping (conflicts but fixable)

| Branch | Notes |
|---|---|
| `scientific-notation-formatting` / `save-scient` | 23 files +844 lines. `save-scient` is one commit ahead of the other — pick one. Big feature. |
| `vendored-mccabe` + `vendoring-in-small-steps` + `save-old-pierre-main` + `match-case-too-complex` | mccabe vendoring family. Active in Sep 2025. Pick a canonical branch. |
| `primer-refactor` + `dataclass-in-package-to-lint` + `refactor-primer_comparator` | primer infra cleanup. Smallest (`dataclass-in-package-to-lint`, 1 commit) may be the easiest path. |
| `fix-element-of-a-list-inside-list` | small (34 lines), 1 conflict |
| `docstring-using-node`, `enable-error-checking-in-doc-tests`, `deprecated-module-partial` | small clean rebases, all WIP |
| `codegen-bot/simplify-complex-conditionals` | 6/7 lines — codegen output, marginal value |
| `files` | "files" option, 157 lines, 2 conflicts |

## TIER 4 — Issue still open but branch stale, low-cost regression tests

For OPEN issues, these tiny test-only branches could be polished into PRs.

| Branch | Issue | Diff |
|---|---|---|
| `issue-3339` | #3339 open | +20 functional test |
| `issue-2072` / `regression-test-2072` | #2072 open | +30 functional test (duplicate of each other — keep one) |
| `false-negative-consider-using-any-or-all` | open | 13 lines WIP |
| `false-negative-consider-using-enumerate` | open | 21 lines WIP |

Note: `issue-8419` is already covered by `regression-tests-fixed-issues` — delete it.

## TIER 5 — Stale, target issue closed, recommend deletion

Targets a closed issue or fundamentally outdated approach. Closed status verified against `.triage/issues_raw.json` (which only contains open issues — "not-in-snapshot" means closed).

Closed-issue branches:

- `cgroupsv2-cpu-count` (#10103 closed)
- `issue-6538` (closed)
- `issue-5288` (closed)
- `super-crash` (#8554 closed)
- `regression-tests-7710` (#7710 closed)
- `first-patch-2471` (#2471 closed)

Old refactor experiments / WIPs:

- `issue-3651`, `fix-implicit-abstract-class`, `decorator-spelling-checker`
- 2024 WIPs: `crash-consider-using-enumerate`, `litteral-dict`, `feature-print-filepaths`, `feature-print-filepaths-save`, `autofix-with-fixit`, `better-message-for-use-implicit-booleaness-not-len`, `document-deleted-messages`, `spelling-checker-refactor-initialization`
- 2022-2023 experiments: `change-primer-datastructure`, `better-primer-diff`, `refactor-primer-stash`, `remove-ini-support`, `remove-isort`, `all-options`, `uniformize-message-use-implicit-booleaness`, `move-pragma-to-message`, `optimized-message-store`, `use-x-literal`, `primer-equivalent-message`, `ruff-for-pylint`, `make-invalid-name-oddity-explicit`, `fix-ignored-unused-variable-configuration`, `fix-inconsistent-circular-import-with-multiple-jobs`, `more-useless-comprehension`, `pylint-default-to-current-dir`, `check-non-constant-module-level-variable`, `relative-path-for-spelling-dict`, `add-number-of-duplicated-line-in-msg`, `remove-return-in-generator`, `fix-panda-numpy-false-positive`

Special case:

- `fix-5083` — #5083 still **open** but 9 conflicts on a 2022 branch. Faster to start over than salvage.

## Suggested next moves (in order)

1. **Open small PRs** from TIER 1 (the copilot fix, confidence test, copilot-instructions cleanup, message-ref script). Low-risk wins.
2. **Pick a canonical conf-upgrade branch** (recommend `wip-upgrade`), merge unique work from the other three, archive the rest. Unblocks #3512.
3. **Decide the fate** of `scientific-notation-formatting` and the mccabe-vendoring family — big efforts, finish or explicitly archive.
4. **Delete TIER 5** in a single sweep once you confirm you don't need any of it as reference.

## Rebase status reference

Conflict-free rebases applied locally (28 branches; none pushed):

`add-tests-for-message-control`, `check-message-reference`, `configuration-upgrader-script`, `copilot/fix-10519`, `copilot-instruction`, `deprecated-module-partial`, `docstring-using-node`, `enable-error-checking-in-doc-tests`, `enforce-the-confidence-in-add-message`, `false-negative-chained-comparison`, `false-negative-consider-using-any-or-all`, `false-negative-consider-using-enumerate`, `first-patch-2471`, `fix-ignored-unused-variable-configuration`, `fix-inconsistent-circular-import-with-multiple-jobs`, `issue-2072`, `issue-3339`, `issue-8419`, `move-pragma-to-message`, `optimized-message-store`, `primer-equivalent-message`, `regression-test-2072`, `relative-path-for-spelling-dict`, `spelling-checker-refactor-initialization`, `upgrade-breaking-change-data-structure`, `use-x-literal`.

(Two of the originally-clean set — `fix-changelog-9167`, `disable-benchmark-in-ci` — rebased to origin/main exactly and were deleted.)
