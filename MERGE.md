# Merge Branch — Unified Tool Testing Repos

This **`merge`** branch consolidates all Testable training repositories into a single branch for testing-team review.

## Root (this directory)

| Repo | Tool | Metrics |
|------|------|---------|
| **Root** | coverage.py + beniget | All Uses Coverage (10 metrics, 100/100) |

**Trigger:** `python all_uses_coverage_trigger.py` → `all_uses_coverage.json`

## Consolidated under `training-repos/`

| Folder | GitHub | Tool | Language |
|--------|--------|------|----------|
| `python-tool-testing-pip-audit` | [pip-audit](https://github.com/visvantha-testable/python-tool-testing-pip-audit) | pip-audit | Python |
| `python-tool-coverage-beniget-pro` | [coverage-beniget-pro](https://github.com/visvantha-testable/python-tool-coverage-beniget-pro) | coverage.py + beniget | Python |
| `python-tool-testing-coverage-py` | [coverage-py](https://github.com/visvantha-testable/python-tool-testing-coverage-py) | coverage.py | Python |
| `typescript-tool-testing-dependabot` | [dependabot](https://github.com/visvantha-testable/typescript-tool-testing-dependabot) | Dependabot | TypeScript |
| `java-tool-testing-jacoco` | [jacoco](https://github.com/visvantha-testable/java-tool-testing-jacoco) | JaCoCo | Java |
| `java-tool-testing-git` | [git](https://github.com/visvantha-testable/java-tool-testing-git) | Git | Java |
| `java-tool-testing-static-du` | [static-du](https://github.com/visvantha-testable/java-tool-testing-static-du) | static du | Java |
| `java-tool-testing-def-use` | [def-use](https://github.com/visvantha-testable/java-tool-testing-def-use) | JaCoCo + static du | Java |

## Verify root beniget (100/100)

```powershell
python -m pip install -r requirements.txt
python all_uses_coverage_trigger.py
python scripts/verify_all_uses_json.py --json all_uses_coverage.json
```

## Verify dependabot (100/100)

```powershell
cd training-repos/typescript-tool-testing-dependabot
npm install && npm run trigger && npm run verify
```

## Branch purpose

- **master** — production-ready beniget training repo (standalone)
- **merge** — all tool testing repos in one place for cross-metric review

Each sub-repo remains independently pushable on its own GitHub remote; this branch is the unified snapshot.
