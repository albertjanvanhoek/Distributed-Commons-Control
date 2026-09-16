#!/usr/bin/env python3
"""Deterministic paired interventions with identical attack paths and actuators."""
import argparse
import csv
import json
import sys
from dataclasses import replace
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from distributed_commons.feedback import FeedbackParameters, simulate_feedback


def experiments():
    ramp = [0.10]*20 + [0.10 + 0.02*k for k in range(1,26)] + [0.60]*30
    jump = [0.10]*20 + [0.60]*55
    base = FeedbackParameters()
    scenarios = [('bounded_ramp', ramp, base),
                 ('capacity_shortage', ramp, replace(base, capacity=0.015)),
                 ('unannounced_jump', jump, base),
                 ('common_mode_limit', ramp, replace(base, correlation=0.1))]
    for name, path, params in scenarios:
        for policy in ('fixed', 'private', 'reactive', 'robust'):
            rows = simulate_feedback(path, params, policy)
            yield dict(scenario=name, policy=policy, rounds=len(rows),
                       unsafe_rounds=sum(r['failure'] > params.safety_target + 1e-12 for r in rows),
                       certified_rounds=sum(r['certified'] is True for r in rows),
                       envelope_violations=sum(r['envelope_valid'] is False for r in rows),
                       max_failure=max(r['failure'] for r in rows),
                       total_added_effort=sum(r['effort_added'] for r in rows))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rows = list(experiments())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
    print(json.dumps(rows, indent=2))
