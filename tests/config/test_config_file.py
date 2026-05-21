# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the ConfigFile reader/writer used by 'pylint-config upgrade'."""

from __future__ import annotations

import textwrap
from pathlib import Path

from pylint.config._breaking_changes import ConfigView
from pylint.config._pylint_config.config_file import ConfigFile


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_config_file_is_a_config_view(tmp_path: Path) -> None:
    """ConfigFile structurally satisfies the ConfigView protocol."""
    path = _write(tmp_path / "pyproject.toml", "[tool.pylint]\n")
    view: ConfigView = ConfigFile.from_path(path)
    assert not view.has_option("max-line-length")


def test_toml_queries(tmp_path: Path) -> None:
    """Queries find enable/disable/load-plugins and options across sub-tables."""
    path = _write(
        tmp_path / "pyproject.toml",
        textwrap.dedent("""\
            [tool.pylint."messages control"]
            disable = "logging-not-lazy,logging-format-interpolation"
            enable = ["useless-suppression"]

            [tool.pylint.main]
            load-plugins = ["pylint.extensions.no_self_use"]

            [tool.pylint.basic]
            const-rgx = "[A-Z]+"
            """),
    )
    config = ConfigFile.from_path(path)
    assert config.is_message_disabled("logging-not-lazy")
    assert config.is_message_enabled("useless-suppression")
    assert config.is_extension_loaded("pylint.extensions.no_self_use")
    assert config.has_option("const-rgx")
    assert not config.has_option("max-line-length")


def test_membership_is_exact(tmp_path: Path) -> None:
    """A partial token is not treated as an enabled or disabled message."""
    path = _write(
        tmp_path / "pyproject.toml",
        '[tool.pylint."messages control"]\ndisable = "logging-format-interpolation"\n',
    )
    config = ConfigFile.from_path(path)
    assert config.is_message_disabled("logging-format-interpolation")
    assert not config.is_message_disabled("logging-format")


def test_rename_option_preserves_value_and_comments(tmp_path: Path) -> None:
    """rename_option keeps the value and the rest of the file's comments."""
    path = _write(
        tmp_path / "pyproject.toml",
        '# top comment\n[tool.pylint.main]\nextension-pkg-whitelist = "numpy"\n',
    )
    config = ConfigFile.from_path(path)
    config.rename_option("extension-pkg-whitelist", "extension-pkg-allow-list")
    config.save()
    written = path.read_text(encoding="utf-8")
    assert 'extension-pkg-allow-list = "numpy"' in written
    assert "extension-pkg-whitelist" not in written
    assert "# top comment" in written


def test_remove_option(tmp_path: Path) -> None:
    """remove_option deletes the option wherever it is set."""
    path = _write(
        tmp_path / "pyproject.toml",
        "[tool.pylint.main]\nsuggestion-mode = true\njobs = 2\n",
    )
    config = ConfigFile.from_path(path)
    config.remove_option("suggestion-mode")
    assert not config.has_option("suggestion-mode")
    assert config.has_option("jobs")


def test_enable_disable_message(tmp_path: Path) -> None:
    """Enable and disable add to the right list and clear the opposite one."""
    path = _write(
        tmp_path / "pyproject.toml",
        '[tool.pylint."messages control"]\ndisable = ["no-self-use"]\n',
    )
    config = ConfigFile.from_path(path)
    config.enable_message("no-self-use")
    assert config.is_message_enabled("no-self-use")
    assert not config.is_message_disabled("no-self-use")

    config.disable_message("no-self-use")
    assert config.is_message_disabled("no-self-use")
    assert not config.is_message_enabled("no-self-use")


def test_extension_mutations(tmp_path: Path) -> None:
    """add_extension and remove_extension edit the load-plugins list."""
    path = _write(tmp_path / "pyproject.toml", "[tool.pylint]\n")
    config = ConfigFile.from_path(path)
    config.add_extension("pylint.extensions.no_self_use")
    assert config.is_extension_loaded("pylint.extensions.no_self_use")
    config.remove_extension("pylint.extensions.no_self_use")
    assert not config.is_extension_loaded("pylint.extensions.no_self_use")


def test_list_value_forms(tmp_path: Path) -> None:
    """A list option keeps its form, string or array, when mutated."""
    string_form = _write(
        tmp_path / "string.toml",
        '[tool.pylint."messages control"]\ndisable = "a,b"\n',
    )
    config = ConfigFile.from_path(string_form)
    config.remove_from_disable("a")
    config.save()
    assert 'disable = "b"' in string_form.read_text(encoding="utf-8")
    assert not ConfigFile.from_path(string_form).is_message_disabled("a")

    array_form = _write(
        tmp_path / "array.toml",
        '[tool.pylint."messages control"]\ndisable = ["a", "b"]\n',
    )
    config = ConfigFile.from_path(array_form)
    config.remove_from_disable("a")
    config.save()
    assert "disable = [" in array_form.read_text(encoding="utf-8")
    reloaded = ConfigFile.from_path(array_form)
    assert not reloaded.is_message_disabled("a")
    assert reloaded.is_message_disabled("b")


def test_new_list_option_is_created(tmp_path: Path) -> None:
    """Mutating an absent list option creates it under [tool.pylint]."""
    path = _write(tmp_path / "pyproject.toml", "[tool.pylint]\n")
    config = ConfigFile.from_path(path)
    config.enable_message("useless-suppression")
    config.save()
    assert ConfigFile.from_path(path).is_message_enabled("useless-suppression")


def test_upgraded_to_marker(tmp_path: Path) -> None:
    """get_upgraded_to and set_upgraded_to read and write the marker."""
    path = _write(tmp_path / "pyproject.toml", "[tool.pylint]\n")
    config = ConfigFile.from_path(path)
    assert config.get_upgraded_to() is None
    config.set_upgraded_to("4.0.0")
    config.save()
    assert ConfigFile.from_path(path).get_upgraded_to() == "4.0.0"


def test_ini_is_migrated_to_pyproject(tmp_path: Path) -> None:
    """An ini source is read and written out as a sibling pyproject.toml."""
    ini = _write(tmp_path / "pylintrc", "[MESSAGES CONTROL]\ndisable = no-self-use\n")
    config = ConfigFile.from_path(ini)
    assert config.migrated_from_ini
    assert config.is_message_disabled("no-self-use")
    written = config.save()
    assert written == tmp_path / "pyproject.toml"
    assert ConfigFile.from_path(written).is_message_disabled("no-self-use")


def test_ini_merges_into_existing_pyproject(tmp_path: Path) -> None:
    """Migrating an ini reuses an existing pyproject.toml and keeps its tables."""
    _write(tmp_path / "pyproject.toml", "[tool.black]\nline-length = 88\n")
    ini = _write(tmp_path / "pylintrc", "[MAIN]\njobs = 2\n")
    config = ConfigFile.from_path(ini)
    written = config.save()
    text = written.read_text(encoding="utf-8")
    assert "[tool.black]" in text
    assert "line-length" in text
    assert config.has_option("jobs")
