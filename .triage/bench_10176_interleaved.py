"""Interleaved benchmark: alternate runs between main and takeover-10176.

A simple loop that runs N for each branch can drift due to system load
(thermal throttling, background tasks). Interleaving N/2 cycles of
(main, takeover, takeover-enabled) makes the comparison robust.
"""

from __future__ import annotations

import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv-takeover" / "bin" / "python"
TARGET = sys.argv[1] if len(sys.argv) > 1 else "pylint/checkers"
CYCLES = int(sys.argv[2]) if len(sys.argv) > 2 else 5


def run_once(extra_args: list[str]) -> float:
    cmd = [
        str(PYTHON),
        "-m",
        "pylint",
        TARGET,
        "--jobs=1",
        *extra_args,
    ]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    if proc.returncode not in (0, 1, 2, 4, 8, 16, 32):
        sys.stderr.write(f"unexpected return code {proc.returncode}\n")
        sys.stderr.write(proc.stderr[:500])
    return elapsed


def checkout(branch: str) -> None:
    subprocess.run(["git", "checkout", branch, "--quiet"], cwd=ROOT, check=True)


SCENARIOS = [
    ("main", "main", []),
    ("takeover-disabled", "takeover-10176", []),
    ("takeover-enabled", "takeover-10176", ["--enable=unguarded-typing-import"]),
]


def main() -> None:
    print(f"target: {TARGET}")
    print(f"cycles: {CYCLES}")
    print(f"scenarios: {[name for name, *_ in SCENARIOS]}")
    print()

    results: dict[str, list[float]] = {name: [] for name, *_ in SCENARIOS}

    # Warmup once per scenario
    print("warmups:")
    for name, branch, extra in SCENARIOS:
        checkout(branch)
        t = run_once(extra)
        print(f"  {name}: {t:.3f}s")
    print()

    for cycle in range(CYCLES):
        print(f"cycle {cycle + 1}/{CYCLES}:")
        for name, branch, extra in SCENARIOS:
            checkout(branch)
            t = run_once(extra)
            results[name].append(t)
            print(f"  {name}: {t:.3f}s", flush=True)
    print()

    print(f"{'scenario':<20}  {'min':>8}  {'median':>8}  {'mean':>8}  {'stdev':>8}")
    print("-" * 60)
    for name in results:
        ts = results[name]
        print(
            f"{name:<20}  "
            f"{min(ts):>7.3f}s  "
            f"{statistics.median(ts):>7.3f}s  "
            f"{statistics.mean(ts):>7.3f}s  "
            f"{statistics.stdev(ts):>7.3f}s"
        )

    base = statistics.median(results["main"])
    print()
    print("deltas vs main (median):")
    for name in results:
        med = statistics.median(results[name])
        pct = (med - base) / base * 100
        print(f"  {name:<20}: {med - base:+.3f}s ({pct:+.2f}%)")


if __name__ == "__main__":
    main()
