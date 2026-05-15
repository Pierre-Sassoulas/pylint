"""Generate regression tests for all FIXED issues.

For each FIXED issue, copies the snippet from .triage/snippets/iNNNN.py to
tests/functional/r/regression_02/regression_NNNNN.py with a proper header.
Creates a .txt file only when the test is expected to report messages
(i.e. for false-negative fixes — fewer of these in our list).
"""

from pathlib import Path

ROOT = Path("/home/pierre/pylint")
SNIPPETS = ROOT / ".triage" / "snippets"
TEST_DIR = ROOT / "tests" / "functional" / "r" / "regression_02"

# (issue_num, title, kind, disable_messages, expected_txt_lines)
# kind: "fp" = false-positive fix (expect 10/10), "fn" = false-negative now raised
# disable_messages: additional disables for the test
# expected_txt_lines: list of "msg:line:col[:endline:endcol[:obj]]:text:CONF" if kind=="fn"
FIXED_ISSUES = [
    # Recent FP fixes (pylint 4.0.x cycle)
    (
        10768,
        "Module-level global reassigned via 'global' should not trigger invalid-name",
        "fp",
        ["missing-docstring", "missing-function-docstring", "global-statement"],
        None,
        None,
    ),
    (
        10766,
        "Module-level reassignment inside `if __name__ == '__main__':` should not trigger invalid-name",
        "fp",
        ["missing-docstring", "missing-function-docstring"],
        None,
        None,
    ),
    (
        10670,
        "Subclass of datetime.datetime with custom __new__ should not trigger E1121",
        "fp",
        ["missing-docstring", "too-many-positional-arguments"],
        None,
        None,
    ),
    (
        10455,
        "Conditional expression + None-narrowing should not trigger E1136",
        "fp",
        ["missing-docstring", "fixme"],
        None,
        None,
    ),
    (
        10442,
        "__main__.py module name under camelCase style should not trigger invalid-name",
        "fp",
        [],
        "--module-naming-style=camelCase",
        None,
    ),
    (
        10422,
        "f-string getattr should be treated like %%-format for not-callable",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        "-d all -e not-callable",
        None,
    ),
    (
        10374,
        "redefined-variable-type should not fire on dummy var assignment",
        "fp",
        [],
        "--load-plugins=pylint.extensions.redefined_variable_type",
        None,
    ),
    (
        10298,
        "Iterable[X]|None narrowing should not trigger not-an-iterable",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        9722,
        "Multi-level property subclass should not trigger comparison-with-callable",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        9497,
        "datetime.datetime member should be detected by no-member",
        "fn",
        [],
        None,
        ["no-member:3:6:3:31::Class 'datetime' has no 'not_a_member' member:INFERENCE"],
    ),
    (
        8805,
        "zipimport.ZipImportError should not trigger no-member",
        "fp",
        ["missing-docstring", "pointless-statement"],
        None,
        None,
    ),
    (
        8600,
        "Generic[T] base class protected-access from child should pass",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        8499,
        "TypeVar name with digits should not trigger invalid-name",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        8419,
        "Path.read_text without encoding should trigger W1514",
        "fn",
        ["missing-docstring"],
        None,
        [
            "unspecified-encoding:3:7:3:30::Using open without explicitly specifying an encoding:HIGH"
        ],
    ),
    (
        8250,
        "Multiple returns should produce one missing-return-doc per function, not per return",
        "fp",
        [],
        "--load-plugins=pylint.extensions.docparams",
        None,
    ),
    (
        8201,
        "trailing-comma-tuple should not be falsely raised here (no-op fixed)",
        "fp",
        ["expression-not-assigned"],
        None,
        None,
    ),
    (
        8179,
        "consider-using-augmented-assign should not fire for string %% formatting",
        "fp",
        ["missing-docstring"],
        "--load-plugins=pylint.extensions.code_style",
        None,
    ),
    (
        8068,
        "del self._m[:] after conditional None init should not trigger unsupported-delete-operation",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        8053,
        "Inherited descriptor with __slots__=() should not trigger assigning-non-slot",
        "fp",
        ["missing-docstring", "too-few-public-methods", "unused-argument"],
        None,
        None,
    ),
    (
        8050,
        "pylint should check a file named exactly like its containing directory",
        "fp",
        ["missing-docstring", "unused-import"],
        None,
        None,
    ),
    (
        7950,
        "Subclass of Abstract that does not inherit abc.ABC should not be considered abstract",
        "fp",
        ["missing-docstring", "too-few-public-methods", "abstract-method"],
        None,
        None,
    ),
    (
        7934,
        "Generic class inheriting TypedDict instance should not flag missing class docstring",
        "fp",
        ["too-few-public-methods"],
        None,
        None,
    ),
    (
        7891,
        "NamedTuple subclass should expose _asdict()",
        "fp",
        ["missing-docstring", "pointless-statement"],
        None,
        None,
    ),
    (
        7647,
        "lambda referencing conditional kwargs dict should not trigger unnecessary-lambda",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        7381,
        "Chained Flag | Flag | Flag should not trigger unsupported-binary-operation",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        7350,
        "Nested try with exhaustive raise should not trigger used-before-assignment",
        "fp",
        ["missing-docstring", "bare-except"],
        None,
        None,
    ),
    (
        7240,
        "List/set comprehension after sys.platform guard should not trigger no-member",
        "fp",
        ["missing-docstring", "unnecessary-comprehension", "invalid-name"],
        None,
        None,
    ),
    (
        5823,
        "@dataclass(slots=True) subclass with super().method() should not suggest super-with-arguments",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        4920,
        "'not isinstance() or attr' narrowing should not trigger no-member",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        4608,
        "'-x if x is not None else None' should not trigger invalid-unary-operand-type",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        4554,
        "'os.path.join(*a)' where 'a' is a populated list should not trigger no-value-for-parameter",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        3925,
        "Destructuring 'a, b = f or (None, None)' should not trigger not-callable",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        3893,
        "Class chosen by loop equality should not trigger unexpected-keyword-arg",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        3603,
        "Class differently defined in if/else branches should not trigger unexpected-keyword-arg",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        3327,
        "Module named 'builtins' (from-imported) should not trigger no-member 'dict has no...'",
        "fp",
        ["missing-docstring", "pointless-statement"],
        None,
        None,
    ),
    (
        3325,
        "property(get, set) with setter setting self._value should not trigger attribute-defined-outside-init",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        2981,
        "Derived(Base[T]) assigning attr defined in Base.__init__ should not trigger attribute-defined-outside-init",
        "fp",
        ["missing-docstring", "too-few-public-methods"],
        None,
        None,
    ),
    (
        2821,
        "MagicMock attribute reassigned to lambda should not trigger no-member",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        1934,
        "Single-iteration for-loop lambda capture should not trigger cell-var-from-loop",
        "fp",
        ["missing-docstring", "consider-using-tuple"],
        None,
        None,
    ),
    (
        1493,
        "Iterating list of callables and calling fn(...) should not trigger not-callable",
        "fp",
        ["missing-docstring"],
        None,
        None,
    ),
    (
        241,
        "import os.path as path used as attribute access should not trigger unused-import",
        "fp",
        ["missing-docstring", "consider-using-from-import"],
        None,
        None,
    ),
]


def write_test(num, title, kind, disables, extra_cli, expected_lines):
    snippet_path = SNIPPETS / f"i{num}.py"
    if not snippet_path.exists():
        print(f"#{num}: SKIPPED — snippet not found at {snippet_path}")
        return False

    snippet = snippet_path.read_text()
    # Strip any pylint:disable comments on first line if present
    test_py_path = TEST_DIR / f"regression_{num}.py"
    rc_path = TEST_DIR / f"regression_{num}.rc"
    txt_path = TEST_DIR / f"regression_{num}.txt"

    # Build disables list as comment
    disable_comment = ""
    if disables:
        disable_comment = f"# pylint: disable={','.join(disables)}\n"

    content = (
        "# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html\n"
        "# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE\n"
        "# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt\n"
        "\n"
        f'"""Regression test for https://github.com/pylint-dev/pylint/issues/{num}\n'
        "\n"
        f"{title}.\n"
        '"""\n'
        "\n"
        f"{disable_comment}"
        f"{snippet}\n"
    )

    test_py_path.write_text(content)
    print(f"#{num}: wrote {test_py_path.relative_to(ROOT)}")

    # Write rc file if extra CLI options needed
    if extra_cli:
        if "--load-plugins" in extra_cli:
            plugins = extra_cli.split("--load-plugins=")[-1].split()[0]
            rc_content = f"[MAIN]\nload-plugins = {plugins}\n"
        elif "--module-naming-style" in extra_cli:
            style = extra_cli.split("--module-naming-style=")[-1].split()[0]
            rc_content = f"[BASIC]\nmodule-naming-style = {style}\n"
        elif "-d all -e" in extra_cli:
            # disable all + enable specific
            enabled = extra_cli.split("-e")[-1].strip()
            rc_content = f"[MAIN]\ndisable = all\nenable = {enabled}\n"
        else:
            rc_content = None
        if rc_content:
            rc_path.write_text(rc_content)
            print(f"#{num}:   + rc file")

    # Write expected .txt for FN-converted fixes
    if kind == "fn" and expected_lines:
        txt_path.write_text("\n".join(expected_lines) + "\n")
        print(f"#{num}:   + txt file (expected: {len(expected_lines)} messages)")

    return True


def main():
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Writing regression tests to {TEST_DIR.relative_to(ROOT)}/\n")
    written = 0
    for item in FIXED_ISSUES:
        if write_test(*item):
            written += 1
    print(f"\n=== Wrote {written}/{len(FIXED_ISSUES)} regression tests ===")


if __name__ == "__main__":
    main()
