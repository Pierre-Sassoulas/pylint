"""Record a verdict for an issue."""

import datetime
import json
import sys

STATE = "/home/pierre/pylint/.triage/triage_state.json"


def record(num, verdict, note, session=None):
    with open(STATE) as f:
        state = json.load(f)
    state["verdicts"][str(num)] = {
        "verdict": verdict,
        "note": note,
        "session": session or state.get("session_count", 0),
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    with open(STATE, "w") as f:
        json.dump(state, f, indent=1)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: record.py NUM VERDICT NOTE [SESSION]")
        sys.exit(1)
    num = sys.argv[1]
    verdict = sys.argv[2]
    note = sys.argv[3]
    session = int(sys.argv[4]) if len(sys.argv) > 4 else None
    record(num, verdict, note, session)
    print(f"recorded #{num} = {verdict}")
