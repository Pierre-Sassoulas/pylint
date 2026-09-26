# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pathlib import Path

from pylint.testutils._primer.primer_command import PrimerCommand
from pylint.testutils._primer.primer_compare_command import CompareCommand
from pylint.testutils._primer.primer_configuration import (
    get_argument_parser,
    get_packages_to_prime_from_json,
)
from pylint.testutils._primer.primer_prepare_command import PrepareCommand
from pylint.testutils._primer.primer_run_command import RunCommand

EXTENDED_PRIMER_SUBDIRECTORY = "extended_primer"
"""Where the extended primer writes its outputs, next to the shared clones.

GitHub owner names cannot contain an underscore, so this never clashes with a
clone directory.
"""


class Primer:
    """Main class to handle priming of packages."""

    def __init__(
        self,
        primer_directory: Path,
        json_path: Path,
        extended_json_path: Path | None = None,
    ) -> None:
        # Preparing arguments
        self.primer_directory = primer_directory
        self._argument_parser = get_argument_parser("Pylint Primer", with_batches=True)
        self._argument_parser.add_argument(
            "--extended",
            action="store_true",
            default=False,
            help="Use the extended list of packages, too big to run on every PR.",
        )

        # Storing arguments
        self.config = self._argument_parser.parse_args()
        if self.config.extended:
            if extended_json_path is None:
                self._argument_parser.error("no extended list of packages to prime")
            json_path = extended_json_path
            self.primer_directory = primer_directory / EXTENDED_PRIMER_SUBDIRECTORY
            self.primer_directory.mkdir(parents=True, exist_ok=True)

        self.packages = get_packages_to_prime_from_json(json_path)
        """All packages to prime."""

        if self.config.command == "prepare":
            command_class: type[PrimerCommand] = PrepareCommand
        elif self.config.command == "run":
            command_class = RunCommand
        elif self.config.command == "compare":
            command_class = CompareCommand
        # pylint: disable-next=possibly-used-before-assignment
        self.command = command_class(self.primer_directory, self.packages, self.config)

    def run(self) -> None:
        self.command.run()
