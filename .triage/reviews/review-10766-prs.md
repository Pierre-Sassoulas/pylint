# Review — #11080 vs #11309 (invalid-name FP in `if __name__ == "__main__":`, issue #10766)

Verified locally with `venv/bin/python` (3.13.1), both PR heads checked out in
worktrees, run with `--rcfile=/dev/null --disable=all --enable=invalid-name`.

## Verdict

**#11080 (Labib-Bin-Salam) is the one to keep.** #11309 (SparshGarg999) implements the
rejected variant of the fix: it moves every main-block name to the _variable_ style
instead of accepting either style, so it trades the old false positive for a new one.

| Sample line inside `if __name__ == "__main__":` | main                                    | #11080     | #11309                                |
| ----------------------------------------------- | --------------------------------------- | ---------- | ------------------------------------- |
| `exit_code = main()`                            | `Constant name ... UPPER_CASE` (the FP) | silent ✅  | silent ✅                             |
| `EXIT_CODE = main()`                            | silent                                  | silent ✅  | **`Variable name ... snake_case`** ❌ |
| `CONSTANT = True`                               | silent                                  | silent ✅  | **flagged** ❌                        |
| `OBJ = Cat()`                                   | silent                                  | silent ✅  | **flagged** ❌                        |
| `BadMix = main()`                               | flagged                                 | flagged ✅ | flagged ✅                            |
| `unused_returnCode = main()`                    | flagged                                 | flagged ✅ | flagged ✅                            |

#11309's regression is not hypothetical — CI is red on every functional job:

```
FAILED tests/test_functional.py::test_functional[base_init_vars]
  Unexpected in testdata:  33: invalid-name        # OBJ = MyClass()
FAILED tests/test_functional.py::test_functional[wrong_import_position_exclude_dunder_main]
  Unexpected in testdata:   5: invalid-name        # CONSTANT = True
```

Second bug in #11309: `_is_in_main_block` only excludes
`current is not current.parent.test`, so the **`else:` branch of the guard** counts as
"main block" too — exactly the branch that runs on import and where constants are most
real:

```python
if __name__ == "__main__":
    pass
else:
    imported_flag = main()   # main + #11080: flagged   #11309: silent (false negative)
```

It also matches `__name__ is "__main__"`, which pylint flags elsewhere and shouldn't
bless.

## Best of each

Almost everything worth keeping is already in #11080. From #11309, only two small
things:

1. Its helper tolerates a chained comparison (`test.ops` loop) where #11080 requires
   exactly one `==`. #11080's stricter form is the better default; not worth importing.
2. Nothing else — the `FunctionDef`/`ClassDef` early bail is dead code, since the caller
   already guarantees `isinstance(frame, nodes.Module)`.

Conversely #11080 has what #11309 lacks: a **functional test**
(`tests/functional/n/name/`), which is the project convention — #11309 puts its cases in
`tests/checkers/base/unittest_multi_naming_style.py`, a file about name _groups_, and
asserts exact `MessageTest` col offsets by hand.

## Remaining work on #11080

1. **The primer "false negative" is by design, but should be documented.** music21 lost
   `Constant name "unused_returnCode" ...` because _music21 sets_
   `variable-rgx = [a-z_][A-Za-z0-9_]{2,30}$`, which accepts camelCase. Reproduced:

   ```
   $ pylint --variable-rgx='[a-z_][A-Za-z0-9_]{2,30}$' sample.py
   main:   C0103: Constant name "unused_returnCode" doesn't conform to UPPER_CASE
   #11080: (nothing)
   ```

   With the default `variable-rgx` the name is still flagged. So this is the accepted
   cost of option (2) from #10700 ("pass against _either_ constant or variable regex"),
   scoped to the `__main__` guard only — it is not a bug in the patch. The other diff is
   only a label change, still emitted:

   `Constant name "te"` → `Variable name "te"` <!-- codespell:ignore te -->

2. Apply Pierre's suggestion (`unused_returnCode = main()  # mixed style is refused`) —
   it pins the primer case under default config, where it _is_ refused.

3. Add a functional case for the **exclusive-assignment** path — the second hook
   (`node_type == "const" and _in_dunder_main_block(node)`) is currently uncovered:

   ```python
   if __name__ == "__main__":
       if sys.argv[1:]:
           result_code = 1
       else:
           result_code = 2
   ```

   main flags it, #11080 doesn't. (Verified — both PRs behave the same here.)

4. Add an `else:`-branch case to lock in that the else body stays constant-checked.

5. `return` after `_check_name_in_main_block(...)` in the `else` branch is dead —
   nothing follows it in that path.

6. Neither PR updates `doc/data/messages/i/invalid-name/details.rst`, where the `const`
   and `variable` rows describe the module-level rules. The `__main__` exception belongs
   there.
