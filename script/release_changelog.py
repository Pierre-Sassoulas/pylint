# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Extract the changelog of a given version and render it as markdown.

This is used by the release automation to build the body of the GitHub
release (which GitHub renders as markdown) directly from the reStructuredText
``What's New`` documents, removing the manual copy-paste step that was a
recurring source of errors (see https://github.com/pylint-dev/pylint/issues/7362).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BASE_DIRECTORY = Path(__file__).parent.parent.absolute()
WHATSNEW_DIR = BASE_DIRECTORY / "doc" / "whatsnew"

# "What's new in Pylint 4.0.5?" delimits a version section.
VERSION_HEADER = re.compile(r"^What's new in Pylint (?P<version>\d+\.\d+\.\d+)\?\s*$")
# A line made only of underline characters, e.g. "-----" or "=====".
UNDERLINE = re.compile(r"^[=~\-^\"'#*+]+\s*$")
RELEASE_DATE = re.compile(r"^Release date:.*$")
# The redundant parenthetical RST issue link, e.g.
# "Closes #10743 (`#10743 <https://.../10743>`_)" -> "Closes #10743"
# (GitHub auto-links the bare "#10743").
PARENTHETICAL_ISSUE_LINK = re.compile(r"\s*\(`#\d+ <https://github\.com/[^>]+>`_\)")
# A generic RST hyperlink: `text <url>`_ -> [text](url)
RST_LINK = re.compile(r"`(?P<text>[^`<]+?) <(?P<url>[^>]+)>`_")
# RST inline literal ``code`` -> markdown `code`. Handled before single backticks.
DOUBLE_BACKTICK = re.compile(r"``(?P<code>[^`]+?)``")


def newsfile_for_version(version: str) -> Path:
    """Return the ``index.rst`` that contains ``version``'s changelog."""
    major, minor, _patch = version.split(".")
    return WHATSNEW_DIR / major / f"{major}.{minor}" / "index.rst"


def extract_section(text: str, version: str) -> str:
    """Return the raw RST lines of ``version``'s section, without its header."""
    lines = text.splitlines()
    start: int | None = None
    end = len(lines)
    for index, line in enumerate(lines):
        match = VERSION_HEADER.match(line)
        if not match:
            continue
        if match.group("version") == version:
            start = index
        elif start is not None:
            # Reached the next version's header: that's the end.
            end = index
            break
    if start is None:
        raise SystemExit(
            f"Could not find a 'What's new in Pylint {version}?' section in "
            f"{newsfile_for_version(version)}"
        )
    # Skip the header line, its underline and an optional "Release date:" line.
    body_start = start + 1
    while body_start < end and (
        UNDERLINE.match(lines[body_start])
        or RELEASE_DATE.match(lines[body_start])
        or not lines[body_start].strip()
    ):
        body_start += 1
    return "\n".join(lines[body_start:end]).strip()


def rst_to_markdown(section: str) -> str:
    """Convert the subset of RST used in the changelog to markdown."""
    lines = section.splitlines()
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        # A category header is a text line immediately followed by an underline
        # of at least the same length (e.g. "False Positives Fixed" + "-----").
        nxt = lines[index + 1] if index + 1 < len(lines) else ""
        stripped = line.strip()
        if stripped and UNDERLINE.match(nxt) and len(nxt.strip()) >= len(stripped):
            out.append(f"## {stripped}")
            index += 2
            continue
        out.append(_convert_inline(line))
        index += 1
    # Collapse the runs of blank lines that separate RST entries.
    markdown = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return markdown + "\n"


def _convert_inline(line: str) -> str:
    line = PARENTHETICAL_ISSUE_LINK.sub("", line)
    line = RST_LINK.sub(r"[\g<text>](\g<url>)", line)
    line = DOUBLE_BACKTICK.sub(r"`\g<code>`", line)
    return line


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Version to extract, e.g. 4.0.5")
    parser.add_argument(
        "--file",
        type=Path,
        default=None,
        help="Override the whatsnew file to read (defaults to the one matching "
        "the version).",
    )
    args = parser.parse_args(argv)

    newsfile = args.file or newsfile_for_version(args.version)
    if not newsfile.exists():
        raise SystemExit(f"Changelog file not found: {newsfile}")
    section = extract_section(newsfile.read_text(encoding="utf-8"), args.version)
    sys.stdout.write(rst_to_markdown(section))


if __name__ == "__main__":
    main()
