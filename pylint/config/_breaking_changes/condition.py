# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod


class Condition(ABC):
    """Abstract base class for conditions that determine if a config is affected."""

    @abstractmethod
    def is_met(self, config: argparse.Namespace) -> bool:
        """Check if the condition is met for the given configuration."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable description of the condition."""


class MessageIsEnabled(Condition):
    """Condition: a message is explicitly enabled."""

    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: argparse.Namespace) -> bool:
        return config.is_message_enabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"{self.msgid_or_symbol} is enabled"


class MessageIsNotEnabled(Condition):
    """Condition: a message is not explicitly enabled."""

    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: argparse.Namespace) -> bool:
        return not config.is_message_enabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"{self.msgid_or_symbol} is not enabled"


class MessageIsDisabled(Condition):
    """Condition: a message is explicitly disabled."""

    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: argparse.Namespace) -> bool:
        return config.is_message_disabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"{self.msgid_or_symbol} is disabled"


class MessageIsNotDisabled(Condition):
    """Condition: a message is not explicitly disabled."""

    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def is_met(self, config: argparse.Namespace) -> bool:
        return not config.is_message_disabled(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"{self.msgid_or_symbol} is not disabled"


class ExtensionIsLoaded(Condition):
    """Condition: an extension is loaded."""

    def __init__(self, extension: str):
        self.extension = extension

    def is_met(self, config: argparse.Namespace) -> bool:
        return config.is_extension_loaded(self.extension)

    def __str__(self) -> str:
        return f"{self.extension} is loaded"


class ExtensionIsNotLoaded(Condition):
    """Condition: an extension is not loaded."""

    def __init__(self, extension: str):
        self.extension = extension

    def is_met(self, config: argparse.Namespace) -> bool:
        return not config.is_extension_loaded(self.extension)

    def __str__(self) -> str:
        return f"{self.extension} is not loaded"


class OptionIsPresent(Condition):
    """Condition: an option is present in configuration."""

    def __init__(self, option: str):
        self.option = option

    def is_met(self, config: argparse.Namespace) -> bool:
        return config.has_option(self.option)

    def __str__(self) -> str:
        return f"{self.option} is present in configuration"


class OptionIsNotPresent(Condition):
    """Condition: an option is not present in configuration."""

    def __init__(self, option: str):
        self.option = option

    def is_met(self, config: argparse.Namespace) -> bool:
        return not config.has_option(self.option)

    def __str__(self) -> str:
        return f"{self.option} is not present in configuration"


class AnyOptionIsPresent(Condition):
    """Condition: at least one of the given options is present."""

    def __init__(self, options: list[str]):
        self.options = options

    def is_met(self, config: argparse.Namespace) -> bool:
        return any(config.has_option(opt) for opt in self.options)

    def __str__(self) -> str:
        return f"At least one of {', '.join(self.options)} is present in configuration"
