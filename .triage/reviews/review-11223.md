# Review — PR #11223 (fix recursive discovery below package roots)

Verified locally: worktree at `28c5ffedd`, its own `uv` venv with pylint installed
editable (the repo `venv/` shadows a worktree, so edits would otherwise not take
effect).

## Verification

- `pytest tests/lint/unittest_discover_files.py tests/lint/unittest_expand_modules.py tests/test_self.py`
  → `174 passed, 1 xfailed`.
- `pylint --rcfile=pylintrc pylint/lint/pylinter.py tests/lint/unittest_discover_files.py`
  → 10.00/10.
- The bug in #9187 is genuinely fixed: on a package `root_package/` containing
  `scripts/script.py`, `_discover_files` now yields `scripts/script.py` where `main`
  yielded nothing for it.
- The package-island case works too: `root_package/scripts/extra_package/` is yielded as
  its own expansion root, and `expand_modules` does not double-count any file (it is a
  dict keyed on normalized filepath).
- Dropping `skip_subtrees` in favour of top-down `dirnames` pruning is a real
  simplification: the `root.startswith(prefix)` prefix matching that the two
  `similarly_named_package` tests exist to guard is gone entirely, so that whole class
  of bug can no longer happen.

## 1. Dot-relative paths defeat the duplicate guard (real defect)

`pylinter.py:694-700` normalizes the package key but compares it against
`os.path.dirname(...)`. `os.path.normpath` collapses a leading `./`, so the parent of a
first-level child stops matching the recorded root:

- `root = "."` → `normpath(".")` = `"."` → recorded.
- `root = "./nested_package"` → `normpath(...)` = `"nested_package"` → `dirname` = `""`,
  which is not in `{"."}` → yielded as a _second_ expansion root.

Repro, from inside the package (this is the ordinary `pylint --recursive=y .`
invocation):

```
root_package/__init__.py
root_package/module.py
root_package/nested_package/__init__.py
root_package/nested_package/module.py
root_package/scripts/script.py
```

```
$ cd root_package && python -c "...; print(tuple(linter._discover_files(['.'])))"
('.', './nested_package', './scripts/script.py')
                ^^^^^^^^^^^^^^^^ redundant: already covered by '.'
```

Expected (and what an absolute path or a trailing-separator path already produces):
`('.', './scripts/script.py')`.

The output is not _wrong_ — `expand_modules` dedupes on the normalized filepath, so no
file is linted twice — but `nested_package/` is expanded twice for nothing, and the PR
description's claim that "normalized package-directory keys prevent duplicate linting"
does not hold for the most common spelling of the argument. None of the new tests
exercise a `.`-relative argument, which is why it slipped through.

Fix — compare like with like by normalizing the _parent_ the same way:

```python
if "__init__.py" in files:
    parent_directory = os.path.normpath(os.path.join(root, os.pardir))
    if parent_directory not in package_directories:
        yield root
    package_directories.add(os.path.normpath(root))
```

`normpath(os.path.join(".", os.pardir))` is `".."`, `normpath("./nested_package/..")` is
`"."`, and the absolute / trailing-separator cases are unchanged. I applied this
locally: the `.` case becomes `('.', './scripts/script.py')` and the full suite above
still passes (`174 passed, 1 xfailed`). Please add a `.`-relative case to
`test_expanded_files_below_package_root_are_not_duplicated` — parametrizing it over
`["", os.sep, "."]`-style arguments would cover all three spellings in one go.

## 2. The behavior change is much wider than the issue suggests — needs an explicit call

This does not only affect "the supplied directory is a package". Because the walk no
longer prunes at a package root _anywhere_, every non-package directory nested at any
depth inside any discovered package is now linted. Measured:

| target                                         | `main`            | this PR                  |
| ---------------------------------------------- | ----------------- | ------------------------ |
| `pylint/tests/functional` (a package)          | 1 root, 471 files | 498 roots, **973 files** |
| `tests/.pylint_primer_tests` (15 cloned repos) | 2647 roots        | **7554 roots**           |

The primer shows the same thing on real code: the only affected package is poetry-core,
and every single one of the 248+ reported messages (the comment is truncated at GitHub's
65 KB limit) comes from `src/poetry/core/_vendor/fastjsonschema/` — a vendored
third-party tree that was previously skipped because `_vendor/` has no `__init__.py`.

I think this is defensible and consistent with the intent of #5682 — the files are
Python source in the tree, and `--ignore` is the escape hatch — but it is a behavior
change that will noticeably increase what `--recursive=y` lints for a lot of projects,
and the changelog fragment currently undersells it:

> Fix `--recursive` discovery when the supplied directory is a package. Python files
> below non-package subdirectories are now linted as expected.

Please reword to say that this applies at any depth, not only to the supplied directory,
and that projects with vendored or generated directories inside a package may see a
larger file set and need `--ignore` / `--ignore-paths`. @Pierre-Sassoulas this is the
part that wants a maintainer decision rather than a code fix.

## 3. Every directory is ignore-tested twice

`os.walk(..., topdown=True)` hands you the child directory names _before_ descending,
and whichever names survive in `dirnames` come back on a later iteration as `root` in
their own right. The loop tests both ends of that handoff:

```python
for root, dirnames, files in os.walk(something, topdown=True):
    if _is_ignored_file(root, ...):                      # (A) tests the directory itself
        dirnames.clear()
        continue

    dirnames[:] = [                                      # (B) tests each child
        dirname
        for dirname in dirnames
        if not _is_ignored_file(os.path.join(root, dirname), ...)
    ]
```

So directory `X` is tested at (B) while its parent is the root, and again at (A) one
iteration later when `os.walk` yields `X` as the root. `_is_ignored_file` normalizes its
argument, so `os.path.join(parent, "X")` and the `root` string `os.walk` builds from the
same two pieces give the identical verdict — the second test can never disagree with the
first. Only the walk top escapes, because no parent filtered it. Instrumented on
`tests/functional`:

```
total calls: 243   unique paths: 122   paths called twice: 121
```

121 subdirectories x 2 + 1 top = 243.

That matters because `_is_ignored_file` is not cheap — `os.path.normpath`, then
`Path(element).absolute()` (an `os.getcwd()` per call), then up to three passes over the
ignore lists, two of them regex:

```python
element = os.path.normpath(element)
basename = Path(element).absolute().name
return (
    basename in ignore_list
    or _is_in_ignore_list_re(basename, ignore_list_re)
    or _is_in_ignore_list_re(element, ignore_list_paths_re)
)
```

Measured at ~17 us per call, and on the primer tree it is ~half of all discovery time.

The fix is to test `something` once before walking and keep only the child filter
inside:

```python
if os.path.isdir(something):
    if _is_ignored_file(
        something,
        self.config.ignore,
        self.config.ignore_patterns,
        self.config.ignore_paths,
    ):
        continue
    package_directories: set[str] = set()
    for root, dirnames, files in os.walk(something, topdown=True):
        dirnames[:] = [...]
```

I measured this on `tests/.pylint_primer_tests`, 3 runs each, same 7554 roots discovered
both ways:

|                    | run 1   | run 2   | run 3   |
| ------------------ | ------- | ------- | ------- |
| PR as-is           | 2019 ms | 2133 ms | 2015 ms |
| root check hoisted | 1456 ms | 1421 ms | 1470 ms |

~28% off discovery, and `_is_ignored_file` drops from 243 calls to 122 on
`tests/functional`. To be fair about the earlier main-vs-PR number I quoted: the 1406 ms
-> 1886 ms regression is mostly the extra tree this PR now walks, _not_ this duplicate;
the duplicate is the ~570 ms above, which is separable and worth taking on its own.

It is also strictly better behavior at the top: when the supplied directory is itself
ignored, the current code still calls `os.walk` and throws the first result away,
whereas hoisting skips the walk entirely. That does break one assertion —
`test_ignore_supplied_package_root` ends with `mock_walk.assert_called_once_with(...)`
and `os.walk` is then called zero times. The assertion is pinning an implementation
detail rather than behavior (see item 4); the meaningful assertion in that test,
`assert not discovered`, still passes. Rest of `tests/lint/` is green either way.

Still not a blocker — discovery is noise next to linting 3x the files — but it is free.

## 4. Test nits

- `unittest_discover_files.py:106,120,142` —
  `mock_walk.assert_called_once_with(str(package), topdown=True)` pins the _call
  spelling_. Switching to `os.walk(something, True)` would break three tests without
  changing any behavior. Asserting the call count is enough; `topdown` is already proven
  by the pruning assertions.
- `test_discover_files_sorts_directories` (`:123`) relies on the fake walk iterating the
  same list object that `_discover_files` sorts in place. That is a faithful model of
  `os.walk`, but it means the test passes because the mock cooperates. A real `tmp_path`
  tree with `z_package` and `a_package` would assert the same ordering against real
  `os.walk` and be much harder to fool.
- `mock_os_walk` hard-codes `assert root == "."`, so it is only reusable by the two
  `mock_tree` tests. Fine as-is, worth a comment saying so.

## Summary

Approach is right, the `skip_subtrees` removal is a genuine improvement, and the fix
does what #9187 asks. Blocking: item 1 (one-line fix + a `.`-relative test case). Needs
a maintainer call: item 2 (changelog wording for the wider behavior change). Items 3 and
4 are cleanups.
