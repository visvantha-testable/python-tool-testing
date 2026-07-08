# Clone beniget, run coverage.py tests, emit All Uses Coverage metrics.
param(
    [string]$WorkDir = "$PSScriptRoot\work",
    [string]$BenigetUrl = "https://github.com/serge-sans-paille/beniget.git"
)

$ErrorActionPreference = "Stop"
$BenigetDir = Join-Path $WorkDir "beniget"

New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

if (-not (Test-Path $BenigetDir)) {
    git clone --depth 1 $BenigetUrl $BenigetDir
}

python -m pip install -r "$PSScriptRoot\requirements.txt" -q
python -m pip install -e $BenigetDir -q

Push-Location $BenigetDir
python -m coverage run --branch -m pytest tests/ -q
python -m coverage json -o coverage.json
Pop-Location

python "$PSScriptRoot\all_uses_coverage.py" `
    --source "$BenigetDir\beniget" `
    --coverage-json "$BenigetDir\coverage.json" `
    --repo-url "https://github.com/serge-sans-paille/beniget" `
    --output-json "$PSScriptRoot\reports\beniget_all_uses.json"
