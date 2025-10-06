# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Everything related to the 'pylint-config' command."""


from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.config._pylint_config.generate_command import handle_generate_command
from pylint.config._pylint_config.help_message import get_help
from pylint.config._pylint_config.upgrade_command import handle_upgrade_command

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


def _handle_pylint_config_commands(linter: PyLinter) -> int:
    """Handle whichever command is passed to 'pylint-config'."""
    if linter.config.config_subcommand == "generate":
        return handle_generate_command(linter)
    if linter.config.config_subcommand == "upgrade":
        return handle_upgrade_command(linter)

    print(get_help(linter._arg_parser))
    return 32
