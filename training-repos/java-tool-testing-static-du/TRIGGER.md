# Platform Trigger — Static DU

## Primary command

```bash
mvn -q -pl static-du-platform exec:java -Dexec.mainClass=com.testable.training.platform.StaticDuTrigger
```

## What the trigger does

1. Runs **Static DU** duplication analysis on `sample_subject/src/main/java`
2. Measures duplicated lines / blocks / files / density
3. Scores all **12** dashboard metrics (IDs 20–31)
4. Exports unified `static_du.json` with `covered: yes` and `score: 100`
5. Validates metric coverage and JSON completeness

## Do NOT run alone

- Raw grep for duplicate strings without the wrapper
- Manual JSON edits without re-running the trigger

## Expected result

```
TRIGGER COMPLETE: static_du.json ready — all 12 Static DU metrics covered=yes 100/100
```
