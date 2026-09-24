"""Benchmark PR #10176 (unguarded-typing-import) overhead on main vs takeover-10176.

The new check is opt-in (default_enabled=False), but the bookkeeping in
NamesConsumer (consumed_as_type) and the call to
``is_node_in_type_annotation_context`` on every name resolution run
unconditionally, so even disabled-by-default users may pay overhead.

Strategy:
- Run pylint on a fixed target with --jobs=1 and a stable config
- Warm up once per branch, then time N iterations
- Compare median and mean wall-clock time
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
ITERATIONS = int(sys.argv[2]) if len(sys.argv) > 2 else 5
EXTRA_ARGS = sys.argv[3:]  # e.g. --enable=unguarded-typing-import


def run_once() -> float:
    # Default config so VariablesChecker is fully active. The new tracking
    # (consumed_as_type / is_node_in_type_annotation_context) runs whenever
    # a name is resolved, regardless of whether unguarded-typing-import is
    # enabled, so the realistic benchmark uses the default config.
    cmd = [
        str(PYTHON),
        "-m",
        "pylint",
        TARGET,
        "--jobs=1",
        *EXTRA_ARGS,
    ]
    start = time.perf_counter()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    # Pylint returns non-zero on warnings/errors; that's expected.
    if proc.returncode not in (0, 1, 2, 4, 8, 16, 32):
        sys.stderr.write(f"unexpected return code {proc.returncode}\n")
        sys.stderr.write(proc.stderr[:500])
    return elapsed


def main() -> None:
    head = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
    ).strip()
    print(f"branch: {head}")
    print(f"target: {TARGET}")
    print(f"iterations: {ITERATIONS} (plus 1 warmup)")
    print(f"extra args: {EXTRA_ARGS}")
    print()

    print("warmup ...", flush=True)
    run_once()

    times: list[float] = []
    for i in range(ITERATIONS):
        t = run_once()
        times.append(t)
        print(f"  run {i + 1}: {t:.3f}s", flush=True)

    print()
    print(f"min:    {min(times):.3f}s")
    print(f"median: {statistics.median(times):.3f}s")
    print(f"mean:   {statistics.mean(times):.3f}s")
    print(f"stdev:  {statistics.stdev(times):.3f}s")
    print(f"max:    {max(times):.3f}s")


if __name__ == "__main__":
    main()
