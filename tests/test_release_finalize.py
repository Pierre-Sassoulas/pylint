# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the ``script/release_finalize.py`` release helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "script" / "release_finalize.py"
_spec = importlib.util.spec_from_file_location("release_finalize", SCRIPT)
assert _spec and _spec.loader
release_finalize = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release_finalize)


def test_parse_version() -> None:
    assert release_finalize.parse_version("4.2.0") == (4, 2, 0)
    assert release_finalize.parse_version("10.0.6") == (10, 0, 6)


@pytest.mark.parametrize("version", ["4.2.0-dev0", "4.2", "v4.2.0", "4.2.0b1"])
def test_parse_version_rejects_non_final(version: str) -> None:
    with pytest.raises(SystemExit):
        release_finalize.parse_version(version)


def test_dry_run_does_not_run_mutating_commands(capsys: pytest.CaptureFixture) -> None:
    runner = release_finalize.Runner(apply=False)
    # A mutating call is skipped and only printed.
    assert runner.gh("api", "--method", "PATCH", "x") == ""
    captured = capsys.readouterr().out
    assert "DRY-RUN would run" in captured
