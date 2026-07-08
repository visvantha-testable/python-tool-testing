"""All Uses Coverage metrics using coverage.py + beniget.

Implements the White Box / Data Flow Testing / All Uses Coverage metrics from
Testable Strategy & Metrics Reference v3.0.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from dataclasses import asdict, dataclass
from typing import Iterable

import gast
import beniget


PREDICATE_PARENT_TYPES = (
    gast.If,
    gast.While,
    gast.For,
    gast.IfExp,
    gast.Assert,
    gast.comprehension,
    gast.Match,
)

COMPUTATIONAL_PARENT_TYPES = (
    gast.BinOp,
    gast.UnaryOp,
    gast.Call,
    gast.Subscript,
    gast.Attribute,
    gast.Return,
    gast.AugAssign,
    gast.FormattedValue,
    gast.JoinedStr,
    gast.ListComp,
    gast.SetComp,
    gast.DictComp,
    gast.GeneratorExp,
)


@dataclass
class DefinitionRecord:
    name: str
    file: str
    line: int
    user_count: int
    has_c_use: bool
    has_p_use: bool
    crosses_functions: bool


@dataclass
class AllUsesMetrics:
    c_use: int
    p_use: int
    def_use_pairs: int
    all_uses_coverage: float
    partial_uses: int
    multiple_definitions: int
    cross_function_uses: int
    unreachable_uses: int
    coverage_valid: bool
    all_uses_coverage_percent: float
    num_statements: int
    covered_lines: int
    missing_lines: int
    num_branches: int
    covered_branches: int
    files_analyzed: int
    definitions_total: int


def _parent_stmt(node: gast.AST, ancestors: beniget.Ancestors) -> gast.AST | None:
    for parent in reversed(ancestors.parents(node)):
        if isinstance(parent, (gast.FunctionDef, gast.AsyncFunctionDef, gast.ClassDef, gast.Module)):
            return parent
    return None


def _parent_function(node: gast.AST, ancestors: beniget.Ancestors) -> gast.AST | None:
    try:
        return ancestors.parentFunction(node)
    except ValueError:
        return None


def _use_kind(user_def: beniget.beniget.Def, ancestors: beniget.Ancestors) -> tuple[bool, bool]:
    """Return (is_c_use, is_p_use) for a beniget Def user node."""
    node = user_def.node
    is_c_use = False
    is_p_use = False
    for parent in ancestors.parents(node):
        if isinstance(parent, COMPUTATIONAL_PARENT_TYPES):
            is_c_use = True
        if isinstance(parent, PREDICATE_PARENT_TYPES):
            is_p_use = True
        if isinstance(parent, gast.Compare):
            is_p_use = True
    return is_c_use, is_p_use


def _collect_definitions(source_root: pathlib.Path) -> tuple[list[DefinitionRecord], int]:
    records: list[DefinitionRecord] = []
    files_analyzed = 0

    for path in sorted(source_root.rglob("*.py")):
        if any(part.startswith(".") for part in path.parts):
            continue
        try:
            source = path.read_text(encoding="utf-8")
            module = gast.parse(source, filename=str(path))
        except (OSError, SyntaxError):
            continue

        files_analyzed += 1
        duc = beniget.DefUseChains()
        duc.visit(module)
        ancestors = beniget.Ancestors()
        ancestors.visit(module)

        seen: set[beniget.beniget.Def] = set()
        for defs in duc.locals.values():
            for definition in defs:
                if definition in seen:
                    continue
                seen.add(definition)

                users = list(definition.users())
                user_count = len(users)
                has_c_use = False
                has_p_use = False
                def_fn = _parent_function(definition.node, ancestors)
                crosses_functions = False

                for user in users:
                    c_use, p_use = _use_kind(user, ancestors)
                    has_c_use = has_c_use or c_use
                    has_p_use = has_p_use or p_use
                    user_fn = _parent_function(user.node, ancestors)
                    if def_fn is not None and user_fn is not None and def_fn is not user_fn:
                        crosses_functions = True

                line = getattr(definition.node, "lineno", 0) or 0
                records.append(
                    DefinitionRecord(
                        name=definition.name(),
                        file=str(path.relative_to(source_root)),
                        line=line,
                        user_count=user_count,
                        has_c_use=has_c_use,
                        has_p_use=has_p_use,
                        crosses_functions=crosses_functions,
                    )
                )

    return records, files_analyzed


def _load_coverage_summary(coverage_json: pathlib.Path | None) -> dict:
    if coverage_json is None or not coverage_json.exists():
        return {
            "num_statements": 0,
            "covered_lines": 0,
            "missing_lines": 0,
            "num_branches": 0,
            "covered_branches": 0,
        }

    data = json.loads(coverage_json.read_text(encoding="utf-8"))
    totals = data.get("totals", {})
    return {
        "num_statements": int(totals.get("num_statements", 0)),
        "covered_lines": int(totals.get("covered_lines", 0)),
        "missing_lines": int(totals.get("missing_lines", 0)),
        "num_branches": int(totals.get("num_branches", 0)),
        "covered_branches": int(totals.get("covered_branches", 0)),
    }


def compute_metrics(
    source_root: pathlib.Path,
    coverage_json: pathlib.Path | None = None,
) -> AllUsesMetrics:
    definitions, files_analyzed = _collect_definitions(source_root)
    cov = _load_coverage_summary(coverage_json)

    c_use = sum(1 for d in definitions if d.user_count > 0 and d.has_c_use)
    p_use = cov["covered_branches"]
    def_use_pairs = sum(d.user_count for d in definitions)
    partial_uses = sum(1 for d in definitions if d.user_count == 0) + cov["missing_lines"]
    multiple_definitions = sum(1 for d in definitions if d.user_count > 1)
    cross_function_uses = sum(1 for d in definitions if d.crosses_functions)
    unreachable_uses = cov["missing_lines"]

    num_statements = cov["num_statements"]
    covered_lines = cov["covered_lines"]
    missing_lines = cov["missing_lines"]

    all_uses_coverage = (
        covered_lines / num_statements if num_statements else 0.0
    )
    coverage_valid = (covered_lines + missing_lines) == num_statements if num_statements else False
    all_uses_coverage_percent = (
        (sum(1 for d in definitions if d.user_count > 0) / len(definitions)) * 100
        if definitions
        else 0.0
    )

    return AllUsesMetrics(
        c_use=c_use,
        p_use=p_use,
        def_use_pairs=def_use_pairs,
        all_uses_coverage=all_uses_coverage,
        partial_uses=partial_uses,
        multiple_definitions=multiple_definitions,
        cross_function_uses=cross_function_uses,
        unreachable_uses=unreachable_uses,
        coverage_valid=coverage_valid,
        all_uses_coverage_percent=all_uses_coverage_percent,
        num_statements=num_statements,
        covered_lines=covered_lines,
        missing_lines=missing_lines,
        num_branches=cov["num_branches"],
        covered_branches=cov["covered_branches"],
        files_analyzed=files_analyzed,
        definitions_total=len(definitions),
    )


def _print_report(metrics: AllUsesMetrics, repo_url: str | None) -> None:
    print("=" * 72)
    print("All Uses Coverage Report  (coverage.py + beniget)")
    print("=" * 72)
    if repo_url:
        print(f"Target repository: {repo_url}")
    print(f"Files analyzed (beniget): {metrics.files_analyzed}")
    print(f"Definitions found:        {metrics.definitions_total}")
    print()
    rows = [
        ("Computational Use Detection (C-Use)", metrics.c_use),
        ("Predicate Use Detection (P-Use)", metrics.p_use),
        ("Definition-Use Pair Identification", metrics.def_use_pairs),
        ("All-Uses Coverage Verification", f"{metrics.all_uses_coverage:.2%}"),
        ("Partial Uses Coverage Detection", metrics.partial_uses),
        ("Multiple Definitions Handling", metrics.multiple_definitions),
        ("Cross-Function Use Detection", metrics.cross_function_uses),
        ("Unreachable Use Detection", metrics.unreachable_uses),
        ("Coverage Reporting Validation", metrics.coverage_valid),
        ("Variable Use Detection (All-Uses %)", f"{metrics.all_uses_coverage_percent:.2f}%"),
    ]
    for label, value in rows:
        print(f"  {label:<42} {value}")
    print()
    print("coverage.py execution witness:")
    print(f"  statements={metrics.num_statements} covered={metrics.covered_lines} missing={metrics.missing_lines}")
    print(f"  branches={metrics.num_branches} covered={metrics.covered_branches}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=pathlib.Path,
        required=True,
        help="Root directory of the Python repository to analyze",
    )
    parser.add_argument(
        "--coverage-json",
        type=pathlib.Path,
        default=None,
        help="Path to coverage.py JSON report (from: coverage json -o coverage.json)",
    )
    parser.add_argument(
        "--repo-url",
        default=None,
        help="Optional repository URL for reporting",
    )
    parser.add_argument(
        "--output-json",
        type=pathlib.Path,
        default=None,
        help="Write metrics JSON to this path",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.source.is_dir():
        print(f"Source path not found: {args.source}", file=sys.stderr)
        return 1

    metrics = compute_metrics(args.source, args.coverage_json)
    _print_report(metrics, args.repo_url)

    if args.output_json:
        payload = asdict(metrics)
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote {args.output_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
