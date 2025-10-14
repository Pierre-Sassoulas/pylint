# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import textwrap
import typing

from pylint.config._breaking_changes.breaking_change import (
    ExtensionRemoved,
    MessageMovedToExtension,
    OptionBehaviorChanged,
    OptionRemoved,
    OptionRenamed,
)

if typing.TYPE_CHECKING:
    from pylint.config._breaking_changes.breaking_change import BreakingChange


CONFIGURATION_BREAKING_CHANGES: dict[str, list[BreakingChange]] = {
    "1.7.0": [
        OptionRemoved(
            option="no-space-check",
            reason="This option is no longer used and should be removed",
        ),

        OptionRemoved()
        (
            BreakingChange.OPTION_REMOVED,
            OptionInformation(
                option="files-output",
                description="This option is no longer used and should be removed",
            ),
            [Condition.OPTION_IS_PRESENT],
            {
                Intention.FIX_CONF: [Solution.REMOVE_OPTION],
            },
        ),
    ],
    "2.6.0": [
               OptionRemoved(
                   option="no-space-check",
                   reason="This option is no longer used and should be removed",
        ),
    ],
    "2.7.3": [
        OptionRenamed(
            old_name="extension-pkg-whitelist", new_name="extension-pkg-allow-list"
        ),
    ],
    "2.14.0": [
        MessageMovedToExtension(
            msgid_or_symbol="no-self-use", extension="pylint.extensions.no_self_use"
        ),
    ],
    "3.0.0": [
        ExtensionRemoved(
            msgid_or_symbol="compare-to-zero",
            extension="pylint.extensions.comparetozero",
        ),
        ExtensionRemoved(
            msgid_or_symbol="compare-to-empty-string",
            extension="pylint.extensions.emptystring",
        ),
    ],
    "4.0.0": [
        OptionRemoved(
            option="suggestion-mode",
            reason="This option is no longer used and should be removed",
        ),
        OptionBehaviorChanged(
            options=["const-rgx", "const-naming-style"],
            change_description=textwrap.dedent(
                """
                In 'invalid-name', module-level constants that are reassigned are now treated
                as variables and checked against ``--variable-rgx`` rather than ``--const-rgx``.
                Module-level lists, sets, and objects can pass against either regex.

                You may need to adjust this option to match your naming conventions.

                See the release notes for concrete examples:
                https://pylint.readthedocs.io/en/stable/whatsnew/4/4.0/index.html"""
            ),
        ),
    ],
}


class BreakingChanges:
    def __init__(self, upgraded_to: str) -> None:
        self.upgraded_to = (int(v) for v in upgraded_to.split("."))

    def __iter__(self) -> iter[BreakingChange]:
        for version, changes in CONFIGURATION_BREAKING_CHANGES.items():
            version_as_tuple = (int(v) for v in version.split("."))
            if version_as_tuple > self.upgraded_to:
                yield from [c for c in changes if c.is_affected()]
