"""Build pylint-issues.html: every open pylint issue, grouped by its type label.

Reads ``sweep_open_issues.json`` (``snippet_sweep.py fetch``), the saved
snippets (``snippets/`` hand-made, ``snippets_auto/`` extracted by
``snippet_sweep.py extract``) and the verdicts of the 13 September 2026
re-run sweep (``issue_verdicts_2026-09-13.json``, 108 issues). Nothing is
re-run here: the page says what the labels say, which snippet exists to
re-run, and what the last sweep found when there was one.

``pr_queue_fetch.sh`` runs fetch, extract and this script, so the page follows
the labels. Also rewrites the "Pylint issues" card of ``index.html``.
"""

from __future__ import annotations

import collections
import html
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ISSUES = HERE / "sweep_open_issues.json"
VERDICTS = HERE / "issue_verdicts_2026-09-13.json"
SNIPPETS = HERE / "snippets"
SNIPPETS_AUTO = HERE / "snippets_auto"
OUT = HERE / "pylint-issues.html"
INDEX = HERE / "index.html"

# An issue with several type labels counts once, under the first one here.
TYPES = (
    ("crash", "Crash 💥", "Crash", "var(--bad)"),
    ("bug", "Bug :beetle:", "Bug", "var(--bad)"),
    ("fp", "False Positive 🦟", "False positive", "var(--warn)"),
    ("fn", "False Negative 🦋", "False negative", "var(--warn)"),
    ("enh", "Enhancement ✨", "Enhancement", "var(--info)"),
    ("doc", "Documentation :green_book:", "Documentation", "var(--info)"),
    ("maint", "Maintenance", "Maintenance", "var(--ink-faint)"),
    ("talk", ("Discussion 🤔", "Proposal 📨", "Question"), "Discussion", "var(--ink-faint)"),
)
NO_TYPE = ("none", "", "No type label", "var(--ink-faint)")

# What the issue waits for, from its labels; first match wins.
STATES = (
    ("pr", ("Needs PR",), "Needs PR"),
    ("decide", ("Needs decision", "Needs specification", "Needs design proposal"), "Needs decision"),
    ("astroid", ("Needs astroid",), "Needs astroid"),
    ("check", ("Needs investigation", "Needs reproduction", "Needs triage"), "Needs investigation"),
)
NO_STATE = ("other", "No status label")

HAND_MADE = re.compile(r"i(\d+)\.py$")
AUTO = re.compile(r"i(\d+)_block\d+\.py$")


def kind(labels: list[str]) -> tuple[str, str, str, str]:
    for key, wanted, title, stripe in TYPES:
        names = (wanted,) if isinstance(wanted, str) else wanted
        if any(label in names for label in labels):
            return key, wanted if isinstance(wanted, str) else names[0], title, stripe
    return NO_TYPE


def state(labels: list[str]) -> tuple[str, str]:
    for key, prefixes, title in STATES:
        if any(label.startswith(prefix) for label in labels for prefix in prefixes):
            return key, title
    return NO_STATE


def snippets() -> tuple[dict[int, str], dict[int, list[str]]]:
    hand = {int(m.group(1)): p.name for p in SNIPPETS.glob("i*.py") if (m := HAND_MADE.match(p.name))}
    auto: dict[int, list[str]] = collections.defaultdict(list)
    for path in sorted(SNIPPETS_AUTO.glob("i*.py")):
        if m := AUTO.match(path.name):
            auto[int(m.group(1))].append(path.name)
    return hand, auto


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def row(issue: dict, hand: dict[int, str], auto: dict[int, list[str]], verdicts: dict) -> str:
    n = issue["number"]
    labels = issue["labels"]
    tkey, tlabel, ttitle, _ = kind(labels)
    skey, stitle = state(labels)
    high = "High priority" in labels
    shown = [label for label in labels if label != tlabel]
    if n in hand:
        snippet = f'<a href="snippets/{hand[n]}">{hand[n]}</a><span class="repro yes">hand-made, verified</span>'
    elif n in auto:
        links = " ".join(f'<a href="snippets_auto/{name}">{name.split("_")[1][:-3]}</a>' for name in auto[n])
        snippet = f'{links}<span class="repro na">extracted, not verified</span>'
    else:
        snippet = '<span class="repro no">no code block</span>'
    old = verdicts.get(str(n))
    finding = ""
    if old:
        finding = (
            f'<span class="chip {"confirmed" if old["group"] == "live" else "feature" if old["group"] == "wanted" else "unrepro"}">'
            f'{esc(old["verdict"])}</span> <span class="msg">13 Sept sweep:</span> {esc(old["finding"])}'
        )
    reactions = f'<span class="date">{issue["reactions"]} reactions</span>' if issue["reactions"] else ""
    milestone = f'<span class="done">{esc(issue["milestone"])}</span>' if issue["milestone"] else ""
    search = esc(f"{n} {issue['title']} {' '.join(labels)}".lower())
    return (
        f'<tr data-t="{tkey}" data-s="{skey}" data-q="{search}">'
        f'<td class="id"><a href="https://github.com/pylint-dev/pylint/issues/{n}">#{n}</a>'
        f'<span class="date">{issue["createdAt"][:10]}</span>{reactions}{milestone}</td>'
        f'<td class="what"><span class="t">{esc(issue["title"])}</span>'
        f'<span class="msg">by {esc(issue["author"])} · updated {issue["updatedAt"][:10]}</span></td>'
        f'<td class="verdict"><span class="chip {"crash" if tkey in ("crash", "bug") else "confirmed" if tkey in ("fp", "fn") else "feature"}">{ttitle}</span>'
        f'{"<span class=\"repro yes\">High priority</span>" if high else ""}'
        f'<span class="repro na">{stitle}</span></td>'
        f'<td class="finding">{snippet}{"<br>" + finding if finding else ""}</td>'
        f'<td class="action labels">{" ".join(f"<span class=\"lab\">{esc(label)}</span>" for label in shown)}</td></tr>'
    )


def sort_key(issue: dict) -> tuple:
    order = [key for key, *_ in TYPES] + [NO_TYPE[0]]
    return (
        order.index(kind(issue["labels"])[0]),
        "High priority" not in issue["labels"],
        -issue["reactions"],
        -issue["number"],
    )


def main() -> None:
    issues = sorted(json.loads(ISSUES.read_text()), key=sort_key)
    verdicts = json.loads(VERDICTS.read_text()) if VERDICTS.exists() else {}
    hand, auto = snippets()
    total = len(issues)
    by_type = collections.Counter(kind(i["labels"])[0] for i in issues)
    by_state = collections.Counter(state(i["labels"])[0] for i in issues)
    numbers = {i["number"] for i in issues}
    n_hand = len(numbers & set(hand))
    n_auto = len((numbers & set(auto)) - set(hand))
    n_none = total - n_hand - n_auto
    n_verdict = len(numbers & {int(k) for k in verdicts})
    snapshot = max(i["updatedAt"] for i in issues)[:10]

    tally = "".join(
        f'<div style="--stripe: {stripe}"><div class="n">{by_type[key]}</div><div class="k">{title}</div></div>'
        for key, _, title, stripe in (*TYPES, NO_TYPE)
        if by_type[key]
    )
    type_buttons = " ".join(
        f'<button class="f" data-dim="t" data-f="{key}" aria-pressed="false">{title} {by_type[key]}</button>'
        for key, _, title, _ in (*TYPES, NO_TYPE)
        if by_type[key]
    )
    state_buttons = " ".join(
        f'<button class="f" data-dim="s" data-f="{key}" aria-pressed="false">{title} {by_state[key]}</button>'
        for key, title in [(key, title) for key, _, title in STATES] + [NO_STATE]
        if by_state[key]
    )
    rows = "\n".join(row(i, hand, auto, verdicts) for i in issues)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pylint issues</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/triage.css">
<style>
  .controls + .controls {{ margin-top: 6px; }}
  .controls input[type=search] {{ font: inherit; padding: 4px 8px; min-width: 16em; max-width: 100%; }}
  td.finding a {{ margin-right: 6px; }}
  td.what .msg {{ display: block; margin-top: 4px; }}
</style>
</head>
<body>
<div class="wrap">
  <nav class="site-nav"><a href="index.html" class="home">Overview</a> <a href="pylint-issues.html" aria-current="page">Pylint issues</a> <a href="astroid.html">Astroid queue</a> <a href="pr-queue.html">Pull request queue</a> <a href="method.html">Method</a></nav>
  <header>
    <div class="eyebrow">pylint-dev/pylint &nbsp;·&nbsp; <b>{total} open</b> &nbsp;·&nbsp; labels as of {snapshot}</div>
    <h1>Pylint issues</h1>
    <p class="standfirst">All {total} open issues, by type label. An issue with several type labels counts once, under the first of crash, bug, false positive, false negative, enhancement, documentation, maintenance, discussion. Snippets: {n_hand} hand-made and verified, {n_auto} extracted from the issue body and not verified, {n_none} with no code block. Re-run them with <code>snippet_sweep.py run</code>. Nothing on this page was re-run: the {n_verdict} rows with a verdict carry what the 13 September 2026 sweep found.</p>
  </header>
<div class="tally">{tally}</div>
<div class="controls"><span class="lbl">Type</span><button class="f" data-dim="t" data-f="all" aria-pressed="true">All {total}</button> {type_buttons}</div>
<div class="controls"><span class="lbl">Waits for</span><button class="f" data-dim="s" data-f="all" aria-pressed="true">All</button> {state_buttons}</div>
<div class="controls"><span class="lbl">Find</span><input type="search" id="q" placeholder="number, title or label"> <span class="lbl" id="shown"></span></div>
<div class="scroll"><table><thead><tr><th>Issue</th><th>Report</th><th>Type</th><th>Snippet · last sweep</th><th>Other labels</th></tr></thead><tbody>
{rows}
</tbody></table></div>
<script>
  const want = {{ t: "all", s: "all" }};
  const q = document.getElementById("q");
  function apply() {{
    const text = q.value.trim().toLowerCase();
    let shown = 0;
    for (const tr of document.querySelectorAll("tbody tr")) {{
      tr.hidden = (want.t !== "all" && tr.dataset.t !== want.t)
        || (want.s !== "all" && tr.dataset.s !== want.s)
        || (text && !tr.dataset.q.includes(text));
      if (!tr.hidden) shown++;
    }}
    document.getElementById("shown").textContent = shown + " shown";
  }}
  for (const btn of document.querySelectorAll("button.f")) {{
    btn.addEventListener("click", () => {{
      for (const b of document.querySelectorAll(`button.f[data-dim="${{btn.dataset.dim}}"]`))
        b.setAttribute("aria-pressed", String(b === btn));
      want[btn.dataset.dim] = btn.dataset.f;
      apply();
    }});
  }}
  q.addEventListener("input", apply);
  apply();
</script>

  <footer>
    Generated by <code>.triage/issues_page.py</code> from <code>sweep_open_issues.json</code>, on branch <code>issue-triage-workspace</code>.
    Open <code>.triage/index.html</code> in a browser; nothing is served.
  </footer>
</div>
</body>
</html>
"""
    OUT.write_text(page)

    card = (
        f'<a href="pylint-issues.html" style="--stripe: var(--warn)"><h2>Pylint issues</h2>'
        f"<p>All {total} open issues by type label: {by_type['crash']} crashes, {by_type['bug']} bugs, "
        f"{by_type['fp']} false positives, {by_type['fn']} false negatives, {by_type['enh']} enhancements.</p>"
        f'<span class="meta">{n_hand + n_auto} with a snippet to re-run · {by_state["pr"]} need a PR</span></a>'
    )
    index = INDEX.read_text()
    index = re.sub(r'<a href="pylint-issues.html" style="[^"]*"><h2>Pylint issues</h2>.*?</a>', card, index, count=1, flags=re.S)
    INDEX.write_text(index)
    print(f"wrote {OUT}: {total} issues, {dict(by_type)}")


if __name__ == "__main__":
    main()
