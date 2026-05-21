# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Base types for the configuration breaking-change data model.

Conditions and solutions are expressed against the ``ConfigView`` interface so
the data model stays decoupled from configuration-file parsing and writing.
"""

from __future__ import annotations

import enum
from abc import ABC, abstractmethod
from typing import Protocol


class Intention(enum.Enum):
    """What a user wants to do about a configuration breaking change."""

    KEEP = "Keep the same behavior"
    USE_DEFAULT = "Use the new default behavior"
    # A FIX_CONF change is unambiguous: it can always be automated.
    FIX_CONF = "Fix the configuration to become consistent again"


class ConfigView(Protocol):
    """Read and write interface over a single configuration file.

    Conditions query it and solutions mutate it. It is implemented by the
    configuration-upgrade command for real files, and by lightweight fakes in
    the tests.
    """

    def is_message_enabled(self, msgid_or_symbol: str) -> bool: ...

    def is_message_disabled(self, msgid_or_symbol: str) -> bool: ...

    def is_extension_loaded(self, extension: str) -> bool: ...

    def has_option(self, option: str) -> bool: ...

    def enable_message(self, msgid_or_symbol: str) -> None: ...

    def disable_message(self, msgid_or_symbol: str) -> None: ...

    def remove_from_enable(self, msgid_or_symbol: str) -> None: ...

    def remove_from_disable(self, msgid_or_symbol: str) -> None: ...

    def add_extension(self, extension: str) -> None: ...

    def remove_extension(self, extension: str) -> None: ...

    def remove_option(self, option: str) -> None: ...

    def rename_option(self, old_name: str, new_name: str) -> None: ...


class Condition(ABC):
    """A predicate over a configuration deciding whether a change applies."""

    @abstractmethod
    def is_met(self, config: ConfigView) -> bool:
        """Whether the condition holds for ``config``."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable description of the condition."""


class Solution(ABC):
    """A single action that resolves part of a breaking change."""

    @abstractmethod
    def apply(self, config: ConfigView) -> None:
        """Apply the action to ``config`` in place."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable description of the action."""


class BreakingChange:
    """A configuration breaking change, its conditions and its solutions.

    Subclasses only customize ``__init__`` to assemble the description,
    conditions and solutions for one kind of change.
    """

    def __init__(
        self,
        description: str,
        conditions: list[Condition],
        solutions: dict[Intention, list[Solution]],
    ) -> None:
        self.description = description
        self.conditions = conditions
        self.solutions = solutions

    def is_affected(self, config: ConfigView) -> bool:
        """Whether ``config`` is affected by this breaking change."""
        return all(condition.is_met(config) for condition in self.conditions)

    def apply_solution(self, config: ConfigView, intention: Intention) -> None:
        """Apply every solution registered for ``intention`` to ``config``."""
        for solution in self.solutions[intention]:
            solution.apply(config)


BreakingChangesDict = dict[str, list[BreakingChange]]
