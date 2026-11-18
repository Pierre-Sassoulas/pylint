# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Run the code of every open issue through pylint and compare two runs.

Find the open issues that a change fixes (or breaks) by linting their code
before and after the change. Four steps, all writing in ``.issue_snippets/``
(ignored by git)::

    python script/issue_snippets.py fetch
    python script/issue_snippets.py extract
    python script/issue_snippets.py run --out before.json
    # change pylint or astroid here
    python script/issue_snippets.py run --out after.json
    python script/issue_snippets.py diff before.json after.json

``fetch`` needs ``gh``, the GitHub CLI. ``extract`` writes each Python code
block of each issue body as ``i<issue>_block<n>.py``. These are not verified:
some are error messages, pylint output or partial code. A snippet that imports a
library gives ``import-error`` until that library is installed.

Pylint reads the snippets and never runs them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_DIR = Path(".issue_snippets")
REPOSITORY = "pylint-dev/pylint"

CODE_BLOCK = re.compile(
    r"```[ \t]*(?:python3?|py)?[ \t]*\n(.*?)```", re.DOTALL | re.IGNORECASE
)
LOOKS_LIKE_CODE = re.compile(r"^\s*(def |class |import |from |\w+\s*=)", re.MULTILINE)
SNIPPET = re.compile(r"i(\d+)_block\d+\.py$")
MESSAGE = re.compile(r"^\d+:\d+:[\w-]+:")

PYLINT_ARGS = [
    "--rcfile=/dev/null",
    "--enable=all",
    "--persistent=n",
    "--score=n",
    "--msg-template={line}:{column}:{symbol}:{msg}",
]


def fetch(args: argparse.Namespace) -> None:
    """Download the open issues: number, title, labels and body."""
    output = subprocess.run(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            REPOSITORY,
            "--state",
            "open",
            "--limit",
            "5000",
            "--json",
            "number,title,labels,body",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    issues = sorted(json.loads(output), key=lambda issue: issue["number"])
    for issue in issues:
        issue["labels"] = sorted(label["name"] for label in issue["labels"])
    args.dir.mkdir(exist_ok=True)
    path = args.dir / "issues.json"
    path.write_text(json.dumps(issues, indent=1, ensure_ascii=False) + "\n", "utf-8")
    print(f"{len(issues)} open issues in {path}")


def extract(args: argparse.Namespace) -> None:
    """Write the Python code blocks of the fetched issues, one file each."""
    issues = json.loads((args.dir / "issues.json").read_text("utf-8"))
    snippets = args.dir / "snippets"
    snippets.mkdir(parents=True, exist_ok=True)
    for old in snippets.glob("i*_block*.py"):
        old.unlink()
    written = 0
    for issue in issues:
        if args.label and not set(args.label) & set(issue["labels"]):
            continue
        body = (issue["body"] or "").replace("\r\n", "\n")
        blocks = [b for b in CODE_BLOCK.findall(body) if LOOKS_LIKE_CODE.search(b)]
        for index, block in enumerate(blocks):
            path = snippets / f"i{issue['number']}_block{index}.py"
            path.write_text(block if block.endswith("\n") else block + "\n", "utf-8")
            written += 1
    print(f"{written} snippets written in {snippets}")


def normalize(output: str, folder: Path) -> list[str]:
    """Keep the messages, without what changes between runs."""
    lines = []
    for line in output.splitlines():
        if not MESSAGE.match(line):
            continue  # module headers and crash reports
        line = line.replace(f"{folder}{os.sep}", "").replace(str(folder), "")
        line = re.sub(r"pylint-crash-[\d-]+\.txt", "pylint-crash.txt", line)
        lines.append(re.sub(r" at 0x[0-9a-f]+", "", line))
    return lines


def lint(path: Path, args: argparse.Namespace, env: dict[str, str]) -> list[str]:
    try:
        result = subprocess.run(
            [args.python, "-m", "pylint", *PYLINT_ARGS, path.name],
            cwd=path.parent,
            env=env,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return ["TIMEOUT"]
    return normalize(result.stdout, path.parent)


def run(args: argparse.Namespace) -> None:
    """Lint every snippet and save the messages of each."""
    env = dict(os.environ)
    if args.pythonpath:
        env["PYTHONPATH"] = args.pythonpath
    versions = subprocess.run(
        [args.python, "-m", "pylint", "--version"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    snippets = (args.dir / "snippets").resolve()
    files = sorted(snippets.glob("i*_block*.py"), key=sort_key)
    with ThreadPoolExecutor(args.jobs) as pool:
        outputs = list(pool.map(lambda path: lint(path, args, env), files))
    results = {path.name: messages for path, messages in zip(files, outputs)}
    data = {"versions": versions, "snippets": results}
    Path(args.out).write_text(
        json.dumps(data, indent=1, ensure_ascii=False) + "\n", "utf-8"
    )
    print(f"{len(results)} snippets linted with:\n{versions}\nSaved in {args.out}")


def issue_number(name: str) -> int:
    match = SNIPPET.search(name)
    return int(match.group(1)) if match else 0


def sort_key(path: Path) -> tuple[int, str]:
    return issue_number(path.name), path.name


def diff(args: argparse.Namespace) -> None:
    """List the snippets whose messages differ between two runs."""
    old = json.loads(Path(args.old).read_text("utf-8"))
    new = json.loads(Path(args.new).read_text("utf-8"))
    titles = {}
    issues = args.dir / "issues.json"
    if issues.exists():
        titles = {
            i["number"]: i["title"] for i in json.loads(issues.read_text("utf-8"))
        }
    print(f"old:\n{old['versions']}\nnew:\n{new['versions']}\n")
    changed = 0
    for name in sorted(set(old["snippets"]) & set(new["snippets"]), key=issue_number):
        before, after = set(old["snippets"][name]), set(new["snippets"][name])
        if before == after:
            continue
        changed += 1
        number = issue_number(name)
        title = titles.get(number, "(closed or unknown)")
        print(f"== https://github.com/{REPOSITORY}/issues/{number} {title} [{name}]")
        for line in sorted(before - after):
            print(f"  - {line}")
        for line in sorted(after - before):
            print(f"  + {line}")
    only_one = set(old["snippets"]) ^ set(new["snippets"])
    print(f"\n{changed} snippets changed, {len(only_one)} only in one run")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dir", type=Path, default=DEFAULT_DIR, help="where issues and snippets go"
    )
    sub = parser.add_subparsers(required=True)
    sub.add_parser("fetch", help=fetch.__doc__).set_defaults(func=fetch)
    extract_parser = sub.add_parser("extract", help=extract.__doc__)
    extract_parser.add_argument(
        "--label",
        action="append",
        help="only issues with this label (repeat for several), e.g. 'Crash 💥'",
    )
    extract_parser.set_defaults(func=extract)
    run_parser = sub.add_parser("run", help=run.__doc__)
    run_parser.add_argument(
        "--python", default=sys.executable, help="interpreter with pylint installed"
    )
    run_parser.add_argument(
        "--pythonpath", help="put this first on the path, e.g. another astroid"
    )
    run_parser.add_argument("--out", required=True, help="JSON file to write")
    run_parser.add_argument("--jobs", type=int, default=4)
    run_parser.add_argument(
        "--timeout", type=int, default=180, help="seconds per snippet"
    )
    run_parser.set_defaults(func=run)
    diff_parser = sub.add_parser("diff", help=diff.__doc__)
    diff_parser.add_argument("old")
    diff_parser.add_argument("new")
    diff_parser.set_defaults(func=diff)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
