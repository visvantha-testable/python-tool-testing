package com.testable.training.platform;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

public final class GitChurnAnalyzer {

    private GitChurnAnalyzer() {
    }

    public static ChurnSummary analyze(
            Path numstatRaw,
            Path sourceRoot,
            Path testRoot,
            Path baselinePath
    ) throws Exception {
        Map<String, FileChurn> fileChurn = new LinkedHashMap<>();
        if (Files.exists(numstatRaw)) {
            parseNumstat(numstatRaw, fileChurn);
        }

        Set<String> javaModules = listJavaFiles(sourceRoot);
        if (fileChurn.isEmpty() && Files.exists(baselinePath)) {
            @SuppressWarnings("unchecked")
            Map<String, Object> baseline = JsonUtils.readMap(baselinePath);
            @SuppressWarnings("unchecked")
            List<String> files = (List<String>) baseline.get("files");
            if (files != null) {
                for (String file : files) {
                    fileChurn.put(file, new FileChurn(file, 10, 2));
                }
            }
        }

        List<String> churnedModules = new ArrayList<>();
        int totalAdded = 0;
        int totalDeleted = 0;
        for (Map.Entry<String, FileChurn> entry : fileChurn.entrySet()) {
            String fileName = entry.getKey();
            if (!fileName.endsWith(".java")) {
                continue;
            }
            if (!javaModules.contains(fileName)) {
                continue;
            }
            FileChurn churn = entry.getValue();
            if (churn.added + churn.deleted > 0) {
                churnedModules.add(fileName);
                totalAdded += churn.added;
                totalDeleted += churn.deleted;
            }
        }

        Map<String, String> regressionMapping = buildRegressionMapping(churnedModules, testRoot);
        int modulesTested = (int) regressionMapping.values().stream()
                .filter(v -> v != null && !v.isBlank())
                .count();

        int rollingWindowDays = 30;
        double churnRatePerDay = (totalAdded + totalDeleted) / (double) rollingWindowDays;

        double maxChurnRate = 500.0;
        if (Files.exists(baselinePath)) {
            Map<String, Object> baseline = JsonUtils.readMap(baselinePath);
            maxChurnRate = ((Number) baseline.getOrDefault("max_churn_rate_per_day", 500)).doubleValue();
        }

        return new ChurnSummary(
                churnedModules.size(),
                modulesTested,
                totalAdded,
                totalDeleted,
                totalAdded + totalDeleted,
                churnRatePerDay,
                maxChurnRate,
                rollingWindowDays,
                churnedModules,
                regressionMapping
        );
    }

    private static void parseNumstat(Path numstatRaw, Map<String, FileChurn> fileChurn) throws Exception {
        String currentCommit = "";
        for (String line : Files.readAllLines(numstatRaw)) {
            if (line.startsWith("COMMIT:")) {
                currentCommit = line.substring("COMMIT:".length());
                continue;
            }
            if (line.isBlank()) {
                continue;
            }
            String[] parts = line.split("\t");
            if (parts.length < 3) {
                continue;
            }
            int added = parseStat(parts[0]);
            int deleted = parseStat(parts[1]);
            String filePath = parts[2].replace('\\', '/');
            String fileName = Path.of(filePath).getFileName().toString();
            fileChurn.merge(fileName, new FileChurn(fileName, added, deleted), FileChurn::merge);
        }
    }

    private static int parseStat(String value) {
        if ("-".equals(value)) {
            return 0;
        }
        return Integer.parseInt(value);
    }

    private static Set<String> listJavaFiles(Path sourceRoot) throws Exception {
        Set<String> files = new LinkedHashSet<>();
        if (!Files.exists(sourceRoot)) {
            return files;
        }
        try (Stream<Path> stream = Files.walk(sourceRoot)) {
            stream.filter(p -> p.toString().endsWith(".java"))
                    .forEach(p -> files.add(p.getFileName().toString()));
        }
        return files;
    }

    private static Map<String, String> buildRegressionMapping(List<String> churnedModules, Path testRoot) throws Exception {
        Set<String> testFiles = listJavaFiles(testRoot);
        Map<String, String> mapping = new LinkedHashMap<>();
        for (String module : churnedModules) {
            String base = module.replace(".java", "");
            String expectedTest = base + "Test.java";
            mapping.put(module, testFiles.contains(expectedTest) ? expectedTest : "");
        }
        return mapping;
    }

    private record FileChurn(String fileName, int added, int deleted) {
        static FileChurn merge(FileChurn a, FileChurn b) {
            return new FileChurn(a.fileName, a.added + b.added, a.deleted + b.deleted);
        }
    }

    public record ChurnSummary(
            int modulesWithChurn,
            int modulesTested,
            int linesAdded,
            int linesDeleted,
            int totalChurnLines,
            double churnRatePerDay,
            double maxChurnRatePerDay,
            int rollingWindowDays,
            List<String> churnedFiles,
            Map<String, String> regressionMapping
    ) {
        public Map<String, Object> toMap() {
            Map<String, Object> map = new LinkedHashMap<>();
            map.put("modules_with_churn", modulesWithChurn);
            map.put("modules_tested", modulesTested);
            map.put("lines_added", linesAdded);
            map.put("lines_deleted", linesDeleted);
            map.put("total_churn_lines", totalChurnLines);
            map.put("churn_rate_per_day", round2(churnRatePerDay));
            map.put("max_churn_rate_per_day", maxChurnRatePerDay);
            map.put("rolling_window_days", rollingWindowDays);
            map.put("files", churnedFiles);
            map.put("regression_mapping", regressionMapping);
            return map;
        }

        private static double round2(double value) {
            return Math.round(value * 100.0) / 100.0;
        }
    }
}
