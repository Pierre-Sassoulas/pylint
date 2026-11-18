"""Guess which open issues are fixed, from snippet_sweep.py runs.

For each open issue, the message it is about comes from its title (or its
body when the title names none): a symbol like ``no-member`` or an id like
``E1101``. Then, on the issue's usable snippets (not a syntax error, not a
timeout):

- false positive or bug: the message is gone from the output;
- false negative: the message now shows;
- crash: no ``astroid-error`` / ``fatal`` any more.

That is a candidate, not a verdict: an extracted snippet can lack the context
or the library that triggers the issue. Candidates are stronger when the
snippet still has the message in an older run (``--old``), which is how
``--old`` with the astroid 4.3.4 run and ``--new`` with the astroid main run
lists the issues the astroid upgrade fixes.

    python3 fixed_scan.py --new run.json [--old older.json] --msgs msgs.json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ISSUES = HERE / "sweep_open_issues.json"
MSGID = re.compile(r"\b([CRWEFI]\d{4})\b")
CRASH = {"astroid-error", "fatal"}
UNUSABLE = {"syntax-error"}


def mentioned(text: str, symbols: dict[str, str]) -> set[str]:
    by_id = {}
    for symbol, msgid in symbols.items():
        by_id.setdefault(msgid, symbol)
    found = {by_id[m] for m in MSGID.findall(text) if m in by_id}
    for symbol in symbols:
        if "-" in symbol and re.search(rf"(?<![\w-]){re.escape(symbol)}(?![\w-])", text):
            found.add(symbol)
    return found


def emitted(lines: list[str]) -> set[str]:
    return {line.split(":")[2] for line in lines if line.count(":") >= 3}


def usable(lines: list[str]) -> bool:
    return lines != ["TIMEOUT"] and not (emitted(lines) & UNUSABLE)


def kind(labels: list[str], title: str) -> str:
    if any(label.startswith("Crash") for label in labels) or "crash" in title.lower():
        return "crash"
    if any(label.startswith("False Negative") for label in labels):
        return "fn"
    if any(label.startswith(("False Positive", "Bug")) for label in labels):
        return "fp"
    return ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--new", required=True)
    parser.add_argument("--old")
    parser.add_argument("--msgs", required=True)
    args = parser.parse_args()
    symbols = json.loads(pathlib.Path(args.msgs).read_text())
    new = json.loads(pathlib.Path(args.new).read_text())["snippets"]
    old = json.loads(pathlib.Path(args.old).read_text())["snippets"] if args.old else {}
    by_issue: dict[int, list[str]] = {}
    for name in new:
        number = int(re.search(r"i(\d+)", name).group(1))
        by_issue.setdefault(number, []).append(name)
    results = []
    for issue in json.loads(ISSUES.read_text()):
        names = by_issue.get(issue["number"])
        what = kind(issue["labels"], issue["title"])
        if not names or not what:
            continue
        targets = mentioned(issue["title"], symbols) or mentioned(issue["body"] or "", symbols)
        if what == "crash":
            targets = CRASH
        if not targets:
            continue
        good = [n for n in names if usable(new[n])]
        if not good:
            continue
        now = set().union(*(emitted(new[n]) for n in good))
        before = set().union(*(emitted(old[n]) for n in good if n in old)) if old else set()
        hit = now & targets
        if what == "fn":
            fixed = bool(hit)
            was = bool(before & targets) if old else None
            confirmed = fixed and was is False
        else:
            fixed = not hit
            was = bool(before & targets) if old else None
            confirmed = fixed and bool(was)
        if not fixed:
            continue
        if old and not confirmed:
            continue
        hand = any(n.startswith("snippets/") for n in good)
        results.append({
            "number": issue["number"],
            "kind": what,
            "title": issue["title"],
            "targets": sorted(targets),
            "snippets": good,
            "hand_made": hand,
            "import_error": "import-error" in now,
            "changed": confirmed,
        })
    print(json.dumps(results, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
