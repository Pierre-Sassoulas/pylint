# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the 'configuration-outdated' hint shown on a stale configuration."""

from __future__ import annotations

from pathlib import Path

from pytest import CaptureFixture

from pylint.testutils._run import _Run as Run

HERE = Path(__file__).parent.absolute()
EMPTY_MODULE = HERE / ".." / "regrtest_data" / "empty.py"

# 'const-rgx' is targeted by a 4.0 breaking change, so a config setting it is
# outdated until 'pylint-config upgrade' reconciles it.
_OUTDATED = '[tool.pylint.basic]\nconst-rgx = "[A-Z]+"\n'


def test_outdated_configuration_is_reported(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """A configuration affected by a breaking change triggers the hint."""
    config = tmp_path / "pyproject.toml"
    config.write_text(_OUTDATED, encoding="utf-8")
    Run([str(EMPTY_MODULE), f"--rcfile={config}"], exit=False)
    assert "configuration-outdated" in capsys.readouterr().out


def test_clean_configuration_has_no_hint(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """A configuration with no applicable breaking change is not flagged."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        '[tool.pylint."messages control"]\ndisable = ["logging-not-lazy"]\n',
        encoding="utf-8",
    )
    Run([str(EMPTY_MODULE), f"--rcfile={config}"], exit=False)
    assert "configuration-outdated" not in capsys.readouterr().out


def test_latest_marker_silences_the_hint(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """'upgraded-to = latest' opts out of the hint."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        f'[tool.pylint]\nupgraded-to = "latest"\n\n{_OUTDATED}', encoding="utf-8"
    )
    Run([str(EMPTY_MODULE), f"--rcfile={config}"], exit=False)
    assert "configuration-outdated" not in capsys.readouterr().out


def test_recent_marker_silences_the_hint(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    """A marker newer than every catalogued change opts out of the hint."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        f'[tool.pylint]\nupgraded-to = "999.0.0"\n\n{_OUTDATED}', encoding="utf-8"
    )
    Run([str(EMPTY_MODULE), f"--rcfile={config}"], exit=False)
    assert "configuration-outdated" not in capsys.readouterr().out


def test_hint_can_be_disabled(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """The hint is suppressible like any other message."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        f'{_OUTDATED}\n[tool.pylint."messages control"]\n'
        'disable = ["configuration-outdated"]\n',
        encoding="utf-8",
    )
    Run([str(EMPTY_MODULE), f"--rcfile={config}"], exit=False)
    assert "configuration-outdated" not in capsys.readouterr().out
