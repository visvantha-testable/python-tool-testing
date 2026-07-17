package com.testable.training.platform;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class MetricCoverageValidator {

    private MetricCoverageValidator() {
    }

    public static int validate(Path repoRoot, Path metricsJson) throws Exception {
        List<String> errors = new ArrayList<>();
        Path churnJson = repoRoot.resolve("artifacts/training/git_churn.json");
        if (!Files.exists(churnJson)) {
            errors.add("missing artifacts/training/git_churn.json");
        }

        Map<String, Double> scores;
        if (metricsJson != null && Files.exists(metricsJson)) {
            @SuppressWarnings("unchecked")
            Map<String, Object> payload = JsonUtils.readMap(metricsJson);
            @SuppressWarnings("unchecked")
            Map<String, Object> normalized = (Map<String, Object>) payload.get("normalized_scores");
            scores = new java.util.LinkedHashMap<>();
            if (normalized != null) {
                normalized.forEach((k, v) -> scores.put(k, ((Number) v).doubleValue()));
            }
        } else if (Files.exists(churnJson)) {
            Map<String, Object> churnMap = JsonUtils.readMap(churnJson);
            GitChurnAnalyzer.ChurnSummary churn = new GitChurnAnalyzer.ChurnSummary(
                    ((Number) churnMap.getOrDefault("modules_with_churn", 0)).intValue(),
                    ((Number) churnMap.getOrDefault("modules_tested", 0)).intValue(),
                    ((Number) churnMap.getOrDefault("lines_added", 0)).intValue(),
                    ((Number) churnMap.getOrDefault("lines_deleted", 0)).intValue(),
                    ((Number) churnMap.getOrDefault("total_churn_lines", 0)).intValue(),
                    ((Number) churnMap.getOrDefault("churn_rate_per_day", 0.0)).doubleValue(),
                    ((Number) churnMap.getOrDefault("max_churn_rate_per_day", 500.0)).doubleValue(),
                    ((Number) churnMap.getOrDefault("rolling_window_days", 30)).intValue(),
                    List.of(),
                    Map.of()
            );
            scores = GitMetricsEngine.compute(churn).normalizedScores();
        } else {
            errors.add("cannot compute scores without git_churn.json");
            scores = Map.of();
        }

        for (MetricDefinition def : MetricDefinition.ALL) {
            Double score = scores.get(def.key());
            if (score == null) {
                errors.add(def.key() + ": missing normalized score");
            } else if (score < 100.0) {
                errors.add(def.key() + ": score " + score + " is below 100/100");
            }
        }

        if (!errors.isEmpty()) {
            System.err.println("Metric coverage validation failed:");
            errors.forEach(err -> System.err.println("  - " + err));
            return 1;
        }

        System.out.println("All " + MetricDefinition.ALL.length + " Git metrics are covered with 100/100 scores.");
        return 0;
    }
}
