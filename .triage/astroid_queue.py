"""Render astroid.html from astroid_queue_data.json (astroid_queue_fetch.py).

Every lane is computed from the data, so the page can no longer list a pull
request that was closed since it was written by hand. pr_queue.py imports the
ranking and the lanes from here for the astroid part of its To do now block.
"""

from __future__ import annotations

import datetime
import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OWNER = "Pierre-Sassoulas"
E = html.escape
KIND_NAMES = ("crash / perf", "bug", "false positive", "false negative", "enhancement", "other")
# Substrings looked for in the lowercased labels of the PR and of its linked
# issues, by rank. "Bug" yields to a false positive or negative, which is the
# more precise kind for an issue labelled with both.
KIND_KEYS = (("crash", "performance"), ("bug",), ("false positive",), ("false negative",), ("enhancement", "brain"))

# lane -> (title, stripe, rubric, next move)
LANES = {
    "backport": (
        "Backports",
        "var(--good)",
        "Opened by the backport bot: the fix is merged on main and ships in the next 4.3.x release once this is merged.",
        "Merge.",
    ),
    "merge": ("Approved and green", "var(--good)", "Nothing left to decide.", "Merge."),
    "review": (
        "Ready to review",
        "var(--accent)",
        "Contributor patch, green CI, no changes requested, not a draft.",
        "Review.",
    ),
    "approve": (
        "Approve the run",
        "var(--warn)",
        "The workflows wait for a maintainer's approval: there is nothing to review until they run.",
        "Approve the run, then review.",
    ),
    "ping": (
        "Yours, waiting on a reviewer",
        "var(--info)",
        "Your own pull requests out of draft: they need a second maintainer.",
        "Ask another maintainer for a review.",
    ),
    "red": (
        "CI red, no changes requested",
        "var(--dup)",
        "Failing checks. Tell a real failure from an unrelated breakage before nudging the author.",
        "Look at the failure, then nudge the author or rerun.",
    ),
    "author": (
        "Waiting on the author",
        "var(--ink-faint)",
        "Changes requested: nothing to do until the author answers.",
        "Wait for the author.",
    ),
    "draft": ("Draft", "var(--ink-faint)", "Not ready, by the author's own account.", "Nothing yet."),
}
LANE_ORDER = list(LANES)
CI_WORDS = {
    "green": "CI green",
    "failing": "CI red",
    "running": "CI running",
    "not-run": "CI never ran",
    "awaiting-approval": "CI held for approval",
}


def priority(p: dict) -> tuple:
    """Kind first, then High priority, then reactions on open linked issues, then most recent."""
    names = [name.lower() for name in p["labels"]]
    for linked in p["links"]:
        names.extend(name.lower() for name in linked["labels"])
    found = {
        rank
        for rank, keys in enumerate(KIND_KEYS)
        if any(key in name for key in keys for name in names)
    }
    if found & {2, 3}:
        found.discard(1)
    category = min(found, default=len(KIND_KEYS))
    high = any(name.startswith("high priority") for name in names)
    reactions = sum(linked["reactions"] for linked in p["links"] if linked["state"] == "open")
    return (category, not high, -reactions, "".join(chr(0x10FFFF - ord(c)) for c in p["updated"]))


def worth(p: dict) -> bool:
    """Worth a maintainer's time now: crash, bug, High priority or two reactions."""
    category, not_high, minus_reactions, _ = priority(p)
    return category <= 1 or not not_high or minus_reactions <= -2


def lane(p: dict) -> str:
    if p["a"] == "app/pylint-backport":
        return "backport"
    if p["draft"]:
        return "draft"
    if p["rd"] == "CHANGES_REQUESTED":
        return "author"
    if p["a"] == OWNER:
        return "ping"
    if p["ci"] == "awaiting-approval":
        return "approve"
    if p["ci"] == "failing":
        return "red"
    if p["rd"] == "APPROVED":
        return "merge"
    return "review"


def why(p: dict) -> str:
    category, not_high, minus_reactions, _ = priority(p)
    parts = [KIND_NAMES[category]]
    if not not_high:
        parts.append("High priority")
    if minus_reactions:
        refs = [
            linked["ref"].replace("pylint-dev/", "")
            for linked in p["links"]
            if linked["state"] == "open" and linked["reactions"]
        ]
        parts.append(f"{-minus_reactions} reaction{'s' * (minus_reactions < -1)} on {', '.join(refs)}")
    parts.append(CI_WORDS[p["ci"]])
    if p["rd"] == "APPROVED":
        parts.append("approved")
    elif p["rd"] == "CHANGES_REQUESTED":
        parts.append("changes requested")
    if p["milestone"]:
        parts.append(f"milestone {p['milestone']}")
    parts.append(f"{p['size']} lines")
    return " · ".join(parts)


def links_cell(p: dict) -> str:
    out = []
    for linked in p["links"]:
        repo, number = linked["ref"].split("#")
        name = "pylint" if repo.endswith("/pylint") else "astroid"
        url = f"https://github.com/{repo}/issues/{number}"
        closed = " (closed)" if linked["state"] != "open" else ""
        reactions = f" · {linked['reactions']} reactions" if linked["reactions"] else ""
        out.append(
            f'<a href="{url}">{name} #{number}</a>{closed}{reactions}<br>'
            f'<span style="color:var(--ink-soft)">{E(linked["title"][:90])}</span>'
        )
    return "<br>".join(out) or '<span style="color:var(--ink-faint)">no linked issue</span>'


def main() -> None:
    data = json.loads((HERE / "astroid_queue_data.json").read_text())
    prs = sorted(data["prs"], key=priority)
    members = {key: [p for p in prs if lane(p) == key] for key in LANE_ORDER}
    snapshot = datetime.date.fromisoformat(data["snapshot"]).strftime("%-d %B %Y")
    body = []
    for key in LANE_ORDER:
        if not members[key]:
            continue
        title, stripe, rubric, action = LANES[key]
        body.append(
            f'<section class="lane"><h2 style="--stripe: {stripe}">{E(title)} '
            f'<span class="count">{len(members[key])}</span></h2><p class="rubric">{rubric}</p>'
            '<div class="scroll"><table><thead><tr><th>PR</th><th>What</th><th>Why here</th>'
            "<th>Bears on</th><th>Next move</th></tr></thead><tbody>"
        )
        for p in members[key]:
            body.append(
                "<tr>"
                f'<td class="id"><a href="https://github.com/pylint-dev/astroid/pull/{p["n"]}">#{p["n"]}</a>'
                f'<span class="date">{E(p["a"])}</span>'
                f'<span class="date">{E(p["created"])} → {E(p["updated"])}</span></td>'
                f'<td class="what"><span class="t">{E(p["t"])}</span>'
                f'<span class="msg">{" · ".join(E(label) for label in p["labels"]) or "no label"}</span></td>'
                f'<td class="finding">{E(why(p))}</td>'
                f'<td class="finding">{links_cell(p)}</td>'
                f'<td class="action">{action}</td>'
                "</tr>"
            )
        body.append("</tbody></table></div></section>")
    tally = "".join(
        f'<div style="--stripe: {LANES[key][1]}"><div class="n">{len(members[key])}</div>'
        f'<div class="k">{E(LANES[key][0])}</div></div>'
        for key in LANE_ORDER
        if members[key]
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Astroid queue</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/triage.css">
<style>
  .lane {{ margin-top: 40px; }}
  .lane h2 {{ font-family: "IBM Plex Serif", Georgia, serif; font-size: 20px; font-weight: 600; margin: 0 0 4px; padding-left: 12px; border-left: 4px solid var(--stripe, var(--line)); }}
  .lane h2 .count {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 13px; color: var(--ink-faint); font-weight: 400; margin-left: 6px; }}
  .lane .rubric {{ margin: 0 0 14px 16px; font-size: 13.5px; color: var(--ink-soft); max-width: 80ch; }}
  td.what {{ width: 28%; }}
  table {{ min-width: 1000px; }}
</style>
</head>
<body>
<div class="wrap">
  <nav class="site-nav"><a href="index.html" class="home">Overview</a> <a href="pylint-issues.html">Pylint issues</a> <a href="astroid.html" aria-current="page">Astroid queue</a> <a href="pr-queue.html">Pull request queue</a> <a href="method.html">Method</a></nav>
  <header>
    <div class="eyebrow">pylint-dev/astroid &nbsp;·&nbsp; <b>{len(prs)} open pull requests</b> &nbsp;·&nbsp; {snapshot}</div>
    <h1>Astroid queue</h1>
    <p class="standfirst">Every open astroid pull request except dependency bumps, generated from the GitHub API on
    {snapshot}. Lanes come from the data (draft, changes requested, held run, CI, review); inside a lane the order is
    crash or performance, bug, false positive, false negative, enhancement, then High priority, then reactions on the
    astroid and pylint issues it bears on.</p>
  </header>
  <div class="tally">{tally}</div>
  {"".join(body)}
  <footer>Generated by <code>astroid_queue.py</code> from <code>astroid_queue_data.json</code>
  (<code>astroid_queue_fetch.py</code>).</footer>
</div>
</body>
</html>
"""
    out = HERE / "astroid.html"
    out.write_text(page)
    print(f"wrote {out} — {len(prs)} PRs: " + ", ".join(f"{k} {len(v)}" for k, v in members.items() if v))


if __name__ == "__main__":
    main()
