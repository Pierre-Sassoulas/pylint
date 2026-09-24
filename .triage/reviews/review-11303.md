# Review — PR #11303 (`Report a changed parameter count in overridden special methods`)

Fixes issue #11295. Approved by DanielNoord, CI red on `pylint` (spelling). Branch is 43
commits behind `main` (based on `d0e52f4f19bd`).

Verified locally by applying **only** the `_different_parameters` hunk on top of current
`main` (`venv/bin/python`, 3.13.1, astroid 4.3.0). Copying the PR's whole
`class_checker.py` over `main` looks like it breaks `attribute_defined_outside_init` —
that is an artifact of the stale base (pre-#11272 `safe_mro`/`safe_slots`), not of this
PR.

Functional suite with the hunk alone: `2 failed, 899 passed, 37 skipped`, the two
failures being the pre-existing `no_name_in_module` / `unbalanced_tuple_unpacking` on
this box.

## 1. False positive — special methods whose arity is fixed by the protocol

The PR now keeps the `Number of parameters` message for every `PYMETHODS` entry outside
the constructor family. But `SPECIAL_METHODS_PARAMS` pins the expected arity for most of
them, and `unexpected-special-method-signature` (E0302) already enforces it against the
interpreter contract. When the child writes the _canonical_ signature and the base does
not, `arguments-differ` now contradicts E0302.

Two real-world families, both in the primer output:

**a. `__exit__` against a `*args` base** — pytest's `WarningsRecorder`:

```python
import warnings

class Recorder(warnings.catch_warnings):
    def __exit__(self, exc_type, exc_val, exc_tb):  # W0221 with the PR
        pass
```

`catch_warnings.__exit__(self, *exc_info)`; the child spells out the three arguments the
`with` statement always passes. E0302 is happy with both. The warning is noise.

**b. Operator dunders on a C-extension base** — astropy's `Quantity`:

```python
import numpy as np

class Quantity(np.ndarray):
    def __rshift__(self, other):   # W0221 with the PR
        return NotImplemented
    def __pow__(self, other):      # W0221 with the PR
        return NotImplemented
```

astroid introspects C slot wrappers as `def __rshift__(self)` — `self` and nothing else:

```
>>> cls.getattr("__rshift__")[0].args.as_string()
'self'
```

So _every_ correct operator override on a class inheriting from a C extension fires.
Pure builtins (`int`, `list`) are safe — their brain entries have no args at all and the
check bails out — so this is specific to introspected extension types (numpy, lxml, …),
which is exactly what makes it invisible in the functional tests.

### Suggested fix

Only keep the count message where the arity is genuinely variable, i.e.
`SPECIAL_METHODS_PARAMS` maps the name to `None` (`__new__`, `__init__`, `__call__`,
`__init_subclass__`) — the constructor family is exempt one branch earlier, so this is
`__call__`, the actual subject of #11295:

```python
    if original.name in CONSTRUCTOR_METHODS:
        output_messages.clear()
    elif original.name in PYMETHODS:
        if SPECIAL_METHODS_PARAMS[original.name] is None:
            # Only these have a variable arity, so a count mismatch against a
            # user-defined base is reported by nothing else. Everywhere else
            # `unexpected-special-method-signature` already checks the arity.
            output_messages[:] = [
                message for message in output_messages if "Number" in message
            ]
        else:
            output_messages.clear()
```

Measured with that variant:

- `CallChild.__call__` still flagged, the PR's own functional test passes unchanged.
- pytest `__exit__` and astropy `__rshift__`/`__pow__` go quiet.
- Full functional suite identical (same 2 pre-existing failures).

The cost is the two tuple-arity entries, `__round__` `(0, 1)` and `__pow__` `(1, 2)`: a
child that _narrows_ inside the accepted range stays unreported. That is rarer than the
numpy pattern it silences.

## 2. New false negative — `__post_init__`

`__post_init__` is not in `PYMETHODS`, so the old code never touched it. Putting it in
`CONSTRUCTOR_METHODS`, which is tested _before_ `PYMETHODS`, exempts it for the first
time:

```python
@dataclass
class Fruit:
    def __post_init__(self, apple): ...

@dataclass
class Apple(Fruit):
    def __post_init__(self, apple, banana): ...   # W0221 on main, silent with the PR
```

Nothing in #11295 asks for this, no functional test covers it, and the primer's "removed
messages" only listed `signature-differs`. Either drop it from the set, or keep it and
add a functional case plus an explicit changelog line — a silently dropped message is
the kind of thing that gets reported as a regression.

## 3. `"Number" in message` is a fragile sentinel

`_different_parameters` collects free-form strings; filtering on the substring
`"Number"` couples the exemption to the wording of `_has_different_parameters`. Matching
the exact `"Number of parameters "` sentinel (already used a few lines above for the
positional/kwonly merge) would at least keep the two spots consistent.

## 4. Pre-existing wording wart, now more visible

Primer, astropy:

```
Number of parameters was 12 in '_NonLinearLSQFitter.__call__' and is now 12 in overriding 'LMLSQFitter.__call__'
```

"was 12 and is now 12" comes from the merged positional+kwonly branch (the existing
`kwonly_4` functional case has the same shape). Not caused by this PR, but the PR puts
it in front of many more users. Worth a follow-up.

## 5. CI

`pylint` job fails on spelling only:

```
Wrong spelling of a word 'substitutability' in a comment
```

Add it to `custom_dict.txt` or reword the comment. Rebase on `main` while at it.

## 6. Issue thread

The reporter asked on 2026-08-25 what distinguishes `__call__` from `__init__` and is
still waiting. Worth answering before merging, since the PR closes the issue while
deliberately not doing what they asked for `__init__` (and now also silently drops
`__post_init__`).
