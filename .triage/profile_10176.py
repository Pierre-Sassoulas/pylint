"""Profile a single pylint run with cProfile and surface relevant hot paths.

Wall-clock benchmarks on pylint runs have ~1s stdev on this box, drowning
out the changes in PR #10176. Profile each branch instead and compare
cumulative time spent in:
  - is_node_in_type_annotation_context  (new call on every consumption)
  - NamesConsumer.mark_as_consumed      (modified to track consumed_as_type)
  - VariablesChecker._check_consumer    (caller of the above)
  - VariablesChecker._check_imports     (signature changed)
  - VariablesChecker._check_type_imports (new method)
"""

from __future__ import annotations

import cProfile
import pstats
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = sys.argv[1] if len(sys.argv) > 1 else "pylint/checkers"
EXTRA_ARGS = sys.argv[2:]


def run_pylint() -> None:
    # Run pylint in-process so cProfile sees the actual work.
    from pylint.lint import Run

    args = [
        TARGET,
        "--jobs=1",
        *EXTRA_ARGS,
    ]
    try:
        Run(args)
    except SystemExit:
        pass


def main() -> None:
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
    ).strip()
    out_path = ROOT / ".triage" / f"profile_{branch.replace('/', '_')}.prof"
    print(f"branch: {branch}")
    print(f"target: {TARGET}")
    print(f"extra args: {EXTRA_ARGS}")
    print(f"writing: {out_path}")
    print()

    profiler = cProfile.Profile()
    profiler.enable()
    run_pylint()
    profiler.disable()
    profiler.dump_stats(str(out_path))

    stats = pstats.Stats(profiler).sort_stats("cumulative")
    print("Top 30 cumulative:")
    stats.print_stats(30)

    print()
    print("Functions of interest:")
    interest = [
        "is_node_in_type_annotation_context",
        "mark_as_consumed",
        "_check_consumer",
        "get_next_to_consume",
        "_check_imports",
        "_check_type_imports",
        "visit_name",
    ]
    stats_dict = stats.stats  # type: ignore[attr-defined]
    rows = []
    for (file, lineno, func), (cc, nc, tt, ct, _) in stats_dict.items():
        for needle in interest:
            if needle in func:
                rows.append((func, file, lineno, nc, tt, ct))
                break
    rows.sort(key=lambda r: r[5], reverse=True)
    print(f"{'function':<45}  {'calls':>10}  {'tottime':>10}  {'cumtime':>10}")
    print("-" * 85)
    for func, file, lineno, nc, tt, ct in rows:
        short_file = Path(file).name
        print(
            f"{func + f' ({short_file}:{lineno})':<45}  "
            f"{nc:>10}  {tt:>10.4f}  {ct:>10.4f}"
        )


if __name__ == "__main__":
    main()
