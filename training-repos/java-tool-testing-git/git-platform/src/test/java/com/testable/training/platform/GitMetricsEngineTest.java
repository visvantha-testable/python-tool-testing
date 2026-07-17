package com.testable.training.platform;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class GitMetricsEngineTest {

    @Test
    void perfectScoreWhenAllChurnedModulesHaveTests() {
        GitChurnAnalyzer.ChurnSummary churn = new GitChurnAnalyzer.ChurnSummary(
                3, 3, 120, 30, 150, 5.0, 500.0, 30,
                java.util.List.of("OrderService.java", "PaymentValidator.java", "RiskPrioritizer.java"),
                java.util.Map.of(
                        "OrderService.java", "OrderServiceTest.java",
                        "PaymentValidator.java", "PaymentValidatorTest.java",
                        "RiskPrioritizer.java", "RiskPrioritizerTest.java"
                )
        );
        GitMetricsEngine.GitDashboardMetrics metrics = GitMetricsEngine.compute(churn);
        assertEquals(100.0, metrics.normalizedScores().get("Risk-Based Testing Prioritization"));
    }

    @Test
    void riskPrioritizationScorePartialCoverage() {
        GitChurnAnalyzer.ChurnSummary churn = new GitChurnAnalyzer.ChurnSummary(
                3, 2, 50, 10, 60, 2.0, 500.0, 30,
                java.util.List.of("A.java", "B.java", "C.java"),
                java.util.Map.of()
        );
        assertEquals(67.0, GitMetricsEngine.computeRiskPrioritizationScore(churn));
    }
}
