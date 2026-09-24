# Review — PR #10974 (Add Pyreverse primer)

Verified locally on a worktree of `0b9449469` (tip, 2026-07-05), isolated `uv` venvs
(3.13.x and 3.15), plus a trial merge of `origin/main` (`5336a3400`).

Verdict: the design is sound and does what was agreed in #10820 and in the PR thread:
mermaid text diffs of a few `-c <class>` diagrams, one comment per PR, gated by the
`pyreverse` label. All four points from the 2026-07-04 review are addressed (glob
discovery of the `.mmd`, package-namespaced target keys, cache bump reverted, shared
`truncate_comment`). The code and fixtures are good quality: the fixture `.mmd` files
are byte-identical to a fresh render of astroid's `ClassDef`, two consecutive runs are
byte-identical, and the whole prepare/run/compare flow works locally on the real astroid
clone and on the PR's own CI run.

Not mergeable as is, for one reason that is nobody's fault: the branch is 145 commits
behind `main`, and `main` gained the `zizmor` pre-commit hook plus the hardened primer
workflows in the meantime. The three new workflow files fail `zizmor` with 34 findings.
CI is green on the PR only because its `.pre-commit-config.yaml` predates the hook. Item
1 is blocking (item 2 is fixed and pushed), 3–4 are correctness fixes, the rest are
optional.

## Verification

- `pytest tests/testutils/_primer/` on the tip → `89 passed` (3.13).
- Same after merging `origin/main` (clean auto-merge, no conflicts; only
  `.pre-commit-config.yaml`, `primer_compare_command.py`, `test_primer.py` merged
  automatically) → `68 passed, 31 skipped` on 3.13 (the `TestPrimer` interpreter gate is
  now 3.15 on main) and `99 passed` on 3.15. So the `truncate_comment` extraction is a
  pure move and survives main's new suppression/false-positive formatting.
- `pylint --rcfile=pylintrc` on all new/modified files → 10.00/10. `mypy` clean on the
  new files (one pre-existing `CaptureFixture` type-arg complaint on `main`'s own
  `test_primer.py:35`, unrelated).
- `git diff origin/main...pr-10974 -- pylint/pyreverse` is empty: no behaviour change to
  pyreverse hides in the PR. The "Make ordering deterministic" commit only sorts the
  compare loop.
- End-to-end: symlinked the local astroid clone into the worktree, ran `run --type=main`
  (6.8 s for 3 targets), changed the inheritance arrow in `mermaidjs_printer.py`, ran
  `run --type=pr`, then `compare`. Comment is 5645 chars, the unified diff and rendered
  mermaid block are correct for all 3 targets. Running `compare` on two identical
  outputs gives the "no effect" comment.
- Determinism: two `run --type=main` outputs are byte-identical.
- The PR's own `Pyreverse Primer / Run` job (run 28754758125) succeeded: venv + projects
  cache restored, both outputs written. The comment workflow cannot run before merge
  (`workflow_run` only fires from the default branch), which is expected.
- `uvx zizmor@1.30.0 .github/workflows/` on the merged tree: `main`'s workflows are
  clean, every finding is in the three `pyreverse_primer_*.yaml` files.

## 1. Rebase and port the workflow hardening from `main` (blocking)

`zizmor` (hook added on `main` after this branch forked) reports on the three new
workflows:

| finding              | count | fix on `main` to mirror                                      |
| -------------------- | ----- | ------------------------------------------------------------ |
| `unpinned-uses`      | 28    | every `uses:` pinned to a full SHA with a `# vX.Y.Z` comment |
| `artipacked`         | 3     | `persist-credentials: false` on every `actions/checkout`     |
| `template-injection` | 2     | `${{ }}` inside `run:` moved to `env:`                       |
| `dangerous-triggers` | 1     | `workflow_run` allow-listed per file in `.github/zizmor.yml` |

Concretely:

- Copy the `uses:` lines from `primer_run_pr.yaml` / `primer_run_main.yaml` /
  `primer_comment.yaml` on `main`. The PR also pins older majors (checkout v6,
  setup-python v6, cache v5, github-script v8, upload-artifact v7.0.0) where `main` is
  on checkout v7.0.1, setup-python v7.0.0, cache v6.1.0, github-script v9.0.0,
  upload-artifact v7.0.1.
- `pyreverse_primer_comment.yaml:97` uses `${{ github.event.workflow_run.head_sha }}` in
  a `run:` block; `main` does `--commit=${GITHUB_EVENT_WORKFLOW_RUN_HEAD_SHA}` with the
  value passed through `env:`. Same for `pyreverse_primer_run_pr.yaml:192`: `main` does
  `git pull origin "${MAIN_RUN_REF}"` with
  `MAIN_RUN_REF: ${{ steps.download-main-run.outputs.result }}`.
- Add `pyreverse_primer_comment.yaml` to the `dangerous-triggers` ignore list in
  `.github/zizmor.yml`, with a one-line reason like the existing `primer_comment.yaml`
  entry.

Two behavioural fixes landed on `main`'s comment workflow after this branch forked and
must be ported too, or the pyreverse comment job will hit the same failures we already
debugged:

- #11235: the comment job uses `actions/cache@…` for the venv but has **no** "Create
  Python virtual environment" step, so `. venv/bin/activate` fails the first time the
  cache is evicted between the main run and the comment run. `main` recreates the venv
  on miss.
- #11153: after restoring the venv, `main` runs `pip install . --no-deps` so `compare`
  uses the checked-out primer code, not the pylint frozen into the cache. The PR's
  comment job runs `compare` straight from the cached venv.

Optional while you're there: `KEY_PREFIX: venv-pyreverse-primer` creates a second venv
cache identical in content to `venv-primer`. Reusing `main`'s
`KEY_PREFIX`/`CACHE_VERSION` would make the pyreverse job hit the pylint primer's cache
instead of building its own.

## 2. Add `tests/.pyreverse_primer_tests/` to `.gitignore` — DONE, pushed `e39d6ee4a`

Also merged `origin/main` into the branch (`3dd9c49a8`, clean) and pushed both to
`Julfried:pyreverse-primer` on 2026-09-08. Expect pre-commit.ci to go red on `zizmor`
until item 1 is done.

Only `tests/.pylint_primer_tests/` is ignored. After a local run the tree has three
untracked files (`comment.txt`, `pyreverse_output_3.13_main.txt`,
`pyreverse_output_3.13_pr.txt`). The `.gitkeep` still needs a force-add, exactly like
the pylint primer directory.

## 3. `_iter_changes` crashes when a target is removed (should fix)

`pyreverse_primer_compare_command.py:124-126` iterates `sorted(base_data)` and indexes
`new_data[target_name]`. A PR that drops a target from `packages_to_prime.json` while
touching pyreverse (so the run is triggered) gets:

```
KeyError: 'astroid/c'
```

(reproduced with a two-target base and a one-target new output). The mirror case, a
target added in the PR, is silently ignored, so the new diagram is never shown. Iterate
`sorted(base_data.keys() | new_data.keys())` and render "Target added" / "Target
removed" lines for the one-sided keys, the way the pylint primer reports new/removed
messages.

## 4. Equality includes `commit`, so a pin bump renders empty diffs (should fix)

`_iter_changes` compares the whole `PyreverseTargetData`, including `commit`. The main
output comes from the last main run's artifact; if `packages_to_prime.json` moved the
astroid pin since then, every target differs by `commit` only and the comment renders,
per target, an "Effect on …" header with an empty ` ```diff ` block and a full rendered
diagram (reproduced). Compare `diagram` (and `output_file`) only; `commit` is
provenance, not content.

## 5. Document the new primer (nice to have)

`doc/development_guide/contributor_guide/tests/launching_test.rst` has a "Primer tests"
section with the exact `tests/primer/__main__.py prepare/run/compare` recipe. Add the
three `tests/primer/pyreverse_primer.py` equivalents and one sentence saying the CI job
only runs on PRs carrying the `pyreverse` label. Without this nobody will find the tool.

## 6. Smaller things (optional)

- **Fixture extension.** `expected_comment.md` needs a new prettier exclusion in
  `.pre-commit-config.yaml`; the pylint primer's `expected.txt` fixtures need none.
  Using `.txt` drops the pre-commit change. Keep `.md` if the GitHub/editor rendering
  matters to you.
- **Tests coupled to the production JSON.** `_load_fixture` hardcodes the `astroid/`
  prefix and `test_run_writes_output` asserts the exact three target names from
  `packages_to_prime.json`. Renaming or adding a real target breaks seven tests with an
  opaque `KeyError` in `_create_comment_for_target`. A test-local targets dict (you
  already build one in `test_render_target_reads_diagram_and_restores_cwd`) would
  decouple them.
- **`paths` filter in `pyreverse_primer_run_pr.yaml`.**
  `tests/primer/test_primer_stdlib.py` is a copy-paste from the pylint primer and
  irrelevant here, and `!tests/primer/packages_to_prime.json` negates a path that is not
  in the positive list (`main` includes `tests/primer/**` first). Either include
  `tests/primer/**` or drop the negation.
- **History.** 33 commits including "Test modification, REVERT BEFORE MERGE!" plus its
  revert and a cache bump plus its revert. Fine for a squash merge, which is what we do.

## What I'd say to the author

Thanks for the patience and for addressing the July review in full. The remaining work
is almost entirely "catch up with `main`": rebase, pin/harden the three workflows the
way the existing primer workflows now are (zizmor will tell you exactly where), port the
two comment-workflow fixes (#11153, #11235), add the gitignore line, and make
`_iter_changes` tolerant of added/removed targets and ignore `commit`. Docs paragraph
welcome. Happy to push those to the branch if you prefer.
