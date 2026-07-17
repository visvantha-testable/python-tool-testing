$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger @args
