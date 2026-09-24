Thanks for the fast import-time fix. I re-ran the pylint benchmark against floatium 0.14.4.

**Startup** (`python -c pass`, 150 runs, CPython 3.12.3):

| floatium | median startup |
|---|---|
| not installed | 13.98 ms |
| 0.14.4, `FLOATIUM_AUTOPATCH=0` | 16.88 ms |
| 0.14.4, autopatch on | 16.68 ms |

About 2.7 ms of overhead, down from the 15-21 ms reported earlier in the thread. Good improvement.

But **`FLOATIUM_AUTOPATCH=0` does not remove it**: off and on both cost ~2.7 ms. `floatium.pth` imports `floatium._autopatch`, which runs `floatium/__init__.py`, whose top-level `from floatium import _ext` loads the C extension before the env var or marker is ever checked. `floatium._ext` is in `sys.modules` either way, and `python -m floatium disable` behaves the same. So the only zero-cost state is "not installed". Having the `.pth` check the env var and marker in a small standalone module, before importing `floatium`, would let an opted-out process pay close to 0 ms.

**For linting, autopatch on made no measurable difference.** pylint over astropy (970 files, 19,936 float literals), end-to-end, the off-vs-on gap stayed within run-to-run noise on a ~1300 s run. Directly: stringifying every astropy literal once costs 4.4 ms stock vs 2.8 ms with floatium, and a lint does only a few passes' worth. Expected: a linter walks AST structure, it does not render numbers. Output is a verified drop-in too: 119,730 `repr`/`str`/`format` comparisons over those literals plus edge cases, zero mismatches.

Net for pylint: 0.14.4 is correct and close to harmless at ~2.7 ms per process, but that 2.7 ms cannot currently be opted out of without uninstalling.
