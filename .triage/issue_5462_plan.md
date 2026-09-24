# Issue #5462 — Configuration auto-upgrade tool implementation plan

**Target audience:** a pylint maintainer (Pierre, or a contributor) picking up
the auto-upgrade tool, wanting "what is decided, what is left, in what order."

**Goal:** ship `pylint-config upgrade`, an interactive tool that migrates a
user's configuration across pylint breaking changes, so future configuration
breaking changes become safe to make. This is the prerequisite for #3512 (the
"recommended" preset): see [[issue-3512-plan]] / `.triage/issue_3512_plan.md`.

## TL;DR

1. The breaking-change **data structure already exists on `main`**
   (`pylint/config/_breaking_changes/`, enum-based, 5 entries, no runner).
   Nothing imports it yet, so it is free to refactor.
2. **Four prototype branches** attacked the runner; none merged; each rewrote
   the data model. The newest (`upgrade-breaking-change-data-structure`,
   2026-05-16) carries the OOP data model this plan builds on.
3. The keystone every prototype stubbed: a real **`ConfigFile`** that reads a
   config, answers `Condition` queries, applies `Solution` mutations, and
   writes the result back.
4. Deliver as **four reviewable PRs**: data model, `ConfigFile`, the command,
   the stale-config hint.

## Locked decisions (2026-05-21)

| Decision | Choice | Rationale |
| --- | --- | --- |
| v1 scope | Full interactive upgrade (KEEP / USE_DEFAULT prompts), not automated-only | user call |
| File formats | TOML only on write. Reading ini/cfg/pylintrc is supported as an ini-to-`pyproject.toml` migration on-ramp | user call: "if someone has ini they start using toml" |
| Stale config | One-line opt-out hint on a normal `pylint` run | user call |
| Data model | Build on `upgrade-breaking-change-data-structure` (OOP), not `wip-upgrade` | newest branch; `wip-upgrade` is 2025-10 |
| `Solution` design | Make `Solution` real objects (`__str__` + `apply`); `BreakingChange.apply_solution` becomes generic in the base | removes the dead `solution.py` and the string/code duplication |
| `upgraded-to` marker | A real registered option (string, sentinel `latest`) | pylint parses it for free during config load |
| Stale-hint mechanism | A `configuration-outdated` informational (`I`) message, opt-out via the normal `disable=` | idiomatic, no bespoke flag, does not affect score/exit |

## Status of the moving parts (2026-05-21)

| Piece | Where | State |
| --- | --- | --- |
| Issue #5462 | GitHub | Open, assigned Pierre, milestone 4.1.0, labels Configuration / Enhancement / High effort / WIP |
| Issue #5465 (whitelist rename) | GitHub | Open, the first concrete use case (the `2.7.3` entry) |
| Data structure | `main`, `pylint/config/_breaking_changes/` | Landed (PR #9088 plus follow-ups). Enum-based, data only, no runner. No importers. |
| `upgrade-breaking-change-data-structure` | local + `pierre/` | Newest (2026-05-16). OOP data model. Has bugs (see PR 1). Needs rebase. |
| `conf-upgrade-script` | local + `pierre/` | 2025-12. Best command wiring: `pylint-config upgrade` subcommand, `ConfigFile` interface (stubs), `upgraded-to` option, `emit_upgrade_warnings`. |
| `wip-upgrade` | local + `pierre/` | 2025-10. Fullest runner logic (`upgrade.py`, 347 lines) but crude: lossy rewrite, naive version compare, substring-match bugs. |
| `configuration-upgrader-script` | local + `pierre/` | Earliest, single-file model. Superseded. |
| `pierre/add-upgrade-option` | `pierre/` | 2023 stub. Superseded. |

The four prototype branches are salvage references, not rebase targets. The
work is reimplemented fresh off `origin/main` (PR 1 below). Archive all four
once their unique pieces are absorbed.

## Architecture

```
pylint/config/_breaking_changes/        pure logic, no file I/O (PR 1)
  base.py             Intention; Condition/Solution ABCs; BreakingChange; ConfigView Protocol
  condition.py        concrete Condition classes
  solution.py         concrete Solution classes (real: __str__ + apply)
  breaking_change.py  thin BreakingChange subclasses
  breaking_changes.py CONFIGURATION_BREAKING_CHANGES catalog + BreakingChanges iterator

pylint/config/_pylint_config/
  config_file.py      ConfigFile: concrete ConfigView, tomlkit read/write (PR 2)
  upgrade_command.py  handle_upgrade_command + interactive loop (PR 3)
  setup.py / main.py  + `upgrade` subparser and dispatch (PR 3)
  utils.py            + intention-choice prompt helper (PR 3)

pylint/lint/base_options.py             + `upgraded-to` option (PR 4)
pylint/config/config_initialization.py  emit `configuration-outdated` (PR 4)
```

Four components carry the design:

1. **`ConfigView` Protocol** (in `base.py`). The query plus mutate interface.
   `Condition` and `Solution` depend on this abstraction, never on a file, so
   `_breaking_changes/` stays free of `tomlkit` and is unit-testable with a
   dict-backed fake. Methods:
   - queries: `is_message_enabled`, `is_message_disabled`,
     `is_extension_loaded`, `has_option`
   - mutations: `enable_message`, `disable_message`, `remove_from_enable`,
     `remove_from_disable`, `add_extension`, `remove_extension`,
     `remove_option`, `rename_option`

2. **`ConfigFile`** (PR 2): the concrete `ConfigView`. Reads toml/ini, keeps a
   `tomlkit` document for lossless writing, always writes `pyproject.toml`.
   TOML input is edited in place with comments preserved; ini input produces a
   fresh `pyproject.toml` (the migration), with a printed notice that ini
   comments were not carried over.

3. **`BreakingChanges` iterator** (PR 1): yields the `(version, change)` pairs
   newer than the config's `upgraded-to` version; `.applicable(config)`
   filters by `is_affected`.

4. **`pylint-config upgrade`** (PR 3): single-intention (`FIX_CONF`) changes
   auto-apply; two-intention changes prompt KEEP vs USE_DEFAULT. Then it stamps
   `upgraded-to` and saves.

## Delivery: four PRs

v1 is the full interactive tool, split across four PRs for reviewability, not
feature-gated. PR 1 also unblocks the #3512 preset work in parallel.

### PR 1 — Data-model consolidation (zero runtime behavior change)

The data model on `main` is imported by nothing, so this is a safe pure
refactor. Branch `config-upgrade-data-model`, off `origin/main`.

- [ ] Rewrite `pylint/config/_breaking_changes/` as `base.py` + `condition.py`
      + `solution.py` + `breaking_change.py` + `breaking_changes.py` +
      `__init__.py` (the OOP model from `upgrade-breaking-change-data-structure`)
- [ ] Name the base module `base.py`, not `typing.py` (do not shadow stdlib)
- [ ] Add the `ConfigView` Protocol; type `Condition.is_met` / `Solution.apply`
      against it, not `argparse.Namespace`
- [ ] Make `Solution` subclasses real: each gets `__str__` (description) and
      `apply(config)`; `BreakingChange.apply_solution` becomes generic in the
      base (`for s in solutions[intention]: s.apply(config)`), no per-subclass
      override
- [ ] Fix the two bugs on the branch: `BreakingChanges.__iter__` called
      `is_affected()` with no `config`; version comparison compared generator
      objects with `>`. Add a tuple-based `_parse_version` (ignore pre-release
      suffixes; honor the `latest` sentinel)
- [ ] Keep `MessageMadeDisabledByDefault` / `MessageMadeEnabledByDefault` even
      though no catalog entry uses them yet: they are the explicit #3512 hook
- [ ] Catalog stays at the 6 versioned entries (1.7.0, 2.6.0, 2.7.3, 2.14.0,
      3.0.0, 4.0.0)
- [ ] Unit tests: each `BreakingChange` against a fake `ConfigView`;
      `_parse_version`; `BreakingChanges` iteration

### PR 2 — `ConfigFile`: concrete `ConfigView` with TOML round-trip

- [ ] New `_pylint_config/config_file.py`. Reuse `_ConfigurationFileParser` /
      `_RawConfParser` for semantic values; keep a `tomlkit` document when the
      input is toml
- [ ] Locate `enable` / `disable` / `load-plugins` / options across the
      `[tool.pylint.*]` sub-tables (they are not all top-level)
- [ ] Parse `enable` / `disable` to token lists for exact membership (the
      `wip-upgrade` substring match flags `no-member` inside
      `c-extension-no-member`); normalize msgid/symbol via `linter.msgs_store`
- [ ] Implement every `ConfigView` query and mutator
- [ ] Write path always emits `pyproject.toml`. TOML input is edited in place
      (comments preserved); ini input writes a new `pyproject.toml` plus the
      comment-loss notice
- [ ] `upgraded-to` read/write helpers
- [ ] Unit tests: round-trip, comment preservation, ini-to-toml migration

### PR 3 — The `pylint-config upgrade` command

- [ ] `setup.py`: `upgrade` subparser; optional positional config path;
      `--non-interactive` (apply only single-intention `FIX_CONF` changes,
      list the rest)
- [ ] `main.py`: dispatch to `handle_upgrade_command`
- [ ] `upgrade_command.py`: discover config (positional or
      `find_default_config_files`), build `ConfigFile`, compute from/to
      versions, iterate `BreakingChanges`, apply or prompt per change, stamp
      `upgraded-to`, `save()`
- [ ] `utils.py`: a validated intention-choice prompt reusing the
      `should_retry_after_invalid_input` / `exit()` pattern
- [ ] Functional tests in `tests/config/pylint_config/` with
      `tests/config/functional/upgrade/<case>/` fixtures (input config,
      scripted answers, `expected.toml`). Discard the broken placeholder test
      from `configuration-upgrader-script` (`assert directory is None`)

### PR 4 — Stale-config hint and docs

- [ ] `base_options.py`: register `upgraded-to` (string,
      `hide_from_config_file: False`, sentinel `latest`)
- [ ] New `configuration-outdated` informational (`I`) message near where
      `unrecognized-option` is defined; opt-out is `disable=configuration-outdated`
      or `upgraded-to = "latest"`
- [ ] `config_initialization.py`: if `upgraded-to` is absent or older than the
      newest catalog version, `add_message("configuration-outdated", ...)`
- [ ] `pylint-config generate` writes `upgraded-to = <current>` so fresh
      configs never nag
- [ ] Docs page under `doc/user_guide/configuration/`;
      `doc/whatsnew/fragments/5462.feature`; closes #5462 and #5465

**Milestone:** PR 1 can land in any 4.x. PR 2-4 should complete before 5.0.0,
since #3512's preset work depends on the upgrader existing.

## Risks and smaller open questions

- TOML sub-table placement: `ConfigFile` must edit an existing key wherever it
  sits; for a new key, pick a canonical table
  (`[tool.pylint.messages_control]` for enable/disable).
- `_parse_version` on odd `upgraded-to` values or pre-releases.
- Flag naming: `--non-interactive` versus interactive-by-default. Recommend
  interactive default.
- Carrying ini comments into the generated toml: recommend no, just warn.
- `useless-suppression` interaction is a #3512 concern, not #5462. Cross-
  referenced, not in scope here.

## Cross-references

- [[issue-3512-plan]] / `.triage/issue_3512_plan.md` — #5462 is its Phase 1;
  this plan supersedes and expands that phase.
- [[pylint-triage-workspace]] — the wider triage workspace.
- `BRANCH_PRIORITIZATION.md` TIER 2 — the four prototype branches.
- `remove-ini-support` branch — aligns with the TOML-only decision; natural
  follow-up.
