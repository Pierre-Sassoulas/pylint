"""For each TRULY-FIXED issue, find the commit that fixed it.

Uses two strategies:
1. Direct: git log --all-branches --grep="#NNNN" or "Closes #NNNN"
2. Indirect: search whatsnew/index.rst pages for the issue number
3. Bisect-by-version: run pylint on the snippet across older tags
"""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/pierre/pylint")
SNIPPETS = ROOT / ".triage" / "snippets"
RCFILE = ROOT / "pylint" / "testutils" / "testing_pylintrc"
WHATSNEW_DIRS = [ROOT / "doc" / "whatsnew" / v for v in ("2", "3", "4")]


def search_whatsnew(issue_num):
    """Look up the whatsnew page that mentions this issue."""
    matches = []
    for base in WHATSNEW_DIRS:
        if not base.exists():
            continue
        for f in base.rglob("*.rst"):
            try:
                text = f.read_text(errors="ignore")
            except Exception:
                continue
            if re.search(rf"#{issue_num}\b|Closes\s+#?{issue_num}\b", text):
                rel = f.relative_to(ROOT)
                matches.append(str(rel))
    return matches


def find_grep_commits(issue_num):
    """Git log --grep for the issue number."""
    commits = []
    patterns = [f"#{issue_num}", f"closes #{issue_num}", f"Closes #{issue_num}"]
    for p in patterns:
        try:
            out = subprocess.run(
                ["git", "log", "--all", "--oneline", f"--grep={p}", "-i"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(ROOT),
            )
            for line in out.stdout.strip().split("\n"):
                line = line.strip()
                if line and line not in commits:
                    commits.append(line)
        except Exception:
            pass
    return commits[:5]


def main():
    with open(ROOT / ".triage" / "triage_state.json") as f:
        state = json.load(f)
    with open(ROOT / ".triage" / "issues_raw.json") as f:
        issues = {i["number"]: i for i in json.load(f)}

    fixeds = sorted(
        [int(n) for n, v in state["verdicts"].items() if v["verdict"] == "FIXED"],
        reverse=True,
    )

    print(f"# Looking for fix commits for {len(fixeds)} TRULY_FIXED issues\n")
    found_count = 0
    for num in fixeds:
        wn = search_whatsnew(num)
        commits = find_grep_commits(num)
        title = (issues.get(num, {}).get("title") or "")[:70]
        print(f"## #{num} — {title}")
        if wn:
            print(f"  Changelog: {', '.join(wn)}")
        if commits:
            print("  Commit candidates:")
            for c in commits[:3]:
                print(f"    {c}")
            found_count += 1
        if not wn and not commits:
            print("  NOT FOUND directly — needs bisect")
        print()
    print(f"\n=== Direct hits: {found_count}/{len(fixeds)} ===")


if __name__ == "__main__":
    main()
