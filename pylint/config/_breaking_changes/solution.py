# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Solutions that resolve a configuration breaking change."""

from __future__ import annotations

from pylint.config._breaking_changes.base import ConfigView, Solution


class AddExtension(Solution):
    """Add an extension to the 'load-plugins' option."""

    def __init__(self, extension: str) -> None:
        self.extension = extension

    def apply(self, config: ConfigView) -> None:
        config.add_extension(self.extension)

    def __str__(self) -> str:
        return f"Add '{self.extension}' to the 'load-plugins' option"


class RemoveExtension(Solution):
    """Remove an extension from the 'load-plugins' option."""

    def __init__(self, extension: str) -> None:
        self.extension = extension

    def apply(self, config: ConfigView) -> None:
        config.remove_extension(self.extension)

    def __str__(self) -> str:
        return f"Remove '{self.extension}' from the 'load-plugins' option"


class EnableMessage(Solution):
    """Add a message to the 'enable' option."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self, config: ConfigView) -> None:
        config.enable_message(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"Add '{self.msgid_or_symbol}' to the 'enable' option"


class DisableMessage(Solution):
    """Add a message to the 'disable' option."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self, config: ConfigView) -> None:
        config.disable_message(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"Add '{self.msgid_or_symbol}' to the 'disable' option"


class RemoveFromEnable(Solution):
    """Remove a message from the 'enable' option."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self, config: ConfigView) -> None:
        config.remove_from_enable(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"Remove '{self.msgid_or_symbol}' from the 'enable' option"


class RemoveFromDisable(Solution):
    """Remove a message from the 'disable' option."""

    def __init__(self, msgid_or_symbol: str) -> None:
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self, config: ConfigView) -> None:
        config.remove_from_disable(self.msgid_or_symbol)

    def __str__(self) -> str:
        return f"Remove '{self.msgid_or_symbol}' from the 'disable' option"


class RemoveOption(Solution):
    """Remove an option from the configuration."""

    def __init__(self, option: str) -> None:
        self.option = option

    def apply(self, config: ConfigView) -> None:
        config.remove_option(self.option)

    def __str__(self) -> str:
        return f"Remove the '{self.option}' option from the configuration"


class RenameOption(Solution):
    """Rename an option, keeping its value."""

    def __init__(self, old_name: str, new_name: str) -> None:
        self.old_name = old_name
        self.new_name = new_name

    def apply(self, config: ConfigView) -> None:
        config.rename_option(self.old_name, self.new_name)

    def __str__(self) -> str:
        return f"Rename the '{self.old_name}' option to '{self.new_name}'"


class ManualReview(Solution):
    """A change that cannot be automated and needs the user's attention."""

    def __init__(self, instruction: str) -> None:
        self.instruction = instruction

    def apply(self, config: ConfigView) -> None:
        # Nothing can be done automatically: the user must act themselves.
        pass

    def __str__(self) -> str:
        return self.instruction


class DoNothing(Solution):
    """No configuration change is required."""

    def apply(self, config: ConfigView) -> None:
        pass

    def __str__(self) -> str:
        return "No action needed"
