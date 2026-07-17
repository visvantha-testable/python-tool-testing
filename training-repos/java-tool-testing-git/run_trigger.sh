#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mvn -q -pl git-platform exec:java -Dexec.mainClass=com.testable.training.platform.GitTrigger "$@"
