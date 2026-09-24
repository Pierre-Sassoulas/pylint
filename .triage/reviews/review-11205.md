# Review — PR #11205 (pyreverse `--theme light|dark`, closes #7572)

Verified locally: worktree of `ef8904d4a` (PR head), compared against `origin/main`
`80999752a`, `venv/bin/python` (3.13.1), graphviz `dot` installed.

## Verification

- `pytest tests/pyreverse` on the branch → **159 passed**.
- Class-diagram output with no flags is byte-identical to main (`.dot`, `.puml`, `.mmd`
  diffed). Package diagrams gain an explicit `fontcolor="black"` — matches what the PR
  description claims.
- Per-node overrides do win over the theme: an exception class in dark theme still gets
  `fontcolor="red"`, `--colorized` still wins on `color`.
- `--theme bogus` is rejected: `invalid choice: 'bogus' (choose from light, dark)`.
- The design decision to make `writer.py` pass `None` instead of hardcoded `"black"` is
  the right one — the writer stops having an opinion about colors and the printer owns
  the theme. Good call.

Gotcha for anyone reproducing: `PYTHONPATH=<worktree>` alone is not enough, the editable
install of the main checkout wins. `cd` into the worktree (or any directory without a
`pylint/` package) first.

## 1. `classes.png` is committed at the repo root (blocking)

```
$ ls -l classes.png
-rw-rw-r-- 1 pierre pierre 2902 classes.png   # PNG image data, 87 x 192
```

Added in `1f3ddef63` ("Staging these files just to ensure smooth reproduction of
files"). The later cleanup commit `542c63302` removed the `.py` reproduction file but
not this. Please drop it.

## 2. The `documentation` CI job is red (blocking)

`doc/additional_tools/pyreverse/configuration.rst` is auto-generated _and tracked_, and
`checks.yaml` fails if it is stale:

```
+--theme
+-------
+*Color theme to use for the generated diagrams.*
+
+**Default:**  ``light``
##[error]Generated documentation is out of date. Run 'tox -e docs' locally and commit the changes.
```

Run `tox -e docs` and commit the regenerated file.

Note while you are there: the generated page prints only the help text and the default —
it does **not** print `choices`. So the help string should name the values itself, e.g.
`"Color theme to use for the generated diagrams: 'light' or 'dark'."`

## 3. `--theme` is missing from `--help` — this is caused by the PR, not pre-existing

The PR description flags this as "a pre-existing cosmetic help-formatting issue
unrelated to this change". It is not: it is the `"dest": "theme"` key in the option
dict.

`_convert_option_to_argument` (`pylint/config/utils.py:109`) turns _any_ optdict
carrying `dest` into a `_StoreOldNamesArgument` with `old_names=[dest]`.
`_add_parser_option` (`pylint/config/arguments_manager.py:141-160`) then registers the
flag twice: once visible, then once more as `--{old_name}` with
`help=argparse.SUPPRESS`. For every other option this is harmless because the flag and
the dest differ (`--color-palette` vs `color_palette`). For `--theme` the dest _is_ the
flag name, so the second registration collides, and the parser is built with
`conflict_handler="resolve"` (`arguments_manager.py:70`) — the hidden action replaces
the visible one.

Fix is to delete the redundant `"dest": "theme"` line; argparse already derives dest
`theme` from `--theme`. Verified:

```
$ pyreverse --help
  --theme <light|dark>  Color theme to use for the generated diagrams.
                        (default: light)
```

## 4. Dark theme leaves every dot edge black (blocking)

`DotPrinter.emit_edge` is untouched, so arrows keep Graphviz's default black stroke and
are drawn on the new `bgcolor="#1e1e1e"`:

```
$ pyreverse --theme dark -o dot -p s -a1 -s1 sample.py
"sample.Dog" -> "sample.Animal" [arrowhead="empty", arrowtail="none"];   # no color=
```

Rendered, the inheritance arrow is a black line on a near-black canvas. The PlantUML
side _does_ handle this (`ArrowColor` in the skinparam block), so the two backends
currently disagree about what "dark theme" means. `emit_edge` needs
`color="{theme.color}"` (and edge labels need a theme-aware `fontcolor`; today they are
hardcoded `green` in `ARROWS`, which happens to survive, but that is luck rather than
design).

This is the one that makes the feature look broken in practice — nearly every real
diagram has edges.

## 5. `-o mmd` and `-o html` silently ignore `--theme` (blocking)

`MermaidJSPrinter` (and `HTMLMermaidJSPrinter`, which subclasses it) inherit the new
`theme` parameter and never read it:

```
$ pyreverse --theme dark -o mmd -p d_mmd colorized.py
classDiagram
  class CheckerCollector {
```

Identical to the light output. Two of the five directly-supported formats accept the
flag and do nothing — worse than rejecting it. This is exactly what @DudeNr33 asked for
in the review; mermaid has first-class theming and the emission is one line:

```
%%{init: {'theme': 'dark'}}%%
```

## 6. PlantUML: `skinparam class` does not cover package diagrams

`NODES` maps `NodeType.PACKAGE` to the PlantUML `package` element, but the header only
styles `class`:

```
$ pyreverse --theme dark -o puml -d p6 pylint.testutils && head p6/packages.puml
skinparam class {
  BackgroundColor #1e1e1e
  ...
}
package "pylint.testutils" as pylint.testutils {
```

So `packages.puml` gets a dark canvas with default light-yellow package boxes. Needs a
`skinparam package { ... }` block too (or the generic form).

## 7. `--colorized --theme dark` produces unreadable labels

```
"colorized.CheckerCollector" [color="#77AADD", fontcolor="#e0e0e0", ..., style="filled"];
```

The palette is a set of pastel _light_ fills; on main those got black text, now they get
`#e0e0e0` text on `#77AADD` fill. Either the dark theme should keep dark text on filled
nodes, or dark mode needs its own palette. Worth at least deciding explicitly, since
`--colorized` is the flag most likely to be combined with `--theme dark`.

## 8. Functional tests still missing (@DudeNr33's request)

The added tests are printer-level only — they construct `DotPrinter(theme="dark")`
directly. Nothing covers the CLI → `Run` → `DiagramWriter.set_printer` → printer path,
which is where `self.config.theme` is read. The
`tests/pyreverse/functional/class_diagrams/colorized_output/` pattern (`.rc` with
`output_formats=` + `command_line_args=`) is a drop-in fit and gives you the readable
before/after that the reviewer asked for:

```
[testoptions]
output_formats=dot,puml,mmd
command_line_args=-S --theme=dark
```

## 9. Cleanup

- The two palettes are duplicated across `dot_printer.py` and `plantuml_printer.py`.
  Since `Printer.__init__` now takes `theme`, resolve it once there
  (`self._theme_colors = self.THEME_COLORS[theme]`) and let each subclass declare only
  its palette. `PlantUmlPrinter.emit_node` currently redoes the dict lookup on every
  single node.
- `THEME_COLORS.get(theme, THEME_COLORS["light"])` — argparse already enforces the
  choices, so the fallback is unreachable and only hides typos. Index directly.
- `PlantUmlPrinter.THEME_COLORS["light"]["bgcolor"] = "white"` is never read (light
  emits no skinparam).
- `bgcolor: ""` as a "not set" sentinel: `None` with `dict[str, str | None]` reads
  better.
- `theme: str` is out of step with `Layout` / `NodeType`, which are enums. A `Theme`
  enum (or at minimum `Literal["light", "dark"]`) would type-check the printer
  constructors.
- `DEFAULT_COLOR` was dropped from `DotPrinter` and `PlantUmlPrinter` but
  `MermaidJSPrinter` still has it. Once mermaid gets theme support that last one should
  go too.
- `tests/pyreverse/data/packages_depth_limited_{0,1}.dot` are converted CRLF → LF.
  Harmless (`_file_lines` strips line ends) but unrelated to the feature — it makes
  those two files look fully rewritten in the diff.
- History has `chore: retrigger CI` and a commit message with a typo ("reproductionof
  files"). Worth squashing before merge.

## Summary

The core plumbing is sound and the writer/printer split is the right shape. Blocking
before merge: drop `classes.png`, regenerate `configuration.rst`, remove
`"dest": "theme"` so the option shows up in `--help`, color the dot edges, and make
`--theme` either work or not be accepted for `mmd`/`html`.
