# Testing Team — Static DU Re-Verification (12 metrics)

Confirm **100/100** on all dashboard Static DU metrics (IDs 20–31).

## Steps

```bash
git clone https://github.com/visvantha-testable/java-tool-testing-static-du.git
cd java-tool-testing-static-du
mvn clean test
mvn -q -pl static-du-platform exec:java -Dexec.mainClass=com.testable.training.platform.StaticDuTrigger
mvn -q -pl static-du-platform exec:java -Dexec.mainClass=com.testable.training.platform.StaticDuJsonVerifierCli
```

Expected:

```
PASS: static_du.json has all 12 Static DU metrics covered=yes with 100/100 score
TRIGGER COMPLETE: static_du.json ready — all 12 Static DU metrics covered=yes 100/100
```

## Inspect `static_du.json`

| Field | Expected |
|-------|----------|
| `tool` | `static du` |
| `metrics_total` | `12` |
| `metrics_covered` | `12` |
| `metric_coverage_complete` | `true` |

Raw evidence in `supplemental_raw_data.static_du_summary`:

- `duplicated_lines` = `0`
- `duplicated_blocks` = `0`
- `duplicated_files` = `0`
- `duplication_density_percent` = `0`
