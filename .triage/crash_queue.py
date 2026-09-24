"""Render `crash-queue.html` from `crash_queue_data.json`.

The JSON holds one row per open issue carrying the crash label: the verdict a
re-run produced, the exception and frame when it still crashes, and the library
version it was tested against. Editing the JSON and re-running this file is the
whole refresh loop -- there is no API to poll, because every verdict here comes
from actually running the snippet in `snippets/`.
"""

from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = json.loads((HERE / "crash_queue_data.json").read_text())
OUT = HERE / "crash-queue.html"

ENV = DATA["env"]
ISSUES = DATA["issues"]
URL = "https://github.com/pylint-dev/pylint/issues/{}"
PR_URL = "https://github.com/pylint-dev/pylint/pull/{}"

LANES = [
    (
        "repro",
        "Still crashes",
        "var(--crit)",
        "A fatal on current <code>main</code>. Four of the six already have a pull request; the other two are "
        "unclaimed and both are small.",
    ),
    (
        "hang",
        "Crashes no longer, hangs instead",
        "var(--warn)",
        "The exception is gone and nothing replaced it: no output, no completion. Worse for a user than the "
        "original crash, which at least ended.",
    ),
    (
        "gone",
        "No longer reproduces",
        "var(--good)",
        "The reporter's own snippet, run with their library installed at a current version, produces messages but "
        "no fatal. Worth a comment asking the reporter to confirm before closing -- most of these are library "
        "pairings, not pylint fixes.",
    ),
    (
        "blocked",
        "Out of reach from this machine",
        "var(--ink-faint)",
        "Needs an operating system, an interpreter, or a private package this run does not have. Not a judgement "
        "on whether the bug is real.",
    ),
]

CHIPS = {
    "repro": ("crashes", "crash"),
    "hang": ("hangs", "confirmed"),
    "gone": ("clean", "stale"),
    "blocked": ("not run", "unrepro"),
}


def row(issue: dict) -> str:
    chip_text, chip_class = CHIPS[issue["verdict"]]
    snippet = (
        f'<span class="lab">snippets/{issue["snippet"]}</span>'
        if issue["snippet"] and issue["snippet"].startswith("i")
        else (
            f'<span class="lab">{issue["snippet"]}</span>' if issue["snippet"] else ""
        )
    )
    tested = f'<span class="lab">{issue["tested"]}</span>' if issue["tested"] else ""
    pr = (
        f'<span class="repro na">fix open: '
        f'<a href="{PR_URL.format(issue["pr"])}">#{issue["pr"]}</a></span>'
        if issue["pr"]
        else ""
    )
    trace = ""
    if issue.get("exc"):
        trace = (
            f'<span class="trace"><span class="lbl">raises</span> {issue["exc"]}<br>'
            f'<span class="lbl">last frame</span> {issue["frame"]}</span>'
        )
    return (
        "<tr>"
        f'<td class="id"><a href="{URL.format(issue["n"])}">#{issue["n"]}</a>'
        f'<span class="date">{issue["family"]}</span></td>'
        f'<td class="what"><span class="t">{issue["title"]}</span>{snippet}</td>'
        f'<td class="verdict"><span class="chip {chip_class}">{chip_text}</span>{tested}{pr}</td>'
        f'<td class="finding">{issue["detail"]}{trace}</td>'
        "</tr>"
    )


body = []
for key, label, stripe, rubric in LANES:
    members = [i for i in ISSUES if i["verdict"] == key]
    members.sort(key=lambda i: i["n"])
    body.append(
        f'<section class="lane" data-lane="{key}">'
        f'<h2 style="--stripe: {stripe}">{label} <span class="count">{len(members)}</span></h2>'
        f'<p class="rubric">{rubric}</p>'
        '<div class="scroll"><table><thead><tr>'
        "<th>Issue</th><th>What it is</th><th>Verdict</th><th>What the re-run showed</th>"
        "</tr></thead><tbody>"
        + "".join(row(i) for i in members)
        + "</tbody></table></div></section>"
    )

counts = {key: sum(1 for i in ISSUES if i["verdict"] == key) for key, *_ in LANES}
page = (
    (HERE / "crash_queue_template.html")
    .read_text()
    .format(
        total=len(ISSUES),
        repro=counts["repro"],
        hang=counts["hang"],
        gone=counts["gone"],
        blocked=counts["blocked"],
        body="".join(body),
        **ENV,
    )
)
OUT.write_text(page)
print(f"wrote {OUT} -- {len(ISSUES)} issues")
for key, label, *_ in LANES:
    print(f"  {label:<38} {counts[key]}")
