package com.testable.training.platform;

import java.util.LinkedHashMap;
import java.util.Map;

public final class GitMetricsEngine {

    private GitMetricsEngine() {
    }

    public static GitDashboardMetrics compute(GitChurnAnalyzer.ChurnSummary churn) {
        double riskPrioritization = computeRiskPrioritizationScore(churn);
        double stability = computeStabilityScore(churn);
        double codeChurnScore = Math.min(riskPrioritization, stability);

        Map<String, Double> scores = new LinkedHashMap<>();
        scores.put(MetricDefinition.RISK_BASED_TESTING.key(), codeChurnScore);

        Map<String, Object> raw = new LinkedHashMap<>();
        raw.put("lines_added", churn.linesAdded());
        raw.put("lines_deleted", churn.linesDeleted());
        raw.put("total_churn_lines", churn.totalChurnLines());
        raw.put("churn_rate_per_day", churn.churnRatePerDay());
        raw.put("max_churn_rate_per_day", churn.maxChurnRatePerDay());
        raw.put("rolling_window_days", churn.rollingWindowDays());
        raw.put("modules_with_churn", churn.modulesWithChurn());
        raw.put("modules_tested", churn.modulesTested());
        raw.put("risk_prioritization_score", riskPrioritization);
        raw.put("stability_score", stability);
        raw.put("code_churn_score", codeChurnScore);

        return new GitDashboardMetrics(scores, raw);
    }

    static double computeRiskPrioritizationScore(GitChurnAnalyzer.ChurnSummary churn) {
        if (churn.modulesWithChurn() == 0) {
            return 100.0;
        }
        double ratio = 100.0 * churn.modulesTested() / churn.modulesWithChurn();
        return Math.min(100.0, Math.round(ratio));
    }

    static double computeStabilityScore(GitChurnAnalyzer.ChurnSummary churn) {
        if (churn.churnRatePerDay() <= churn.maxChurnRatePerDay()) {
            return 100.0;
        }
        double excess = churn.churnRatePerDay() - churn.maxChurnRatePerDay();
        double penalty = Math.min(100.0, excess / churn.maxChurnRatePerDay() * 100.0);
        return Math.max(0.0, Math.round(100.0 - penalty));
    }

    public record GitDashboardMetrics(Map<String, Double> scores, Map<String, Object> rawParameters) {
        public Map<String, Double> normalizedScores() {
            return scores;
        }
    }
}
