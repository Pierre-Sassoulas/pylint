# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for issue #7585.

This test verifies that pylint does not enter an infinite loop when
the c-extension-no-member checker is activated with the --jobs 0 option.
"""

import os
import subprocess
import sys
import tempfile
import unittest

import pylint


class Issue7585TestCase(unittest.TestCase):
    """Test case for issue #7585."""

    def test_no_infinite_loop_with_c_extension_no_member(self):
        """Test that pylint does not enter an infinite loop with c-extension-no-member."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file that uses a C extension module
            test_file = os.path.join(tmpdir, "test_file.py")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(
                    """
import sys
# This should trigger c-extension-no-member warning
result = sys.non_existent_attribute
"""
                )

            # Create a pylint configuration file
            pylintrc = os.path.join(tmpdir, ".pylintrc")
            with open(pylintrc, "w", encoding="utf-8") as f:
                f.write(
                    """
[MESSAGES CONTROL]
enable=c-extension-no-member
disable=all
"""
                )

            # Run pylint with --jobs 0 and a timeout
            pylint_path = os.path.dirname(os.path.dirname(pylint.__file__))
            cmd = [
                sys.executable,
                "-m",
                "pylint",
                "--rcfile",
                pylintrc,
                "--jobs",
                "0",
                test_file,
            ]

            # Use a timeout to prevent the test from hanging if the bug is present
            try:
                result = subprocess.run(
                    cmd,
                    cwd=pylint_path,
                    timeout=10,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                # If we get here, pylint completed without hanging
                self.assertIn("c-extension-no-member", result.stdout)
            except subprocess.TimeoutExpired:
                self.fail("Pylint entered an infinite loop")
