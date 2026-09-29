# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import abc
import argparse
from pathlib import Path
from typing import TypedDict

from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer import PackageToLint


class PackageData(TypedDict):
    commit: str
    messages: list[JSONMessage]


PackageMessages = dict[str, PackageData]


class PrimerCommand:
    """Generic primer action with required arguments."""

    def __init__(
        self,
        primer_directory: Path,
        packages: dict[str, PackageToLint],
        config: argparse.Namespace,
    ) -> None:
        self.primer_directory = primer_directory
        self.packages = packages
        self.config = config

    def packages_in_batch(self) -> list[tuple[str, PackageToLint]]:
        """The packages of the batch given by --batches and --batchIdx.

        The longest packages to lint are handed out first, each to the batch that
        has the least to lint so far, so that the batches take about as long.
        Between batches with as much to lint, the one with fewer packages wins, so
        packages without a ``lint_time`` are spread too.
        """
        packages = list(self.packages.items())
        if self.config.batches is None:
            return packages
        # (seconds to lint, number of packages) of each batch
        loads = [(0, 0)] * self.config.batches
        batch_of: dict[str, int] = {}
        for name, data in sorted(packages, key=lambda p: (-p[1].lint_time, p[0])):
            batch = loads.index(min(loads))
            batch_of[name] = batch
            seconds, count = loads[batch]
            loads[batch] = (seconds + data.lint_time, count + 1)
        return [p for p in packages if batch_of[p[0]] == self.config.batchIdx]

    @abc.abstractmethod
    def run(self) -> None:
        pass
