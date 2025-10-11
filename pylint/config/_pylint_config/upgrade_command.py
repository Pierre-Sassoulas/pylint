# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Everything related to the 'pylint-config upgrade' command."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from pylint.config import find_default_config_files
from pylint.config._breaking_changes import BreakingChanges

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def handle_upgrade_command(_: PyLinter) -> int:
    config_path = next(find_default_config_files(), None)
    if not config_path or not config_path.exists():
        print("Error: No configuration file found to upgrade. Exiting", file=sys.stderr)
        return 1
    print(f"Upgrading configuration file: {config_path}")
    return 0


def check_upgrade_needed(linter: PyLinter) -> list[str]:
    for breaking_change in BreakingChanges("0.0.0"):
        if breaking_change.changes_are_required_in_config(linter.config):
            print(f"Breaking change detected: {breaking_change}")
        else:
            print(f"No breaking change for: {breaking_change}")


def emit_upgrade_warnings(linter: PyLinter) -> None:
    """Emit warnings if upgrade is needed."""
    warnings = check_upgrade_needed(linter)
    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
