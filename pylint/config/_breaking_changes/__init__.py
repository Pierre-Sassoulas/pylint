# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""List the breaking changes in configuration files and their solutions."""

__all__ = ["BreakingChanges"]

from pylint.config._breaking_changes.breaking_changes import (
    BreakingChanges,
)
