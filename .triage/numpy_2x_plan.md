# `astroid` numpy 2.x brain modernization — implementation plan

**Target audience:** an astroid maintainer / contributor with no prior context on this
audit. **Goal:** close the largest cluster of open pylint issues by upgrading the
`astroid/brain/brain_numpy_*` files to track numpy 2.x's API surface and fix two
sub-cases where the current brain returns a stub that's _wrong_ (not just missing).

This plan was drawn from a full triage of all 1020 open pylint issues
(`.triage/triage_state.json` + audit docs). Of the 197 EXTDEP-verdict issues, 18 mention
numpy explicitly; plus 4 REPRO issues touch numpy. After deduping, **~20 distinct numpy
issues** are in scope here, ~14 of which would close with the brain patches below.

## Repro environment

- pylint 4.0.5 / astroid 4.0.2 / Python 3.12.3 / numpy 2.4.4 / Linux
- Repros run with the project's own `pylint/testutils/testing_pylintrc` (so the
  project's `pylintrc` opt-outs don't mask false positives).
- All "Fires?" verdicts below come from running the snippet on this stack.

## Per-issue findings (verified)

| Issue                                                                                                                                                                           | Title (short)                                               |                  Fires?                  | Root cause                                                                                                                                    | Fix size                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | :--------------------------------------: | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| [#10806](https://github.com/pylint-dev/pylint/issues/10806)                                                                                                                     | `np.finfo(float).eps`                                       |                    ✅                    | No `finfo` class in any brain file                                                                                                            | **S**                        |
| [#5831](https://github.com/pylint-dev/pylint/issues/5831)                                                                                                                       | `np.finfo(np.float64).resolution`                           |                    ✅                    | Same — same fix                                                                                                                               | **S** (covered by #10806)    |
| [#10440](https://github.com/pylint-dev/pylint/issues/10440)                                                                                                                     | `i, j = np.unravel_index(...)` → unbalanced-tuple-unpacking |                    ✅                    | `brain_numpy_core_multiarray.METHODS_TO_BE_INFERRED["unravel_index"]` returns a fixed 1-tuple `(ndarray,)` instead of a variable-length tuple | **S**                        |
| [#9989](https://github.com/pylint-dev/pylint/issues/9989)                                                                                                                       | `np.mgrid[1:2:3j, …].shape` → no-member                     |                    ✅                    | `mgrid` not modeled at all; astroid falls back to inferring `tuple`                                                                           | **S**                        |
| [#9956](https://github.com/pylint-dev/pylint/issues/9956)                                                                                                                       | `np.dtypes.StringDType` → no-member                         |                    ✅                    | `numpy.dtypes` submodule not modeled                                                                                                          | **M**                        |
| [#7883](https://github.com/pylint-dev/pylint/issues/7883)                                                                                                                       | `x.reshape(3, 2, 2, order='F')` → too-many-args             |                    ✅                    | `brain_numpy_ndarray.ndarray.reshape` signature is `(self, shape, order='C')` — needs `(self, *shape, order='C')`                             | **S**                        |
| [#9385](https://github.com/pylint-dev/pylint/issues/9385), [#5543](https://github.com/pylint-dev/pylint/issues/5543)                                                            | `from numpy import empty_like` → E1137 on `a[0] = 1`        |                    ✅                    | Brain only registers `numpy.empty_like` via `numpy.core.multiarray`; `from numpy import empty_like` doesn't traverse the same inference tip   | **S**                        |
| [#7981](https://github.com/pylint-dev/pylint/issues/7981)                                                                                                                       | `x.strides[0]` after `np.pad` → unsubscriptable             |                    ✅                    | `ndarray.strides` declared as plain `None` in the brain instead of a tuple                                                                    | **S**                        |
| [#10312](https://github.com/pylint-dev/pylint/issues/10312)                                                                                                                     | `np.where(...)[:, np.newaxis]`                              |             ❌ already clean             | —                                                                                                                                             | —                            |
| [#10548](https://github.com/pylint-dev/pylint/issues/10548)                                                                                                                     | `np.concatenate(..., dtype=…)`                              | ❌ already clean (brain has dtype kwarg) | —                                                                                                                                             | —                            |
| [#10031](https://github.com/pylint-dev/pylint/issues/10031)                                                                                                                     | inheriting from `set[int]`                                  |             ❌ already clean             | —                                                                                                                                             | —                            |
| [#9590](https://github.com/pylint-dev/pylint/issues/9590)                                                                                                                       | `np.int16(arr)[0]`                                          |             ❌ already clean             | —                                                                                                                                             | —                            |
| [#9681](https://github.com/pylint-dev/pylint/issues/9681)                                                                                                                       | pyreverse infinite recursion on `np.array` class attr       |     ⚠ pyreverse-specific (not brain)     | recursion in pyreverse's class-attribute walker when `np.array(...)` is the inferred initializer                                              | **M** (pyreverse, not brain) |
| [#3602](https://github.com/pylint-dev/pylint/issues/3602)                                                                                                                       | pyreverse `-S` hang/crash with numpy                        |           ⚠ pyreverse-specific           | same as #9681                                                                                                                                 | (same)                       |
| [#7702](https://github.com/pylint-dev/pylint/issues/7702), [#8018](https://github.com/pylint-dev/pylint/issues/8018), [#4083](https://github.com/pylint-dev/pylint/issues/4083) | `np.ufunc.reduce` / `scipy.fft` invalid-sequence-index      |              ⚠ ufunc brain               | `numpy.ufunc.reduce` returns ndarray-or-scalar; brain doesn't model                                                                           | **M**                        |
| [#5533](https://github.com/pylint-dev/pylint/issues/5533)                                                                                                                       | numpy ufunc + `%` formatting → bad-string-format-type       |       ⚠ format-checker, not brain        | pylint format checker sees `ndarray` not as numeric                                                                                           | **L** (pylint, not astroid)  |
| [#8117](https://github.com/pylint-dev/pylint/issues/8117)                                                                                                                       | numpy.bool singleton-comparison                             |                  DESIGN                  | needs pylint config knob, not brain                                                                                                           | —                            |

**Closes with this plan:** #10806, #5831, #10440, #9989, #9956, #7883, #9385, #5543,
#7981 = **9 issues** (plus #10548, #10312, #10031, #9590 already fixed in upstream
astroid main — **4 more closeable by upgrade alone**).

That's roughly **13 of 22 open numpy issues** with the work below. The pyreverse cases
(#9681, #3602) need a separate pyreverse fix. The ufunc.reduce cluster (#7702, #8018,
#4083) is one further brain addition.

---

## Concrete brain-plugin changes

### Patch 1 — Add `finfo` and `iinfo` classes — closes #10806, #5831

**File:** `astroid/brain/brain_numpy_core_numerictypes.py` (or a new
`brain_numpy_lib_getlimits.py` since `finfo` / `iinfo` live in `numpy.lib._getlimits`
upstream).

**Why:** the brain has no model of `np.finfo` at all. Every attribute access on a
`finfo` instance is therefore reported as `no-member`.

**Suggested stub:**

```python
class finfo:
    bits: int
    dtype: "numpy.dtype"
    eps: float
    epsneg: float
    iexp: int
    machep: int
    max: float
    maxexp: int
    min: float
    minexp: int
    negep: int
    nexp: int
    nmant: int
    precision: int
    resolution: float
    smallest_normal: float
    smallest_subnormal: float
    tiny: float
    def __init__(self, dtype): ...

class iinfo:
    bits: int
    dtype: "numpy.dtype"
    min: int
    max: int
    kind: str
    def __init__(self, type): ...
```

(Match astroid's existing pattern: register the class via
`AstroidManager().register_transform(...)` keyed on the attribute name or via a
`register_module_extender` for the public re-export `numpy.finfo` / `numpy.iinfo`.)

**Test:** existing pylint repro #10806 already in this audit's
`.triage/snippets/i10806.py`; add a functional test under `astroid/tests` mirroring it.

### Patch 2 — Variadic `ndarray.reshape` — closes #7883

**File:** `astroid/brain/brain_numpy_ndarray.py`

**Current:**

```python
def reshape(self, shape, order='C'): return np.ndarray([0, 0])
```

**Change to:**

```python
def reshape(self, *shape, order='C'): return np.ndarray([0, 0])
```

numpy's actual `reshape` accepts both `arr.reshape((3, 2, 2))` and
`arr.reshape(3, 2, 2)` — the brain must accept either. The same pattern applies to
`resize` further down in the file. Audit all `ndarray` methods that take a shape arg
(`reshape`, `resize`, possibly `view`) and switch to `*shape`.

### Patch 3 — `strides` typed as tuple — closes #7981

**File:** `astroid/brain/brain_numpy_ndarray.py`

**Current:**

```python
self.strides = None
```

**Change to:**

```python
self.strides = (0,)  # tuple of ints — model as a non-empty tuple so indexing infers OK
```

(Same treatment as `self.shape` already gets; `self.shape = numpy.ndarray([0, 0])` is
itself questionable but downstream code subscripts it without complaint.)

### Patch 4 — Variable-length tuple return for `unravel_index` — closes #10440

**File:** `astroid/brain/brain_numpy_core_multiarray.py`

**Current:**

```python
"unravel_index": """def unravel_index(indices, shape, order='C'):
        return (numpy.ndarray([0, 0]),)""",
```

This declares a fixed 1-tuple return. Users unpacking `i, j = np.unravel_index(...)`
trip the `unbalanced-tuple-unpacking` checker because astroid thinks the result has
length 1.

**Two options:**

1. Return `Uninferable` for the length (preferred — matches numpy's actual contract:
   length is `len(shape)`, only known if `shape` is a literal):

   ```python
   "unravel_index": """def unravel_index(indices, shape, order='C'):
           return numpy.ndarray([0, 0])  # let unpacker see a non-tuple sequence""",
   ```

   This is what `np.where` already does — returns ndarray, downstream code unpacks it
   freely.

2. Make the brain context-aware: inspect the second argument and, if it's a literal
   tuple of length N, return a tuple of length N. More work; same downstream effect for
   the common case.

Option 1 is fine for closing the bug.

### Patch 5 — Model `np.mgrid` / `np.ogrid` — closes #9989

**File:** new `astroid/brain/brain_numpy_lib_index_tricks.py` or fold into existing
`brain_numpy_core_numeric.py`.

`np.mgrid` is an instance of `numpy.lib._index_tricks_impl.MGridClass`. The user-visible
contract:

- `np.mgrid[1:2:3j, 3:4:5j]` returns an `ndarray` (not a tuple)
- the resulting array's `.shape` is `(ndim, *each_axis_size)`

Stub:

```python
class MGridClass:
    def __getitem__(self, key): return numpy.ndarray([0, 0])
mgrid = MGridClass()
ogrid = MGridClass()
```

Register on the `numpy` module so `np.mgrid` resolves.

### Patch 6 — Model `numpy.dtypes` submodule — closes #9956

**File:** new `astroid/brain/brain_numpy_dtypes.py`.

numpy 2.0 added the `numpy.dtypes` submodule with `StringDType`, `BoolDType`,
`Float64DType`, … (full list from `dir(np.dtypes)`):

```
BoolDType, ByteDType, BytesDType, CLongDoubleDType, Complex128DType,
Complex64DType, DateTime64DType, Float16DType, Float32DType, Float64DType,
Int16DType, Int32DType, Int64DType, Int8DType, IntDType, LongDType,
LongDoubleDType, LongLongDType, ObjectDType, ShortDType, StrDType,
StringDType, TimeDelta64DType, UByteDType, UInt16DType, UInt32DType,
UInt64DType, UInt8DType, UIntDType, ULongDType, ULongLongDType, UShortDType,
VoidDType
```

Each is a subclass of `numpy.dtype`. Stub each as a `class XxxDType(dtype): pass` and
register them on the `numpy.dtypes` submodule via `register_module_extender`.

Use the existing `numpy_supports_type_hints()` gate in `brain_numpy_utils.py` to skip on
pre-2.0 numpy (this submodule didn't exist before then).

### Patch 7 — `empty_like` (and friends) reachable via `from numpy import` — closes #9385, #5543

**File:** `astroid/brain/brain_numpy_core_multiarray.py`

The brain currently registers `empty_like` (and the rest of `METHODS_TO_BE_INFERRED`)
via an inference-tip keyed on the _attribute_ `np.empty_like`. When a user does
`from numpy import empty_like`, the call site is a plain `Name` node, not an
`Attribute`, and the tip never fires — so the returned value is inferred as whatever the
function's literal body says (here `numpy.ndarray((0, 0))` parsed _abstractly_), losing
the "I am an ndarray" type tag.

**Fix:** register the same set of stubs at the `numpy` _module_ level as well, so a
`from numpy import empty_like` import lookup resolves the name to the stub. The existing
machinery is `register_module_extender` — add a module extender for `numpy` that
re-exposes the `METHODS_TO_BE_INFERRED` definitions, OR have the per-function inference
tip key off the `Name` node too (use both `infer_numpy_name` and `infer_numpy_attribute`
in `brain_numpy_utils.py`).

This unblocks the same pattern for all functions in `METHODS_TO_BE_INFERRED` (currently
~20 of them), not just `empty_like` — likely fixes other latent issues.

### Patch 8 — `ufunc.reduce` / `accumulate` / `outer` (out of scope but adjacent) — closes #7702, #8018, #4083

**File:** `astroid/brain/brain_numpy_core_umath.py`

Three open issues report `invalid-sequence-index` when indexing the return value of
`np.ufunc.reduce` and similar. The ufunc brain (`brain_numpy_core_umath.py`) models the
ufunc _functions_ but not the _method_ returns. Add stubs for `reduce`, `accumulate`,
`outer`, `reduceat` returning ndarray.

Not strictly numpy 2.x — these issues predate 2.0 — but they're in the same brain file
and easy to bundle.

### Out-of-scope: pyreverse fixes (#9681, #3602)

These two issues are not brain-plugin work — they're recursion in pyreverse's
class-attribute traversal when the inferred initializer is an ndarray. They need a
recursion-depth check or a "stop here if astroid value is a brain stub" guard in
pyreverse. List them in the related-work section of the brain PR but don't fix in this
plan.

---

## Test strategy

For each patch:

1. Add an astroid unit test under `tests/test_brain_numpy_*.py` matching the existing
   patterns: `extract_node("...")`, infer, assert the inferred result is an `Instance`
   of `numpy.ndarray` (or a tuple of expected length).
2. Add a pylint functional regression test under `tests/functional/r/regression_03/`
   using the existing pattern from `.triage/snippets/iNNNN.py` — assert that the bug's
   message id does NOT fire on the snippet.

The 8 snippets in `.triage/snippets/` for issues #10806, #5831, #10440, #9989, #9956,
#7883, #9385, #7981 are already in this repo and ready to copy into the functional test
suite once the brain fix lands.

---

## Rollout

Suggested order (smallest blast radius first):

1. Patch 2 (variadic `reshape`) — one-character signature change, mechanical
2. Patch 3 (`strides` tuple type) — same
3. Patch 4 (`unravel_index` return) — one-line
4. Patch 1 (`finfo` / `iinfo`) — new class stubs, no API change
5. Patch 7 (`empty_like` via `from`-import) — touches inference-tip registration
6. Patch 5 (`mgrid`) — new brain submodule
7. Patch 6 (`numpy.dtypes`) — new brain submodule, version-gated
8. Patch 8 (`ufunc.reduce`) — extends existing brain

Patches 1–4 can land as a single PR ("numpy brain: fix shape/tuple-length / add
finfo+iinfo"). Patches 5–6 as a second PR ("numpy brain: model mgrid/ogrid and
numpy.dtypes for numpy 2.x"). Patch 7 as a small independent PR. Patch 8 separately.

## Verifying the close

After the astroid release, re-run this script from the pylint repo to confirm closure:

```bash
.triage/reverify_fixed.py  # see existing helper for the FIXED audit
```

Each closed snippet stops reporting its bug. The maintainer can then close the
corresponding pylint issues with a pointer to the astroid PR / release tag.

---

## Other numpy-adjacent issues (out of scope for this plan)

- **DESIGN bucket numpy issues** (#9889 prefer-stubs, #9783 dynamic brain registration,
  #9250 class-attribute inference, #8023 docparams numpy style, #8117
  singleton-comparison numpy.bool, #6211 numpy doc style, #4146 any/all detection, #3420
  numpy doctring, etc.) are pylint or pyproject decisions, not astroid work.
- **scipy** issues (#10831, #8018, #4083, #3104) need a separate scipy brain effort or
  ride on the ufunc patch. Note that scipy itself doesn't have an astroid brain
  currently — opportunity to add one.
- **pandas 3.x** is the equivalent next-largest cluster (12 EXTDEP issues, plus REPRO
  #10166). Worth a sister plan in the same shape.

## Audit trail

- Source data: `.triage/triage_state.json`, `.triage/issues_raw.json`
- Numpy-issue list: `.triage/numpy_issues.json`
- Repros that fire on current astroid: confirmed in this session against pylint 4.0.5 /
  astroid 4.0.2 / numpy 2.4.4.
- Companion analyses: `.triage/REPRO_AUDIT.md`, `.triage/ROOT_ISSUES_ANALYSIS.md`,
  `.triage/EXTERNAL_PLUGINS_AUDIT.md`, `.triage/FIXED_AUDIT.md`, `.triage/DUP_AUDIT.md`,
  `.triage/UNCLEAR_AUDIT.md`.
