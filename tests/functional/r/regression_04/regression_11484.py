"""Regression test for https://github.com/pylint-dev/pylint/issues/11484.

The functional ``Enum`` API called with tuples as separate arguments,
instead of a list of tuples, crashed.
"""

from enum import Enum

ResultKind = Enum("ResultKind", ("VAL_TRUE", 1), ("VAL_VAR", 2))
