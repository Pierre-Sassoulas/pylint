"""Run every issue snippet under two setups and list the issues whose output changed.

Use it before an astroid or pylint upgrade to find the open issues the upgrade
fixes (or breaks). Snippets come from two folders:

- ``.triage/snippets/``: hand-made reproductions, verified during triage.
  A helper module of ``iNNNN.py`` is ``iNNNN_<name>.py`` in the same folder.
- ``.triage/snippets_auto/``: code blocks extracted by ``extract`` from the open
  issues labeled "False Positive" or "False Negative" that have no hand-made
  snippet. Not verified: some are pylint output or partial code.

Typical use, comparing astroid 4.3.3 with 4.3.4 on one pylint checkout::

    python .triage/snippet_sweep.py fetch
    python .triage/snippet_sweep.py extract
    pip install --target /tmp/astroid-new --no-deps astroid==4.3.4
    python .triage/snippet_sweep.py run --python venv/bin/python --out /tmp/old.json
    python .triage/snippet_sweep.py run --python venv/bin/python \\
        --pythonpath /tmp/astroid-new --out /tmp/new.json
    python .triage/snippet_sweep.py diff /tmp/old.json /tmp/new.json

``diff .triage/snippet_baseline.json <new run>`` compares with the last recorded
baseline instead. A snippet that imports a library gives ``import-error`` until
that library is installed in the interpreter: ``LIBRARIES`` lists the ones the
baseline had.

Never pass ``-I`` to the interpreter: it drops ``PYTHONPATH``, so ``--pythonpath``
would be silently ignored.
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

TRIAGE = Path(__file__).resolve().parent
SNIPPETS = TRIAGE / "snippets"
SNIPPETS_AUTO = TRIAGE / "snippets_auto"
OPEN_ISSUES = TRIAGE / "sweep_open_issues.json"
BASELINE = TRIAGE / "snippet_baseline.json"

LABELS = ("False Positive 🦟", "False Negative 🦋")

# Libraries imported by the snippets; installed for the baseline.
LIBRARIES = (
    "numpy scipy pandas sqlalchemy pydantic flask attrs scikit-learn psycopg "
    "langchain-core marshmallow pyroute2 pyzmq pygments shapely gitpython wtforms "
    "flask-wtf statsmodels pytz geoip2 connexion django djangorestframework "
    "requests matplotlib kazoo temppathlib pyserial opencv-python-headless "
    "PySide6 pyspark torch"
).split()

EXTENSIONS = ",".join(
    f"pylint.extensions.{name}"
    for name in (
        "bad_builtin broad_try_clause check_elif code_style comparison_placement "
        "confusing_elif consider_refactoring_into_while_condition "
        "consider_ternary_expression dict_init_mutate docparams docstyle dunder "
        "empty_comment eq_without_hash for_any_all magic_value mccabe no_self_use "
        "overlapping_exceptions private_import redefined_loop_name "
        "redefined_variable_type set_membership typing while_used"
    ).split()
)

PYLINT_ARGS = [
    "--rcfile=/dev/null",
    "--enable=all",
    "--persistent=n",
    "--score=n",
    f"--load-plugins={EXTENSIONS}",
    "--msg-template={line}:{column}:{symbol}:{msg}",
]

CODE_BLOCK = re.compile(r"```[ \t]*(?:python3?|py)?[ \t]*\n(.*?)```", re.S | re.I)
LOOKS_LIKE_CODE = re.compile(r"^\s*(def |class |import |from |\w+\s*=)", re.M)
HAND_MADE = re.compile(r"i(\d+)\.py$")


def fetch(_args: argparse.Namespace) -> None:
    """Download the open issues (number, title, labels, body)."""
    out = subprocess.run(
        [
            "gh", "issue", "list", "--repo", "pylint-dev/pylint", "--state", "open",
            "--limit", "5000", "--json", "number,title,labels,body",
        ],
        check=True, capture_output=True, text=True,
    ).stdout
    issues = sorted(json.loads(out), key=lambda issue: issue["number"])
    for issue in issues:
        issue["labels"] = sorted(label["name"] for label in issue["labels"])
    OPEN_ISSUES.write_text(json.dumps(issues, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(issues)} open issues in {OPEN_ISSUES}")


def extract(_args: argparse.Namespace) -> None:
    """Write the code blocks of labeled issues without a hand-made snippet."""
    issues = json.loads(OPEN_ISSUES.read_text())
    hand_made = {int(m.group(1)) for p in SNIPPETS.iterdir() if (m := HAND_MADE.match(p.name))}
    SNIPPETS_AUTO.mkdir(exist_ok=True)
    for old in SNIPPETS_AUTO.glob("*.py"):
        old.unlink()
    written = 0
    for issue in issues:
        if issue["number"] in hand_made or not set(issue["labels"]) & set(LABELS):
            continue
        body = (issue["body"] or "").replace("\r\n", "\n")
        blocks = [b for b in CODE_BLOCK.findall(body) if LOOKS_LIKE_CODE.search(b)]
        for index, block in enumerate(blocks):
            path = SNIPPETS_AUTO / f"i{issue['number']}_block{index}.py"
            path.write_text(block if block.endswith("\n") else block + "\n")
            written += 1
    print(f"{written} snippets written in {SNIPPETS_AUTO}")


def snippet_files() -> list[Path]:
    """Every snippet to lint: hand-made ones (not their helpers) and extracted ones."""
    hand_made = [p for p in SNIPPETS.glob("i*.py") if HAND_MADE.match(p.name)]
    return sorted(hand_made) + sorted(SNIPPETS_AUTO.glob("i*.py"))


def normalize(output: str, path: Path) -> list[str]:
    """Drop what changes between runs: paths, crash file names, addresses."""
    lines = []
    for line in output.splitlines():
        if not re.match(r"^\d+:\d+:[\w-]+:", line):
            continue  # module headers and tracebacks
        line = line.replace(str(path.parent) + "/", "").replace(str(path.parent), "")
        line = re.sub(r"pylint-crash-[\d-]+\.txt", "pylint-crash.txt", line)
        lines.append(re.sub(r" at 0x[0-9a-f]+", "", line))
    return lines


def lint(path: Path, python: str, env: dict[str, str], timeout: int) -> list[str]:
    try:
        result = subprocess.run(
            [python, "-m", "pylint", *PYLINT_ARGS, path.name],
            cwd=path.parent, env=env, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return ["TIMEOUT"]
    return normalize(result.stdout, path)


def run(args: argparse.Namespace) -> None:
    """Lint every snippet and save the messages by snippet."""
    env = dict(os.environ)
    if args.pythonpath:
        env["PYTHONPATH"] = args.pythonpath
    versions = subprocess.run(
        [args.python, "-m", "pylint", "--version"],
        env=env, capture_output=True, text=True, check=True,
    ).stdout.strip()
    # A dev version does not say which commit was linted.
    pylint_dir = subprocess.run(
        [args.python, "-c", "import os, pylint; print(os.path.dirname(pylint.__file__))"],
        env=env, capture_output=True, text=True, check=True,
    ).stdout.strip()
    commit = subprocess.run(
        ["git", "-C", pylint_dir, "log", "-1", "--format=%h %s"],
        capture_output=True, text=True,
    ).stdout.strip()
    if commit:
        versions = f"{versions}\npylint commit {commit}"
    files = snippet_files()
    with ThreadPoolExecutor(args.jobs) as pool:
        outputs = pool.map(lambda p: lint(p, args.python, env, args.timeout), files)
        results = {
            str(path.relative_to(TRIAGE)): messages
            for path, messages in zip(files, outputs)
        }
    data = {"versions": versions, "snippets": results}
    Path(args.out).write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(results)} snippets linted with:\n{versions}\nSaved in {args.out}")


def issue_number(snippet: str) -> int:
    return int(re.search(r"i(\d+)", snippet).group(1))


def diff(args: argparse.Namespace) -> None:
    """List the snippets whose messages differ between two runs."""
    old, new = (json.loads(Path(p).read_text()) for p in (args.old, args.new))
    titles = {}
    if OPEN_ISSUES.exists():
        titles = {i["number"]: i["title"] for i in json.loads(OPEN_ISSUES.read_text())}
    print(f"old:\n{old['versions']}\nnew:\n{new['versions']}\n")
    changed = 0
    for snippet in sorted(set(old["snippets"]) | set(new["snippets"]), key=issue_number):
        before = old["snippets"].get(snippet)
        after = new["snippets"].get(snippet)
        if before == after or before is None or after is None:
            continue
        changed += 1
        number = issue_number(snippet)
        print(f"== #{number} {titles.get(number, '(closed or unknown)')}  [{snippet}]")
        for line in sorted(set(before) - set(after)):
            print(f"  - {line}")
        for line in sorted(set(after) - set(before)):
            print(f"  + {line}")
    missing = set(old["snippets"]) ^ set(new["snippets"])
    print(f"\n{changed} snippets changed, {len(missing)} only in one run")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(required=True)
    sub.add_parser("fetch", help=fetch.__doc__).set_defaults(func=fetch)
    sub.add_parser("extract", help=extract.__doc__).set_defaults(func=extract)
    run_parser = sub.add_parser("run", help=run.__doc__)
    run_parser.add_argument("--python", default=sys.executable, help="interpreter with pylint")
    run_parser.add_argument("--pythonpath", help="put this first, e.g. another astroid")
    run_parser.add_argument("--out", required=True)
    run_parser.add_argument("--jobs", type=int, default=3, help="3 fits in 15 GB with torch")
    run_parser.add_argument("--timeout", type=int, default=180)
    run_parser.set_defaults(func=run)
    diff_parser = sub.add_parser("diff", help=diff.__doc__)
    diff_parser.add_argument("old")
    diff_parser.add_argument("new")
    diff_parser.set_defaults(func=diff)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
