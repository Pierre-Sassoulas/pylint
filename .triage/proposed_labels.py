"""Labels proposed during a triage pass, before Pierre applies them on GitHub.

One "update" run has to categorize first and prioritize second. The ranking
reads labels (crash, bug, false positive...), so a pull request or issue that
has no label yet would rank last until the labels are applied and the page is
rendered again. Instead, the pass writes its label proposals to
``proposed_labels.json`` and both renderers merge them into the fetched data
before ranking. The page then lists the ``gh`` commands that apply them.

File format::

    {"pylint": {"11826": {"kind": "pr", "labels": ["Documentation :green_book:"]}},
     "astroid": {"3474": {"kind": "pr", "labels": ["Bug 🪳", "Brain 🧠"]}}}

``kind`` is ``pr`` or ``issue``. Run ``python3 .triage/proposed_labels.py --prune``
after a fetch (the refresh does it) to drop the entries whose labels are all on
GitHub by now; the renderers also skip labels already present in their data.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
FILE = HERE / "proposed_labels.json"


def load() -> dict[str, dict[str, dict]]:
    if not FILE.exists():
        return {"pylint": {}, "astroid": {}}
    data = json.loads(FILE.read_text())
    data.setdefault("pylint", {})
    data.setdefault("astroid", {})
    return data


def save(data: dict) -> None:
    FILE.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True))


def merge(repo: str, number: int, labels: list[str]) -> list[str]:
    """Return ``labels`` plus the proposed labels for this item, without duplicates."""
    entry = load()[repo].get(str(number))
    if not entry:
        return labels
    return labels + [name for name in entry["labels"] if name not in labels]


def pending(repo: str, known: dict[int, list[str]]) -> list[tuple[int, str, list[str]]]:
    """Proposals not yet applied, as (number, kind, missing labels).

    ``known`` maps item numbers to the labels the fetched data already shows on
    GitHub; items absent from it are listed in full.
    """
    out = []
    for key, entry in sorted(load()[repo].items(), key=lambda kv: int(kv[0])):
        have = known.get(int(key), [])
        missing = [name for name in entry["labels"] if name not in have]
        if missing:
            out.append((int(key), entry["kind"], missing))
    return out


def command(repo: str, number: int, kind: str, labels: list[str]) -> str:
    verb = "pr" if kind == "pr" else "issue"
    return f'gh {verb} edit {number} -R pylint-dev/{repo} --add-label "{",".join(labels)}"'


def prune() -> None:
    """Drop proposals whose labels are all on GitHub now (read-only ``gh`` calls)."""
    data = load()
    for repo, entries in data.items():
        for key in list(entries):
            kind = "pr" if entries[key]["kind"] == "pr" else "issue"
            result = subprocess.run(
                ["gh", kind, "view", key, "-R", f"pylint-dev/{repo}", "--json", "labels,state"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                print(f"{repo} {key}: gh failed, kept", file=sys.stderr)
                continue
            info = json.loads(result.stdout)
            have = {label["name"] for label in info["labels"]}
            if set(entries[key]["labels"]) <= have or info["state"] != "OPEN":
                del entries[key]
                print(f"{repo} {key}: applied or closed, dropped")
    save(data)


if __name__ == "__main__":
    if "--prune" in sys.argv:
        prune()
    for repo in ("pylint", "astroid"):
        for number, kind, labels in pending(repo, {}):
            print(command(repo, number, kind, labels))
