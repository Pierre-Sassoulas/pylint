# Issue #3512 — "Disable certain messages by default" implementation plan

**Target audience:** a pylint maintainer or motivated contributor picking up the
6-year-old issue and looking for "what is left and in what order."

**Goal:** ship pylint 5.0.0 with a small, named "recommended" preset that disables
the consensus-noisy messages out of the box, without breaking the configs of
existing users — by piggybacking on the auto-upgrade tool (#5462) that's
already partly scaffolded.

## TL;DR

1. **Pick the architecture.** Three were tried; the live one is Jacob's
   `pylint.recommended` "message sets" approach (PR #10619, draft, milestone
   5.0.0). The other two — adding a default to `--disable` (PR #7111, closed)
   and demoting messages to extensions à la `no-self-use` — are dead ends per
   thread consensus.
2. **Land the prerequisite first.** Issue #5462 (auto-upgrade-conf) only has
   the *data scaffolding* (`pylint/config/_breaking_changes/__init__.py`,
   178 lines) — no command. Without the command, every disabled-by-default
   message becomes an unrecoverable silent behavior change for upgrading users.
3. **Then ship `pylint.recommended`** with a corresponding
   `CONFIGURATION_BREAKING_CHANGES["5.0.0"]` block so upgraders are
   interactively offered KEEP (enable explicitly) or USE_DEFAULT (do nothing).
4. **Cross-linter survey says we're on the right track.** Biome, RuboCop and
   Clippy all ship a curated "recommended" set ON by default; ESLint and Ruff
   ship empty / minimal; the upgrade-prompt flow mirrors RuboCop's
   pending-cops pattern almost verbatim. See "Prior art" section below.

## Status of the moving parts (2026-05-15)

| Piece                                     | Where                                                     | State                                                      |
| ----------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------- |
| Issue #3512                               | github                                                    | Open, milestone 4.1.0 (stale label), discussion exhausted  |
| PR #7111 (default for `disable`)          | github                                                    | **Closed** — wrong abstraction                             |
| PR #3650 (disable design checker)         | github                                                    | Closed — no consensus on the wholesale move                |
| PR #10619 (`pylint.recommended` set)      | github                                                    | **Draft**, milestone 5.0.0, ~75 LOC, awaiting design lock-in |
| Issue #5462 (auto-upgrade-conf)           | github                                                    | Open, assigned to Pierre, milestone 4.1.0, WIP label       |
| `pylint/config/_breaking_changes/__init__.py` | local                                                 | Data structure only — enums + 2.7.3/2.14.0/3.0.0/4.0.0 entries, **no driver**            |
| `pylint-config generate`                  | `pylint/config/_pylint_config/`                           | Implemented — but only `generate`, not `upgrade`           |

## Contributor map (who's said what, and where they land)

| Contributor              | Stance / contribution                                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **@AWhetter**            | Original author, drafted the master table of every message. Last active on this thread 2020-05.                                                        |
| **@Pierre-Sassoulas**    | Owns #5462. Champions template-/preset-based defaults (ESLint `extends` model). Wants name `style`, not `message-sets`. Wants legacy/error-only/high-confidence presets too. |
| **@PCManticore**         | Reviewed AWhetter's table in detail (2020-04). Skeptical of wholesale moves. Inactive on pylint for years.                                            |
| **@danrneal**            | Volunteered, opened #3650 (close design checker by default). Closed without merge. Last active 2020-08.                                                |
| **@carlio**              | Prospector author — pointed at prospector's profile/blender machinery as prior art. One-shot drive-by; no expected involvement.                       |
| **@thejcannon**          | Suggested adding a mypy-overlap column. Single drive-by comment 2022-02.                                                                              |
| **@DanielNoord**         | Drove the actionable list in 2022. Closed #7111 himself when the abstraction broke. Open to the message-sets approach.                               |
| **@jacobtylerwalls**     | **Current author of PR #10619.** Prefers per-message starting defaults but accepted the preset compromise. Calls out `useless-suppression` interaction. Most likely to land this. |
| **@martimlobao**         | One-shot, opinion on `no-member`/`import-error`.                                                                                                       |

Active steering committee for the work: **Pierre, Daniel, Jacob.** Everyone else is either inactive or commented once.

## Architecture (the recommended path)

Build on PR #10619's "message sets" model, but with the rough edges polished:

```
pylint/message_sets.py
  ─ define a MessageSet dataclass:
      @dataclass(frozen=True)
      class MessageSet:
          enable:  frozenset[str]
          disable: frozenset[str]
  ─ expose `core` (empty, identity) and `recommended` (the consensus list)
  ─ make the type public so plugins can export their own (e.g. pylint_django.recommended)

pylint/config/base_options.py
  ─ option `--style` (or `--preset`) takes dotted names: --style=pylint.recommended,my_org.house_style
  ─ option resolves *before* `enable`/`disable` so explicit user disables can layer on top

pylint/config/_breaking_changes/__init__.py
  ─ add CONFIGURATION_BREAKING_CHANGES["5.0.0"] entries: one
    MESSAGE_MADE_DISABLED_BY_DEFAULT block per newly-disabled symbol,
    each with KEEP → ENABLE_MESSAGE_EXPLICITLY and USE_DEFAULT → DO_NOTHING.

pylint/config/_pylint_config/upgrade_command.py  (new)
  ─ pair to existing generate_command.py
  ─ reads existing config (pylintrc | setup.cfg | pyproject.toml)
  ─ walks CONFIGURATION_BREAKING_CHANGES bumping from user's installed→current version
  ─ prompts interactively (or accepts --intention {keep,default,fix} flags) per breaking change
  ─ writes the upgraded file back
```

**Load order** (most important to get right, see `useless-suppression`):

1. Internal defaults from each message's `Message.default_enabled`
2. Message sets named in `--style` / `style=` (applied in order)
3. User's `enable=` / `disable=` in rcfile
4. CLI `--enable` / `--disable`

`useless-suppression` should consider a `# pylint: disable=X` "non-useless" if
`X` was disabled-by-preset-but-not-by-default — otherwise everyone upgrading
who uses `useless-suppression` gets noise. Jacob already flagged this.

## Prior art across the linting ecosystem

Survey of how the five most-used linters in other ecosystems handle the same
problem. Pylint is not in a vacuum here — the right answer is mostly already
out there.

| Linter           | Defaults out of the box                                                                                   | Preset / preset-like system                                                                                                | Upgrade UX for changed defaults                                                                                                          |
| ---------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **ESLint** (JS)  | **Empty** — fresh install lints nothing. Must opt into `js/recommended` via `extends:` in flat config.    | `extends: ["js/recommended"]`. Third-party shared configs are plain npm packages exporting a config object. Composed in order; later overrides earlier. | New default rules are non-event: users opt in via their `extends` choice and choose when to bump the dep.                                  |
| **Ruff** (Py)    | **Small + opinionated** — `["F", "E4", "E7", "E9"]` (Pyflakes + a subset of pycodestyle, no `W`, no `C90`). | **No named presets.** Selection is by category code: `select`, `extend-select`, `ignore`, `extend-ignore`. Critically, `select` *resets* the default, `extend-select` *adds*. | **`--preview` flag.** New unstable rules ship preview-only, never auto-enabled by category selection unless `--preview` is on. Stable defaults can change in majors. |
| **Clippy** (Rs)  | **Broad warn-by-default** — `clippy::all` includes correctness, style, complexity, perf, suspicious.       | Named lint groups: `all`, `style`, `perf`, `pedantic`, `restriction`, `nursery`, `cargo`. `pedantic` and `restriction` are allow-by-default. | Attribute-driven (`#![warn(clippy::pedantic)]`). No upgrade tool; relies on attribute scoping + cargo features.                          |
| **RuboCop** (Rb) | **All stable cops enabled.** New cops ship in a `pending` state and warn the user.                       | **Departments** (`Style`, `Layout`, `Lint`, `Metrics`, …). `inherit_from` / `inherit_gem` chain for shared configs.       | **Pending-cops pattern.** New cops are pending in minors; user must set `Enabled: true|false`, or bulk-resolve with `AllCops.NewCops: enable|disable|pending`. Major version flips all pending → enabled. |
| **Biome** (JS)   | **`recommended` ON by default.** Disable with `"recommended": false`.                                    | Groups: `correctness`, `suspicious`, `complexity`, `style`, `performance`, `security`, `accessibility`, `nursery`. `nursery` is opt-in. | `nursery` group is the preview channel. Recommended set grows; users can pin via `"recommended": false` then enable specific groups.    |
| **golangci-lint** (Go) v2 | **`linters.default: standard`** — small curated set. `all`, `fast`, `none` also available.    | Inline `presets`, plus `linters.default` + `enable` / `disable`. v2 (2025) added exclusion presets like `legacy` for migration.        | v2 release broke compat deliberately; provided a migration command and exclusion presets for legacy behavior.                            |

What this tells us about pylint's choice:

1. **"Recommended ON by default" is the dominant pattern.** Clippy, Biome,
   RuboCop and current-pylint all ship with a curated set enabled. Only
   ESLint defaults to empty, and Ruff defaults to a tiny set. So
   `--preset=pylint.recommended` as the **default value** of the option
   (not opt-in) is on-brand for pylint's history *and* matches the majority
   of the field.
2. **RuboCop's pending-cops pattern is the closest prior art for our
   prerequisite #5462.** Every facet of `pylint/config/_breaking_changes/`
   maps onto it. Worth borrowing the user-visible vocabulary too: the prompt
   should say "the following messages were disabled by default in pylint
   5.0 — please choose KEEP, USE_DEFAULT, or PENDING for each" with a bulk
   `--new-defaults=keep|default|pending` flag.
3. **Ruff's `--preview` mode is independently worth lifting.** Same plumbing
   as presets (an extra layer in load order) but solves the orthogonal
   problem of "where do new unstable rules go before they become default."
   Pylint has no such channel today; rules ship straight to enabled-by-default.
   Adding it during this work avoids the next 6-year stall.
4. **Composition order is unanimous** across linters: bundled defaults →
   shared/preset chain (in order) → user config → CLI. Pylint's proposed
   order matches.
5. **Naming consensus:** "preset" / "shared config" / "group" / "department"
   are all live. No one calls them "message sets" or "styles." Both
   `--style` (Pierre) and `--message-sets` (Jacob current) are unique and
   harder to translate to existing user mental models. **`--preset` is the
   safest choice** — RuboCop uses it informally, golangci-lint formally,
   and ESLint users will recognize the concept from npm.
6. **Useless-suppression has no analogue elsewhere.** None of the surveyed
   linters has a "your `disable` line is redundant" check. This is a pylint
   peculiarity and means *we* have to design the preset-disabled-vs-truly-
   default distinction; there's no prior art to copy. Jacob's call to make
   `useless-suppression` preset-aware stands.

## Resolved naming / data-structure questions

These three are blockers for PR #10619 review consensus — pick them first, the
rest is mechanical:

- **Option name:** `--style` (Pierre) vs `--message-sets` (Jacob current) vs
  `--preset` (not yet proposed). Pierre's argument is that "style" can
  eventually expand to cover options and load-plugins, not just enable/disable.
  **Recommendation: `--preset`** — supported by the cross-linter survey
  (golangci-lint uses it formally, RuboCop informally, ESLint users will
  recognize the concept from npm shared configs). Neither `--style` nor
  `--message-sets` has any prior art in the field. It also doesn't pre-commit
  to "everything goes
  here" the way `style` does, and it doesn't bake the implementation noun
  (`message-sets`) into the surface.
- **Data type:** `dict[str, set[str]]` (current draft) vs frozen dataclass
  (Daniel's request). **Recommendation: dataclass** so it's documented,
  introspectable, importable by plugins.
- **Default for the option:** `pylint.core` (empty identity) or `pylint.recommended`.
  **Recommendation:** ship 5.0.0 with `pylint.recommended` as the default —
  that is the entire point of the issue. The auto-upgrade handles the
  back-compat angst.

## The consensus disable list (for `pylint.recommended`)

Synthesized from the 2022-05-05 list, 2022-06-29 narrowing, and the dissents
that followed. Three confidence tiers:

**Tier A — broad consensus, ship:**
- `missing-module-docstring`, `missing-class-docstring`, `missing-function-docstring`
- `too-many-ancestors`, `too-many-instance-attributes`, `too-few-public-methods`,
  `too-many-public-methods`, `too-many-return-statements`, `too-many-branches`,
  `too-many-arguments`, `too-many-locals`, `too-many-statements`,
  `too-many-boolean-expressions`, `too-many-nested-blocks`
- `bad-classmethod-argument`, `bad-mcs-classmethod-argument`
- `fixme`

**Tier B — needs one more pass before ship:**
- `duplicate-code` — Daniel still skeptical (PR #6448 regressions); Pierre says
  the new ignore-signatures/ignore-imports options fix it. **Default: include
  in the disable list, easy to flip back.**

**Tier C — discussed, do NOT disable:**
- `empty-docstring`, `invalid-characters-in-docstring`
- `inconsistent-quotes`, `bad-indentation`
- `global-statement`, `global-at-module-level`, `global-used`
- `inconsistent-return-statements`
- `no-member`, `import-error`, `c-extension-no-member` (most valuable pylint
  signal; if false positives are a problem, fix them, don't hide them)
- `wrong-import-order`, `ungrouped-imports`, `wrong-import-position`
- `empty-docstring`

## Phased checklist

### Phase 0 — alignment (1 design doc, no code)

- [ ] Open a "design proposal" issue (or use the `Needs design proposal 🔒`
      label that's already on #5604) summarizing the three resolved questions
      above (name, data type, default value)
- [ ] Get 👍 from Pierre + Daniel + Jacob, or settle the dissents
- [ ] Update PR #10619 description / convert from draft once aligned

### Phase 1 — finish the auto-upgrade prerequisite (#5462)

This unblocks everything below. The data scaffold already exists; what's
missing is the runner.

- [ ] Add `pylint-config upgrade` subcommand in
      `pylint/config/_pylint_config/upgrade_command.py` (mirror
      `generate_command.py`)
- [ ] Config loader: detect format (pylintrc / setup.cfg / pyproject.toml) and
      parse to a mutable structure (re-use existing parsers in `config_file_parser.py`)
- [ ] Implement `Condition` evaluation against the parsed config (the enum is
      there; the evaluator isn't)
- [ ] Implement `Solution` application against the parsed config (likewise)
- [ ] Interactive prompt loop: per breaking change, show the description, list
      the `Solutions[Intention]` choices, ask user
- [ ] Non-interactive mode: `--intention keep|default|fix` global flag, plus
      `--from-version X.Y` to scope the bump
- [ ] Write back, preserving comments where possible (pyproject.toml: use
      `tomlkit`; ini: use the same writer the generate command uses)
- [ ] Tests: fixture configs for each `BreakingChange` enum value × each
      `Intention`. Reuse `tests/config/`
- [ ] Docs: `doc/user_guide/configuration/auto_upgrade.rst`
- [ ] Whatsnew note for the release that ships this (likely 4.x patch)

**Owner candidates:** Pierre (already assigned), or a contributor following
the data structure in `_breaking_changes/__init__.py` and the
`pylint-config generate` pattern.

### Phase 2 — message-set infrastructure (PR #10619 polish)

Polishes the existing 75-line draft into mergeable shape.

- [ ] Replace `dict[str, set[str]]` with frozen dataclass `MessageSet`
- [ ] Rename CLI option to the agreed name (probably `--preset`)
- [ ] Move `pylint/message_sets.py` → `pylint/presets/__init__.py` (or keep
      flat — coordinate with naming choice)
- [ ] Wire load order: presets resolve at `_arg_parser` time, before user
      enable/disable
- [ ] Make presets composable: `--preset=pylint.recommended,my_org.house`
- [ ] Make `useless-suppression` preset-aware (don't flag user re-disables of
      preset-disabled messages)
- [ ] Allow third-party presets (`pylint_django.recommended`) — document the
      contract in the dataclass docstring
- [ ] Test matrix: empty preset / single preset / two-preset composition /
      preset disables overridden by user enable / preset enables overridden by
      user disable / CLI overrides everything
- [ ] Document in `doc/user_guide/messages/`

### Phase 3 — populate `pylint.recommended`

Mechanical once Phase 2 lands.

- [ ] Add Tier A symbols to `recommended.disable`
- [ ] Add `duplicate-code` to `recommended.disable` (Tier B)
- [ ] Add unit test that `pylint --preset=pylint.recommended` on a
      synthetic file with one violation per disabled symbol emits zero diagnostics
- [ ] Add unit test that `--preset=pylint.recommended --enable=fixme` re-enables

### Phase 4 — register the 5.0.0 breaking-change entries

Drives the upgrade tool's prompts for users upgrading 4.x→5.0.

- [ ] For each Tier A + Tier B symbol, append a
      `BreakingChange.MESSAGE_MADE_DISABLED_BY_DEFAULT` entry to
      `CONFIGURATION_BREAKING_CHANGES["5.0.0"]`
- [ ] Condition: `MESSAGE_IS_NOT_DISABLED` (i.e. user implicitly relies on the
      old default)
- [ ] Solutions:
        `Intention.KEEP → [Solution.ENABLE_MESSAGE_EXPLICITLY]`,
        `Intention.USE_DEFAULT → [Solution.DO_NOTHING]`
- [ ] Phase 1 tests automatically cover these via the fixture sweep

### Phase 5 — docs, release, follow-up issues

- [ ] `doc/whatsnew/5/5.0.rst` — top-level migration section: "What changed,
      and how to keep the old behavior in one command"
- [ ] `doc/faq.rst` — update the "why are messages disabled by default" entry
      to reference presets, not extensions
- [ ] `doc/tutorial.rst` — already has Jacob's grammar fix; add a section on
      `--preset`
- [ ] Close & cross-link: #3512 (this), #746 (5-year-old umbrella), #2399
      (predecessor)
- [ ] Re-scope #5604 (gamification) — much of it falls out of presets +
      `--preset=pylint.error-only` as a follow-up
- [ ] Optional follow-up: ship `pylint.error-only`, `pylint.legacy` (=
      pre-5.0 defaults), `pylint.high-confidence` as Pierre suggested

## Risks & open questions

1. **`useless-suppression` regressions on upgrade.** This is the same trap
   that bit `no-self-use`. Mitigation: preset-aware suppression check, plus
   the auto-upgrade tool catches the most common case.
2. **Plugins exporting presets won't work for plugins not yet loaded when
   `--preset` is parsed.** Need to ensure `--load-plugins` resolves before
   preset import. Probably already true via existing arg ordering but verify
   in Phase 2.
3. **Config format coverage in the upgrade tool.** Three formats × a real
   parser-modifier-writer for each is more work than it looks. Don't skimp
   on tests.
4. **Default = `pylint.recommended` vs default = `pylint.core`.** Shipping
   with `core` is technically safer (zero behavior change) but defeats the
   issue. The 6 years of stalling suggest "safe" wins by default; recommend
   pushing back on that here — the auto-upgrade tool is precisely what makes
   the bold choice safe.

## Cross-references

- [[numpy-2x-brain-plan]] — sibling plan for the largest false-positive
  cluster (different lever for the same "out-of-the-box experience" goal)
- `.triage/REPRO_AUDIT.md` — confirms that ~30 of the 181 REPRO issues touch
  symbols in Tier A/B; this preset cuts default noise meaningfully even
  before any false-positive fix lands
- `.triage/EXTERNAL_PLUGINS_AUDIT.md` — third-party presets (e.g.
  `pylint_django.recommended`) is the natural exit ramp for the 18
  external-plugin-covered enhancement issues
