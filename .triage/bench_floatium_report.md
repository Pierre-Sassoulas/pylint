# Floatium 0.14.4 vs pylint on astropy

Prompted by https://discuss.python.org/t/faster-float-to-string-conversions/107397/14
post #14, where floatium 0.14.4 is announced with a reduced import time.

Question: now that floatium's import is fast, is it worth it, or at least harmless,
for a CLI linter like pylint?

## Environment

- floatium 0.14.4, pylint 4.0.5, astroid 4.0.4, CPython 3.12.3
- astropy pinned at commit `1fb40bc1` (the commit in `tests/primer/packages_to_prime.json`), 970 `.py` files
- Linux, 3 CPUs, single-user idle box
- Isolated venv `/tmp/floatium-bench`, floatium installed normally (autopatch `.pth`)
- A/B toggle: `FLOATIUM_AUTOPATCH` env var (`0` = no patch, `1` = patch). Both states keep floatium installed.
- pylint 4.0.5 (released) was used instead of the local 4.1.0-dev0 so the run is reproducible by anyone. Float-handling is materially the same in both.

## TL;DR

- floatium 0.14.4 adds about 2.7 ms to interpreter startup. The version discussed earlier in the thread cost 15 to 21 ms, so this is a 6-8x improvement. It is slightly above the "<2 ms" quoted in post #14 on this machine.
- `FLOATIUM_AUTOPATCH=0` does NOT remove that cost. It skips the float-slot patching but not the import. The C extension loads either way. Only uninstalling avoids it.
- Patching is a verified drop-in: 119,730 string-form comparisons on astropy's float literals, 0 mismatches.
- floatium has no measurable effect on a pylint run. End-to-end on full astropy the delta is within noise. Reason: pylint spends about 6 ms stringifying floats out of a 1300 s run.
- Net for pylint: a 2.7 ms startup tax with no runtime payoff. Not floatium's fault; linters just do not convert floats to strings much.

## Part A: interpreter startup overhead

`python -c pass`, 150 runs per state, machine idle, OFF/ON interleaved.

| site state | min | median | p90 |
|---|---|---|---|
| no floatium (`.pth` removed) | 11.26 | 13.98 | 16.22 |
| installed, `FLOATIUM_AUTOPATCH=0` | 14.00 | 16.88 | 19.74 |
| installed, autopatch ON | 13.49 | 16.68 | 19.65 |

(milliseconds)

- ON overhead vs no floatium: +2.7 ms median, +2.2 ms min.
- OFF overhead vs no floatium: +2.9 ms median, +2.7 ms min.
- ON minus OFF: -0.2 ms median, i.e. noise. Autopatch ON and OFF cost the same.

Why OFF does not help. `site.py` runs `floatium.pth`, which does `import floatium._autopatch`.
Importing that submodule first executes `floatium/__init__.py`, whose top-level
`from floatium import _ext` loads the 187 KB C extension unconditionally. The opt-out
check (`FLOATIUM_AUTOPATCH` / marker file) only happens later, inside `_autopatch._run()`,
after the C extension is already loaded. Verified: `floatium._ext` is in `sys.modules`
with autopatch both on and off. The "import lazily" comment in `_autopatch.py` is
defeated by the eager `_ext` import in `__init__.py`.

Import composition (`-X importtime`, idle machine): the `floatium._ext` dlopen is the
single largest component (about 1.2 to 1.6 ms self time) and is paid in both states;
the whole floatium import chain is roughly 2 to 3 ms cumulative. This corroborates the
Part A wall-clock magnitude.

## astropy float census

19,936 float literals across 970 files, about 20 per file. repr lengths: min 3,
median 3, max 23. 79% are 5 characters or fewer (`1.0`, `0.5`, `2.0`, and so on).
astropy is float-dense, but the literals are mostly short and easy to format. That
matters below.

## Part B: end-to-end pylint on full astropy

`pylint -j1 --rcfile=/dev/null --persistent=n astropy/`, 3 runs per condition,
interleaved OFF/ON. One run lints all 970 files and emits about 44.7k messages.

| run | OFF (s) | ON (s) |
|---|---|---|
| rep 1 | 1286.41 | 1370.57 |
| rep 2 | 1322.46 | 1309.21 |
| rep 3 | 1278.99 | 1287.91 |
| **median** | **1286.41** | **1309.21** |
| mean | 1295.95 | 1322.56 |
| sd | 18.99 | 35.04 |

Median delta ON minus OFF is +22.8 s (+1.8%). This is not significant:

- Within-condition spread (sd 19 to 35 s, ranges 43 and 83 s wide) is larger than the delta.
- The condition ranges overlap almost entirely (OFF max 1322 is above ON min 1288).
- Welch t is about 1.2, p about 0.3 with n=3.
- The apparent gap is carried by one outlier, rep 1 ON at 1371 s, roughly 3 sigma above
  the other five runs. Drop it and the OFF and ON means land within 3 s of each other.

Conclusion: no measurable effect.

Side finding, unrelated to floatium. pylint is nondeterministic on astropy. The six runs
emitted 44,481 to 44,865 message lines, all six different, including OFF vs OFF. So the
workload itself drifts run to run, which is part of the timing noise and which defeated
the planned output-hash integrity check (correctness was checked directly instead, see T1).
A caught `TypeError: 'UninferableBase' object is not iterable` in `class_checker.py`
(`_called_in_methods`) fires during these runs and may be related. Worth a separate look.

## Why Part B cannot see floatium (T2)

End-to-end wall time is the wrong instrument at this magnitude. Measured directly,
in-process, with `floatium.enabled()` toggling the patch (no subprocess noise),
250 passes:

`repr()` over all 19,936 astropy literals:

- stock CPython: 4.409 ms/pass, 221 ns/call
- floatium: 2.821 ms/pass, 142 ns/call
- saving: 1.6 ms/pass, 36% faster

`str()` is the same within noise (36.6% faster).

The speedup is 36%, not the roughly 3x a synthetic 17-digit value shows (439 vs 151 ns
in a separate microbenchmark). astropy's literals are short, 79% are 5 chars or fewer,
and stock CPython already formats those quickly (221 ns here vs 439 ns on the hard
value). floatium runs at a near-constant 142 ns either way. Its edge is largest on
hard many-digit values, not on the floats that actually appear in source code.

A pylint run stringifies each float literal at most a small number of times; most are
never rendered back to text at all. Even a generous 5 passes' worth of conversions is
about 8 ms saved. An absurd 50x overestimate is about 80 ms. One standard deviation of
Part B noise is 19,000 to 35,000 ms. floatium's realistic contribution is therefore
roughly 3,000x below the noise floor. It cannot show up in end-to-end timing, and no
realistic number of reps would change that.

## T1: drop-in correctness

`floatium.enabled()` A/B. `repr`, `str`, `:.6g`, `:.17g`, `:e`, `:.3f` applied to all
19,936 astropy literals plus 19 edge cases (`0.0`, `-0.0`, smallest subnormal `5e-324`,
smallest normal, `1e308`, `1.797e308`, `inf`, `-inf`, `nan`, `1e16`, `1e17`, and so on).

119,730 comparisons. **0 mismatches.** floatium 0.14.4's output is char-for-char
identical to stock CPython for this corpus.

## Bottom line for the thread

The new version is a real fix: startup overhead dropped from 15-21 ms to about 2.7 ms,
and the output is a verified drop-in. Two points still worth raising:

1. The env-var opt-out does not work as a cost opt-out. `FLOATIUM_AUTOPATCH=0` and
   `python -m floatium disable` both skip patching but still load the C extension
   (about 2.7 ms), because `floatium.pth` imports `floatium._autopatch`, which runs
   `floatium/__init__.py`, which eagerly imports `_ext`. For a CLI tool the only
   zero-cost state is "not installed". If the `.pth` imported a tiny standalone module
   that did the env and marker check before importing anything that pulls in
   `__init__.py`, an opted-out process could pay close to 0 ms.

2. For a linter there is no runtime upside. pylint converts floats to strings for about
   6 ms out of a 1300 s lint of astropy. floatium's 36% speedup on that is invisible.
   This is expected: linters analyze structure, they do not render numbers. floatium's
   win is for float-output-heavy workloads (serialization, numeric REPLs, reporting),
   not static analysis.

For pylint specifically: floatium 0.14.4 is close to harmless (about 2.7 ms per
invocation) but brings no benefit, and that 2.7 ms cannot currently be opted out of
without uninstalling.

## Artifacts

Kept under `/tmp` for re-runs:

- `/tmp/bench_startup.py` - Part A and the float census
- `/tmp/bench_pylint.py` - Part B (`<reps>` arg)
- `/tmp/bench_float.py` - T1 correctness and T2 cost
- `/tmp/bench_pylint_result.txt` - Part B raw output
- `/tmp/floatium-bench` - the venv, `/tmp/astropy-bench` - astropy at `1fb40bc1`
