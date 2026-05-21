# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""The catalog of configuration breaking changes, indexed by pylint version."""

from __future__ import annotations

import textwrap
from collections.abc import Iterator

from pylint.config._breaking_changes.base import (
    BreakingChange,
    BreakingChangesDict,
    ConfigView,
)
from pylint.config._breaking_changes.breaking_change import (
    ExtensionRemoved,
    MessageMovedToExtension,
    OptionBehaviorChanged,
    OptionRemoved,
    OptionRenamed,
)

CONFIGURATION_BREAKING_CHANGES: BreakingChangesDict = {
    "1.7.0": [
        OptionRemoved(
            "files-output",
            "This option is no longer used and should be removed.",
        ),
    ],
    "2.6.0": [
        OptionRemoved(
            "no-space-check",
            "This option is no longer used and should be removed.",
        ),
    ],
    "2.7.3": [
        OptionRenamed("extension-pkg-whitelist", "extension-pkg-allow-list"),
    ],
    "2.14.0": [
        MessageMovedToExtension("no-self-use", "pylint.extensions.no_self_use"),
    ],
    "3.0.0": [
        ExtensionRemoved("compare-to-zero", "pylint.extensions.comparetozero"),
        ExtensionRemoved("compare-to-empty-string", "pylint.extensions.emptystring"),
    ],
    "4.0.0": [
        OptionRemoved(
            "suggestion-mode",
            "This option is no longer used and should be removed.",
        ),
        OptionBehaviorChanged(
            ["const-rgx", "const-naming-style"],
            textwrap.dedent("""\
                In 'invalid-name', module-level constants that are reassigned
                are now treated as variables and checked against
                ``--variable-rgx`` rather than ``--const-rgx``. Module-level
                lists, sets and objects can pass against either regex. See the
                release notes for concrete examples:
                https://pylint.readthedocs.io/en/stable/whatsnew/4/4.0/index.html"""),
        ),
    ],
}


def _parse_version(version: str) -> tuple[int, int, int]:
    """Parse 'X.Y.Z' into a comparable triple, ignoring any pre-release suffix."""
    numbers: list[int] = []
    for chunk in version.split("."):
        digits = ""
        for character in chunk:
            if not character.isdigit():
                break
            digits += character
        numbers.append(int(digits) if digits else 0)
    numbers += [0, 0, 0]
    return numbers[0], numbers[1], numbers[2]


class BreakingChanges:
    """The breaking changes a configuration still needs to catch up with."""

    def __init__(self, upgraded_to: str = "0.0.0") -> None:
        self._is_latest = upgraded_to.strip().lower() == "latest"
        self._upgraded_to = _parse_version(upgraded_to)

    def __iter__(self) -> Iterator[tuple[str, BreakingChange]]:
        """Yield every ``(version, change)`` newer than ``upgraded_to``."""
        if self._is_latest:
            return
        for version, changes in CONFIGURATION_BREAKING_CHANGES.items():
            if _parse_version(version) > self._upgraded_to:
                for change in changes:
                    yield version, change

    def applicable(self, config: ConfigView) -> Iterator[tuple[str, BreakingChange]]:
        """Yield the newer ``(version, change)`` pairs that affect ``config``."""
        for version, change in self:
            if change.is_affected(config):
                yield version, change
