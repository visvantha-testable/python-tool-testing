# Testing Team Guide — Python Tool Coverage + Beniget Pro

## Trigger Command

```powershell
python all_uses_coverage_trigger.py
```

Do **not** run raw `coverage run` or `beniget` alone on the platform — use the trigger above.

## Output

| File | Purpose |
|------|---------|
| `all_uses_coverage.json` | Primary platform output (10 metrics, status=READY) |
| `reports/coverage.json` | coverage.py JSON witness |
| `reports/beniget_defuse.json` | Beniget def-use chains per file |
| `reports/all_uses_metrics.json` | Raw metric values |

## Subject Data

From [testable-whitebox-python](https://github.com/bipinvk47/testable-whitebox-python):

- `sample_subject/src/data_processor.py` — primary data-flow patterns
- `sample_subject/tests/test_data_processor.py` — drives execution coverage

## Verification

```powershell
python scripts/verify_all_uses_json.py --json all_uses_coverage.json
```

Expected: 10/10 metrics with `score=100` and `covered=yes`.
