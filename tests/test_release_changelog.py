# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the ``script/release_changelog.py`` release helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "script" / "release_changelog.py"
_spec = importlib.util.spec_from_file_location("release_changelog", SCRIPT)
assert _spec and _spec.loader
release_changelog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release_changelog)


SAMPLE = """
***************************
 What's New in Pylint 4.0
***************************

:Release:4.0
:Date: 2025-10-12

What's new in Pylint 4.0.5?
---------------------------
Release date: 2026-02-20


False Positives Fixed
---------------------

- Fix a false positive for ``invalid-name``.

  Closes #10790 (`#10790 <https://github.com/pylint-dev/pylint/issues/10790>`_)

Other Bug Fixes
---------------

- See the `astroid changelog <https://example.com/changelog>`_ for details.

  Closes #10801 (`#10801 <https://github.com/pylint-dev/pylint/issues/10801>`_)



What's new in Pylint 4.0.4?
---------------------------
Release date: 2025-11-30


Other Bug Fixes
---------------

- Older fix, should not appear.

  Closes #1 (`#1 <https://github.com/pylint-dev/pylint/issues/1>`_)
"""


def test_extract_section_isolates_version() -> None:
    section = release_changelog.extract_section(SAMPLE, "4.0.5")
    assert "invalid-name" in section
    assert "Older fix" not in section
    # The version header, underline and release date are stripped.
    assert "What's new in Pylint 4.0.5?" not in section
    assert "Release date" not in section


def test_extract_section_missing_version() -> None:
    with pytest.raises(SystemExit):
        release_changelog.extract_section(SAMPLE, "9.9.9")


def test_rst_to_markdown_conversion() -> None:
    markdown = release_changelog.rst_to_markdown(
        release_changelog.extract_section(SAMPLE, "4.0.5")
    )
    # Category underlines become markdown headers.
    assert "## False Positives Fixed" in markdown
    assert "## Other Bug Fixes" in markdown
    # Double backticks become single backticks.
    assert "`invalid-name`" in markdown
    assert "``invalid-name``" not in markdown
    # The redundant parenthetical issue link is dropped, the bare ref kept.
    assert "Closes #10790" in markdown
    assert "<https://github.com/pylint-dev/pylint/issues/10790>" not in markdown
    # Generic RST links become markdown links.
    assert "[astroid changelog](https://example.com/changelog)" in markdown


def test_newsfile_for_version() -> None:
    assert release_changelog.newsfile_for_version("4.1.0").parts[-3:] == (
        "4",
        "4.1",
        "index.rst",
    )
