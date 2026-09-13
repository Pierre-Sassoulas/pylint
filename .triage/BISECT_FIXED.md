# Bisecting the issues that stopped reproducing

Snapshot: 2026-09-13, from the `Needs triage :inbox_tray:` and
`Needs investigation :microscope:` sweeps. For every issue whose snippet no
longer reproduces on `main`, this records the commit that fixed it — and when
that commit is only an astroid pin bump, the astroid commit underneath it.

## Results

Boundaries were confirmed by hand (parent vs commit, dependency version printed
on both sides) before being recorded.

| Issue | pylint commit | astroid commit underneath |
|---|---|---|
| 10016 | `4f6c24120` Fix false positive related to overload decorator + NoReturn, 2026-01-02 | — fixed in pylint's own checkers |
| 10317 | `a0e601d03` Bump astroid to 4.0.0rc0 | `3db2bd943` Add brain module for statistics inference |
| 7680 | `7521eb1dc` Bump astroid to 3.2.0 | `a7f5d5ff4` Prefer last same-named function in a class rather than first in `igetattr()` |
| 4577 | `11807f0ae` Update astroid requirement to 2.11.0 | `74710868d` Fix crash on `Super.getattr` for previously uninferable attributes — **body snippet only, see below** |
| 9077 | `f53283ea1` Upgrade astroid to 3.0.0a4 | `12c3d1556` Recognize stub `pyi` Python files — which is what apsw ships |
| 9973 | `44bb14ef8` Bump astroid to 4.0.0-a0 | `7710b7b44` Make constants have synthetic root as their parent |
| 8026 | `98eb21b13` Bump astroid to 4.0.0b0 | `fda78968f` Drop support for Python 3.9 — a 34-file cleanup, not a targeted fix |
| 10433 | `40817ce1a` Bump astroid to 4.1.1 | `36e6134ed` Fix method classification for pygobject>=3.51.0 — this issue verbatim |
| 10181 | none — see below | `24027e606` Avoid enum transform crash for extension classes |
| 8024 | none | `cython/cython@6e31b41f6` Merge Shadow.pyi type annotation files — `int : TypeAlias = py_int` now sits in an `if TYPE_CHECKING:` block pylint reads |
| 9311 | none | torch 2.8.0 (release boundary; 2.7.0 still fails). Bisecting pytorch means source builds, hours per step |

Nine of the eleven were fixed outside pylint. Exactly one — 10016 — landed in
`pylint/checkers/`, and it closed a different report as a side effect, which is
why nobody came back to close this one.

## Two that need care

**10181 has no owning pylint commit.** It needs astroid 4.3.0. `main` permits
that (`astroid>=4.2.0b1,<=4.3`) but `requirements_test_min.txt` still pins
4.2.0b5, so the crash survives a CI run and disappears on a fresh install. An
earlier pass credited the pin-widening commit; re-testing with that commit's own
pinned astroid shows both sides still crashing.

**4577 is not fixed.** The body snippet is, but the thread carries five more and
@FredStober's still fires on `main`: `E1136 Value 'dataframe' is
unsubscriptable` for `DataFrame(...).fillna(0)` under pandas 1.5.3 and 2.0.3,
silent on 2.2.3 and 3.0.5. The message tracks the pandas version, not any pylint
change. The root cause the reporters named is untouched — `pd.read_csv(...)`
still infers to `[NoneType x4, TextFileReader, Uninferable]` on astroid 4.3.0,
never `DataFrame`; the message stops only because pylint declines to judge a
candidate list containing `Uninferable`. @anders-kiaer's `max_inferred` analysis
still holds: lower it to 20 and even `TextFileReader` drops out.

## Harness

Per step: install pylint (or astroid) from a detached worktree into a venv
holding the reporter's library, run the snippet, grep for the reported message.
`git bisect run` with `--term-old=buggy --term-new=fixed`, so the reported
"first fixed commit" is the one where the message disappears.

Three traps, each of which produces a confident wrong answer rather than an error:

1. **setuptools `build/lib` persists across checkouts.** A file deleted in a
   later commit keeps being packaged into every subsequent wheel. Symptom seen
   here: a pylint 3.3.5 install crashing inside `pylint/checkers/python3.py`, a
   file removed after 2.5. Purge `build/` and `*.egg-info` in the source tree
   **and** `pylint/` plus `pylint-*.dist-info` in site-packages before each install.
2. **`rc=$?` after a pipe captures the last stage.**
   `res=$(check.sh ... | head -1); rc=$?` always yields `head`'s 0, so every step
   reports "buggy", the bisect walks forward and converges on the tip. Capture
   unpiped; trim only for display.
3. **The astroid pin is a range.** An installer that leaves an already-satisfying
   astroid in place makes each step depend on the previous one. Pin each commit's
   own CI-tested astroid from `requirements_test_min.txt`.

Old tags need old toolchains: pylint <= 2.6 `setup.py` carries a
`python_requires` modern setuptools rejects; pylint 2.8 wants
`inspect.formatargspec`, gone in 3.11, so py3.10; pylint 2.x imports
`pkg_resources`, so `setuptools<81`. pylint 1.6.5 and 2.5.0 will not build on
any Python available here at all.

Library issues need the reporter's *era*, not just their pylint: 4577 only shows
itself with pandas pinned back, and 9311 turned out to be fixed by torch with
pylint untouched. 10433 needed a Fedora 43 container for CPython 3.14 plus the
real NetworkManager GI typelib; PyGObject has no wheels and cannot be built here.
