# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Perform the GitHub house-keeping that follows a published release.

This automates the manual post-release steps documented in
``doc/development_guide/contributor_guide/release.rst`` (see
https://github.com/pylint-dev/pylint/issues/7362):

* minor/major release (``X.Y.0``):
    - create the ``maintenance/X.Y.x`` branch from the tag,
    - mark the closed ``backport maintenance/X.(Y-1).x`` issues as ``backported``
      then rename that label to ``backport maintenance/X.Y.x``,
    - close the ``X.Y.0`` milestone and open ``X.Y.1`` and ``X.(Y+1).0``;
* patch release (``X.Y.Z`` with ``Z > 0``):
    - close the ``X.Y.Z`` milestone and open ``X.Y.(Z+1)``.

It relies on the ``gh`` CLI being authenticated (``GH_TOKEN``). Nothing is
performed unless ``--apply`` is passed; by default every action is only printed.

The branch-protection pattern update and the Read the Docs version clean-up
still require elevated, project-specific credentials and are therefore only
reported as reminders rather than performed.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess

REPO = "pylint-dev/pylint"
VERSION_RE = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


class Runner:
    """Thin wrapper around ``gh`` that honours the dry-run flag."""

    def __init__(self, apply: bool) -> None:
        self.apply = apply

    def gh(self, *args: str, read_only: bool = False) -> str:
        """Run a ``gh`` command. Mutating calls are skipped in dry-run mode."""
        command = ["gh", *args]
        if not self.apply and not read_only:
            print(f"DRY-RUN would run: {' '.join(command)}")
            return ""
        print(f"Running: {' '.join(command)}")
        return subprocess.run(
            command, check=True, capture_output=True, text=True
        ).stdout


def parse_version(version: str) -> tuple[int, int, int]:
    match = VERSION_RE.match(version)
    if not match:
        raise SystemExit(
            f"Refusing to finalize for non-final version {version!r} "
            "(expected MAJOR.MINOR.PATCH)."
        )
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
    )


def create_maintenance_branch(runner: Runner, major: int, minor: int, tag: str) -> None:
    branch = f"maintenance/{major}.{minor}.x"
    print(f"\n# Creating maintenance branch {branch} from {tag}")
    if runner.apply:
        sha = subprocess.run(
            ["git", "rev-parse", f"{tag}^{{commit}}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    else:
        sha = f"<sha of {tag}>"
    runner.gh(
        "api",
        f"repos/{REPO}/git/refs",
        "-f",
        f"ref=refs/heads/{branch}",
        "-f",
        f"sha={sha}",
    )


def rotate_backport_label(runner: Runner, major: int, minor: int) -> None:
    old_label = f"backport maintenance/{major}.{minor - 1}.x"
    new_label = f"backport maintenance/{major}.{minor}.x"
    print(f"\n# Marking closed {old_label!r} issues as 'backported'")
    issues = _closed_issues_with_label(runner, old_label)
    for number in issues:
        runner.gh(
            "issue", "edit", str(number), "--repo", REPO, "--add-label", "backported"
        )
    print(f"# Renaming label {old_label!r} -> {new_label!r}")
    runner.gh(
        "api",
        "--method",
        "PATCH",
        f"repos/{REPO}/labels/{old_label.replace(' ', '%20')}",
        "-f",
        f"new_name={new_label}",
    )


def _closed_issues_with_label(runner: Runner, label: str) -> list[int]:
    output = runner.gh(
        "issue",
        "list",
        "--repo",
        REPO,
        "--state",
        "closed",
        "--label",
        label,
        "--json",
        "number",
        "--limit",
        "1000",
        read_only=True,
    )
    if not output:
        return []
    return [item["number"] for item in json.loads(output)]


def rotate_milestones(runner: Runner, new_milestones: list[str], close: str) -> None:
    print(f"\n# Closing milestone {close} and opening {', '.join(new_milestones)}")
    milestones = _open_milestones(runner)
    if close in milestones:
        runner.gh(
            "api",
            "--method",
            "PATCH",
            f"repos/{REPO}/milestones/{milestones[close]}",
            "-f",
            "state=closed",
        )
    else:
        print(f"  (milestone {close} not found among open milestones, skipping close)")
    for title in new_milestones:
        if title in milestones:
            print(f"  (milestone {title} already exists, skipping)")
            continue
        runner.gh("api", f"repos/{REPO}/milestones", "-f", f"title={title}")


def _open_milestones(runner: Runner) -> dict[str, int]:
    output = runner.gh(
        "api",
        f"repos/{REPO}/milestones?state=open&per_page=100",
        read_only=True,
    )
    if not output:
        return {}
    return {item["title"]: item["number"] for item in json.loads(output)}


def manual_reminders(major: int, minor: int) -> None:
    print(
        "\n# Steps that still require project admin / Read the Docs credentials:\n"
        f"  - Update the protected-branch pattern to 'maintenance/{major}.{minor}*'.\n"
        f"  - Delete the 'maintenance/{major}.{minor - 1}.x' branch once it is "
        "no longer needed.\n"
        "  - Hide/deactivate the superseded patch releases on Read the Docs, "
        "keeping only the latest."
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="The released version, e.g. 4.2.0 or 4.0.6")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform the actions (otherwise only print them).",
    )
    args = parser.parse_args(argv)

    major, minor, patch = parse_version(args.version)
    runner = Runner(args.apply)
    tag = f"v{args.version}"

    if patch == 0:
        print(f"== Finalizing minor/major release {args.version} ==")
        create_maintenance_branch(runner, major, minor, tag)
        rotate_backport_label(runner, major, minor)
        rotate_milestones(
            runner,
            new_milestones=[f"{major}.{minor}.1", f"{major}.{minor + 1}.0"],
            close=f"{major}.{minor}.0",
        )
        manual_reminders(major, minor)
    else:
        print(f"== Finalizing patch release {args.version} ==")
        rotate_milestones(
            runner,
            new_milestones=[f"{major}.{minor}.{patch + 1}"],
            close=f"{major}.{minor}.{patch}",
        )

    if not args.apply:
        print("\nDry-run only. Re-run with --apply to perform these actions.")


if __name__ == "__main__":
    main()
