#!/usr/bin/env bash
# Refresh pr_queue_data.json for pr_queue.py.
#
# The combined `gh pr list` query times out on this repository, so each field
# set is fetched on its own and joined here. `action_required` names the runs a
# maintainer still has to release; a pull request with neither a run nor an
# entry there never got one at all, which is a different problem.
set -euo pipefail

REPO=pylint-dev/pylint
OWNER=Pierre-Sassoulas
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

retry() {
  local out=$1 fields=$2 i
  for i in 1 2 3 4; do
    gh pr list --repo "$REPO" --limit 100 --json "$fields" >"$TMP/$out" && return 0
    sleep 5
  done
  return 1
}

retry base.json number,author,title,createdAt,updatedAt,isDraft,labels,additions,deletions,changedFiles,reviewDecision,mergeable,headRefName,url
retry revs.json number,reviews
retry ci.json number,statusCheckRollup
retry meta.json number,closingIssuesReferences,comments

gh api "repos/$REPO/actions/runs?status=action_required&per_page=100" \
  --jq '[.workflow_runs[].head_branch] | unique' >"$TMP/pending.json"

# Linked issues, fetched one by one so labels and state_reason are current
# rather than whatever the issue snapshot held.
jq -r '[.[] | select(.author.login != "'"$OWNER"'") | .closingIssuesReferences[]?.number]
       | unique | .[]' "$TMP/meta.json" >"$TMP/linked.txt"
: >"$TMP/issues.ndjson"
while read -r n; do
  gh api "repos/$REPO/issues/$n" \
    --jq '{number, title, state, state_reason, labels: [.labels[].name], comments}' \
    >>"$TMP/issues.ndjson"
done <"$TMP/linked.txt"
jq -s '.' "$TMP/issues.ndjson" >"$TMP/issues.json"

OWNER="$OWNER" TMP="$TMP" HERE="$HERE" python3 - <<'PY'
import json, os, pathlib

tmp = pathlib.Path(os.environ["TMP"])
owner = os.environ["OWNER"]
load = lambda name: json.loads((tmp / name).read_text())

base = {p["number"]: p for p in load("base.json")}
revs = {p["number"]: p["reviews"] for p in load("revs.json")}
checks = {p["number"]: p["statusCheckRollup"] for p in load("ci.json")}
meta = {p["number"]: p for p in load("meta.json")}
pending = set(load("pending.json"))
maintainers = {"Pierre-Sassoulas", "DanielNoord", "jacobtylerwalls", "DudeNr33", "cdce8p"}


def ci_state(number):
    runs = checks.get(number) or []
    if base[number]["headRefName"] in pending:
        return "awaiting-approval", len(runs), 0
    failed = [r for r in runs if r.get("conclusion") in ("FAILURE", "TIMED_OUT")]
    # Fewer than six checks means the test matrix never reported: only the
    # always-on integrations (Read the Docs, pre-commit.ci) are present.
    if len(runs) <= 5:
        return "not-run", len(runs), 0
    if any(r.get("status") in ("IN_PROGRESS", "QUEUED") for r in runs):
        return "running", len(runs), len(failed)
    return ("failing" if failed else "green"), len(runs), len(failed)


rows = []
for number, pr in sorted(base.items()):
    if pr["author"]["login"] == owner:
        continue
    state, total, failed = ci_state(number)
    reviews = revs.get(number) or []
    comments = meta[number].get("comments") or []
    rows.append(
        {
            "n": number,
            "a": pr["author"]["login"],
            "t": pr["title"],
            "draft": pr["isDraft"],
            "size": pr["additions"] + pr["deletions"],
            "files": pr["changedFiles"],
            "created": pr["createdAt"][:10],
            "updated": pr["updatedAt"][:10],
            "labels": [label["name"] for label in pr["labels"]],
            "rd": pr["reviewDecision"] or "NONE",
            "merge": pr["mergeable"],
            "ci": state,
            "citot": total,
            "cifail": failed,
            "nrev": len(reviews),
            "mrev": sorted({r["author"]["login"] for r in reviews} & maintainers),
            "links": [
                [ref["number"], "", ""]
                for ref in (meta[number].get("closingIssuesReferences") or [])
            ],
            "lastcom": [comments[-1]["author"]["login"], comments[-1]["createdAt"][:10]]
            if comments
            else ["-", "-"],
        }
    )

out = {
    "snapshot": __import__("datetime").date.today().isoformat(),
    "owner": owner,
    "open_total": len(base),
    "open_own": sum(1 for p in base.values() if p["author"]["login"] == owner),
    "prs": rows,
    "issues": load("issues.json"),
}
path = pathlib.Path(os.environ["HERE"]) / "pr_queue_data.json"
path.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(f"{path}: {len(rows)} pull requests, {len(out['issues'])} linked issues")
PY

echo "now run: python3 $HERE/pr_queue.py"
