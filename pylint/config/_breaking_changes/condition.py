# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Conditions that decide whether a configuration is affected by a change."""

from __future__ import annotations

from pylint.config._breaking_changes.base import Condition, ConfigView


class MessageIsEnabled(Condition):
    """The message is explicitly enabled."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: ConfigView) -> bool:
        return config.is_message_enabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"'{self.msgid_or_symbol}' is enabled"


class MessageIsNotEnabled(Condition):
    """The message is not explicitly enabled."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: ConfigView) -> bool:
        return not config.is_message_enabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"'{self.msgid_or_symbol}' is not enabled"


class MessageIsDisabled(Condition):
    """The message is explicitly disabled."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: ConfigView) -> bool:
        return config.is_message_disabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"'{self.msgid_or_symbol}' is disabled"


class MessageIsNotDisabled(Condition):
    """The message is not explicitly disabled."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: ConfigView) -> bool:
        return not config.is_message_disabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"'{self.msgid_or_symbol}' is not disabled"


class ExtensionIsLoaded(Condition):
    """The extension is loaded."""

    def __init__(self, extension: str) -> None:
        self.extension = extension

    def is_met(self, config: ConfigView) -> bool:
        return config.is_extension_loaded(self.extension)

    def __str__(self) -> str:
        return f"'{self.extension}' is loaded"


class ExtensionIsNotLoaded(Condition):
    """The extension is not loaded."""

    def __init__(self, extension: str) -> None:
        self.extension = extension

    def is_met(self, config: ConfigView) -> bool:
        return not config.is_extension_loaded(self.extension)

    def __str__(self) -> str:
        return f"'{self.extension}' is not loaded"


class OptionIsPresent(Condition):
    """The option is present in the configuration."""

    def __init__(self, option: str) -> None:
        self.option = option

    def is_met(self, config: ConfigView) -> bool:
        return config.has_option(self.option)

    def __str__(self) -> str:
        return f"'{self.option}' is present in the configuration"


class OptionIsNotPresent(Condition):
    """The option is not present in the configuration."""

    def __init__(self, option: str) -> None:
        self.option = option

    def is_met(self, config: ConfigView) -> bool:
        return not config.has_option(self.option)

    def __str__(self) -> str:
        return f"'{self.option}' is not present in the configuration"


class AnyOptionIsPresent(Condition):
    """At least one of the options is present in the configuration."""

    def __init__(self, options: list[str]) -> None:
        self.options = options

    def is_met(self, config: ConfigView) -> bool:
        return any(config.has_option(option) for option in self.options)

    def __str__(self) -> str:
        joined = ", ".join(f"'{option}'" for option in self.options)
        return f"at least one of {joined} is present in the configuration"
