"""Unit tests for All Uses Coverage metric extraction."""

import json
import pathlib
import subprocess
import sys

import pytest

from all_uses_coverage import compute_metrics


SAMPLE = pathlib.Path(__file__).resolve().parent / "sample_subject"


def test_compute_metrics_on_sample_subject():
    metrics = compute_metrics(SAMPLE)
    assert metrics.files_analyzed == 1
    assert metrics.definitions_total >= 3
    assert metrics.c_use >= 1
    assert metrics.def_use_pairs >= 2
    assert metrics.cross_function_uses >= 1
    assert metrics.multiple_definitions >= 1
    assert 0 <= metrics.all_uses_coverage_percent <= 100


def test_coverage_json_integration(tmp_path):
    coverage = {
        "totals": {
            "num_statements": 10,
            "covered_lines": 8,
            "missing_lines": 2,
            "num_branches": 4,
            "covered_branches": 3,
        }
    }
    cov_path = tmp_path / "coverage.json"
    cov_path.write_text(json.dumps(coverage), encoding="utf-8")

    metrics = compute_metrics(SAMPLE, cov_path)
    assert metrics.p_use == 3
    assert metrics.all_uses_coverage == pytest.approx(0.8)
    assert metrics.unreachable_uses == 2
    assert metrics.coverage_valid is True


def test_cli_runs():
    result = subprocess.run(
        [
            sys.executable,
            str(pathlib.Path(__file__).resolve().parents[1] / "all_uses_coverage.py"),
            "--source",
            str(SAMPLE),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "All Uses Coverage Report" in result.stdout
