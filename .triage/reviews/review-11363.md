# Review — PR #11363 (unnecessary-ellipsis false positive on Protocol methods)

Verified locally on a worktree of `d5e052b2e`, repo `venv/` (3.13.1), astroid as pinned.

Verdict: the fix is correct and narrowly scoped, and it implements exactly what
DanielNoord asked for in
[#9319 (comment)](https://github.com/pylint-dev/pylint/issues/9319#issuecomment-2440172178)
("`pylint` should not consider `...` unused if it is being used in the method of a
`Protocol`"). Reusing `is_protocol_class` and `is_function_body_ellipsis` instead of
hand-rolling the predicates is the right call. Nothing blocking; the items below are
documentation and test-coverage gaps plus two style nits.

## Verification

- `pytest tests/test_functional.py -k unnecessary_ellipsis` → 1 passed.
- Full `pytest tests/` → `2185 passed, 264 skipped, 5 xfailed`. The only two failures,
  `test_functional[no_name_in_module]` and
  `test_functional[unbalanced_tuple_unpacking]`, fail identically on `main` in this
  environment (pre-existing astroid drift, unrelated).
- `mypy pylint/checkers/ellipsis_checker.py` → clean. `pylint --rcfile=pylintrc` on it →
  10.00/10.
- `git show --check` → no whitespace / line-ending damage.
- Behaviour sweep over 12 shapes. Correctly **silent**: `class P(Protocol)`,
  `@runtime_checkable`, `typing.Protocol` spelled out, subscripted `Protocol[T]` base,
  `class P(OtherProtocol, Protocol)`, a `Protocol` nested inside another class,
  `async def` in a `Protocol`, and both the `@overload` stubs and the implementation
  inside a `Protocol`. Correctly **still reported**: a class that subclasses a protocol
  _without_ re-listing `Protocol` (so a nominal class), a class-level `...` after a
  class docstring inside a `Protocol`, and `@abstractmethod` on an `abc.ABC`.
- Perf: measured a 2000-method stub-heavy file on `main` vs the branch — 1.49 s both.
  The extra `is_protocol_class` inference is a wash (astroid caches it), so no concern.

## 1. Nothing explains the carve-out (please fix)

Neither the `visit_const` docstring nor the `W2301` help text was touched, and there is
no comment at the new `return`. The docstring still reads as an exhaustive list of the
emit rules:

```
Emits a warning when:
 - A line consisting of an ellipsis is preceded by a docstring.
 - A statement exists in the same scope as the ellipsis.
```

The _why_ here is the whole point of the change and it is nowhere in the code — a reader
six months from now sees three predicates and no rationale. Add a bullet and a short
comment, e.g.:

```python
        Does not emit when the ellipsis is the sole body of a ``Protocol`` method:
        there it marks the method as unimplemented, and removing it makes type
        checkers infer an implicit ``None`` return that clashes with the annotation.
```

## 2. The message page should document the exception (please fix)

`doc/data/messages/u/unnecessary-ellipsis/` has only `good.py` / `bad.py`. Users who hit
this message land on that page, and there is now a documented carve-out they cannot
discover from it. The repo already has the mechanism — `details.rst` alongside the
examples (see `doc/data/messages/f/fixme/details.rst`). A three-line `details.rst`
naming the `Protocol` exception would close the loop.

## 3. Missing regression tests at the boundary (please fix)

The fixture pins the two Protocol-method cases, which is the core of the fix. Three
neighbours are load-bearing and unpinned — I confirmed all three behave correctly today,
which is exactly why they are worth freezing:

```python
class ProtocolSubclass(ProtocolInterface):  # not a Protocol: no `Protocol` base
    def value(self) -> int:
        """Return a value."""
        ...  # [unnecessary-ellipsis]


class ProtocolClassBody(Protocol):
    """A protocol whose own body needs no ellipsis."""
    ...  # [unnecessary-ellipsis]
```

The first is precisely the line `is_protocol_class` draws (per the typing spec, a class
that subclasses a protocol without re-listing `Protocol` is nominal, not structural) and
nothing currently guards it. The second keeps someone from later widening the guard from
`FunctionDef` to `ClassDef`.

On the accepting side, an `async def` Protocol method is worth one more case — it works
today only because astroid's `AsyncFunctionDef` subclasses `FunctionDef`, which is not
obvious from the `isinstance(scope, nodes.FunctionDef)` line.

## 4. Import style is now mixed (nit)

```python
from pylint.checkers import BaseChecker, utils
from pylint.checkers.utils import only_required_for_messages
```

Two spellings of the same module in a 55-line file. Simplest fix is to drop the `utils`
import and extend the existing one:

```python
from pylint.checkers.utils import (
    is_function_body_ellipsis,
    is_protocol_class,
    only_required_for_messages,
)
```

## 5. Guard order reads backwards (nit)

The method now says "unless Protocol stub → return" _before_ the reader knows what the
emit condition is. Flipping the two blocks makes the intent read in the order it is
meant — "this would be reported, except when it is a Protocol stub":

```python
        scope = node.parent.parent
        if not (
            (isinstance(scope, (nodes.ClassDef, nodes.FunctionDef)) and scope.doc_node)
            or len(scope.body) > 1
        ):
            return

        if (
            isinstance(scope, nodes.FunctionDef)
            and is_function_body_ellipsis(scope)
            and is_protocol_class(scope.parent)
        ):
            return

        self.add_message("unnecessary-ellipsis", node=node)
```

Purely readability — I measured the perf angle and there is none.

## 6. Fixture naming and placement (nit)

`ProtocolWithImplementation` is misleading: the class provides no implementation, the
_method_ has a statement after the ellipsis. The file already names that shape
`ellipsis_and_subsequent_statement` — mirroring it
(`ProtocolEllipsisAndSubsequentStatement`) keeps the fixture self-describing. The two
classes are also appended after `assert "x" != ...` with no separator, while every other
group in the file has a `#` heading (`# Function overloading`, `# Method overloading`).
A `# Protocol methods` line would match.

## Not a problem

- `@abstractmethod` keeps warning. That is deliberate and matches the maintainer's
  position in the issue thread; the PR description says so. No objection — worth leaving
  the issue's abstractmethod half to a separate discussion rather than smuggling it in.
- Primer will only ever show removals for this change (the diff is strictly a
  suppression), so no false-positive risk to chase there.
- Changelog fragment name, type and wording all match repo convention.
