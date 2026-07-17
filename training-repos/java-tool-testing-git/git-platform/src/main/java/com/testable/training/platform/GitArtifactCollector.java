package com.testable.training.platform;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class GitArtifactCollector {

    private GitArtifactCollector() {
    }

    public static void collect(Path repoRoot, Path outputDir) throws Exception {
        Files.createDirectories(outputDir);
        Path sourceRoot = repoRoot.resolve("sample_subject/src/main/java");
        Path testRoot = repoRoot.resolve("sample_subject/src/test/java");

        String since = "30 days ago";
        Path numstatRaw = outputDir.resolve("git_log_numstat.txt");
        runGitLog(repoRoot, since, sourceRoot, numstatRaw);

        GitChurnAnalyzer.ChurnSummary churn = GitChurnAnalyzer.analyze(
                numstatRaw,
                sourceRoot,
                testRoot,
                repoRoot.resolve("config/golden_baseline_churn.json")
        );

        JsonUtils.write(outputDir.resolve("git_churn.json"), churn.toMap());
        JsonUtils.write(outputDir.resolve("regression_mapping.json"), churn.regressionMapping());

        Map<String, Object> gitMeta = new LinkedHashMap<>();
        gitMeta.put("tool", "Git");
        gitMeta.put("rolling_window", since);
        gitMeta.put("source_root", sourceRoot.toString());
        gitMeta.put("test_root", testRoot.toString());
        gitMeta.put("numstat_raw", numstatRaw.toString());
        JsonUtils.write(outputDir.resolve("git_meta.json"), gitMeta);

        System.out.println("Collected Git artifacts into " + outputDir);
        System.out.println("  modules_with_churn=" + churn.modulesWithChurn());
        System.out.println("  modules_tested=" + churn.modulesTested());
        System.out.println("  total_churn_lines=" + churn.totalChurnLines());
    }

    private static void runGitLog(Path repoRoot, String since, Path sourceRoot, Path output) throws Exception {
        List<String> command = List.of(
                "git", "log",
                "--since=" + since,
                "--numstat",
                "--pretty=format:COMMIT:%H|%ad",
                "--date=short",
                "--",
                sourceRoot.toString()
        );
        ProcessBuilder builder = new ProcessBuilder(command);
        builder.directory(repoRoot.toFile());
        builder.redirectErrorStream(true);
        Process process = builder.start();

        StringBuilder outputText = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                outputText.append(line).append('\n');
            }
        }
        int exit = process.waitFor();
        if (exit != 0 && outputText.length() == 0) {
            throw new IllegalStateException("git log failed with exit code " + exit);
        }
        Files.writeString(output, outputText.toString(), StandardCharsets.UTF_8);
    }
}
