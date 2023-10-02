# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Everything related to the 'pylint-config upgrade' command."""


from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.config._pylint_config.help_message import get_subparser_help

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


def handle_upgrade_command(linter: PyLinter) -> int:
    """Handle 'pylint-config upgrade'."""
    print(get_subparser_help(linter, "generate"))
    return 32
