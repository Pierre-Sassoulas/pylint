"""Repro attempt for the ASTSafetyError report.

Reported on macOS with Python 3.13. On Linux with 3.14 there is no
fatal, but ``black.parsing.InvalidInput`` now draws a
``no-name-in-module`` that deserves an issue of its own.
"""

from black import FileMode, format_str
from black.parsing import InvalidInput
