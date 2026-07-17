package com.testable.training.platform;

public record MetricDefinition(
        String l3,
        String l4,
        String l5,
        String scoreField
) {
    public static final MetricDefinition RISK_BASED_TESTING = new MetricDefinition(
            "Development Process Analysis",
            "Code Churn",
            "Risk-Based Testing Prioritization",
            "code_churn_score"
    );

    public static final MetricDefinition[] ALL = {RISK_BASED_TESTING};

    public String key() {
        return l5;
    }
}
