# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt


from __future__ import annotations

import argparse
import enum
from abc import ABC, abstractmethod


class Intention(enum.Enum):
    KEEP = "Keep the same behavior"
    USE_DEFAULT = "Use the new default behavior"
    # This could/should always be automated
    FIX_CONF = "Fix the configuration to become consistent again"


class Condition(ABC):
    """Abstract base class for conditions that determine if a config is affected."""

    @abstractmethod
    def is_met(self, config: argparse.Namespace) -> bool:
        """Check if the condition is met for the given configuration."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable description of the condition."""


class Solution(ABC):
    """Abstract base class for solution."""

    @abstractmethod
    def apply(self) -> bool:
        """Apply the solution."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a human-readable description of the condition."""


class BreakingChange(ABC):
    """Abstract base class for breaking changes."""

    def __init__(
        self,
        description: str,
        conditions: list[Condition],
        solutions: dict[Intention, list[Solution]],
    ):
        self.description = description
        self.conditions = conditions
        self.solutions = solutions

    def is_affected(self, config: argparse.Namespace) -> bool:
        """Check if the configuration is affected by this breaking change."""
        return all(condition.is_met(config) for condition in self.conditions)

    @abstractmethod
    def apply_solution(self, config: argparse.Namespace, intention: Intention) -> None:
        """Apply the chosen solution to the configuration."""
        for solution in self.solutions[intention]:
            pass  # Implement specific solution application logic in subclasses


BreakingChangesDict = dict[str, list[BreakingChange]]
