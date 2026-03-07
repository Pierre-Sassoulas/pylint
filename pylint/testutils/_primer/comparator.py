# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import abc
import json
from collections.abc import Iterator
from pathlib import Path

from pylint.reporters.json_reporter import OldJsonExport
from pylint.testutils._primer.primer_command import (
    PackageData,
    PackageMessages,
)


class Comparator(abc.ABC):
    """Abstract base class for primer comparators."""

    missing_messages: PackageMessages
    new_messages: PackageMessages

    @abc.abstractmethod
    def __iter__(
        self,
    ) -> Iterator[tuple[str, PackageData, PackageData]]:
        """Yield (package, missing_messages, new_messages) for packages with
        changes.
        """


class PylintComparator(Comparator):
    """Compare two primer runs and compute missing/new messages per package."""

    def __init__(
        self,
        main_data: PackageMessages,
        pr_data: PackageMessages,
    ) -> None:
        self.missing_messages: PackageMessages = {}
        for package, data in main_data.items():
            package_missing_messages: list[OldJsonExport] = []
            for message in data["messages"]:
                try:
                    pr_data[package]["messages"].remove(message)
                except ValueError:
                    package_missing_messages.append(message)
            self.missing_messages[package] = PackageData(
                commit=pr_data[package]["commit"],
                messages=package_missing_messages,
            )
        self.new_messages = pr_data

    def __iter__(
        self,
    ) -> Iterator[tuple[str, PackageData, PackageData]]:
        for package, missing in self.missing_messages.items():
            new = self.new_messages[package]
            if not missing["messages"] and not new["messages"]:
                print(f"PRIMER: No changes in {package}.")
                continue
            yield package, missing, new

    @staticmethod
    def load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result
