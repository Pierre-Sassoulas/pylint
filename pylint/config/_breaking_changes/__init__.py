# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Data model of the configuration breaking changes and their solutions.

This package is pure data and logic with no knowledge of configuration files.
The configuration-upgrade command pairs it with a concrete ``ConfigView``.
"""

from pylint.config._breaking_changes.base import (
    BreakingChange,
    Condition,
    ConfigView,
    Intention,
    Solution,
)
from pylint.config._breaking_changes.breaking_changes import (
    CONFIGURATION_BREAKING_CHANGES,
    BreakingChanges,
)

__all__ = [
    "CONFIGURATION_BREAKING_CHANGES",
    "BreakingChange",
    "BreakingChanges",
    "Condition",
    "ConfigView",
    "Intention",
    "Solution",
]
