# Python Tool Testing

White Box **All Uses Coverage** metric validation using **coverage.py + beniget**, aligned with *Testable Strategy & Metrics Reference v3.0*.

## Recommended Target Repository

| Field | Value |
|-------|-------|
| **Repository** | [serge-sans-paille/beniget](https://github.com/serge-sans-paille/beniget) |
| **Strategy** | White Box → Data Flow Testing → All Uses Coverage |
| **Tools** | coverage.py (execution witness) + beniget (static def-use chains) |

**Why beniget?** It is the canonical Python def-use chain analyzer, ships a pytest suite for coverage.py, and its source contains the data-flow patterns required by all ten All Uses Coverage sub-metrics (C-Use, P-Use, def-use pairs, cross-function uses, multiple definitions, unreachable uses, and reporting validation).

## All Uses Coverage Metrics

| L4 Classification | L5 Metric | Tool |
|-------------------|-----------|------|
| Computational Use Detection (C-Use) | Data Processing Validation | coverage.py + beniget |
| Predicate Use Detection (P-Use) | Logic Influence Assessment | coverage.py + beniget |
| Definition-Use Pair Identification | Path Correlation Mapping | coverage.py + beniget |
| All-Uses Coverage Verification | Comprehensive Data Proofing | coverage.py + beniget |
| Partial Uses Coverage Detection | Data Flow Gap Analysis | coverage.py + beniget |
| Multiple Definitions Handling | Ambiguity Resolution | coverage.py + beniget |
| Cross-Function Use Detection | Inter-procedural Tracking | coverage.py + beniget |
| Unreachable Use Detection | Ghost Use Identification | coverage.py + beniget |
| Coverage Reporting Validation | Data Integrity Audit | coverage.py + beniget |
| Variable Use Detection | All-Uses Coverage % | coverage.py + beniget |

See `config/target_repo.json` for machine-readable mapping and formulas.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python -m pytest tests/ -q
```

### Analyze beniget (full pipeline)

```powershell
.\run_beniget_analysis.ps1
```

### Manual analysis

```powershell
git clone https://github.com/serge-sans-paille/beniget.git work/beniget
cd work/beniget
pip install -e .
python -m coverage run --branch -m pytest tests/ -q
python -m coverage json -o coverage.json
cd ../..
python all_uses_coverage.py `
  --source work/beniget/beniget `
  --coverage-json work/beniget/coverage.json `
  --repo-url https://github.com/serge-sans-paille/beniget `
  --output-json reports/beniget_all_uses.json
```

## Project Layout

```
python-tool-testing/
├── all_uses_coverage.py      # Metric extractor (beniget + coverage.py JSON)
├── config/target_repo.json   # Strategy/metric/tool mapping
├── run_beniget_analysis.ps1  # End-to-end beniget pipeline
├── requirements.txt
└── tests/
```

## References

- [beniget](https://github.com/serge-sans-paille/beniget) — static def-use chains for Python
- [coverage.py](https://github.com/nedbat/coveragepy) — execution coverage measurement
