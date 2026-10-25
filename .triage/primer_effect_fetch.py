"""Write `primer_effect.json`: what the latest primer comment says each open PR changes.

The primer bot comments "Effect of this PR on checked open source code" with,
per project, numbered "Added messages" / "Removed messages" lists, or says the
change has "no effect". Only the newest such comment counts: older ones are for
earlier commits. Read-only, about a minute.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).resolve().parent
REPO = "pylint-dev/pylint"
OUT = HERE / "primer_effect.json"

PROJECT = re.compile(r"\*\*Effect on \[([^\]]+)\]")
SECTION = re.compile(r"^(New|Added|Removed|Changed) messages", re.M)
# "1) symbol:" then "*message*" on the next line, or "1) [symbol](url):" then
# "message: `old` → `new`" for a changed message.
ITEM = re.compile(r"^\d+\) \[?([a-z0-9-]+)\]?(?:\([^)]*\))?:\n(.*)$", re.M)
COMMIT = re.compile(r"generated for commit ([0-9a-f]{7,40})")


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def parse(body: str) -> dict:
    effect: dict = {"added": 0, "removed": 0, "changed": 0, "projects": {}, "items": []}
    commit = COMMIT.search(body)
    effect["commit"] = commit.group(1)[:9] if commit else ""
    if "no effect" in body:
        return effect
    # Split on project headers, then on the Added/Removed headers inside each.
    chunks = PROJECT.split(body)[1:]
    for project, text in zip(chunks[::2], chunks[1::2]):
        counts = {"added": 0, "removed": 0, "changed": 0}
        parts = SECTION.split(text)[1:]
        for kind, section in zip(parts[::2], parts[1::2]):
            kind = {"New": "added", "Added": "added"}.get(kind, kind.lower())
            for symbol, message in ITEM.findall(section):
                counts[kind] += 1
                # The same item in many PRs' comments is primer noise
                # (pr_queue.py drops those); the message text tells them apart.
                effect["items"].append([project, kind, symbol, message.strip()[:200]])
        for kind, count in counts.items():
            effect[kind] += count
        effect["projects"][project] = counts
    return effect


def latest(number: int) -> tuple[int, dict | None]:
    comments = json.loads(
        gh(
            "api",
            "--paginate",
            f"repos/{REPO}/issues/{number}/comments?per_page=100",
            "--jq",
            '[.[] | select(.user.login == "github-actions[bot]") '
            '| select(.body | test("Effect of this PR|no effect")) | {created_at, body}]',
        ).replace("]\n[", ",")
        or "[]"
    )
    if not comments:
        return number, None
    newest = max(comments, key=lambda c: c["created_at"])
    return number, {"date": newest["created_at"][:10], **parse(newest["body"])}


def main() -> None:
    numbers = json.loads(gh("pr", "list", "--repo", REPO, "--limit", "500", "--json", "number", "--jq", "[.[].number]"))
    with ThreadPoolExecutor(8) as pool:
        found = dict(pool.map(latest, numbers))
    data = {str(n): e for n, e in sorted(found.items()) if e is not None}
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"wrote {OUT}: {len(data)} of {len(numbers)} PRs have a primer comment")


if __name__ == "__main__":
    main()
