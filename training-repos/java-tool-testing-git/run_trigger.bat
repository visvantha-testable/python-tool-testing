@echo off
cd /d "%~dp0"
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger %*
