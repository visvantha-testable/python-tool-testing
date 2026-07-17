# Static DU Training Repository — 12 Duplication Metrics at 100/100 (Java)

Single **Java/Maven** reference repository for **static du** (static code duplication) training and Testable dashboard certification.

**Repository:** https://github.com/visvantha-testable/java-tool-testing-static-du

## What this repo proves (dashboard IDs 20–31)

| # | Tool | Metric |
|---|------|--------|
| 20 | static du | Duplicated lines (%) |
| 21 | static du | Duplicated blocks |
| 22 | static du | Duplicated files |
| 23 | static du | Duplicated lines |
| 24 | static du | duplicated_blocks_count |
| 25 | static du | duplicated_files_count |
| 26 | static du | duplicated_lines_count |
| 27 | static du | duplication_density |
| 28 | static du | duplication_density_percent |
| 29 | static du | number_of_duplicated_blocks |
| 30 | static du | number_of_duplicated_files |
| 31 | static du | number_of_duplicated_lines |

All **12 metrics** score **100/100** with `covered: yes` (zero duplication in `sample_subject`).

## Platform trigger (required)

**Do not run raw scans alone.** Use the Java wrapper:

```bash
mvn -q -pl static-du-platform exec:java -Dexec.mainClass=com.testable.training.platform.StaticDuTrigger
```

Or:

```bash
./run_trigger.sh
.\run_trigger.ps1
run_trigger.bat
```

Primary output: **`static_du.json`**

## Local verification

```bash
mvn clean test
mvn -q -pl static-du-platform exec:java -Dexec.mainClass=com.testable.training.platform.StaticDuTrigger
mvn -q -pl static-du-platform exec:java -Dexec.mainClass=com.testable.training.platform.StaticDuJsonVerifierCli
```

Requires **Java 17+** and **Maven 3.9+**.

## Structure

```
pom.xml
sample_subject/          # Unique Java modules (no copy-paste duplication)
static-du-platform/      # StaticDuTrigger + duplication analyzer + 12-metric engine
artifacts/training/      # static_du_summary.json
config/                  # metric_coverage.json, platform_trigger.json
```

## Testing team

See [TESTING_TEAM.md](TESTING_TEAM.md) and [TRIGGER.md](TRIGGER.md).
