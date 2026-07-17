# Python Tool Coverage + Beniget Pro

White Box **All Uses Coverage** metric validation using **coverage.py + beniget**, aligned with *Testable Strategy & Metrics Reference v3.0*.

Training data from [bipinvk47/testable-whitebox-python](https://github.com/bipinvk47/testable-whitebox-python).

## Subject Repository

| Field | Value |
|-------|-------|
| **Source** | https://github.com/bipinvk47/testable-whitebox-python.git |
| **Local path** | `sample_subject/src` |
| **Key file** | `data_processor.py` — C-Use, P-Use, def-use pairs, cross-function, ghost uses |
| **Tests** | `sample_subject/tests/` |
| **Strategy** | White Box → Data Flow Testing → All Uses Coverage |
| **Tools** | coverage.py (execution witness) + beniget (static def-use chains) |

## Platform Trigger

```powershell
python all_uses_coverage_trigger.py
```

Writes **`all_uses_coverage.json`** to repository root with all 10 All Uses Coverage metrics at 100/100.

## All Uses Coverage Metrics (10)

| ID | L4 Classification | L5 Metric | Tool |
|----|-------------------|-----------|------|
| 89 | Computational Use Detection (C-Use) | Data Processing Validation | coverage.py + beniget |
| 90 | Predicate Use Detection (P-Use) | Logic Influence Assessment | coverage.py + beniget |
| 91 | Definition-Use Pair Identification | Path Correlation Mapping | coverage.py + beniget |
| 92 | All-Uses Coverage Verification | Comprehensive Data Proofing | coverage.py + beniget |
| 93 | Partial Uses Coverage Detection | Data Flow Gap Analysis | coverage.py + beniget |
| 94 | Multiple Definitions Handling | Ambiguity Resolution | coverage.py + beniget |
| 95 | Cross-Function Use Detection | Inter-procedural Tracking | coverage.py + beniget |
| 96 | Unreachable Use Detection | Ghost Use Identification | coverage.py + beniget |
| 97 | Coverage Reporting Validation | Data Integrity Audit | coverage.py + beniget |
| 98 | Variable Use Detection | All-Uses Coverage % | coverage.py + beniget |

## Quick Start

```powershell
python -m pip install -r requirements.txt
python -m pytest tests/ -q
python all_uses_coverage_trigger.py
```

### One-shot pipeline

```powershell
.\run_beniget_analysis.ps1
```

## Project Layout

```
python-tool-coverage-beniget-pro/
├── all_uses_coverage.py           # Metric extractor (beniget + coverage.py JSON)
├── all_uses_coverage_trigger.py   # Platform trigger → all_uses_coverage.json
├── sample_subject/                # From testable-whitebox-python
│   ├── src/                       # data_processor.py, calculator.py, ...
│   └── tests/                     # pytest suite
├── scripts/run_beniget.py         # Beniget def-use chain helper
├── config/                        # metric + trigger configs
├── run_beniget_analysis.ps1       # End-to-end pipeline
└── tests/                         # Unit tests for metric extractor
```

## References

- [testable-whitebox-python](https://github.com/bipinvk47/testable-whitebox-python) — source training data
- [beniget](https://github.com/serge-sans-paille/beniget) — static def-use chains for Python
- [coverage.py](https://github.com/nedbat/coveragepy) — execution coverage measurement
