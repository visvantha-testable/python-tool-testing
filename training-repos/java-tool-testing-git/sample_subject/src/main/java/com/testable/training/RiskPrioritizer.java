package com.testable.training;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class RiskPrioritizer {

    public List<String> prioritizeByChurn(List<ChurnRecord> records) {
        List<ChurnRecord> sorted = new ArrayList<>(records);
        sorted.sort(Comparator.comparingInt(ChurnRecord::churnScore).reversed());
        List<String> prioritized = new ArrayList<>();
        for (ChurnRecord record : sorted) {
            prioritized.add(record.moduleName());
        }
        return prioritized;
    }

    public int computeChurnScore(int linesAdded, int linesDeleted) {
        return linesAdded + linesDeleted;
    }

    public boolean requiresRegressionTest(int churnScore, int threshold) {
        return churnScore >= threshold;
    }

    public record ChurnRecord(String moduleName, int linesAdded, int linesDeleted, int churnScore) {
        public ChurnRecord(String moduleName, int linesAdded, int linesDeleted) {
            this(moduleName, linesAdded, linesDeleted, linesAdded + linesDeleted);
        }
    }
}
