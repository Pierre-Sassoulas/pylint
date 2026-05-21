# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Everything related to the 'pylint-config upgrade' command."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from pylint import __version__
from pylint.config import find_default_config_files
from pylint.config._breaking_changes import BreakingChanges
from pylint.config._breaking_changes.breaking_changes import _parse_version
from pylint.config._pylint_config.config_file import ConfigFile
from pylint.config._pylint_config.utils import (
    InvalidUserInput,
    should_retry_after_invalid_input,
)

if TYPE_CHECKING:
    from pylint.config._breaking_changes import BreakingChange, Intention
    from pylint.lint.pylinter import PyLinter


def _current_version() -> str:
    """Return the running pylint version as a clean 'X.Y.Z' string."""
    return ".".join(str(part) for part in _parse_version(__version__))


def _resolve_config_path(linter: PyLinter) -> Path | None:
    """Return the configuration file to upgrade, given or auto-discovered."""
    given = linter.config.config_path
    if given:
        return Path(given)
    return next(find_default_config_files(), None)


@should_retry_after_invalid_input
def _prompt_intention(change: BreakingChange) -> Intention:
    """Ask the user which intention to apply for an ambiguous change."""
    intentions = list(change.solutions)
    for index, intention in enumerate(intentions, start=1):
        actions = "; ".join(str(solution) for solution in change.solutions[intention])
        print(f"  {index}) {intention.value}: {actions}")
    # pylint: disable-next=bad-builtin
    answer = input(f"Choose how to proceed (1-{len(intentions)}): ").strip()
    choices = {str(i) for i in range(1, len(intentions) + 1)}
    if answer not in choices:
        raise InvalidUserInput(", ".join(sorted(choices)), answer)
    return intentions[int(answer) - 1]


def _resolve_intention(
    change: BreakingChange, *, interactive: bool
) -> Intention | None:
    """Return the intention to apply, prompting only for ambiguous changes."""
    intentions = list(change.solutions)
    if len(intentions) == 1:
        return intentions[0]
    if not interactive:
        return None
    return _prompt_intention(change)


def _apply_changes(
    config: ConfigFile,
    changes: list[tuple[str, BreakingChange]],
    *,
    interactive: bool,
) -> tuple[int, int]:
    """Apply or skip every change and return the (applied, skipped) counts."""
    applied = 0
    skipped = 0
    for version, change in changes:
        print(f"\n[{version}] {change.description}")
        intention = _resolve_intention(change, interactive=interactive)
        if intention is None:
            skipped += 1
            print("  Skipped: re-run without --non-interactive to choose.")
            continue
        change.apply_solution(config, intention)
        applied += 1
        for solution in change.solutions[intention]:
            print(f"  Applied: {solution}")
    return applied, skipped


def handle_upgrade_command(linter: PyLinter) -> int:
    """Handle the 'pylint-config upgrade' command."""
    config_path = _resolve_config_path(linter)
    if config_path is None or not config_path.is_file():
        print("No configuration file found to upgrade.", file=sys.stderr)
        return 32

    config = ConfigFile.from_path(config_path)
    if config.migrated_from_ini:
        print(
            f"'{config_path}' is an ini file; its pylint options are migrated "
            f"to '{config.target}' (its comments are not carried over)."
        )

    marker = config.get_upgraded_to()
    if marker is not None and marker.strip().lower() == "latest":
        print(f"'{config_path}' is pinned to the latest defaults; nothing to do.")
        return 0

    changes = list(BreakingChanges(marker or "0.0.0").applicable(config))
    if not changes:
        print(f"'{config_path}' is already up to date.")
        config.set_upgraded_to(_current_version())
        config.save()
        return 0

    interactive = not linter.config.non_interactive
    applied, skipped = _apply_changes(config, changes, interactive=interactive)
    if skipped == 0:
        config.set_upgraded_to(_current_version())
    written = config.save()
    print(f"\nApplied {applied} change(s), {skipped} left to review.")
    print(f"Wrote '{written}'.")
    return 0
