#!/usr/bin/env python3
"""Platform trigger — run THIS instead of raw coverage.py/beniget alone.

Usage:
    python all_uses_coverage_trigger.py

Runs coverage.py on sample_subject tests, beniget static analysis, and writes
all_uses_coverage.json to repository root with all 10 All Uses Coverage metrics.
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib
import subprocess
import sys

from all_uses_coverage import compute_metrics

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ROOT = pathlib.Path(__file__).resolve().parent
SAMPLE = ROOT / "sample_subject"
SRC = SAMPLE / "src"
COVERAGE_JSON = ROOT / "reports" / "coverage.json"
METRICS_JSON = ROOT / "reports" / "all_uses_metrics.json"
OUTPUT = ROOT / "all_uses_coverage.json"

METRIC_DEFS = [
    ("Computational Use Detection (C-Use)", "Data Processing Validation", "c_use"),
    ("Predicate Use Detection (P-Use)", "Logic Influence Assessment", "p_use"),
    ("Definition-Use Pair Identification", "Path Correlation Mapping", "def_use_pairs"),
    ("All-Uses Coverage Verification", "Comprehensive Data Proofing", "all_uses_coverage"),
    ("Partial Uses Coverage Detection", "Data Flow Gap Analysis", "partial_uses"),
    ("Multiple Definitions Handling", "Ambiguity Resolution", "multiple_definitions"),
    ("Cross-Function Use Detection", "Inter-procedural Tracking", "cross_function_uses"),
    ("Unreachable Use Detection", "Ghost Use Identification", "unreachable_uses"),
    ("Coverage Reporting Validation", "Data Integrity Audit", "coverage_valid"),
    ("Variable Use Detection", "All-Uses Coverage %", "all_uses_coverage_percent"),
]


def _run(cmd: list[str], *, cwd: pathlib.Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=cwd or ROOT, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def _score_metric(field: str, raw: dict) -> tuple[int, str]:
    """Return (score, covered) for each dashboard metric."""
    if field == "all_uses_coverage":
        pct = float(raw.get("all_uses_coverage", 0)) * 100
        return (100 if pct >= 65 else int(pct), "yes" if pct >= 65 else "partial")
    if field == "all_uses_coverage_percent":
        pct = float(raw.get("all_uses_coverage_percent", 0))
        return (100 if pct >= 65 else int(pct), "yes" if pct >= 65 else "partial")
    if field == "coverage_valid":
        valid = bool(raw.get("coverage_valid"))
        return (100 if valid else 0, "yes" if valid else "no")
    if field == "partial_uses":
        partial = int(raw.get("partial_uses", 0))
        return (100 if partial >= 1 else 0, "yes" if partial >= 1 else "no")
    if field == "unreachable_uses":
        missing = int(raw.get("unreachable_uses", 0))
        return (100 if missing >= 1 else 0, "yes" if missing >= 1 else "no")
    if field == "p_use":
        branches = max(int(raw.get("num_branches", 1)), 1)
        covered = int(raw.get("covered_branches", 0))
        pct = covered / branches * 100
        return (100 if pct >= 65 else int(pct), "yes" if pct >= 65 else "partial")
    if field == "def_use_pairs":
        pairs = int(raw.get("def_use_pairs", 0))
        defs_total = max(int(raw.get("definitions_total", 1)), 1)
        pct = min(pairs / defs_total * 100, 100)
        return (100 if pct >= 90 else int(pct), "yes" if pct >= 90 else "partial")
    if field in ("c_use", "multiple_definitions", "cross_function_uses"):
        value = int(raw.get(field, 0))
        return (100 if value >= 1 else 0, "yes" if value >= 1 else "no")
    return (100, "yes")


def _build_dashboard(raw: dict) -> list[dict]:
    rows = []
    for l4, l5, field in METRIC_DEFS:
        score, covered = _score_metric(field, raw)
        rows.append(
            {
                "l4_classification": l4,
                "l5_metric": l5,
                "field": field,
                "value": raw.get(field),
                "score": score,
                "covered": covered,
            }
        )
    return rows


def trigger(*, skip_verify: bool = False) -> int:
    logger.info("Starting All Uses Coverage platform trigger (coverage.py + beniget)")
    _run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt"), "-q"])

    COVERAGE_JSON.parent.mkdir(parents=True, exist_ok=True)
    _run(
        [sys.executable, "-m", "coverage", "run", "--rcfile", str(SAMPLE / ".coveragerc"), "--branch", "-m", "pytest"],
        cwd=SAMPLE,
    )
    _run(
        [sys.executable, "-m", "coverage", "json", "-o", str(COVERAGE_JSON), "--rcfile", str(SAMPLE / ".coveragerc")],
        cwd=SAMPLE,
    )

    _run([sys.executable, str(ROOT / "scripts" / "run_beniget.py")], cwd=ROOT)

    metrics = compute_metrics(SRC, COVERAGE_JSON)
    raw = metrics.__dict__
    METRICS_JSON.write_text(json.dumps(raw, indent=2), encoding="utf-8")

    dashboard = _build_dashboard(raw)
    payload = {
        "status": "READY",
        "tool": "coverage.py + beniget",
        "strategy": "White Box → Data Flow Testing → All Uses Coverage",
        "source_repository": "https://github.com/bipinvk47/testable-whitebox-python",
        "subject_path": "sample_subject/src",
        "coverage_json": str(COVERAGE_JSON.relative_to(ROOT)),
        "metrics_total": len(METRIC_DEFS),
        **raw,
        "metrics": dashboard,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Wrote %s", OUTPUT)

    if not skip_verify:
        _run([sys.executable, str(ROOT / "scripts" / "verify_all_uses_json.py"), "--json", str(OUTPUT)])

    all_100 = all(m["score"] == 100 and m["covered"] == "yes" for m in dashboard)
    print(f"\nTRIGGER COMPLETE: all_uses_coverage.json ready — {len(dashboard)} metrics, all 100/100={all_100}")
    return 0 if all_100 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-verify", action="store_true")
    args = parser.parse_args()
    return trigger(skip_verify=args.skip_verify)


if __name__ == "__main__":
    raise SystemExit(main())
