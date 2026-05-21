# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the 'pylint-config upgrade' command."""

from __future__ import annotations

import warnings
from collections.abc import Iterator
from pathlib import Path

import pytest
from pytest import CaptureFixture, MonkeyPatch

from pylint.config._pylint_config.config_file import ConfigFile
from pylint.lint.run import _PylintConfigRun as Run


@pytest.fixture(autouse=True)
def _ignore_runtime_note() -> Iterator[None]:
    """Silence the unrelated runtime NOTE warnings emitted by pylint-config."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        yield


def test_upgrade_non_interactive_renames_option(tmp_path: Path) -> None:
    """A FIX_CONF change such as an option rename is applied without prompting."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        '[tool.pylint.main]\nextension-pkg-whitelist = "numpy"\n', encoding="utf-8"
    )
    Run(["upgrade", str(config), "--non-interactive"], exit=False)
    text = config.read_text(encoding="utf-8")
    assert "extension-pkg-allow-list" in text
    assert "extension-pkg-whitelist" not in text


def test_upgrade_interactive_keep(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    """Choosing KEEP on a moved-to-extension change loads the extension."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        '[tool.pylint."messages control"]\nenable = ["no-self-use"]\n',
        encoding="utf-8",
    )
    monkeypatch.setattr("builtins.input", lambda _: "1")
    Run(["upgrade", str(config)], exit=False)
    assert ConfigFile.from_path(config).is_extension_loaded(
        "pylint.extensions.no_self_use"
    )


def test_upgrade_interactive_use_default(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    """Choosing USE_DEFAULT on a moved-to-extension change drops the message."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        '[tool.pylint."messages control"]\nenable = ["no-self-use"]\n',
        encoding="utf-8",
    )
    monkeypatch.setattr("builtins.input", lambda _: "2")
    Run(["upgrade", str(config)], exit=False)
    assert not ConfigFile.from_path(config).is_message_enabled("no-self-use")


def test_upgrade_non_interactive_skips_ambiguous(tmp_path: Path) -> None:
    """A non-interactive run leaves an ambiguous change untouched and unstamped."""
    config = tmp_path / "pyproject.toml"
    config.write_text(
        '[tool.pylint."messages control"]\nenable = ["no-self-use"]\n',
        encoding="utf-8",
    )
    Run(["upgrade", str(config), "--non-interactive"], exit=False)
    reloaded = ConfigFile.from_path(config)
    assert reloaded.is_message_enabled("no-self-use")
    assert reloaded.get_upgraded_to() is None


def test_upgrade_nothing_to_do(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """An up-to-date configuration is reported and stamped with the version."""
    config = tmp_path / "pyproject.toml"
    config.write_text("[tool.pylint]\n", encoding="utf-8")
    Run(["upgrade", str(config)], exit=False)
    assert "up to date" in capsys.readouterr().out
    assert ConfigFile.from_path(config).get_upgraded_to() is not None


def test_upgrade_pinned_to_latest(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """A configuration pinned with 'upgraded-to = latest' is left untouched."""
    config = tmp_path / "pyproject.toml"
    original = '[tool.pylint]\nupgraded-to = "latest"\n'
    config.write_text(original, encoding="utf-8")
    Run(["upgrade", str(config)], exit=False)
    assert "pinned to the latest" in capsys.readouterr().out
    assert config.read_text(encoding="utf-8") == original


def test_upgrade_no_config_file(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """A missing configuration file is reported on stderr."""
    Run(["upgrade", str(tmp_path / "absent.toml")], exit=False)
    assert "No configuration file" in capsys.readouterr().err


def test_upgrade_migrates_ini(tmp_path: Path) -> None:
    """An ini configuration is upgraded into a sibling pyproject.toml."""
    ini = tmp_path / ".pylintrc"
    ini.write_text("[MAIN]\nextension-pkg-whitelist = numpy\n", encoding="utf-8")
    Run(["upgrade", str(ini), "--non-interactive"], exit=False)
    pyproject = tmp_path / "pyproject.toml"
    assert pyproject.is_file()
    assert "extension-pkg-allow-list" in pyproject.read_text(encoding="utf-8")
