# Testing Team — Git Code Churn Re-Verification

Use this checklist to confirm **100/100** on the **Risk-Based Testing Prioritization** metric.

## Prerequisites

- Java 17+
- Maven 3.9+
- Git installed and on PATH
- Clone: `git clone https://github.com/visvantha-testable/java-tool-testing-git.git`

## Steps

1. **Build and test the subject**

   ```bash
   mvn clean test
   ```

   All JUnit tests in `sample_subject` must pass.

2. **Run the platform trigger** (do not use raw `git log` alone)

   ```bash
   mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger
   ```

3. **Verify output**

   ```bash
   mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitJsonVerifierCli
   ```

   Expected: `PASS: git.json has all 1 Git metrics covered=yes with 100/100 score`

4. **Inspect `git.json`**

   Confirm these fields:

   | Field | Expected |
   |-------|----------|
   | `tool` | `Git` |
   | `metrics_total` | `1` |
   | `metrics_covered` | `1` |
   | `metric_coverage_complete` | `true` |
   | `metrics[0].l5_metric` | `Risk-Based Testing Prioritization` |
   | `metrics[0].classification` | `Code Churn` |
   | `metrics[0].covered` | `yes` |
   | `metrics[0].score` | `100` |
   | `metrics[0].result` | `PASS` |

5. **Confirm raw Git evidence**

   Check `supplemental_raw_data` in `git.json`:

   - `git_churn.modules_with_churn` = `3`
   - `git_churn.modules_tested` = `3`
   - `git_churn.files` lists all three Java modules
   - `regression_mapping` maps each module to its `*Test.java`

## Metric definition

| Level | Value |
|-------|-------|
| L3 Strategy | Development Process Analysis |
| L4 Classification | Code Churn |
| L5 Metric | Risk-Based Testing Prioritization |
| KPI | Code Churn Score |
| Definition | Rate of code change (lines added + deleted) over a rolling window; high churn signals instability and elevated regression risk |

## Score formula

```
risk_prioritization = min(100, round(100 × modules_tested / modules_with_churn))
stability = 100 if churn_rate_per_day ≤ baseline max else penalized
code_churn_score = min(risk_prioritization, stability)
```

This training repo is configured so **modules_with_churn = modules_tested = 3** and churn rate stays within baseline → **100/100**.

## CI

GitHub Actions runs the same trigger on every push to `master`. Check the Actions tab for green build status.
