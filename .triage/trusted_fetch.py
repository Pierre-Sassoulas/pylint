"""Write `trusted.json`: which authors of open PRs are trusted contributors.

A trusted contributor had a pull request merged in pylint or astroid before
LLM-written code was common (ChatGPT came out on 30 November 2022), so they
learned the codebase themselves at some point. Their PRs cost less to review
and go first in every lane. Once trusted, always trusted: known authors are
not asked again. Read-only, one search request per new author.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import time

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "trusted.json"
CUTOFF = "2023-01-01"
REPOS = ("pylint-dev/pylint", "pylint-dev/astroid")


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def first_merged(login: str) -> str:
    """Creation date of the author's oldest PR merged before the cutoff, or ''."""
    query = " ".join(
        [*(f"repo:{repo}" for repo in REPOS), f"author:{login}", "is:pr", "is:merged", f"created:<{CUTOFF}"]
    )
    # Under load the search API answers with incomplete or empty results, so
    # a "no" is only stored once two answers agree on it.
    misses = 0
    while misses < 2:
        answer = json.loads(
            gh(
                "api", "-X", "GET", "search/issues", "-f", f"q={query}", "-f", "sort=created",
                "-f", "order=asc", "-f", "per_page=1",
                "--jq", "{incomplete: .incomplete_results, date: (.items[0].created_at // \"\")}",
            )
        )
        if answer["date"]:
            return answer["date"][:10]
        if not answer["incomplete"]:
            misses += 1
        # The search API allows 30 requests a minute.
        time.sleep(2.1)
    return ""


def main() -> None:
    known = json.loads(OUT.read_text()) if OUT.exists() else {}
    authors = set()
    for repo in REPOS:
        authors.update(
            json.loads(
                gh("pr", "list", "--repo", repo, "--state", "open", "--limit", "500",
                   "--json", "author", "--jq", "[.[].author.login]")
            )
        )
    for login in sorted(authors - set(known)):
        if login.startswith("app/") or login.endswith("[bot]"):
            known[login] = ""
            continue
        known[login] = first_merged(login)
    OUT.write_text(json.dumps(dict(sorted(known.items())), indent=2))
    trusted = sorted(login for login, date in known.items() if date)
    print(f"wrote {OUT}: {len(trusted)} trusted of {len(known)} authors: {', '.join(trusted)}")


if __name__ == "__main__":
    main()
