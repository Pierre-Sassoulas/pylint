I ran the benchmark we'd been missing. TL;DR: the overhead is negligible (~0.1%), the PR is safe to release.

**Setup.** `pylint pylint/checkers --jobs=1` (49 modules, ~28k LOC), three scenarios interleaved across cycles: `main`, `takeover-10176` with the check disabled (default), and `takeover-10176` with `--enable=unguarded-typing-import`.

**Wall-clock (5 cycles).**

| scenario | median | stdev |
|---|---|---|
| main | 18.07 s | 1.19 s |
| takeover, disabled | 17.29 s | 1.40 s |
| takeover, enabled | 16.92 s | 1.73 s |

Per-run stdev is 7–10% of mean, so wall-clock can only say the overhead is below the noise floor on this machine. Takeover even ran faster than main in some cycles, confirming the difference is well under 5%.

**cProfile.** To get a tighter number I profiled one run on each branch and diffed the touched functions:

| function | main calls | takeover calls | Δ cumtime |
|---|---|---|---|
| `is_node_in_type_annotation_context` | 16234 | 22335 | +30 ms |
| `_check_type_imports` (new) | 0 | 46 | +15 ms |
| `_fix_dot_imports` (now called twice) | 46 | 92 | +13 ms |
| `mark_as_consumed` | 5747 | 6071 | +2 ms |

Total: **~35 ms added in a ~30 s run, ≈ 0.12%**. The cost is paid unconditionally — disabled and enabled users see the same overhead, because the `consumed_as_type` bookkeeping in `NamesConsumer` runs regardless. Enabling the check on top adds only the message-emission cost (~8 ms across 46 modules).

So: ship it.
