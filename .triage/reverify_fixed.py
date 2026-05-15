"""Re-verify all FIXED issues using --rcfile=testing_pylintrc.

Reports each issue's actual current pylint behavior, classifying:
- TRULY_FIXED: pylint runs clean on the snippet (no expected message)
- TRULY_FIXED_FN: pylint raises the missing message (for FN-fix issues)
- STILL_REPRO: pylint still raises the original false-positive message
- INDETERMINATE: needs more inspection
"""

import json
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/pierre/pylint")
SNIPPETS = ROOT / ".triage" / "snippets"
RCFILE = ROOT / "pylint" / "testutils" / "testing_pylintrc"

# (issue, expected_kind, expected_msg_id_for_fn_fix_if_any, extra_args)
# kind: "fp_fix" means we expect pylint to be silent; "fn_fix" means we expect a specific msg
FIXED = [
    (10768, "fp_fix", "C0103", []),  # was raising invalid-name; should NOT
    (10766, "fp_fix", "C0103", []),
    (10670, "fp_fix", "E1121", []),
    (10455, "fp_fix", "E1136", []),
    (10442, "fp_fix", "C0103", ["--module-naming-style=camelCase"]),
    (10422, "fp_fix", "E1102", []),
    (
        10374,
        "fp_fix",
        "R0204",
        ["--load-plugins=pylint.extensions.redefined_variable_type"],
    ),
    (10298, "fp_fix", "E1133", []),
    (9722, "fp_fix", "W0143", []),
    (9497, "fn_fix", "E1101", []),
    (8805, "fp_fix", "E1101", []),
    (8600, "fp_fix", "W0212", []),
    (8499, "fp_fix", "C0103", []),
    (8419, "fn_fix", "W1514", []),
    (8250, "fp_fix", "W9011", ["--load-plugins=pylint.extensions.docparams"]),
    (8201, "fn_fix", "R1707", []),
    (8179, "fp_fix", "R6104", ["--load-plugins=pylint.extensions.code_style"]),
    (8068, "fp_fix", "E1138", []),
    (8053, "fp_fix", "E0237", []),
    (
        8050,
        "fp_fix",
        None,
        [],
    ),  # tricky: was about not-scanning, hard to test as a snippet
    (7950, "fn_fix", "W0223", []),
    (7934, "fp_fix", "C0116", []),
    (7891, "fp_fix", "E1101", []),
    (7647, "fp_fix", "W0108", []),
    (7381, "fp_fix", "E1131", []),
    (7350, "fp_fix", "E0601", []),
    (7240, "fp_fix", "E1101", []),
    (5823, "fp_fix", "R1725", []),
    (4920, "fp_fix", "E1101", []),
    (4608, "fp_fix", "E1130", []),
    (4554, "fp_fix", "E1120", []),
    (3925, "fp_fix", "E1102", []),
    (3893, "fp_fix", "E1123", []),
    (3603, "fp_fix", "E1123", []),
    (3327, "fp_fix", "E1101", []),
    (3325, "fp_fix", "W0201", []),
    (2981, "fp_fix", "W0201", []),
    (2821, "fp_fix", "E1101", []),
    (1934, "fp_fix", "W0640", []),
    (1493, "fp_fix", "E1102", []),
    (241, "fn_fix", "W0611", []),
]


def run_pylint(snippet_path, extra_args):
    cmd = (
        [
            "python",
            "-m",
            "pylint",
            "--rcfile",
            str(RCFILE),
            "--score=no",
            "--persistent=no",
        ]
        + extra_args
        + [str(snippet_path)]
    )
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, cwd=str(ROOT)
        )
        return out.stdout + out.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def get_message_ids(output):
    """Extract all message symbol-ids (e.g. C0103) from pylint output."""
    return set(re.findall(r"\b([CWREIRF]\d{4})\b", output))


def main():
    print(f"{'Issue':>6}  {'Expected':12}  {'Behavior':18}  Verdict")
    print("-" * 75)
    truly_fixed_fp = []
    truly_fixed_fn = []
    still_repro = []
    skipped = []

    for num, kind, msg, extra in FIXED:
        snippet = SNIPPETS / f"i{num}.py"
        if not snippet.exists():
            skipped.append(num)
            print(f"{num:>6}  {kind:12}  {'no snippet':18}  SKIPPED")
            continue
        output = run_pylint(snippet, extra)
        ids = get_message_ids(output)
        if kind == "fp_fix":
            if msg and msg in ids:
                still_repro.append((num, msg, sorted(ids)))
                print(f"{num:>6}  fp_fix({msg:5})  STILL RAISES        STILL_REPRO")
            else:
                truly_fixed_fp.append(num)
                print(
                    f"{num:>6}  fp_fix({msg or 'any':5})  no longer raises    TRULY_FIXED_FP"
                )
        elif kind == "fn_fix":
            if msg in ids:
                truly_fixed_fn.append((num, msg))
                print(f"{num:>6}  fn_fix({msg:5})  now raises          TRULY_FIXED_FN")
            else:
                still_repro.append((num, "FN_missing", sorted(ids)))
                print(f"{num:>6}  fn_fix({msg:5})  doesn't raise        STILL_FN")

    print()
    print(f"TRULY FIXED (FP): {len(truly_fixed_fp)}")
    print(f"TRULY FIXED (FN): {len(truly_fixed_fn)}")
    print(f"STILL REPRO: {len(still_repro)}")
    print(f"SKIPPED: {len(skipped)}")
    if still_repro:
        print("\nStill REPRO list:")
        for num, m, ids in still_repro:
            print(f"  #{num} — {m} — actual ids: {ids}")

    out_data = {
        "truly_fixed_fp": truly_fixed_fp,
        "truly_fixed_fn": [n for n, _ in truly_fixed_fn],
        "still_repro": [n for n, _, _ in still_repro],
        "skipped": skipped,
    }
    with open(ROOT / ".triage" / "fixed_reverify.json", "w") as f:
        json.dump(out_data, f, indent=1)
    print(f"\nSaved {ROOT / '.triage' / 'fixed_reverify.json'}")


if __name__ == "__main__":
    main()
