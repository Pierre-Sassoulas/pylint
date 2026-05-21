# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""The kinds of configuration breaking change pylint can have."""

from __future__ import annotations

from pylint.config._breaking_changes.base import BreakingChange, Intention
from pylint.config._breaking_changes.condition import (
    AnyOptionIsPresent,
    ExtensionIsLoaded,
    ExtensionIsNotLoaded,
    MessageIsDisabled,
    MessageIsEnabled,
    MessageIsNotDisabled,
    OptionIsPresent,
)
from pylint.config._breaking_changes.solution import (
    AddExtension,
    DoNothing,
    EnableMessage,
    ManualReview,
    RemoveExtension,
    RemoveFromDisable,
    RemoveFromEnable,
    RemoveOption,
    RenameOption,
)


class MessageMovedToExtension(BreakingChange):
    """A message moved out of the core into an optional extension."""

    def __init__(self, msgid_or_symbol: str, extension: str) -> None:
        super().__init__(
            description=(
                f"'{msgid_or_symbol}' was moved to the '{extension}' extension."
            ),
            conditions=[
                MessageIsEnabled(msgid_or_symbol),
                ExtensionIsNotLoaded(extension),
            ],
            solutions={
                Intention.KEEP: [AddExtension(extension)],
                Intention.USE_DEFAULT: [RemoveFromEnable(msgid_or_symbol)],
            },
        )


class ExtensionRemoved(BreakingChange):
    """An extension was removed and its message is now part of pylint."""

    def __init__(self, msgid_or_symbol: str, extension: str) -> None:
        super().__init__(
            description=(
                f"The '{extension}' extension was removed; its message "
                f"'{msgid_or_symbol}' is now part of pylint itself."
            ),
            conditions=[
                MessageIsNotDisabled(msgid_or_symbol),
                ExtensionIsLoaded(extension),
            ],
            solutions={
                Intention.FIX_CONF: [
                    RemoveExtension(extension),
                    EnableMessage(msgid_or_symbol),
                ],
            },
        )


class OptionRenamed(BreakingChange):
    """An option was renamed."""

    def __init__(self, old_name: str, new_name: str) -> None:
        super().__init__(
            description=f"The '{old_name}' option was renamed to '{new_name}'.",
            conditions=[OptionIsPresent(old_name)],
            solutions={Intention.FIX_CONF: [RenameOption(old_name, new_name)]},
        )


class OptionRemoved(BreakingChange):
    """An option was removed."""

    def __init__(self, option: str, reason: str) -> None:
        super().__init__(
            description=f"The '{option}' option was removed. {reason}",
            conditions=[OptionIsPresent(option)],
            solutions={Intention.FIX_CONF: [RemoveOption(option)]},
        )


class OptionBehaviorChanged(BreakingChange):
    """The behavior of one or more options changed without a config change."""

    def __init__(self, options: list[str], change_description: str) -> None:
        joined = ", ".join(f"'{option}'" for option in options)
        super().__init__(
            description=f"The behavior of {joined} changed. {change_description}",
            conditions=[AnyOptionIsPresent(options)],
            solutions={
                Intention.KEEP: [
                    ManualReview(
                        f"Review the value of {joined} and adjust it if needed."
                    )
                ],
                Intention.USE_DEFAULT: [DoNothing()],
            },
        )


class MessageMadeDisabledByDefault(BreakingChange):
    """A message that used to be enabled is now disabled by default."""

    def __init__(self, msgid_or_symbol: str) -> None:
        super().__init__(
            description=(
                f"'{msgid_or_symbol}' is now disabled by default; "
                "it used to be enabled by default."
            ),
            conditions=[MessageIsNotDisabled(msgid_or_symbol)],
            solutions={
                Intention.KEEP: [EnableMessage(msgid_or_symbol)],
                Intention.USE_DEFAULT: [DoNothing()],
            },
        )


class MessageMadeEnabledByDefault(BreakingChange):
    """A message that used to be disabled is now enabled by default."""

    def __init__(self, msgid_or_symbol: str) -> None:
        super().__init__(
            description=(
                f"'{msgid_or_symbol}' is now enabled by default; "
                "it used to be disabled by default."
            ),
            conditions=[MessageIsDisabled(msgid_or_symbol)],
            solutions={
                Intention.KEEP: [DoNothing()],
                Intention.USE_DEFAULT: [RemoveFromDisable(msgid_or_symbol)],
            },
        )
