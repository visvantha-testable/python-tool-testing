#!/usr/bin/env python3
"""Verify all_uses_coverage.json has all 10 metrics at 100/100."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REQUIRED_FIELDS = [
    "c_use",
    "p_use",
    "def_use_pairs",
    "all_uses_coverage",
    "partial_uses",
    "multiple_definitions",
    "cross_function_uses",
    "unreachable_uses",
    "coverage_valid",
    "all_uses_coverage_percent",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=pathlib.Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.json.read_text(encoding="utf-8"))
    if data.get("status") != "READY":
        print(f"FAIL: status={data.get('status')!r}, expected READY", file=sys.stderr)
        return 1

    for field in REQUIRED_FIELDS:
        if field not in data:
            print(f"FAIL: missing root field {field!r}", file=sys.stderr)
            return 1

    metrics = data.get("metrics", [])
    if len(metrics) != 10:
        print(f"FAIL: expected 10 metrics, got {len(metrics)}", file=sys.stderr)
        return 1

    failures = []
    for m in metrics:
        if m.get("score") != 100 or m.get("covered") != "yes":
            failures.append(m.get("l4_classification"))

    if failures:
        print(f"FAIL: metrics not at 100/100: {failures}", file=sys.stderr)
        return 1

    print("OK: all_uses_coverage.json verified — 10/10 metrics at 100/100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
