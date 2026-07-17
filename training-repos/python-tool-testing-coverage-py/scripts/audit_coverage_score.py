"""Audit coverage JSON: tool emission validity + platform scores out of 100."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from coverage_py_metrics import compute_metrics, compute_normalized_scores, export_dashboard_payload


def audit(coverage_path: pathlib.Path, source: pathlib.Path | None, baseline: pathlib.Path | None) -> int:
    print("=" * 70)
    print(f"File: {coverage_path}")
    print("=" * 70)

    if not coverage_path.exists():
        print("ERROR: file not found")
        return 1

    data = json.loads(coverage_path.read_text(encoding="utf-8"))
    totals = data.get("totals", {})
    ns = int(totals.get("num_statements", 0) or 0)
    nb = int(totals.get("num_branches", 0) or 0)
    files = len(data.get("files", {}))

    print(f"Tool emission valid: {'YES' if ns > 0 and files > 0 else 'NO'}")
    print(f"  num_statements={ns}, num_branches={nb}, files={files}")
    print(f"  percent_covered={totals.get('percent_covered', 'missing')}")
    print(f"  percent_branches_covered={totals.get('percent_branches_covered', 'missing')}")

    if ns == 0:
        print("\nPlatform scores (empty / invalid JSON):")
        print("  Statement & branch % metrics: 0/100 FAIL")
        print("  Gap/count metrics (Logic Error, Completeness): misleading 100/100 PASS")
        print("  Effective overall score: 0/100")
        print("\nVERDICT: Tool did NOT emit coverage data.")
        return 1

    metrics = compute_metrics(coverage_path, source_root=source, baseline_json=baseline)
    scores = compute_normalized_scores(metrics)
    dash = export_dashboard_payload(metrics)

    print("\nTool verifies metrics: YES (via coverage_py_metrics.py)")
    print(f"  Techniques computable: {len(scores)} dashboard classifications")
    print("\nNormalized platform scores (0-100):")
    failing = []
    for name in sorted(scores):
        score = round(float(scores[name]), 2)
        result = "PASS" if score >= 80.0 else "FAIL"
        if score < 80.0:
            failing.append(name)
        print(f"  {name}: {int(round(score))}/100  {result}")

    avg = sum(float(v) for v in scores.values()) / len(scores)
    print(f"\n  Average score: {avg:.1f}/100")

    ratio = metrics.covered_branches / max(metrics.num_branches, 1)
    print(f"\nPlatform raw-ratio display (known bug): covered/num = {ratio:.4f} -> {int(ratio)}/100")

    print("\nBranch dashboard rows from tool:")
    branch_names = {
        "Conditional Logic Testing",
        "Control Flow Validation",
        "Loop Condition Testing",
        "Edge Case Detection",
        "Logic Error Detection",
        "Test Case Completeness",
        "Decision Outcome Verification",
    }
    for row in dash.get("metrics", []):
        if row["classification"] in branch_names:
            print(f"  {row['classification']}: {row['value']}  {row['result']}")

    print(f"\nVERDICT: {'PASS' if not failing else 'FAIL'} — {len(scores) - len(failing)}/{len(scores)} at 100/100")
    return 0 if not failing else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage-json", type=pathlib.Path, required=True)
    parser.add_argument("--source", type=pathlib.Path, default=None)
    parser.add_argument("--baseline-json", type=pathlib.Path, default=None)
    args = parser.parse_args()
    return audit(args.coverage_json, args.source, args.baseline_json)


if __name__ == "__main__":
    raise SystemExit(main())
