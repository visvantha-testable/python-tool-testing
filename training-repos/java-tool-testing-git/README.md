# Git Training Repository — Code Churn at 100/100 (Java)

Single **Java/Maven** reference repository for **Git** code churn training and Testable dashboard certification.

**Repository:** https://github.com/visvantha-testable/java-tool-testing-git

## What this repo proves

| Category | Classification | Metric | KPI |
|----------|----------------|--------|-----|
| Development Process Analysis | Code Churn | Risk-Based Testing Prioritization | Code Churn Score |

**1 metric** scores **100/100** with `covered: yes`.

The metric measures the **rate of code change** (lines added + deleted) over a rolling 30-day window via native `git log --numstat`. High churn signals instability and elevated regression risk. This repo demonstrates full **risk-based testing prioritization**: every churned module in `sample_subject` has a matching JUnit regression test.

## Platform trigger (required)

**Do not run raw `git log` alone on the platform.** Use the Java wrapper:

```bash
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger
```

Or use the helper script:

```bash
./run_trigger.sh        # Linux/macOS
.\run_trigger.ps1       # Windows
run_trigger.bat         # Windows CMD
```

This produces `git.json` at the repository root — the unified output Testable expects.

## Local verification

```bash
mvn clean test
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger
```

Requires **Java 17+**, **Maven 3.9+**, and **Git** installed.

## Structure

```
pom.xml                  # Maven parent (100% Java project)
sample_subject/          # Git training subject + JUnit 5 tests
git-platform/            # Java platform trigger + Code Churn metric engine
  src/main/java/com/testable/training/platform/
artifacts/training/      # git log numstat, churn stats, regression mapping
config/                  # metric_coverage.json, platform_trigger.json
.github/workflows/ci.yml # Build + trigger + verify on push
```

## Tool stack

- **Git** — native `git log --since="30 days ago" --numstat` on `sample_subject/src/main/java`
- **Churn analysis (Java)** — lines added/deleted per module over rolling window
- **Regression mapping** — churned `.java` files mapped to `*Test.java` counterparts
- **Code Churn Score** — 100 when all churned modules have regression tests and churn rate is within baseline

## Output files

| File | Purpose |
|------|---------|
| `git.json` | Primary platform output (1 metric) |
| `git_metrics.json` | Full metric payload + raw parameters |
| `platform_metrics.json` | Flat score map for dashboard |
| `dashboard_metrics.json` | Dashboard export |
| `testable_dashboard.json` | Testable-compatible summary |

## Testing team

See [TESTING_TEAM.md](TESTING_TEAM.md) for re-verification steps and [TRIGGER.md](TRIGGER.md) for platform execution details.
