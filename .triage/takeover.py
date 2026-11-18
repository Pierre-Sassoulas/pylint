"""When a pull request waiting on its author comes back into the to-do list.

A pull request whose next move is the author's (changes requested, red CI) is
left out of the priority list: there is nothing for a maintainer to do. Once
the author has been silent for ``TAKEOVER_DAYS``, or the PR carries the
"Needs take over" label, it needs a maintainer again (push the fix or close),
so it comes back, ranked above plain reviews when it is worth the time.

The author's last activity comes from ``author_activity.json``
(``author_activity_fetch.py``): last commit, or last comment or review by the
author. Bot comments and maintainer reviews do not count.
"""

from __future__ import annotations

import datetime
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FILE = HERE / "author_activity.json"
# Same order of magnitude as the 15 days after which AGENTS.md lets someone
# else take a claimed issue, doubled: a contributor with requested changes
# deserves more time than a bare "I'm on it".
TAKEOVER_DAYS = 30
TAKEOVER_LABEL = "Needs take over"

_DATA = json.loads(FILE.read_text()) if FILE.exists() else {}
_SNAPSHOT = datetime.date.fromisoformat(_DATA["snapshot"]) if "snapshot" in _DATA else datetime.date.today()


def last_activity(repo: str, number: int) -> str:
    return _DATA.get(repo, {}).get(str(number), "")


def silent_days(repo: str, number: int) -> int | None:
    """Days since the author last acted, or None when unknown."""
    date = last_activity(repo, number)
    if not date:
        return None
    return (_SNAPSHOT - datetime.date.fromisoformat(date)).days


def needs_takeover(repo: str, number: int, labels: list[str]) -> bool:
    if any(label.startswith(TAKEOVER_LABEL) for label in labels):
        return True
    days = silent_days(repo, number)
    return days is not None and days >= TAKEOVER_DAYS


def describe(repo: str, number: int, labels: list[str]) -> str:
    days = silent_days(repo, number)
    parts = []
    if any(label.startswith(TAKEOVER_LABEL) for label in labels):
        parts.append("labelled Needs take over")
    if days is not None:
        parts.append(f"author silent {days} days (last {last_activity(repo, number)})")
    return " · ".join(parts)
