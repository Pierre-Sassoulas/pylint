# Review — PR #7611 "Implement chained comparison improvements and related checks"

Second pass, at `b3f292d9b` (pushed). The branch now sits on a merge of current `main`
with nine follow-up commits; the first review's findings are resolved or consciously
deferred. This pass re-reads the result, including my own commits.

Net: `13 files changed, 908 insertions(+), 82 deletions(-)` against `origin/main`.

## Verified fixed

Each row was reproduced as a failure before the fix and re-run after.

| Was                                                   | Now                                      | Commit      |
| ----------------------------------------------------- | ---------------------------------------- | ----------- |
| `a >= 5 and 5 >= a` → `impossible-comparison`         | `chained-comparison-all-equal: a == 5`   | `c763a1fda` |
| `1 < a < 10 and b or c` (different expression)        | `1 < a < 10 and (b or c)`                | `a7c999b31` |
| two identical `impossible-comparison` per node        | one                                      | `d0e6099e7` |
| `a >= a` → "cycle to equality: a"                     | silent; `comparison-with-itself` owns it | `5c770fd18` |
| ~1000-term chain → `RecursionError` → `F0002`         | skipped above 64 operands                | `5d2de83f7` |
| `a < b < 0 < 786 == c`                                | `a < b < 0 and c == 786`                 | `aa740ed53` |
| pandas `result < 0 == neg_ct`                         | no message                               | `aa740ed53` |
| music21 `endTimeDifference <= 0 == offsetDifference`  | no message                               | `aa740ed53` |
| `a > 1 and a > 10` → `10 < a`                         | `a > 10`                                 | `274c117f8` |
| unbounded message length                              | truncated at 64 chars                    | `8d0bee3a6` |
| `impossible-comparison/good.py` unrelated to `bad.py` | good fixes bad, apples in baskets        | `cfe178ede` |

Evidence beyond the functional suite:

- **Primer at `5d2de83f7`**: zero `impossible-comparison` and zero
  `chained-comparison-all-equal` across all 15 packages, so the cycle work introduces no
  false positive on real code. 18 sites became "changed messages" (`UNDEFINED → HIGH`
  plus the suggestion), all of them good: `200 <= code < 300`,
  `min_last_seen <= last_seen <= max_last_seen`, `0 < weight < 1`.
- **The three primer "new messages" re-checked against the local build**, using the
  primer's own clones: pandas `mean_.py:143` and music21 `verticality.py:800` are gone;
  sentry `artifact_bundles.py:341`
  (`INDEXING_THRESHOLD <= total_bundles == indexed_bundles`) is kept, correctly — its
  junction is a variable. The sites that had to survive still do (astropy
  `_is_int(v) and 0 <= v <= 999`, sentry `slicing.py`, music21 `axis.py`).
- **4000 randomly generated conditions** (mixed operators, literals, calls, attributes,
  subscripts, `or` groups) produce no crash and no fatal in 3.8s. This matters because
  `symbols` is now a plain dict: a missing edge raises instead of silently rendering
  `>`.
- **Worst case under the cap** (60 literals against one variable, 61 operands) collapses
  to `a > 59` in 0.73s.
- `2200 passed` across the functional, checker and message-documentation suites, with
  the same two failures `origin/main` has here (`no_name_in_module`,
  `unbalanced_tuple_unpacking`, both from the astroid pin). mypy and the spelling lint
  are clean.

CI on `5d2de83f7` was 47 pass / 1 fail — the spelling job, on `canonicalizes` and
`orderable`, reworded in `b3f292d9b` rather than by growing `custom_dict.txt`. CI for
`b3f292d9b` is still running.

## New findings from this pass

### 1. The suggestion reorders independent chains alphabetically

```python
if z < y and y < x and a < b:
# R1716: ... : a < b and z < y < x
```

`_check_comparisons` wraps each segment's paths in `sorted(...)`. Segmentation exists
precisely to keep short-circuit order across boundaries, and then the parts inside a
segment are reordered anyway. Nothing here can short-circuit, but a comparison can
raise, and the suggestion reads nothing like the code it replaces. Ordering by the
position of the first comparison that fed each path would cost little. Predates this
round of fixes.

### 2. The truncation marker is valid Python that means something else

`8d0bee3a6` renders `first(x) and second(x) and ...`. Pasted back, `and ...` is
`and Ellipsis` — always truthy, so a copied suggestion silently drops the tail instead
of failing. `truncated_dict_suggestion` sets the precedent with `', ... '`, but inside a
dict literal that is at least syntactically inert. Worth a marker that cannot be
mistaken for code. My commit, my call to redo if you agree.

### 3. `isinstance(x, str)` carries two meanings in one method

Six occurrences across the two files. In `_check_comparisons` it distinguishes a
boundary (`str`) from a graph (`_ComparisonGraph`); three lines later, in
`_split_at_literal_equalities` and `_render_path`, the same test distinguishes a
variable (`str`) from a literal (`int | float`). Two predicates named `_is_boundary` /
`_is_variable` would stop a reader from having to hold both conventions at once.

### 4. Small drift

- `_segment_comparisons`' docstring lists the reasons it returns `None` but not the
  operand cap added in `5d2de83f7`, and the cap's call site has no comment (the constant
  carries it).
- `aa740ed53` contains the `_render_path` docstring for the behaviour that only arrives
  in `274c117f8` — an artefact of splitting the work into commits after the fact.

## Still open, deliberately

- **Seven false negatives in the sentry primer.** `_add_compare_to_graph` is
  all-or-nothing: any operand that is not a `Name` or a numeric `Const` disqualifies the
  whole `Compare`. That loses `ival >= 0 and ival <= Bounded.MAX_VALUE` (attribute),
  `m > 0 and len(x) > m` (call) and `a > -1 and a < 5` (negative literals are
  `UnaryOp`), all of which `main` reports. Suggested remedy stands: accept any operand
  as an opaque node keyed by `as_string()`, but only when that text occurs once in the
  `BoolOp`, so `next(it) > 0 and next(it) < 10` still bails.
- **`impossible-comparison` takes no arguments,** so the reader is told a condition is
  always False without being told which pair contradicts. Adding the cycle to the
  message would change its signature, hence left alone.
- **Confidence stays `HIGH`.** The first review suggested lowering it, but pylint
  defines `HIGH` as "warning that is not based on inference result" — provenance, not
  certainty. This check is purely syntactic, so `HIGH` is the accurate label and
  `INFERENCE` would be a false claim. The underlying worry (a custom `__gt__` can make
  `a > b and b > a` true) needs operand inference to address, not a different label.
- **R1738 / R1739.** #7611 predates #11236 by four years and is closer to merge, so
  `consider-narrowing-parameter` should move to R1740. Nothing to change on this branch.

## Shape of the branch

The history is the contributor's, with `main` merged in (`95b994ceb`, no conflicts) and
the nine fixes on top, so `areveny`'s authorship survives and the push was a
fast-forward throughout. If the project squashes on merge none of that matters; if not,
`aa740ed53`'s stray docstring is the only wart.
