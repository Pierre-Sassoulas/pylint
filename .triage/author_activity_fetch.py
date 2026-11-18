"""Refresh author_activity.json: when each pull request's author last acted.

A pull request waiting on its author stays out of the to-do list until the
author has been silent long enough for a take-over (see ``takeover.py``).
"Updated" is no help for that: a bot comment, a label or a maintainer's review
all bump it. So this records, per open pull request, the latest of the last
commit date and the last comment or review written by the author.
Commits are counted only when the author wrote them.

Read-only GitHub calls through ``gh api graphql``, 50 pull requests a query.
Output::

    {"snapshot": "2026-11-18",
     "pylint": {"11690": "2026-10-18", ...},
     "astroid": {"3384": "2026-11-16", ...}}
"""

from __future__ import annotations

import datetime
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "author_activity.json"

QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: OPEN, first: 50, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        author { login }
        commits(last: 30) { nodes { commit { committedDate authors(first: 3) { nodes { user { login } } } } } }
        comments(last: 30) { nodes { author { login } createdAt } }
        reviews(last: 30) { nodes { author { login } submittedAt } }
      }
    }
  }
}
"""


def gh_graphql(name: str, cursor: str | None) -> dict:
    args = ["gh", "api", "graphql", "-f", f"query={QUERY}", "-F", "owner=pylint-dev", "-F", f"name={name}"]
    if cursor:
        args += ["-F", f"cursor={cursor}"]
    for _ in range(4):
        done = subprocess.run(args, capture_output=True, text=True, check=False)
        if done.returncode == 0:
            return json.loads(done.stdout)["data"]["repository"]["pullRequests"]
    raise RuntimeError(done.stderr)


def last_author_activity(pr: dict) -> str:
    login = (pr["author"] or {}).get("login")
    # Only the author's own commits: a maintainer pushing a fix or a merge of
    # main to the branch is not the author coming back.
    dates = [
        node["commit"]["committedDate"]
        for node in pr["commits"]["nodes"]
        if any(
            (person["user"] or {}).get("login") == login
            for person in node["commit"]["authors"]["nodes"]
        )
    ]
    dates += [
        node["createdAt"]
        for node in pr["comments"]["nodes"]
        if (node["author"] or {}).get("login") == login
    ]
    dates += [
        node["submittedAt"]
        for node in pr["reviews"]["nodes"]
        if (node["author"] or {}).get("login") == login and node["submittedAt"]
    ]
    return max(dates)[:10] if dates else ""


def main() -> None:
    result: dict[str, object] = {"snapshot": datetime.date.today().isoformat()}
    for name in ("pylint", "astroid"):
        activity: dict[str, str] = {}
        cursor = None
        while True:
            page = gh_graphql(name, cursor)
            for pr in page["nodes"]:
                activity[str(pr["number"])] = last_author_activity(pr)
            if not page["pageInfo"]["hasNextPage"]:
                break
            cursor = page["pageInfo"]["endCursor"]
        result[name] = activity
    OUT.write_text(json.dumps(result, indent=1, sort_keys=True))
    print(f"wrote {OUT}: {len(result['pylint'])} pylint, {len(result['astroid'])} astroid")


if __name__ == "__main__":
    main()
