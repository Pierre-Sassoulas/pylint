# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Read, query, mutate and write a pylint configuration file.

``ConfigFile`` is the concrete ``ConfigView`` used by ``pylint-config
upgrade``. It reads a toml or ini configuration and always writes it back as
pyproject-style toml. Editing a toml source preserves its comments and layout
through tomlkit; an ini source is migrated into a sibling ``pyproject.toml``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import tomlkit

from pylint.config.config_file_parser import _RawConfParser

# Options whose value is a list of items, written as a string or a toml array.
_ENABLE = "enable"
_DISABLE = "disable"
_LOAD_PLUGINS = "load-plugins"
# Marker recording the pylint version the configuration was last upgraded to.
_UPGRADED_TO = "upgraded-to"


class ConfigFile:
    """A pylint configuration file exposed as a mutable ``ConfigView``."""

    def __init__(
        self,
        source: Path,
        document: tomlkit.TOMLDocument,
        *,
        migrated_from_ini: bool,
    ) -> None:
        self.source = source
        self.migrated_from_ini = migrated_from_ini
        self._document = document
        self._pylint = _ensure_pylint_table(document)

    @classmethod
    def from_path(cls, path: Path) -> ConfigFile:
        """Read the configuration at ``path``.

        A toml file is edited in place. An ini file is migrated into a sibling
        ``pyproject.toml``: an existing one is reused, otherwise a new document
        is created. Comments of an ini file are not carried over.
        """
        if path.suffix == ".toml":
            document = tomlkit.parse(path.read_text(encoding="utf-8"))
            return cls(path, document, migrated_from_ini=False)
        pyproject = path.parent / "pyproject.toml"
        if pyproject.is_file():
            document = tomlkit.parse(pyproject.read_text(encoding="utf-8"))
        else:
            document = tomlkit.document()
        _inject_ini_options(document, path)
        return cls(path, document, migrated_from_ini=True)

    @property
    def target(self) -> Path:
        """Where ``save`` writes: the toml source, or a sibling pyproject."""
        if self.migrated_from_ini:
            return self.source.parent / "pyproject.toml"
        return self.source

    def save(self) -> Path:
        """Write the configuration back as toml and return the written path."""
        target = self.target
        target.write_text(tomlkit.dumps(self._document), encoding="utf-8")
        return target

    # -- ConfigView queries ------------------------------------------------

    def is_message_enabled(self, msgid_or_symbol: str) -> bool:
        return msgid_or_symbol in self._get_list(_ENABLE)

    def is_message_disabled(self, msgid_or_symbol: str) -> bool:
        return msgid_or_symbol in self._get_list(_DISABLE)

    def is_extension_loaded(self, extension: str) -> bool:
        return extension in self._get_list(_LOAD_PLUGINS)

    def has_option(self, option: str) -> bool:
        return self._find_table(option) is not None

    # -- ConfigView mutations ---------------------------------------------

    def enable_message(self, msgid_or_symbol: str) -> None:
        self._remove_from_list(_DISABLE, msgid_or_symbol)
        self._add_to_list(_ENABLE, msgid_or_symbol)

    def disable_message(self, msgid_or_symbol: str) -> None:
        self._remove_from_list(_ENABLE, msgid_or_symbol)
        self._add_to_list(_DISABLE, msgid_or_symbol)

    def remove_from_enable(self, msgid_or_symbol: str) -> None:
        self._remove_from_list(_ENABLE, msgid_or_symbol)

    def remove_from_disable(self, msgid_or_symbol: str) -> None:
        self._remove_from_list(_DISABLE, msgid_or_symbol)

    def add_extension(self, extension: str) -> None:
        self._add_to_list(_LOAD_PLUGINS, extension)

    def remove_extension(self, extension: str) -> None:
        self._remove_from_list(_LOAD_PLUGINS, extension)

    def remove_option(self, option: str) -> None:
        table = self._find_table(option)
        if table is not None:
            del table[option]

    def rename_option(self, old_name: str, new_name: str) -> None:
        table = self._find_table(old_name)
        if table is None:
            return
        value = table[old_name]
        del table[old_name]
        table[new_name] = value

    # -- upgraded-to marker ------------------------------------------------

    def get_upgraded_to(self) -> str | None:
        """Return the recorded ``upgraded-to`` version, if the marker is set."""
        table = self._find_table(_UPGRADED_TO)
        if table is None:
            return None
        return str(table[_UPGRADED_TO])

    def set_upgraded_to(self, version: str) -> None:
        """Record ``version`` as the ``upgraded-to`` marker."""
        table = self._find_table(_UPGRADED_TO) or self._pylint
        table[_UPGRADED_TO] = version

    # -- internals ---------------------------------------------------------

    def _tables(self) -> list[Any]:
        """The ``[tool.pylint]`` table and every sub-table, the root first."""
        found: list[Any] = []

        def walk(table: Any) -> None:
            found.append(table)
            for value in table.values():
                if isinstance(value, dict):
                    walk(value)

        walk(self._pylint)
        return found

    def _find_table(self, key: str) -> Any | None:
        """The ``[tool.pylint]`` (sub-)table directly holding ``key``."""
        for table in self._tables():
            value = table.get(key)
            if value is not None and not isinstance(value, dict):
                return table
        return None

    def _get_list(self, key: str) -> list[str]:
        """The value of ``key`` as a list, from wherever it is set."""
        table = self._find_table(key)
        if table is None:
            return []
        return _as_list(table[key])

    def _add_to_list(self, key: str, item: str) -> None:
        table = self._find_table(key)
        if table is None:
            self._pylint[key] = [item]
            return
        value = table[key]
        if isinstance(value, str):
            items = _as_list(value)
            if item not in items:
                items.append(item)
            table[key] = ",".join(items)
        elif item not in _as_list(value):
            value.append(item)

    def _remove_from_list(self, key: str, item: str) -> None:
        table = self._find_table(key)
        if table is None:
            return
        value = table[key]
        if isinstance(value, str):
            table[key] = ",".join(i for i in _as_list(value) if i != item)
            return
        for index in range(len(value) - 1, -1, -1):
            if str(value[index]).strip() == item:
                del value[index]


def _as_list(value: Any) -> list[str]:
    """Read a pylint list option, written either as a string or an array."""
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value]


def _ensure_pylint_table(document: tomlkit.TOMLDocument) -> Any:
    """Return ``document``'s ``[tool.pylint]`` table, creating it if needed."""
    tool = document.get("tool")
    if tool is None:
        tool = tomlkit.table(is_super_table=True)
        document["tool"] = tool
    pylint = tool.get("pylint")
    if pylint is None:
        pylint = tomlkit.table()
        tool["pylint"] = pylint
    return pylint


def _inject_ini_options(document: tomlkit.TOMLDocument, ini_path: Path) -> None:
    """Copy the pylint options of an ini file into ``document``."""
    config_content, _ = _RawConfParser.parse_ini_file(ini_path)
    pylint = _ensure_pylint_table(document)
    for option, value in config_content.items():
        pylint[option] = value
