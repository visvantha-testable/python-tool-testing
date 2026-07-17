# Run All Uses Coverage pipeline on sample_subject (from testable-whitebox-python).
param(
    [string]$SampleDir = "$PSScriptRoot\sample_subject",
    [string]$SourceDir = "$PSScriptRoot\sample_subject\src"
)

$ErrorActionPreference = "Stop"

python -m pip install -r "$PSScriptRoot\requirements.txt" -q

Push-Location $SampleDir
python -m coverage run --branch -m pytest -q
Pop-Location

Push-Location $SampleDir
python -m coverage json -o "$PSScriptRoot\reports\coverage.json" --rcfile ".coveragerc"
Pop-Location

python "$PSScriptRoot\scripts\run_beniget.py"

python "$PSScriptRoot\all_uses_coverage.py" `
    --source "$SourceDir" `
    --coverage-json "$PSScriptRoot\reports\coverage.json" `
    --repo-url "https://github.com/bipinvk47/testable-whitebox-python" `
    --output-json "$PSScriptRoot\reports\all_uses_metrics.json"

python "$PSScriptRoot\all_uses_coverage_trigger.py"
