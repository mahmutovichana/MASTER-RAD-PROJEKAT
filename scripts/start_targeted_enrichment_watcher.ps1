param([Parameter(Mandatory=$true)][string]$GitHubToken)
$ErrorActionPreference='Stop'
$env:GITHUB_TOKEN=$GitHubToken
python scripts/run_targeted_enrichment_watcher_v1.py --root . --stall-minutes 15
