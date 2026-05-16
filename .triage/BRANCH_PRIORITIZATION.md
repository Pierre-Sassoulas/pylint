# Local branch prioritization

Snapshot date: 2026-05-16. Audited from `pierre@pylint` local clone vs `origin/main` at `371933bfb` ("Fix pylint skipping similarly named project directory (#10970)").

## Method

- For every non-system local branch, tested rebaseability with `git merge-tree --merge-base=$(git merge-base origin/main $b) origin/main $b`.
- Rebased the 28 conflict-free branches locally (no pushes).
- Cross-referenced each branch's target issue against `.triage/issues_raw.json` to know which are still OPEN.
- Categorized into tiers by recency, scope size, conflict count, and whether the target issue is still open.

Numbers below are post-rebase (commits ahead of `origin/main`).

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
| `scientific-notation-formatting` | **Live PR #10425 (draft)**, 69 commits, last 2026-04-26. Local stale copy + `save-scient` deleted 2026-05-16 after verifying both were 6 months behind the remote; local branch now tracks `pierre/scientific-notation-formatting` from scratch. Resume work directly on this branch. |
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
3. **Decide the fate** of the mccabe-vendoring family — big effort, finish or explicitly archive. (Scientific notation already settled: work continues on PR #10425.)
4. **Delete TIER 5** in a single sweep once you confirm you don't need any of it as reference.

## Conflicting branches — prioritized by recovery effort vs value

45 branches don't rebase cleanly. Conflict count comes from `git merge-tree`; the actual rebase may surface more (intermediate commits) or fewer (auto-resolved renames) — treat it as an effort estimate, not gospel. `maintenance/4.0.x` and `backport-sys-fix` are upstream-maintenance branches and excluded from this ranking.

### CONFLICT-TIER A — Worth resolving (recent + open issue / active plan)

Resolve the conflicts on these by hand; they map to ongoing work.

| Branch | Conflicts | Date | Reason |
|---|---|---|---|
| `wip-upgrade` | 1 | 2025-10 | Canonical conf-upgrade branch candidate; unblocks #3512 via #5462 (open) |
| `conf-upgrade-script` | 1 | 2025-12 | Same effort as `wip-upgrade`; salvage anything unique then drop |
| ~~`save-scient`~~ | — | — | Deleted 2026-05-16: was 6 months stale; live work is in PR #10425 head branch `pierre/scientific-notation-formatting` (69 commits, last 2026-04-26). No salvageable unique work. |
| ~~`scientific-notation-formatting`~~ (stale local) | — | — | Same story — deleted and re-created from `pierre/scientific-notation-formatting`. Now tracks the live PR branch. |
| `vendoring-in-small-steps` | 1 | 2025-09 | mccabe vendoring (step-by-step variant); smallest conflict in the family |
| `vendored-mccabe` | 2 | 2025-09 | mccabe vendoring main line |
| `save-old-pierre-main` | 3 | 2025-10 | mccabe vendoring snapshot — likely supersede with `vendored-mccabe` |
| `match-case-too-complex` | 3 | 2025-09 | mccabe too-complex with match-case edges (depends on vendored mccabe) |
| `primer-refactor` | 2 | 2025-09 | Primer infra cleanup |
| `refactor-primer_comparator` | 2 | 2025-09 | Has a merge commit — easier to redo on top of fresh main |
| `dataclass-in-package-to-lint` | 1 | 2025-09 | Smallest of the primer trio (1 commit, +13/-25). Easiest path. |

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

### CONFLICT-TIER D — Stale + closed issue / obsolete → delete

Target issue is closed (verified via `.triage/issues_raw.json`), or the approach has been superseded. Recommend `git branch -D` once you've eyeballed the list.

Closed-issue branches:

- `issue-5288` (1 conflict, 2023-03, closed)
- `issue-6538` (1 conflict, 2022-05, closed)
- `issue-3651` (6 conflicts, 2022-08, closed)
- `super-crash` (2 conflicts, 2023-05, #8554 closed)
- `regression-tests-7710` (3 conflicts, 2023-09, #7710 closed)
- `cgroupsv2-cpu-count` (1 conflict, 2024-12, #10103 closed)
- `check-non-constant-module-level-variable` (2 conflicts, 2023-08, #3585 closed)

2024 stale WIPs (no clear issue, dormant 1+ year):

- `crash-consider-using-enumerate` (1)
- `litteral-dict` (1)
- `feature-print-filepaths` (2) and `feature-print-filepaths-save` (2)
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

1. `dataclass-in-package-to-lint` (1 conflict, 1 commit, smallest)
2. `vendoring-in-small-steps` (1 conflict)
3. `wip-upgrade` (1 conflict) — most strategic value
4. `vendored-mccabe` (2 conflicts) — mccabe family
5. Stop and re-evaluate after these four. Everything below is either redundant with the above, a TIER-D delete candidate, or a "start over" call.

For the scientific-notation feature, no local conflict-resolution is needed: work continues directly on `pierre/scientific-notation-formatting` (PR #10425).

## Rebase status reference

Conflict-free rebases applied locally (28 branches; none pushed):

`add-tests-for-message-control`, `check-message-reference`, `configuration-upgrader-script`, `copilot/fix-10519`, `copilot-instruction`, `deprecated-module-partial`, `docstring-using-node`, `enable-error-checking-in-doc-tests`, `enforce-the-confidence-in-add-message`, `false-negative-chained-comparison`, `false-negative-consider-using-any-or-all`, `false-negative-consider-using-enumerate`, `first-patch-2471`, `fix-ignored-unused-variable-configuration`, `fix-inconsistent-circular-import-with-multiple-jobs`, `issue-2072`, `issue-3339`, `issue-8419`, `move-pragma-to-message`, `optimized-message-store`, `primer-equivalent-message`, `regression-test-2072`, `relative-path-for-spelling-dict`, `spelling-checker-refactor-initialization`, `upgrade-breaking-change-data-structure`, `use-x-literal`.

(Two of the originally-clean set — `fix-changelog-9167`, `disable-benchmark-in-ci` — rebased to origin/main exactly and were deleted.)
