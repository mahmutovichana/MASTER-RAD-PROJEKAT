[CmdletBinding()]
param(
    [string] $OutputDirectory = (Join-Path $PSScriptRoot '..\artifacts\iis')
)

$ErrorActionPreference = 'Stop'
$repo = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$web = Join-Path $repo 'src\Web'
$output = [System.IO.Path]::GetFullPath($OutputDirectory)
$stage = Join-Path $output 'rbbh-test-automation-front'
$zip = Join-Path $output 'rbbh-test-automation-front.zip'
if (-not $stage.StartsWith($output, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Neispravna staging putanja.'
}

Push-Location $web
try {
    & pnpm.cmd install --frozen-lockfile
    if ($LASTEXITCODE -ne 0) { throw 'pnpm install nije uspio.' }
    & pnpm.cmd localization:build
    if ($LASTEXITCODE -ne 0) { throw 'Localization build nije uspio.' }
    & pnpm.cmd build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend build nije uspio.' }
}
finally { Pop-Location }

New-Item -ItemType Directory -Path $output -Force | Out-Null
if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
Copy-Item -LiteralPath (Join-Path $web 'dist') -Destination $stage -Recurse
if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel Optimal
Write-Host "IIS paket je spreman: $zip"
