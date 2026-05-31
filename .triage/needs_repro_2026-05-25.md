# "Needs reproduction" triage — 2026-05-25

Tested on `try-reproduce-9168-on-macos` branch (pylint 4.1.0-dev0, astroid 4.2.0b3, Linux,
Python 3.12.3). Where the issue says "Python 3.13" or "Python 3.9", I spun up a venv
on that interpreter via `uv` (3.13) or noted the version is below the supported floor (3.9).

## Summary

| Category | Issues |
|---|---|
| **Repro confirmed on main** (4) | #22, #2966, #3662, #10278, #10352 |
| **Apparently fixed** (6) | #4899, #4917, #7268, #8980, #9137, #9983 |
| **Out of support / obsolete** (1) | #4667 (Py3.9 only) |
| **Cannot repro without external env** (5) | #6352 (GTK), #7122 (apt_pkg/Debian), #10090 (black/macOS/Py3.13), #10413 (Windows pythoncom), #10513 (pyo3 binary) |
| **No code / cannot repro** (4) | #9224 (multi-job race), #10012 (flaky), #10941 (no code), and #10090 partial below |

---

## Detailed findings

### ✅ Reproduces — has minimal repro

**#22 — Pyreverse: ValueError: need more than 1 value to unpack** *(2013!)*
- Same bug as 2013. `pyreverse -c Foo` on a multi-module project still crashes at
  `pylint/pyreverse/diadefslib.py:253` with `ValueError: not enough values to unpack`
  because the code does `module, klass = klass.rsplit(".", 1)` without checking that the
  class name is qualified.
- Minimal repro:
  ```
  mkdir -p pkg && touch pkg/__init__.py
  echo "class Foo: pass" > pkg/a.py
  echo "class Bar: pass" > pkg/b.py
  pyreverse -c Foo -o dot pkg/
  ```
- **Action**: remove "Needs reproduction" label, add fix. Easy: defer to `else` branch
  when there's no dot in the class name.

**#2966 — Linting more than one dir adds to sys.path and shadows stdlib**
- Repro is exactly as described in the issue. Pylint emits `No name 'handlers' in module 'logging'`
  because the local `a_lib/logging.py` shadows the stdlib `logging`.
- **Action**: remove "Needs reproduction". This is the well-known sys.path mutation problem;
  could be discussed in light of `--source-roots` semantics.

**#3662 — kwargs used by decorator being flagged as unused**
- Reproduces with `marshmallow` installed: the `**kwargs` of a `@validates_schema` method
  fires `W0613(unused-argument)`. Pylint can't tell that marshmallow invokes the method.
- **Action**: remove "Needs reproduction"; this is a class of "decorator-driven kwargs"
  false-positive shared with several other libraries. May want a marshmallow brain or
  a generic suppression for `**kwargs` on decorated methods.

**#10278 — ImportError when implicit namespace exists in site-packages**
- Reproduced exactly using the script in the issue body (mkdir test1 in site-packages,
  then `pylint --source-roots . test1/test2` in `project/`). Crashes inside
  `astroid.modutils.modpath_from_file_with_callback` → `ImportError: Unable to find module`.
- **Action**: remove "Needs reproduction" and remove "Waiting on author" — clear,
  scripted repro. The fix probably lives in `pylint/lint/expand_modules.py:171`
  passing `additional_search_path` or in astroid's `modpath_from_file_with_callback`.

**#10352 — Empty transform plugin + PEP-695 type params → false missing-function-docstring**
- Reproduces with the user's exact `pylintbug.py` + `pylintbugplug.py`. Pylint complains
  about a missing docstring on `ChildClass.do_something` which overrides
  `BaseClass.do_something` through `MiddleClass[T]`. The old-style `Generic[T]` equivalent
  passes cleanly.
- **Action**: remove "Needs reproduction". The bug is the interaction between PEP-695
  `BaseClass[T]` mro-handling and the override-docstring exemption, gated on the
  presence of any `astroid.MANAGER.register_transform(FunctionDef, ...)` call.

### 🟢 Apparently fixed since the issue was filed

For each of these I built the user's minimal reproducer and ran current main; the
reported message no longer appears.

- **#4899** — pydantic `field(default_factory=lambda: [])` no longer triggers
  false `no-member`/`not-an-iterable`.
- **#4917** — Variable created in `with SQLUnitOfWork() as uow:` is no longer typed as
  the context-manager class (when I model it minimally).
- **#7268** — `class Color(NamedTuple): A,B,C = 1,2,3` no longer crashes the astroid
  NamedTuple brain.
- **#8980** — `from azure.monitor.opentelemetry.exporter import ...` no longer emits a
  spurious `no-name-in-module` (verified with the real package installed).
- **#9137** — minimal `LEGACY_JSON_OPTIONS.with_options(...)` no longer crashes with
  `'UninferableBase' object is not iterable`. (The user's full repro pulls in Django +
  pymongo + a custom module; if they can re-test we should close.)
- **#9983** — `Registry(**{f"{name}_factory": factory})` no longer emits the
  `unexpected-keyword-arg: 'Uninferable_factory'` false positive.
- **Action**: ask each reporter to confirm on a current release and close if they agree.

### ⚠️ Out of support

- **#4667** — bug is "no-member on argparse on **Python 3.9 only**". Pylint now requires
  `>=3.10` (the editable install on 3.9 refuses to install). Recommend closing as
  out-of-support unless we can show the FP also exists on 3.10+.

### 🟡 Cannot reproduce without external environment

These have specific repros but require a platform/lib I don't have:

- **#6352** — needs system PyGObject / GTK 3. PyGObject wheels aren't on PyPI for my
  Linux without `gobject-introspection` dev headers.
- **#7122** — needs `python3-apt` on Debian/Ubuntu (no wheel on PyPI).
- **#10090** — needs Python 3.13 + macOS + ansible + black 24.10.0. On Linux+3.13 with
  the snippet I get a *different* false positive (`No name 'InvalidInput' in module
  'black.parsing'`), and no `AttributeError` crash. The original `ASTSafetyError` crash
  appears to be macOS-specific (or fixed); pinging the reporter is the right move.
- **#10413** — Windows-only (`pythoncom`).
- **#10513** — the hang only happens against the **actual pyo3-built `.so`**. The
  Python-level distilled class doesn't hang. To reproduce we'd need to `cargo build`
  the example crate. Worth a try on someone's macOS/Linux box with Rust.

### 🟡 No reproducer / flaky

- **#9224** — `source-roots` + `-j>1` non-deterministic `no-member`. User can't share
  the monorepo. Likely a job-scheduling/cache race in `--source-roots` expansion;
  hard to chase without a smaller reproducer.
- **#10012** — "occasionally" the disable for `too-many-lines` doesn't fire. With
  `--rcfile=/dev/null` I cannot reproduce: the disable on line 4 (after a module
  docstring) works correctly, both at default and `--max-module-lines=100`. The user's
  setup is pre-commit through CI; the flake may be pre-commit cache or a multi-job
  artifact. Ask them to share a deterministic repro.
- **#10941** — only a final traceback line, no code, no full stack. I already pinged
  them in the comments asking for the astroid trace. Lapsed since 2026-03; can be
  closed for inactivity.

---

## Recommended next steps

1. **Drop the "Needs reproduction" label on**: #22, #2966, #3662, #10278, #10352.
2. **Ask reporter to retest and close** on: #4899, #4917, #7268, #8980, #9137, #9983.
3. **Close as out-of-support**: #4667.
4. **Close for inactivity / no info**: #10941.
5. **Ping reporter for more data** on: #9224, #10012, #10090, #10513.
6. **Leave with label** (need platform-specific testers): #6352, #7122, #10413.

Reproduction scaffolds are in `/tmp/repro/<issue#>/`.
