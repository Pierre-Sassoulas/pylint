"""Refresh astroid_queue_data.json: the open astroid pull requests, for the
"To do now" block of pr-queue.html.

Read-only GitHub calls through ``gh``. Each pull request gets its CI state,
whether its runs wait for approval, and the labels and reactions of the issues
it closes in astroid or names in pylint (``pylint-dev/pylint#N`` or an issue
URL), since astroid fixes are usually wanted for a pylint issue.
"""

from __future__ import annotations

import datetime
import json
import pathlib
import re
import subprocess

REPO = "pylint-dev/astroid"
HERE = pathlib.Path(__file__).resolve().parent
PYLINT_REF = re.compile(r"pylint-dev/pylint(?:#|/issues/|/pull/)(\d+)")


def gh(*args: str) -> object:
    for _ in range(4):
        done = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
        if done.returncode == 0:
            return json.loads(done.stdout)
    raise RuntimeError(done.stderr)


def ci_state(runs: list, held: bool) -> tuple[str, int]:
    failed = [r for r in runs if r.get("conclusion") in ("FAILURE", "TIMED_OUT")]
    if held:
        return "awaiting-approval", 0
    if not runs:
        return "not-run", 0
    if any(r.get("status") in ("IN_PROGRESS", "QUEUED") for r in runs):
        return "running", len(failed)
    return ("failing" if failed else "green"), len(failed)


def issue(repo: str, number: int, cache: dict) -> dict:
    key = f"{repo}#{number}"
    if key not in cache:
        data = gh("api", f"repos/{repo}/issues/{number}")
        cache[key] = {
            "ref": key,
            "title": data["title"],
            "state": data["state"],
            "labels": [label["name"] for label in data["labels"]],
            "reactions": data["reactions"]["total_count"],
            "pr": "pull_request" in data,
        }
    return cache[key]


def main() -> None:
    fields = (
        "number,title,author,isDraft,labels,reviewDecision,milestone,additions,"
        "deletions,createdAt,updatedAt,body,closingIssuesReferences,headRefOid"
    )
    prs = gh("pr", "list", "--repo", REPO, "--limit", "300", "--json", fields)
    held = set(
        line
        for line in subprocess.run(
            [
                "gh", "api", "--paginate",
                f"repos/{REPO}/actions/runs?status=action_required&per_page=100",
                "--jq", '.workflow_runs[] | select(.name != "changelog") | .head_sha',
            ],
            capture_output=True, text=True, check=True,
        ).stdout.split()
    )
    cache: dict = {}
    rows = []
    for pr in sorted(prs, key=lambda p: p["number"]):
        # Dependency bumps are skipped; backports need a maintainer to merge.
        if pr["author"]["login"].startswith("app/") and pr["author"]["login"] != "app/pylint-backport":
            continue
        n = pr["number"]
        runs = gh("pr", "view", str(n), "--repo", REPO, "--json", "statusCheckRollup")[
            "statusCheckRollup"
        ] or []
        state, failed = ci_state(runs, pr["headRefOid"] in held)
        refs = [
            (f"{ref['repository']['owner']['login']}/{ref['repository']['name']}", ref["number"])
            for ref in pr["closingIssuesReferences"] or []
        ]
        refs += [
            ("pylint-dev/pylint", number)
            for number in sorted({int(m) for m in PYLINT_REF.findall(pr["body"] or "")})
        ]
        links = []
        for repo, number in dict.fromkeys(refs):
            try:
                linked = issue(repo, number, cache)
            except RuntimeError:  # deleted, transferred or private
                continue
            if not linked["pr"]:
                links.append(linked)
        rows.append(
            {
                "n": n,
                "a": pr["author"]["login"],
                "t": pr["title"],
                "draft": pr["isDraft"],
                "labels": [label["name"] for label in pr["labels"]],
                "rd": pr["reviewDecision"] or "NONE",
                "milestone": (pr["milestone"] or {}).get("title", ""),
                "size": pr["additions"] + pr["deletions"],
                "created": pr["createdAt"][:10],
                "updated": pr["updatedAt"][:10],
                "ci": state,
                "cifail": failed,
                "links": links,
            }
        )
    out = {"snapshot": datetime.date.today().isoformat(), "prs": rows}
    path = HERE / "astroid_queue_data.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"{path}: {len(rows)} pull requests")


if __name__ == "__main__":
    main()
