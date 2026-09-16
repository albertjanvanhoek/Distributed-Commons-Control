#!/usr/bin/env python3
"""Generate the exact static selected-versus-sufficient phase map."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from distributed_commons import assess_control_phase  # noqa: E402


def phase_map() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for monitors in (1, 3, 5, 9):
        for correlation in (0.0, 0.05, 0.15, 0.30, 0.50):
            for effort_cost in (0.10, 0.25, 0.50, 1.0, 2.0):
                assessment = assess_control_phase(
                    bad_attempt_rate=0.20,
                    monitors=monitors,
                    correlation=correlation,
                    safety_target=0.03,
                    monitor_reward=1.0,
                    effort_cost=effort_cost,
                )
                rows.append(
                    {
                        "monitors": monitors,
                        "correlation": correlation,
                        "effort_cost": effort_cost,
                        "phase": assessment.phase.value,
                        "required_effort": assessment.required_effort,
                        "selected_effort": assessment.selected_effort,
                        "effort_margin": assessment.effort_margin,
                        "correlation_floor": assessment.correlation_floor,
                        "selected_bad_finalization": (
                            assessment.selected_bad_finalization
                        ),
                        "critical_effort_cost": assessment.critical_effort_cost,
                    }
                )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = phase_map()

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    counts = Counter(str(row["phase"]) for row in rows)
    print(f"classified {len(rows)} parameter combinations")
    for phase, count in sorted(counts.items()):
        print(f"{phase}: {count}")


if __name__ == "__main__":
    main()
