# Metrics Coverage — Git Tool

| # | L3 Strategy | L4 Classification | L5 Metric | Score Field | Expected |
|---|-------------|-------------------|-----------|-------------|----------|
| 1 | Development Process Analysis | Code Churn | Risk-Based Testing Prioritization | code_churn_score | 100/100 |

**Total: 1 metric — all at 100/100**

## KPI: Code Churn Score

Rate of code change (lines added + deleted) over a rolling 30-day window. High churn signals instability and elevated regression risk. Score reaches 100 when:

1. Every churned module has a matching regression test (`modules_tested ≥ modules_with_churn`)
2. Churn rate per day is within the baseline threshold (`max_churn_rate_per_day`)

## Raw parameters exported

- `lines_added`, `lines_deleted`, `total_churn_lines`
- `churn_rate_per_day`, `max_churn_rate_per_day`, `rolling_window_days`
- `modules_with_churn`, `modules_tested`
- `risk_prioritization_score`, `stability_score`, `code_churn_score`
