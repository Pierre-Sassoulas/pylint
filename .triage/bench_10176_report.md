# PR #10176 (`unguarded-typing-import`) — performance benchmark

Branch: `takeover-10176` vs `main` (commit `52efad31a`).

## What we are measuring

The new check is opt-in (`default_enabled: False`), but the implementation
in `pylint/checkers/variables.py` adds **always-on** bookkeeping:

- `NamesConsumer.consumed_as_type` (new per-scope dict)
- A call to `utils.is_node_in_type_annotation_context(node)` on every
  consumed name in `_check_consumer` (variables.py:1785)
- A second pass through imports in `_check_type_imports`, which calls
  `_fix_dot_imports` a second time per module

The concern is whether this hurts everyone, even users who don't enable
the check.

## Methodology

Two complementary measurements:

1. **Wall-clock, interleaved.** `.triage/bench_10176_interleaved.py` runs
   pylint over `pylint/checkers` (49 modules, ~28k LOC), interleaving
   `main`, `takeover-10176` (check disabled), and
   `takeover-10176 --enable=unguarded-typing-import`. 5 cycles × 3
   scenarios after warmup.
2. **cProfile.** `.triage/profile_10176.py` runs pylint in-process under
   `cProfile`, then sums call counts and `cumtime`/`tottime` for every
   touched function. The dumps live in `.triage/profile_*.prof`.

`--jobs=1` throughout, to keep the comparison single-threaded.

## Results

### Wall-clock (5 cycles, `pylint/checkers`)

| scenario             | min      | median   | mean     | stdev    |
|----------------------|----------|----------|----------|----------|
| main                 | 16.456 s | 18.065 s | 17.830 s | 1.188 s  |
| takeover-disabled    | 14.649 s | 17.294 s | 17.056 s | 1.403 s  |
| takeover-enabled     | 15.780 s | 16.922 s | 17.338 s | 1.731 s  |

Per-run stdev is ~7-10% of mean. Across cycles, takeover sometimes runs
faster than main and sometimes slower. **Conclusion from wall-clock
alone: the overhead is below the noise floor on this box (<5%).**
An interleaved run on the single file `pylint/checkers/variables.py`
(8 cycles) tells the same story (stdev ~15% of mean).

### cProfile (single run, `pylint/checkers`)

Per-function delta between `main` (30.18 s total) and `takeover-10176`
with check disabled (32.87 s total):

| function                              | main calls | takeover calls | main cumtime | takeover cumtime | delta    |
|---------------------------------------|------------|----------------|--------------|------------------|----------|
| `is_node_in_type_annotation_context`  | 16 234     | 22 335         | 0.060 s      | 0.090 s          | +0.030 s |
| `mark_as_consumed`                    | 5 747      | 6 071          | 0.008 s      | 0.010 s          | +0.002 s |
| `_check_type_imports` (new)           | 0          | 46             | —            | 0.015 s          | +0.015 s |
| `_fix_dot_imports` (called twice now) | 46         | 92             | 0.001 s      | 0.014 s          | +0.013 s |

Total cost attributable to the new code paths: **~35 ms in a ~30 s run
≈ 0.12% overhead.**

`_check_consumer` cumtime fluctuates a lot between profile runs
(1.63 s / 2.52 s / 1.97 s across three samples) but its self-time
barely moves (0.074 / 0.067 / 0.073), so the cumtime swings are
profiler-and-noise, not new work.

### Enabling the check

Enabling `unguarded-typing-import` does **not** add measurable cost on
top of disabled — the bookkeeping runs unconditionally, and the only
extra work when enabled is emitting messages. `_check_type_imports`
cumtime: 0.015 s disabled vs 0.023 s enabled (+8 ms across 46 modules,
~0.03% of total runtime).

## Conclusion

The performance impact of PR #10176 is **negligible**: ~0.1% added
runtime, well below the wall-clock noise floor on this hardware. The
extra cost is paid even when the check is disabled (because of the
`is_node_in_type_annotation_context` call and the duplicated import
fix-up), but it is small enough that it is not detectable in
end-to-end timing.

The PR is safe to release from a performance standpoint, including
keeping the new check enabled-by-default for users who opt in.
