# Platform Trigger — Git Code Churn

## Primary command

```bash
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger
```

## What the trigger does

1. Runs native **Git** `git log --since="30 days ago" --numstat` on `sample_subject/src/main/java`
2. Parses lines added/deleted per Java module over the rolling window
3. Maps churned modules to regression test classes in `sample_subject/src/test/java`
4. Computes **Code Churn Score** for **Risk-Based Testing Prioritization**
5. Exports unified `git.json` with `covered: yes` and `score: 100`
6. Validates metric coverage and JSON completeness

## Primary output

| File | Location |
|------|----------|
| `git.json` | Repository root |

## Do NOT run on the platform

- Raw `git log` without the Java wrapper
- Raw `git diff` or `git shortlog` alone
- Any non-Java script trigger

The platform expects the **wrapper trigger** that produces the unified JSON bundle.

## Configuration

| File | Purpose |
|------|---------|
| `config/platform_trigger.json` | Platform trigger metadata |
| `config/metric_coverage.json` | Single metric definition |
| `config/golden_baseline_churn.json` | Baseline churn rate threshold |

## Skip verification (debug only)

```bash
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger -Dexec.args="--skip-verify"
```

## Expected result

```
TRIGGER COMPLETE: git.json ready — Code Churn metric covered=yes 100/100
```
