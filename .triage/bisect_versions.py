"""Bisect across pylint versions to find when each FIXED issue was actually fixed.

Creates a temporary venv per version, installs pylint==X.Y.Z, runs all
snippets, captures which messages fire. Cross-correlates to find the
introduction version.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/home/pierre/pylint")
SNIPPETS = ROOT / ".triage" / "snippets"
RCFILE = ROOT / "pylint" / "testutils" / "testing_pylintrc"

# Coarse bisect — major minor versions
VERSIONS = [
    "2.6.0",
    "2.10.0",
    "2.13.0",
    "2.15.0",
    "2.17.0",
    "3.0.0",
    "3.1.0",
    "3.2.0",
    "3.3.0",
    "4.0.0",
    "4.0.5",
]

# (issue, expected_msg_id, extra_args, kind)
FIXED_ISSUES = [
    (10670, "E1121", [], "fp"),
    (10455, "E1136", [], "fp"),
    (10442, "C0103", ["--module-naming-style=camelCase"], "fp"),
    (10422, "E1102", [], "fp"),
    (
        10374,
        "R0204",
        ["--load-plugins=pylint.extensions.redefined_variable_type"],
        "fp",
    ),
    (10298, "E1133", [], "fp"),
    (9722, "W0143", [], "fp"),
    (9497, "E1101", [], "fn"),
    (8805, "E1101", [], "fp"),
    (8419, "W1514", [], "fn"),
    (8250, "W9011", ["--load-plugins=pylint.extensions.docparams"], "fp"),
    (8179, "R6104", ["--load-plugins=pylint.extensions.code_style"], "fp"),
    (8068, "E1138", [], "fp"),
    (8053, "E0237", [], "fp"),
    (8050, None, [], "fp"),
    (7891, "E1101", [], "fp"),
    (7647, "W0108", [], "fp"),
    (7381, "E1131", [], "fp"),
    (7350, "E0601", [], "fp"),
    (7240, "E1101", [], "fp"),
    (5823, "R1725", [], "fp"),
    (4920, "E1101", [], "fp"),
    (4608, "E1130", [], "fp"),
    (4554, "E1120", [], "fp"),
    (3925, "E1102", [], "fp"),
    (3893, "E1123", [], "fp"),
    (3603, "E1123", [], "fp"),
    (3327, "E1101", [], "fp"),
    (2981, "W0201", [], "fp"),
    (2821, "E1101", [], "fp"),
    (1934, "W0640", [], "fp"),
    (1493, "E1102", [], "fp"),
]


def install_pylint_at(venv_dir, version):
    """Create a venv and install pylint==version + compatible astroid."""
    if not venv_dir.exists():
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            check=True,
            capture_output=True,
        )
    pip = venv_dir / "bin" / "pip"
    # Install pylint at the requested version; it should pull a compatible astroid
    res = subprocess.run(
        [str(pip), "install", "--quiet", f"pylint=={version}"],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if res.returncode != 0:
        return False, res.stderr[:200]
    return True, "ok"


def run_pylint_in(venv_dir, snippet, extra):
    pylint_bin = venv_dir / "bin" / "pylint"
    if not pylint_bin.exists():
        return ""
    cmd = (
        [
            str(pylint_bin),
            "--rcfile",
            str(RCFILE),
            "--score=no",
            "--persistent=no",
        ]
        + extra
        + [str(snippet)]
    )
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return out.stdout + out.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def get_ids(output):
    return set(re.findall(r"\b([CWREIRF]\d{4})\b", output))


def main(target_issues=None):
    """If target_issues given (list of ints), only bisect those."""
    if target_issues:
        issues_to_test = [it for it in FIXED_ISSUES if it[0] in target_issues]
    else:
        issues_to_test = FIXED_ISSUES

    tmpdir = Path(tempfile.mkdtemp(prefix="pylint_bisect_"))
    print(f"Using temp dir: {tmpdir}")
    results = {}  # {issue: {version: behavior}}

    try:
        for version in VERSIONS:
            print(f"\n=== Installing pylint {version} ===", flush=True)
            venv_dir = tmpdir / f"venv_{version}"
            ok, msg = install_pylint_at(venv_dir, version)
            if not ok:
                print(f"  install failed: {msg}", flush=True)
                continue
            for num, msg_id, extra, kind in issues_to_test:
                snippet = SNIPPETS / f"i{num}.py"
                if not snippet.exists():
                    continue
                output = run_pylint_in(venv_dir, snippet, extra)
                ids = get_ids(output)
                if kind == "fp":
                    behavior = "FP-fires" if (msg_id and msg_id in ids) else "clean"
                else:  # fn
                    behavior = "detects" if msg_id in ids else "misses"
                results.setdefault(num, {})[version] = behavior
                print(f"  #{num}: {behavior}", flush=True)

        # Save
        with open(ROOT / ".triage" / "bisect_results.json", "w") as f:
            json.dump(results, f, indent=1)
        print(f"\nSaved results to {ROOT / '.triage' / 'bisect_results.json'}")

        # Print summary table
        print("\n## Bisect summary\n")
        header = "Issue  | " + " | ".join(VERSIONS)
        print(header)
        print("-" * len(header))
        for num in sorted(results.keys(), reverse=True):
            row = [f"#{num:5d}"] + [results[num].get(v, "??")[:9] for v in VERSIONS]
            print(" | ".join(row))
    finally:
        # Don't delete — useful for debugging
        print(f"\nKept temp dir at {tmpdir} (delete manually with: rm -rf {tmpdir})")


if __name__ == "__main__":
    main()
