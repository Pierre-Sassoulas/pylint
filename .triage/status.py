"""Print roll-up of triage progress, counting only currently-open issues."""

import collections
import json

RAW = "/home/pierre/pylint/.triage/issues_raw.json"
STATE = "/home/pierre/pylint/.triage/triage_state.json"
with open(RAW) as f:
    issues = json.load(f)
with open(STATE) as f:
    state = json.load(f)

open_issues = {i["number"] for i in issues if i.get("state", "open") == "open"}
closed = [i["number"] for i in issues if i.get("state") == "closed"]
total = len(issues)
print(f"Total cached issues:  {total}")
print(f"  open:               {len(open_issues)}")
print(f"  closed since cache: {len(closed)}")
if closed:
    print(f"    closed: {sorted(closed, reverse=True)}")
print()
verdicts_open = {
    int(n): v for n, v in state["verdicts"].items() if int(n) in open_issues
}
print(f"Triaged open:         {len(verdicts_open)} / {len(open_issues)}")
print(f"Sessions:             {state.get('session_count', 0)}")
counts = collections.Counter(v["verdict"] for v in verdicts_open.values())
print("\nVerdict breakdown (open only):")
for v in ["DESIGN", "EXTDEP", "REPRO", "FIXED", "UNCLEAR", "DUP", "STALE"]:
    print(f"  {v:10s}  {counts.get(v, 0)}")
