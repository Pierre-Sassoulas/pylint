"""Audit all FIXED issues: find existing tests, find fix commit, identify gaps."""

import json
import subprocess
from pathlib import Path

ROOT = Path("/home/pierre/pylint")
TESTS_DIR = ROOT / "tests" / "functional"


def grep_existing_test(issue_num):
    """Look for any test file that references this issue."""
    patterns = [
        rf"issues/{issue_num}\b",
        rf"#{issue_num}\b",
        rf"Issue{issue_num}\b",
        rf"regression_{issue_num}\b",
    ]
    matches = []
    for p in patterns:
        try:
            out = subprocess.run(
                ["grep", "-rln", "--include=*.py", "-E", p, str(TESTS_DIR)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            for line in out.stdout.strip().split("\n"):
                line = line.strip()
                if line and "primer_tests" not in line and line not in matches:
                    matches.append(line)
        except Exception:
            pass
    return matches


def find_fix_commit(issue_num):
    """Find commits that close/fix this issue."""
    patterns = [
        f"#{issue_num}",
        f"closes #{issue_num}",
        f"fix #{issue_num}",
        f"fixes #{issue_num}",
        f"Closes #{issue_num}",
    ]
    commits = []
    for p in patterns:
        try:
            out = subprocess.run(
                ["git", "log", "--oneline", "--all", f"--grep={p}", "-i"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(ROOT),
            )
            for line in out.stdout.strip().split("\n"):
                if line and line not in commits:
                    commits.append(line)
        except Exception:
            pass
    return commits


def main():
    with open(ROOT / ".triage" / "triage_state.json") as f:
        state = json.load(f)
    with open(ROOT / ".triage" / "issues_raw.json") as f:
        issues = {i["number"]: i for i in json.load(f)}

    fixeds = sorted(
        [int(n) for n, v in state["verdicts"].items() if v["verdict"] == "FIXED"],
        reverse=True,
    )

    report = []
    for num in fixeds:
        issue = issues.get(num, {})
        title = (issue.get("title") or "")[:80]
        tests = grep_existing_test(num)
        commits = find_fix_commit(num)
        report.append(
            {
                "num": num,
                "title": title,
                "tests": tests,
                "commits": commits,
            }
        )

    # Print summary
    print(f"# FIXED-issue audit ({len(fixeds)} issues)\n")
    n_with_test = sum(1 for r in report if r["tests"])
    n_with_commit = sum(1 for r in report if r["commits"])
    print(f"- Have existing test: {n_with_test} / {len(fixeds)}")
    print(f"- Identified fix commit: {n_with_commit} / {len(fixeds)}")
    print()
    for r in report:
        print(f"## #{r['num']} — {r['title']}")
        if r["tests"]:
            print(
                f"  Tests: {', '.join(t.replace(str(ROOT)+'/', '') for t in r['tests'][:3])}"
            )
        else:
            print("  Tests: ** NONE — need to add **")
        if r["commits"]:
            for c in r["commits"][:3]:
                print(f"  Commit: {c}")
        else:
            print("  Commit: ** NOT FOUND — need to bisect **")
        print()

    # Save to file too
    with open(ROOT / ".triage" / "fixed_audit.json", "w") as f:
        json.dump(report, f, indent=1)
    print(f"\nSaved JSON to {ROOT / '.triage' / 'fixed_audit.json'}")


if __name__ == "__main__":
    main()
