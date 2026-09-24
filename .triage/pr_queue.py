"""Render `pr-queue.html` from `pr_queue_data.json`.

The JSON holds only what the GitHub API said on the snapshot date: pull request
metadata, check-run outcomes, reviews, and the linked issues with their labels.
The lane each pull request sits in, and the two sentences next to it, are the
triage judgement and live in `V` below.

Refresh the JSON with `pr_queue_fetch.sh`, then re-run this file.
"""

from __future__ import annotations

import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = json.loads((HERE / "pr_queue_data.json").read_text())
OUT = HERE / "pr-queue.html"

rows = {r["n"]: r for r in DATA["prs"]}
issues = {i["number"]: i for i in DATA["issues"]}

# lane key -> (label, stripe var, one-line rubric)
LANES = {
    "merge": (
        "Merge lane",
        "var(--good)",
        "Reviewed and green, or one green run away. Nothing left to decide.",
    ),
    "review": (
        "Review now",
        "var(--accent)",
        "Full CI green, no maintainer has looked, and the issue behind it is still open.",
    ),
    "approve": (
        "Approve the run",
        "var(--warn)",
        "Held in <code>action_required</code>: the test matrix has never run, so there is nothing to review yet. "
        "One click each.",
    ),
    "retrigger": (
        "Retrigger CI",
        "var(--warn)",
        "No test workflow at all — the queued run expired before anyone approved it. Needs a push or a "
        "close/reopen, not a click.",
    ),
    "author": (
        "Author's move",
        "var(--ink-faint)",
        "Red CI or requested changes. Waiting on the contributor, not on you.",
    ),
    "decide": (
        "Decide first",
        "var(--dup)",
        "The code is not the blocker — the behaviour it introduces has never been agreed.",
    ),
    "stale": (
        "Stale / take over",
        "var(--ink-faint)",
        "Author gone for a year or more. Take the branch over or close it.",
    ),
}

# n: (lane, verdict-chip-text, chip-class, finding, action)
V = {
    # ---- merge lane -------------------------------------------------------
    11172: (
        "merge",
        "ready",
        "stale",
        "48/48 green, 20 lines, and <b>no maintainer has reviewed it in two months</b>. Second PR from a "
        "contributor whose other one is already in the round-trip.",
        "Cheapest merge left in the queue. Read it and land it.",
    ),
    # ---- review now -------------------------------------------------------
    11002: (
        "review",
        "ready",
        "stale",
        "44/44 green, zero reviews since May. Fixes a false negative filed as a good-first-issue; 181 lines is "
        "mostly tests.",
        "Review. Four months of silence on a green PR is how contributors are lost.",
    ),
    10507: (
        "review",
        "ready",
        "stale",
        "44/44 green, zero reviews, untouched since September 2025. Widens <code>invalid-envvar-default</code> to "
        "<code>os.environ.get</code>.",
        "Review or close with a reason. A year of silence on green CI is the worst of both.",
    ),
    11409: (
        "review",
        "ready",
        "confirmed",
        "48/48 green after you released the run on 23 September, and the primer reports no effect. 45 lines, "
        "<code>not-callable</code> on subscripted classes.",
        "Review. The author already rewrote a corrupted <code>typecheck.py</code> once, so check the diff is "
        "really 45 lines.",
    ),
    # ---- approve the workflow run ----------------------------------------
    11396: (
        "approve",
        "held",
        "confirmed",
        "50 lines. Stops <code>too-many-try-statements</code> counting a <code>pass</code> that Python's grammar "
        "requires.",
        "Approve the run. Small, and the issue has a clear accepted shape.",
    ),
    11398: (
        "approve",
        "held",
        "confirmed",
        "23 lines — the smallest held PR. False positive open since 2023.",
        "Approve the run, review the same day.",
    ),
    11411: (
        "approve",
        "held",
        "crash",
        "89 lines, and <b>the only held pull request that also conflicts with main</b>.",
        "Ask for a rebase first; approving a run on a conflicting head wastes the runners.",
    ),
    11416: (
        "approve",
        "held",
        "confirmed",
        "51 lines, <code>no-member</code> on an annotated enum value. Second PR from this contributor this month.",
        "Approve the run.",
    ),
    11417: (
        "approve",
        "held",
        "feature",
        "36 lines, but it runs the For and With checkers over their async forms — every async body in "
        "the world becomes newly checkable.",
        "Approve the run <b>and</b> require a primer run. This is the one held PR that can move "
        "real-world message counts.",
    ),
    # ---- retrigger --------------------------------------------------------
    11377: (
        "retrigger",
        "no ci",
        "unrepro",
        "15 lines, the smallest open PR here, and it has sat since 3 September with no test workflow at all.",
        "Push the button that starts CI, then review — it should be a ten-minute read.",
    ),
    11376: (
        "retrigger",
        "mis-linked",
        "duplicate",
        "<b>Links an issue closed as completed in June 2024</b>, and the titles do not match: the PR is about "
        "<code>invalid-name</code> parameter kinds, the issue about <code>duplicate-argument-name</code>.",
        "Ask which behaviour is actually being fixed before spending CI on it.",
    ),
    11308: (
        "retrigger",
        "no ci",
        "confirmed",
        "31 lines, stdin line endings on Windows. Open since 19 August with no run and no comment.",
        "Retrigger, then review. Nobody has said a word to this contributor.",
    ),
    11230: (
        "retrigger",
        "no ci",
        "confirmed",
        "36 lines, deterministic recursive discovery. Touches the same nondeterminism you chased in the primer "
        "file-order work.",
        "Retrigger, then read it against the known ordering issue.",
    ),
    11233: (
        "retrigger",
        "no ci",
        "confirmed",
        "313 lines against a duplicate-code false positive. You reviewed it once in August; CI has never run.",
        "Retrigger before the next review round, otherwise you are reading untested code.",
    ),
    11190: (
        "retrigger",
        "no ci",
        "confirmed",
        "39 lines, <code>superfluous-parens</code> false negative. Author's last comment is a month old and "
        "unanswered.",
        "Retrigger and answer.",
    ),
    11111: (
        "retrigger",
        "no ci",
        "crash",
        "23 lines against a crash on a non-UTF-8 bytes format string. Carries <em>Blocked</em>, but the "
        "blocker is not recorded on the PR.",
        "Retrigger, and write down what it is blocked on — nobody else can tell.",
    ),
    10904: (
        "retrigger",
        "no ci",
        "feature",
        "110 lines adding a <code>:pylint:</code> Sphinx role. <b>Overlaps your own doc-linking series</b> — same "
        "target, different mechanism.",
        "Decide which mechanism wins before reviewing. Yours is further along; say so on the PR either way.",
    ),
    10950: (
        "retrigger",
        "no ci",
        "confirmed",
        "61 lines protecting versioned functional-test output from <code>--update-functional-output</code>. Small "
        "and squarely a maintainer concern.",
        "Retrigger and review — this is test-harness hygiene you benefit from directly.",
    ),
    10961: (
        "retrigger",
        "no ci",
        "feature",
        "162 lines adding pytest-remaster to the functional suite. No review, no CI, no comment since April.",
        "Decide whether a new test dependency is wanted at all before retriggering.",
    ),
    # ---- author's move ----------------------------------------------------
    11410: (
        "author",
        "primer red",
        "confirmed",
        "Released on 23 September: tests green, but <b>the primer adds about 80 messages across 8 packages</b>, "
        "mostly <code>no-member</code>, and patch coverage is 75%.",
        "Point the author at the primer comment. Stub-driven inference is leaking into code that has no stub.",
    ),
    10570: (
        "author",
        "yours in flight",
        "stale",
        "The exhausted-iterator checker you took over. Lives on the contributor's fork; 13 reviews deep.",
        "Yours to land, not a queue item.",
    ),
    11223: (
        "author",
        "waiting",
        "confirmed",
        "50/50 green and <em>High priority</em>, but three review rounds deep and the author's last word was a "
        "month ago.",
        "Ping once. If it stays quiet, take the branch over — the bug is worth it.",
    ),
    11393: (
        "author",
        "waiting",
        "confirmed",
        "12 lines of test coverage; one check red; author replied today.",
        "Short round-trip, keep it moving.",
    ),
    11370: (
        "author",
        "waiting",
        "confirmed",
        "One red check. Reviewed once by a maintainer, no follow-up from the author since August.",
        "Ping.",
    ),
    11215: (
        "author",
        "waiting",
        "confirmed",
        "One red check, changes requested, backport label already set.",
        "Waiting on the author.",
    ),
    11217: (
        "author",
        "waiting",
        "confirmed",
        "One red check, <em>Waiting on author</em>, and the issue needs an astroid update as well.",
        "Waiting on two things; say which one blocks first.",
    ),
    11171: (
        "author",
        "waiting",
        "confirmed",
        "49/49 green but changes requested and untouched since mid-July.",
        "Ping — green CI with an open request is easy to forget.",
    ),
    11205: (
        "author",
        "wip",
        "feature",
        "609 lines over 41 files, marked <em>Work in progress</em> by the author, conflicting, and holding a "
        "queued run.",
        "Leave it. Do not approve the run while it conflicts.",
    ),
    11278: (
        "author",
        "draft",
        "crash",
        "Draft, green, fixes a pyreverse crash. Changes requested in August, no reply.",
        "Ping once; a crash fix should not sit in draft.",
    ),
    11241: (
        "author",
        "waiting",
        "confirmed",
        "Conflicting, no CI, four reviews deep. Author replied end of August.",
        "Needs a rebase from the author before anything else.",
    ),
    11255: (
        "author",
        "waiting",
        "confirmed",
        "Changes requested, no CI run, author's last reply in mid-August.",
        "Waiting on the author.",
    ),
    11132: (
        "author",
        "waiting",
        "confirmed",
        "<em>Waiting on author</em> since July, backport label set, no CI.",
        "Waiting on the author.",
    ),
    11011: (
        "author",
        "waiting",
        "confirmed",
        "Eight red checks and 27 recorded reviews. A real performance idea buried in a stalled review.",
        "Either take the idea over on your own branch or close it — 27 reviews is past the useful point.",
    ),
    11087: (
        "author",
        "approved, red",
        "confirmed",
        "<b>Approved, but ten checks are red</b> — the approval predates months of drift on main.",
        "Rebase it yourself and merge, or drop the approval. Approved-and-red is the worst state in the queue.",
    ),
    11177: (
        "author",
        "waiting",
        "feature",
        "Optional pytest-random-order for isolation hunting; one red check, one maintainer review.",
        "Low stakes, decide yes or no rather than letting it age.",
    ),
    11194: (
        "author",
        "waiting",
        "feature",
        "636 lines adding a whole new docparams message, conflicting, three red checks, zero reviews.",
        "Say up front whether a new W9022 is wanted; do not read 636 lines first.",
    ),
    10749: (
        "author",
        "waiting",
        "feature",
        "891 lines over 17 files for a type-annotations checker. Green, changes requested, silent since June.",
        "Too big to land as-is. Ask for a split or close it.",
    ),
    10903: (
        "author",
        "waiting",
        "confirmed",
        "TOML boolean handling for <code>store_true</code> options; two red checks, <em>Waiting on "
        "author</em> and <em>Needs take over</em> both set.",
        "Small enough to take over — it is a real configuration bug.",
    ),
    10953: (
        "author",
        "waiting",
        "confirmed",
        "One red check, no reviews, author's last word in April.",
        "Pairs with 10950 and 10961 from the same contributor — handle the three together.",
    ),
    # ---- decide first -----------------------------------------------------
    10600: (
        "decide",
        "needs decision",
        "feature",
        "A maintainer's own PR for a new CodeStyle check, one red check, <em>Needs decision</em> since 2025.",
        "This is a maintainer-to-maintainer decision, not a review. Settle it.",
    ),
    10658: (
        "decide",
        "needs decision",
        "feature",
        "Six red checks; the issue carries <em>Needs decision</em>. Overlaps 10962 exactly.",
        "Decide the <code>len()</code>-versus-zero question once and close whichever PR loses.",
    ),
    10962: (
        "decide",
        "needs decision",
        "feature",
        "Eleven red checks, marked <em>Blocked</em>, targeting the same issue as 10658.",
        "Same decision as 10658. Two contributors are waiting on one call.",
    ),
    10793: (
        "decide",
        "needs decision",
        "feature",
        "Eight red checks, no reviews, <em>Needs decision</em> on the issue since 2025.",
        "Decide whether the message is wanted before anyone rebases it.",
    ),
    10759: (
        "decide",
        "blocked",
        "feature",
        "SARIF reporter, 16 reviews, one red check, <em>Blocked</em>. The author is still responsive.",
        "The blocker needs naming. Sixteen rounds without one is a process failure, not the author's.",
    ),
    10619: (
        "decide",
        "wip",
        "feature",
        "A maintainer's own WIP draft for a default message set; the issue needs a specification first.",
        "Specification before code. Related to your own preset work — keep them in one place.",
    ),
    9967: (
        "decide",
        "needs decision",
        "feature",
        "Source-roots fallback, conflicting, no CI, no reviews; the issue carries <em>Needs decision</em>.",
        "Decide the fallback semantics, then ask for a rebase — not the other way round.",
    ),
    # ---- stale ------------------------------------------------------------
    11277: (
        "stale",
        "close?",
        "duplicate",
        "Draft with no CI and no comment; <b>the issue it closes was closed as a duplicate today</b>.",
        "Close it, pointing at the surviving issue.",
    ),
    10333: (
        "stale",
        "abandoned",
        "duplicate",
        "Changes requested in April 2025, no reply since. One of the two issues it claims is already closed.",
        "Take over or close.",
    ),
    10190: (
        "stale",
        "abandoned",
        "unrepro",
        "Marked <em>Work in progress</em>, no CI, no reviews, last touched by a maintainer in March 2025.",
        "Close with thanks; the issue stays open.",
    ),
    9806: (
        "stale",
        "abandoned",
        "unrepro",
        "31 lines of pyreverse docs, two maintainer reviews, author gone since 2024.",
        "Rewrite the 31 lines yourself — faster than another ping.",
    ),
    9721: (
        "stale",
        "abandoned",
        "unrepro",
        "Out-of-source linting, no reviews in two years, conflicting, <em>Needs take over</em>.",
        "Take over or close.",
    ),
    9693: (
        "stale",
        "abandoned",
        "unrepro",
        "A test that documents a pyreverse gap. Mergeable, no CI, author gone since 2024.",
        "The test alone has value — take it over.",
    ),
    9690: (
        "stale",
        "abandoned",
        "unrepro",
        "34 lines fixing functional-test ref updating; changes requested in 2024, never answered.",
        "Take over — it is one file and you know the harness.",
    ),
    9550: (
        "stale",
        "abandoned",
        "duplicate",
        "Preliminary per-directory-config work, conflicting, 14 reviews, silent since 2024. Pairs with 9395.",
        "Decide the per-directory-config story once, then close both or take both.",
    ),
    9395: (
        "stale",
        "abandoned",
        "duplicate",
        "The larger half of the same per-directory-config attempt. Conflicting, changes requested, <em>High "
        "priority</em> on the issue.",
        "High priority and abandoned is a bad combination — either own it or say it is not happening.",
    ),
    5401: (
        "stale",
        "abandoned",
        "feature",
        "The pylintd daemon, opened in 2021, conflicting, no CI.",
        "Close it. Four years is an answer.",
    ),
}

LANE_ORDER = ["merge", "review", "approve", "retrigger", "author", "decide", "stale"]

missing = sorted(
    n for n, r in rows.items() if n not in V and not r["a"].startswith("app/")
)
extra = sorted(n for n in V if n not in rows)
assert not missing, f"no verdict for {missing}"
assert not extra, f"verdict for a closed PR: {extra}"

E = html.escape


def issue_cell(links: list) -> str:
    if not links:
        return '<span class="repro na">no linked issue</span>'
    out = []
    for number, _state, _labels in links:
        info = issues.get(number, {})
        state = info.get("state", "?")
        reason = info.get("state_reason") or ""
        labels = info.get("labels", [])
        kinds = ("Crash", "False Positive", "False Negative", "Bug", "Enhancement")
        sought = ("Help wanted", "Good first issue", "Hacktoberfest", "High priority")
        kind = next((name for name in labels if name.startswith(kinds)), "")
        wanted = [name for name in labels if name.startswith(sought)]
        cls = "no" if state == "closed" else "yes"
        tail = f" — {E(reason)}" if state == "closed" and reason else ""
        bits = [f'<span class="repro {cls}">#{number} {E(state)}{tail}</span>']
        if kind:
            bits.append(f'<span class="lab">{E(kind)}</span>')
        for w in wanted:
            bits.append(f'<span class="lab">{E(w)}</span>')
        out.append("".join(bits))
    return "".join(out)


CI_WORDS = {
    "green": ("all green", "no"),
    "failing": ("red", "yes"),
    "running": ("running", "na"),
    "not-run": ("never ran", "yes"),
    "awaiting-approval": ("held for approval", "yes"),
}

body = []
for lane in LANE_ORDER:
    label, stripe, rubric = LANES[lane]
    members = [n for n in rows if V.get(n, (None,))[0] == lane]
    members.sort(key=lambda n: rows[n]["updated"], reverse=True)
    body.append(
        f'<section class="lane" data-lane="{lane}">'
        f'<h2 style="--stripe: {stripe}">{E(label)} <span class="count">{len(members)}</span></h2>'
        f'<p class="rubric">{rubric}</p>'
        f'<div class="scroll"><table><thead><tr>'
        f"<th>PR</th><th>What</th><th>State</th><th>Why it sits here</th><th>Next move</th>"
        f"</tr></thead><tbody>"
    )
    for n in members:
        r = rows[n]
        _lane, chip, chip_cls, finding, action = V[n]
        ci_word, ci_dot = CI_WORDS[r["ci"]]
        fails = f" ({r['cifail']} failing)" if r["cifail"] else ""
        conflict = (
            '<span class="lab">conflicting</span>'
            if r["merge"] == "CONFLICTING"
            else ""
        )
        draft = '<span class="lab">draft</span>' if r["draft"] else ""
        reviewers = ", ".join(r["mrev"]) if r["mrev"] else "none"
        body.append(
            "<tr>"
            f'<td class="id"><a href="https://github.com/pylint-dev/pylint/pull/{n}">#{n}</a>'
            f'<span class="date">{E(r["a"])}</span>'
            f'<span class="date">{E(r["created"])} → {E(r["updated"])}</span></td>'
            f'<td class="what"><span class="t">{E(r["t"])}</span>'
            f'<span class="msg">{r["size"]} lines · {r["files"]} files</span>{draft}{conflict}</td>'
            f'<td class="verdict"><span class="chip {chip_cls}">{E(chip)}</span>'
            f'<span class="repro {ci_dot}">CI {ci_word}{fails}</span>'
            f'<span class="repro na">reviewed by {E(reviewers)}</span>'
            f'{issue_cell(r["links"])}</td>'
            f'<td class="finding">{finding}</td>'
            f'<td class="action">{action}</td>'
            "</tr>"
        )
    body.append("</tbody></table></div></section>")

n_open = DATA["open_total"]
n_own = DATA["open_own"]
n_bot = sum(1 for r in rows.values() if r["a"].startswith("app/"))
counts = {
    lane: sum(1 for n in rows if V.get(n, (None,))[0] == lane) for lane in LANE_ORDER
}
n_silent = sum(1 for n, r in rows.items() if n in V and r["lastcom"][0] == "-")
n_conflict = sum(1 for n, r in rows.items() if n in V and r["merge"] == "CONFLICTING")
total = sum(counts.values())
held = counts["approve"] + counts["retrigger"]

page = (
    (HERE / "pr_queue_template.html")
    .read_text()
    .format(
        n_open=n_open,
        n_own=n_own,
        n_bot=n_bot,
        total=total,
        held=held,
        counts=counts,
        n_silent=n_silent,
        n_conflict=n_conflict,
        snapshot=DATA["snapshot"],
        body="".join(body),
    )
)
OUT.write_text(page)
print(f"wrote {OUT} — {total} PRs")
for lane in LANE_ORDER:
    print(f"  {lane:10s} {counts[lane]}")
