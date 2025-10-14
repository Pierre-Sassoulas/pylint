# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse
from abc import ABC, abstractmethod

from pylint.config._breaking_changes.condition import (
    AnyOptionIsPresent,
    Condition,
    ExtensionIsLoaded,
    ExtensionIsNotLoaded,
    MessageIsDisabled,
    MessageIsEnabled,
    MessageIsNotDisabled,
    OptionIsPresent,
)
from pylint.config._breaking_changes.intention import Intention


class BreakingChange(ABC):
    """Abstract base class for breaking changes."""

    def __init__(
        self,
        description: str,
        conditions: list[Condition],
        solutions: dict[Intention, list[str]],
    ):
        self.description = description
        self.conditions = conditions
        self.solutions = solutions

    def is_affected(self, config: argparse.Namespace) -> bool:
        """Check if the configuration is affected by this breaking change."""
        # All conditions must be met for the config to be affected
        return all(condition.is_met(config) for condition in self.conditions)

    @abstractmethod
    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        """Apply the chosen solution to the configuration."""


class MessageMovedToExtension(BreakingChange):
    """Breaking change when a message is moved to an extension."""

    def __init__(
        self,
        msgid_or_symbol: str,
        extension: str,
    ):
        self.msgid_or_symbol = msgid_or_symbol
        self.extension = extension

        description = (
            f"{msgid_or_symbol} was moved to {extension}. "
            f"The message is enabled but the extension is not loaded."
        )

        conditions = [
            MessageIsEnabled(msgid_or_symbol),
            ExtensionIsNotLoaded(extension),
        ]

        solutions = {
            Intention.KEEP: [
                f"Add {extension} to 'load-plugins' option to keep using {msgid_or_symbol}"
            ],
            Intention.USE_DEFAULT: [
                f"Remove {msgid_or_symbol} from 'enable' or add to 'disable' option"
            ],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        if intention == Intention.KEEP:
            config.add_extension(self.extension)
        elif intention == Intention.USE_DEFAULT:
            config.remove_from_enable(self.msgid_or_symbol)


class ExtensionRemoved(BreakingChange):
    """Breaking change when an extension is removed."""

    def __init__(
        self,
        msgid_or_symbol: str,
        extension: str,
    ):
        self.msgid_or_symbol = msgid_or_symbol
        self.extension = extension

        description = (
            f"{extension} was removed. "
            f"The message {msgid_or_symbol} is no longer available from this extension."
        )

        conditions = [
            MessageIsNotDisabled(msgid_or_symbol),
            ExtensionIsLoaded(extension),
        ]

        solutions = {
            Intention.FIX_CONF: [
                f"Remove {extension} from 'load-plugins' option",
                f"Add {msgid_or_symbol} to 'enable' option if you want to keep checking for it",
            ],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        if intention == Intention.FIX_CONF:
            config.remove_extension(self.extension)
            config.enable_message(self.msgid_or_symbol)


class OptionRenamed(BreakingChange):
    """Breaking change when an option is renamed."""

    def __init__(
        self,
        old_name: str,
        new_name: str,
    ):
        self.old_name = old_name
        self.new_name = new_name

        description = f"Option {old_name} was renamed to {new_name}"

        conditions = [
            OptionIsPresent(old_name),
        ]

        solutions = {
            Intention.FIX_CONF: [f"Rename {old_name} to {new_name} in configuration"],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        if intention == Intention.FIX_CONF:
            config.rename_option(self.old_name, self.new_name)


class OptionRemoved(BreakingChange):
    """Breaking change when an option is removed."""

    def __init__(
        self,
        option: str,
        reason: str,
    ):
        self.option = option
        self.reason = reason

        description = f"Option {option} was removed. {reason}"

        conditions = [
            OptionIsPresent(option),
        ]

        solutions = {
            Intention.FIX_CONF: [f"Remove {option} from configuration"],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        if intention == Intention.FIX_CONF:
            config.remove_option(self.option)


class OptionBehaviorChanged(BreakingChange):
    """Breaking change when an option's behavior changes."""

    def __init__(
        self,
        options: list[str],
        change_description: str,
    ):
        self.options = options
        self.change_description = change_description

        options_str = ", ".join(options)
        description = (
            f"Behavior changed for options: {options_str}. {change_description}"
        )

        conditions = [
            AnyOptionIsPresent(options),
        ]

        solutions = {
            Intention.KEEP: [
                f"Review and adjust {', '.join(options)} to match your naming conventions"
            ],
            Intention.USE_DEFAULT: ["No action needed - use the new default behavior"],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        # This type of change typically requires manual review
        # No automatic fix can be applied
        pass


class MessageMadeDisabledByDefault(BreakingChange):
    """Breaking change when a message is disabled by default."""

    def __init__(
        self,
        msgid_or_symbol: str,
    ):
        self.msgid_or_symbol = msgid_or_symbol

        description = (
            f"{msgid_or_symbol} was disabled by default. "
            f"It was previously enabled by default."
        )

        conditions = [
            MessageIsNotDisabled(msgid_or_symbol),
        ]

        solutions = {
            Intention.KEEP: [
                f"Add {msgid_or_symbol} to 'enable' option to keep the old behavior"
            ],
            Intention.USE_DEFAULT: [
                "No action needed - the message will be disabled by default"
            ],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        if intention == Intention.KEEP:
            config.enable_message(self.msgid_or_symbol)


class MessageMadeEnabledByDefault(BreakingChange):
    """Breaking change when a message is enabled by default."""

    def __init__(
        self,
        msgid_or_symbol: str,
    ):
        self.msgid_or_symbol = msgid_or_symbol

        description = (
            f"{msgid_or_symbol} was enabled by default. "
            f"It was previously disabled by default."
        )

        conditions = [
            MessageIsDisabled(msgid_or_symbol),
        ]

        solutions = {
            Intention.KEEP: [
                f"Keep {msgid_or_symbol} in 'disable' option to maintain old behavior"
            ],
            Intention.USE_DEFAULT: [f"Remove {msgid_or_symbol} from 'disable' option"],
        }

        super().__init__(description, conditions, solutions)

    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        if intention == Intention.USE_DEFAULT:
            config.remove_from_disable(self.msgid_or_symbol)
