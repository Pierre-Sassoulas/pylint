# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the 'pylint-config upgrade' command."""


import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from pylint import _run_pylint_config

FUNCTIONAL_DIRECTORIES = (Path(__file__).parent / "functional").iterdir()


@pytest.mark.parametrize(
    "directory", FUNCTIONAL_DIRECTORIES, ids=FUNCTIONAL_DIRECTORIES
)
def test_upgrade_config_functional(directory: Path) -> None:
    argv = [str(directory / ".pylintrc"), "-o", ".pylintrc_result"]
    with patch("sys.argv", ["pylint-config", "upgrade", *argv]):
        print(sys.argv)
        _run_pylint_config()
    assert directory is None
