# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the configuration breaking-change data model."""

from __future__ import annotations

import pytest

from pylint.config._breaking_changes import (
    CONFIGURATION_BREAKING_CHANGES,
    BreakingChanges,
    Intention,
)
from pylint.config._breaking_changes.breaking_change import (
    ExtensionRemoved,
    MessageMadeDisabledByDefault,
    MessageMadeEnabledByDefault,
    MessageMovedToExtension,
    OptionBehaviorChanged,
    OptionRemoved,
    OptionRenamed,
)
from pylint.config._breaking_changes.breaking_changes import _parse_version
from pylint.config._breaking_changes.condition import (
    MessageIsNotEnabled,
    OptionIsNotPresent,
)
from pylint.config._breaking_changes.solution import DisableMessage


class _FakeConfig:
    """In-memory ConfigView used to exercise the breaking-change data model."""

    def __init__(
        self,
        *,
        enabled: set[str] | None = None,
        disabled: set[str] | None = None,
        plugins: set[str] | None = None,
        options: set[str] | None = None,
    ) -> None:
        self.enabled: set[str] = enabled or set()
        self.disabled: set[str] = disabled or set()
        self.plugins: set[str] = plugins or set()
        self.options: set[str] = options or set()

    def is_message_enabled(self, msgid_or_symbol: str) -> bool:
        return msgid_or_symbol in self.enabled

    def is_message_disabled(self, msgid_or_symbol: str) -> bool:
        return msgid_or_symbol in self.disabled

    def is_extension_loaded(self, extension: str) -> bool:
        return extension in self.plugins

    def has_option(self, option: str) -> bool:
        return option in self.options

    def enable_message(self, msgid_or_symbol: str) -> None:
        self.enabled.add(msgid_or_symbol)
        self.disabled.discard(msgid_or_symbol)

    def disable_message(self, msgid_or_symbol: str) -> None:
        self.disabled.add(msgid_or_symbol)
        self.enabled.discard(msgid_or_symbol)

    def remove_from_enable(self, msgid_or_symbol: str) -> None:
        self.enabled.discard(msgid_or_symbol)

    def remove_from_disable(self, msgid_or_symbol: str) -> None:
        self.disabled.discard(msgid_or_symbol)

    def add_extension(self, extension: str) -> None:
        self.plugins.add(extension)

    def remove_extension(self, extension: str) -> None:
        self.plugins.discard(extension)

    def remove_option(self, option: str) -> None:
        self.options.discard(option)

    def rename_option(self, old_name: str, new_name: str) -> None:
        self.options.discard(old_name)
        self.options.add(new_name)


def test_message_moved_to_extension() -> None:
    """It applies when the message is enabled and the extension is not loaded."""
    change = MessageMovedToExtension("no-self-use", "pylint.extensions.no_self_use")
    assert change.is_affected(_FakeConfig(enabled={"no-self-use"}))
    assert not change.is_affected(
        _FakeConfig(enabled={"no-self-use"}, plugins={"pylint.extensions.no_self_use"})
    )

    keep = _FakeConfig(enabled={"no-self-use"})
    change.apply_solution(keep, Intention.KEEP)
    assert keep.is_extension_loaded("pylint.extensions.no_self_use")

    use_default = _FakeConfig(enabled={"no-self-use"})
    change.apply_solution(use_default, Intention.USE_DEFAULT)
    assert not use_default.is_message_enabled("no-self-use")


def test_extension_removed() -> None:
    """It applies when the extension is loaded and the message is not disabled."""
    change = ExtensionRemoved("compare-to-zero", "pylint.extensions.comparetozero")
    assert change.is_affected(_FakeConfig(plugins={"pylint.extensions.comparetozero"}))
    assert not change.is_affected(_FakeConfig())

    config = _FakeConfig(plugins={"pylint.extensions.comparetozero"})
    change.apply_solution(config, Intention.FIX_CONF)
    assert not config.is_extension_loaded("pylint.extensions.comparetozero")
    assert config.is_message_enabled("compare-to-zero")


def test_option_renamed() -> None:
    """It applies when the old option name is present, and renames it."""
    change = OptionRenamed("extension-pkg-whitelist", "extension-pkg-allow-list")
    assert change.is_affected(_FakeConfig(options={"extension-pkg-whitelist"}))
    assert not change.is_affected(_FakeConfig())

    config = _FakeConfig(options={"extension-pkg-whitelist"})
    change.apply_solution(config, Intention.FIX_CONF)
    assert not config.has_option("extension-pkg-whitelist")
    assert config.has_option("extension-pkg-allow-list")


def test_option_removed() -> None:
    """It applies when the option is present, and removes it."""
    change = OptionRemoved("files-output", "No longer used.")
    assert change.is_affected(_FakeConfig(options={"files-output"}))
    assert not change.is_affected(_FakeConfig())

    config = _FakeConfig(options={"files-output"})
    change.apply_solution(config, Intention.FIX_CONF)
    assert not config.has_option("files-output")


def test_option_behavior_changed() -> None:
    """It applies when any option is present and never edits the configuration."""
    change = OptionBehaviorChanged(["const-rgx", "const-naming-style"], "Changed.")
    assert change.is_affected(_FakeConfig(options={"const-rgx"}))
    assert not change.is_affected(_FakeConfig())

    config = _FakeConfig(options={"const-rgx"})
    change.apply_solution(config, Intention.KEEP)
    change.apply_solution(config, Intention.USE_DEFAULT)
    assert config.has_option("const-rgx")


def test_message_made_disabled_by_default() -> None:
    """It applies unless the message is already disabled; KEEP enables it."""
    change = MessageMadeDisabledByDefault("a-message")
    assert change.is_affected(_FakeConfig())
    assert not change.is_affected(_FakeConfig(disabled={"a-message"}))

    keep = _FakeConfig()
    change.apply_solution(keep, Intention.KEEP)
    assert keep.is_message_enabled("a-message")

    use_default = _FakeConfig()
    change.apply_solution(use_default, Intention.USE_DEFAULT)
    assert not use_default.is_message_enabled("a-message")


def test_message_made_enabled_by_default() -> None:
    """It applies when the message is disabled; USE_DEFAULT drops the disable."""
    change = MessageMadeEnabledByDefault("a-message")
    assert change.is_affected(_FakeConfig(disabled={"a-message"}))
    assert not change.is_affected(_FakeConfig())

    keep = _FakeConfig(disabled={"a-message"})
    change.apply_solution(keep, Intention.KEEP)
    assert keep.is_message_disabled("a-message")

    use_default = _FakeConfig(disabled={"a-message"})
    change.apply_solution(use_default, Intention.USE_DEFAULT)
    assert not use_default.is_message_disabled("a-message")


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("4.0.0", (4, 0, 0)),
        ("4.0", (4, 0, 0)),
        ("2.7.3", (2, 7, 3)),
        ("4.0.0a1", (4, 0, 0)),
        ("3", (3, 0, 0)),
        ("0.0.0", (0, 0, 0)),
    ],
)
def test_parse_version(version: str, expected: tuple[int, int, int]) -> None:
    """It parses a version into a comparable triple, ignoring any suffix."""
    assert _parse_version(version) == expected


def test_breaking_changes_from_scratch() -> None:
    """A configuration never upgraded sees every catalogued change."""
    catalogued = sum(len(c) for c in CONFIGURATION_BREAKING_CHANGES.values())
    assert len(list(BreakingChanges("0.0.0"))) == catalogued
    assert list(BreakingChanges()) == list(BreakingChanges("0.0.0"))


def test_breaking_changes_up_to_date() -> None:
    """A configuration upgraded past the last catalogued version sees nothing."""
    assert not list(BreakingChanges("99.0.0"))
    assert not list(BreakingChanges("latest"))


def test_breaking_changes_only_newer_than_upgraded_to() -> None:
    """Only changes strictly newer than the upgraded-to version are yielded."""
    versions = {version for version, _ in BreakingChanges("2.14.0")}
    assert versions == {"3.0.0", "4.0.0"}


def test_breaking_changes_applicable_filters_by_config() -> None:
    """applicable() keeps only the changes that affect the configuration."""
    config = _FakeConfig(options={"extension-pkg-whitelist"})
    applicable = list(BreakingChanges("0.0.0").applicable(config))
    assert len(applicable) == 1
    version, change = applicable[0]
    assert version == "2.7.3"
    assert isinstance(change, OptionRenamed)


def test_catalog_changes_have_solutions() -> None:
    """Every catalogued change offers a non-empty solution per intention."""
    for changes in CONFIGURATION_BREAKING_CHANGES.values():
        for change in changes:
            assert change.solutions
            assert all(change.solutions.values())


def test_catalog_descriptions_render() -> None:
    """Every catalogued change, condition and solution renders some text."""
    for changes in CONFIGURATION_BREAKING_CHANGES.values():
        for change in changes:
            assert change.description
            assert all(str(condition) for condition in change.conditions)
            for solutions in change.solutions.values():
                assert all(str(solution) for solution in solutions)


def test_negated_conditions() -> None:
    """MessageIsNotEnabled and OptionIsNotPresent are the negative conditions."""
    not_enabled = MessageIsNotEnabled("a-message")
    assert not_enabled.is_met(_FakeConfig())
    assert not not_enabled.is_met(_FakeConfig(enabled={"a-message"}))

    not_present = OptionIsNotPresent("an-option")
    assert not_present.is_met(_FakeConfig())
    assert not not_present.is_met(_FakeConfig(options={"an-option"}))


def test_disable_message_solution() -> None:
    """DisableMessage adds the message to the 'disable' option."""
    config = _FakeConfig()
    DisableMessage("a-message").apply(config)
    assert config.is_message_disabled("a-message")
