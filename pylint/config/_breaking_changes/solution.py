# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt


from pylint.config._breaking_changes.typing import Solution


class AddExtension(Solution):
    def __init__(self, extension: str):
        self.extension = extension

    def apply(self) -> None:
        raise NotImplementedError


class RemoveExtension(Solution):
    def __init__(self, extension: str):
        self.extension = extension

    def apply(self) -> None:
        raise NotImplementedError


class EnableMessage(Solution):
    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self) -> None:
        raise NotImplementedError


class DisableMessage(Solution):
    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self) -> None:
        raise NotImplementedError


class RemoveMessageDisable(Solution):
    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self) -> None:
        raise NotImplementedError


class RemoveMessageEnable(Solution):
    def __init__(self, msgid_or_symbol: str):
        self.msgid_or_symbol = msgid_or_symbol

    def apply(self) -> None:
        raise NotImplementedError


class RemoveOption(Solution):
    def __init__(self, option: str):
        self.option = option

    def apply(self) -> None:
        raise NotImplementedError


class RenameOption(Solution):
    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name

    def apply(self) -> None:
        raise NotImplementedError
