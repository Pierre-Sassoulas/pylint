"""Fetch comments for each UNCLEAR issue and summarize."""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path("/home/pierre/pylint")

with open(ROOT / ".triage" / "triage_state.json") as f:
    state = json.load(f)

unclears = sorted(
    [int(n) for n, v in state["verdicts"].items() if v["verdict"] == "UNCLEAR"],
    reverse=True,
)

out_path = ROOT / ".triage" / "unclear_comments.json"
results = {}

for num in unclears:
    url = f"https://api.github.com/repos/pylint-dev/pylint/issues/{num}/comments"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "triage-script",
        },
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            comments = json.loads(resp.read())
        slim = [
            {
                "author": c["user"]["login"] if c.get("user") else None,
                "created_at": c["created_at"],
                "body": (c["body"] or "")[:2000],
            }
            for c in comments
        ]
        results[num] = slim
        print(f"#{num}: {len(slim)} comments")
    except urllib.error.HTTPError as e:
        print(f"#{num}: HTTP error {e.code}")
        results[num] = {"error": f"{e.code} {e.reason}"}
    time.sleep(0.5)

with open(out_path, "w") as f:
    json.dump(results, f, indent=1)
print(f"\nSaved to {out_path}")
