# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test the primer commands."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from _pytest.capture import CaptureFixture

from pylint.constants import IS_PYPY
from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer import PackageToLint
from pylint.testutils._primer.comparator import PackageDiff, iter_common_keys
from pylint.testutils._primer.primer import Primer
from pylint.testutils._primer.primer_compare_command import CompareCommand

HERE = Path(__file__).parent
TEST_DIR_ROOT = HERE.parent.parent
PRIMER_DIRECTORY = TEST_DIR_ROOT / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = TEST_DIR_ROOT / "primer/packages_to_prime.json"
CASES_PATH = HERE / "cases"

# If you change this, also change DEFAULT_PYTHON in
# ``.github/workflows/primer_comment.yaml``
PRIMER_CURRENT_INTERPRETER = (3, 15)

DEFAULT_ARGS = ["python tests/primer/__main__.py", "compare", "--commit=v2.14.2"]


def _message(message: str, clone_directory: Path) -> JSONMessage:
    path = clone_directory / "example.py"
    return JSONMessage(
        confidence="HIGH",
        type="convention",
        module="example",
        obj="",
        line=1,
        column=0,
        endLine=None,
        endColumn=None,
        path=str(path),
        absolutePath=str(path),
        symbol="missing-docstring",
        message=message,
        messageId="C0114",
    )


@pytest.mark.parametrize("args", [[], ["wrong_command"]])
def test_primer_launch_bad_args(args: list[str], capsys: CaptureFixture) -> None:
    with pytest.raises(SystemExit):
        with patch("sys.argv", ["python tests/primer/__main__.py", *args]):
            Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
    out, err = capsys.readouterr()
    assert not out
    assert "usage: Pylint Primer" in err


@pytest.mark.parametrize(
    ("args", "command_path"),
    [
        (
            ["prepare", "--read-commit-string"],
            "pylint.testutils._primer.primer.PrepareCommand",
        ),
        (["run", "--type=main"], "pylint.testutils._primer.primer.RunCommand"),
    ],
)
def test_primer_selects_command(args: list[str], command_path: str) -> None:
    with patch(command_path) as command:
        with patch("sys.argv", ["python tests/primer/__main__.py", *args]):
            Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()

    command.assert_called_once()
    command.return_value.run.assert_called_once()


def test_primer_extended_uses_extended_packages(tmp_path: Path) -> None:
    extended_json = tmp_path / "extended.json"
    extended_json.write_text(
        '{"extended-only": {"url": "https://github.com/example/extended-only",'
        ' "branch": "main", "commit": "main", "directories": ["."]}}',
        encoding="utf-8",
    )
    argv = ["python tests/primer/__main__.py", "--extended", "run", "--type=main"]
    with patch("sys.argv", argv):
        primer = Primer(tmp_path, PACKAGES_TO_PRIME_PATH, extended_json)

    assert list(primer.packages) == ["extended-only"]
    assert primer.command.primer_directory == tmp_path / "extended_primer"
    assert primer.command.primer_directory.is_dir()


def test_primer_extended_needs_extended_packages(capsys: CaptureFixture) -> None:
    argv = ["python tests/primer/__main__.py", "--extended", "run", "--type=main"]
    with pytest.raises(SystemExit), patch("sys.argv", argv):
        Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH)
    assert "no extended list of packages to prime" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("batches", "batch_idx", "expected"),
    [
        (None, None, ["a", "b", "c", "d", "e"]),
        (2, 0, ["a", "c", "e"]),
        (2, 1, ["b", "d"]),
    ],
)
def test_packages_in_batch(
    batches: int | None, batch_idx: int | None, expected: list[str]
) -> None:
    packages = {
        name: PackageToLint(
            url=f"https://github.com/example/{name}",
            branch="main",
            directories=["."],
            commit="main",
        )
        for name in "abcde"
    }
    config = argparse.Namespace(batches=batches, batchIdx=batch_idx)
    command = CompareCommand(PRIMER_DIRECTORY, packages, config)
    assert [name for name, _ in command.packages_in_batch()] == expected


@pytest.mark.parametrize(
    ("extended", "expected"),
    [
        (False, "**no effect** on the checked open source code."),
        (True, "**no effect** on the extended primer's open source code."),
    ],
)
def test_compare_no_effect_names_the_primer(extended: bool, expected: str) -> None:
    config = argparse.Namespace(commit="deadbeef", extended=extended, pr=None)
    command = CompareCommand(PRIMER_DIRECTORY, {}, config)
    assert expected in command._create_comment([])  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("extended", "pr", "has_hint"),
    [(False, 1234, True), (False, None, False), (True, 1234, False)],
)
def test_compare_tells_how_to_launch_the_extended_primer(
    extended: bool, pr: int | None, has_hint: bool
) -> None:
    config = argparse.Namespace(commit="deadbeef", extended=extended, pr=pr)
    command = CompareCommand(PRIMER_DIRECTORY, {}, config)
    comment = command._create_comment([])  # type: ignore[arg-type]
    hint = "`gh workflow run primer_run_extended.yaml -R pylint-dev/pylint -f pr=1234`"
    assert (hint in comment) is has_hint
    assert comment.endswith("*This comment was generated for commit deadbeef*")


def test_truncated_compare_stops_iterating_packages() -> None:
    max_comment_length = 500
    packages = {
        name: PackageToLint(
            url=f"https://github.com/example/{name}",
            branch="main",
            directories=["."],
            commit="main",
        )
        for name in ("first", "second")
    }
    comparator = [
        PackageDiff(
            package="first",
            missing={"commit": "main", "messages": []},
            new={
                "commit": "pr",
                "messages": [_message("x" * 300, packages["first"].clone_directory)],
            },
            changed=[],
        ),
        PackageDiff(
            package="second",
            missing={"commit": "main", "messages": []},
            new={
                "commit": "pr",
                "messages": [
                    _message("should be skipped", packages["second"].clone_directory)
                ],
            },
            changed=[],
        ),
    ]
    command = CompareCommand(
        PRIMER_DIRECTORY,
        packages,
        argparse.Namespace(commit="deadbeef", extended=False, pr=None),
    )

    with patch(
        "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
        max_comment_length,
    ):
        comment = command._create_comment(comparator)  # type: ignore[arg-type]

    assert "first" in comment
    assert "second" not in comment
    assert "This comment was truncated" in comment
    assert len(comment) < max_comment_length


@pytest.mark.skipif(
    sys.platform != "linux"
    or sys.version_info[:2] != PRIMER_CURRENT_INTERPRETER
    or IS_PYPY,
    reason=(
        "Primers are internal and will always be run for only one interpreter (currently"
        f" {PRIMER_CURRENT_INTERPRETER}, on linux)"
    ),
)
class TestPrimer:
    @pytest.mark.parametrize(
        "directory",
        [
            pytest.param(p, id=str(p.relative_to(CASES_PATH)))
            for p in CASES_PATH.iterdir()
            if p.is_dir()
        ],
    )
    def test_compare(self, directory: Path) -> None:
        """Test for the standard case.

        Directory in 'cases/' with 'main.json', 'pr.json' and 'expected.txt'.
        """
        self.__assert_expected(directory)

    def test_compare_batched(self) -> None:
        fixture = HERE / "batched_cases"
        self.__assert_expected(
            fixture,
            fixture / "main_BATCHIDX.json",
            fixture / "pr_BATCHIDX.json",
            batches=2,
        )

    def test_truncated_compare(self) -> None:
        """Test for the truncation of comments that are too long."""
        max_comment_length = 525
        directory = CASES_PATH / "message_changed"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory, expected_file=directory / "expected_truncated.txt"
            )
        assert len(content) < max_comment_length

    def test_truncated_compare_stops_iterating_packages(self) -> None:
        """Once the comment exceeds MAX, further packages should be skipped."""
        max_comment_length = 500
        directory = CASES_PATH / "multi_package"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory,
                expected_file=directory / "expected_truncated_break.txt",
            )
        # Only the first package made it in; the second was skipped by the break.
        assert "astroid" in content
        assert "astropy" not in content
        assert len(content) < max_comment_length

    def test_truncated_compare_in_details(self) -> None:
        """Test for the truncation of comments that are too long inside details."""
        max_comment_length = 420
        directory = CASES_PATH / "message_changed"
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            content = self.__assert_expected(
                directory, expected_file=directory / "expected_truncated_in_details.txt"
            )
        assert len(content) < max_comment_length

    def test_truncate_falls_back_when_no_line_break(self) -> None:
        """When the pre-limit prefix has no line break, cut inside the line."""
        max_comment_length = 200
        config = argparse.Namespace(commit="v2.14.2", extended=False, pr=None)
        command = CompareCommand(PRIMER_DIRECTORY, {}, config)
        spaceless = "x" * 500
        with patch(
            "pylint.testutils._primer.primer_compare_command.MAX_GITHUB_COMMENT_LENGTH",
            max_comment_length,
        ):
            truncated = command._truncate_comment(spaceless)
        assert "..." in truncated
        assert len(truncated) < max_comment_length

    @staticmethod
    def __assert_expected(
        directory: Path,
        main: Path | None = None,
        pr: Path | None = None,
        expected_file: Path | None = None,
        batches: int = 0,
    ) -> str:
        if main is None:
            main = directory / "main.json"
        if pr is None:
            pr = directory / "pr.json"
        if expected_file is None:
            expected_file = directory / "expected.txt"
        new_argv = [*DEFAULT_ARGS, f"--base-file={main}", f"--new-file={pr}"]
        if batches:
            new_argv.append(f"--batches={batches}")
        with patch("sys.argv", new_argv):
            Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH).run()
        with open(PRIMER_DIRECTORY / "comment.txt", encoding="utf8") as f:
            content = f.read()
        with open(expected_file, encoding="utf8") as f:
            expected = f.read()
        # rstrip so the expected.txt can end with a newline
        assert content == expected.rstrip("\n")
        return content


def test_iter_common_keys_skips_added_and_removed() -> None:
    base = {"kept": {"commit": "aaa"}, "removed": {"commit": "aaa"}}
    new = {"kept": {"commit": "aaa"}, "added": {"commit": "aaa"}}
    assert list(iter_common_keys(base, new)) == ["kept"]
    assert not list(iter_common_keys({}, {}))
