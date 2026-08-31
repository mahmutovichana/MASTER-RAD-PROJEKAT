<#
.SYNOPSIS
    Pokrece testove sa code coverage mjerenjem i ispisuje ukupan i per-package
    (Domain/Application/Infrastructure) line-rate.
#>

$root = Split-Path -Parent $PSScriptRoot
$resultsDir = Join-Path $root "coverage-temp"

if (Test-Path $resultsDir) {
    Remove-Item -Recurse -Force $resultsDir
}

dotnet test (Join-Path $root "PropertyValuation\Tests\Application.Tests\Application.Tests.csproj") `
    --collect:"XPlat Code Coverage" `
    --settings (Join-Path $root "coverlet.runsettings") `
    --results-directory $resultsDir

$cobertura = Get-ChildItem -Path $resultsDir -Filter "coverage.cobertura.xml" -Recurse |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $cobertura) {
    Write-Error "coverage.cobertura.xml nije pronadjen u $resultsDir"
    exit 1
}

[xml]$xml = Get-Content $cobertura.FullName

$totalCovered = 0
$totalLines = 0
$perPackage = @{}

foreach ($package in $xml.coverage.packages.package) {
    $pkgCovered = 0
    $pkgLines = 0

    foreach ($class in $package.classes.class) {
        foreach ($line in $class.lines.line) {
            $pkgLines++
            if ([int]$line.hits -gt 0) { $pkgCovered++ }
        }
    }

    $totalCovered += $pkgCovered
    $totalLines += $pkgLines

    if (-not $perPackage.ContainsKey($package.name)) {
        $perPackage[$package.name] = @{ Covered = 0; Total = 0 }
    }
    $perPackage[$package.name].Covered += $pkgCovered
    $perPackage[$package.name].Total += $pkgLines
}

Write-Host ""
Write-Host "=== Coverage Report ==="
foreach ($key in $perPackage.Keys | Sort-Object) {
    $p = $perPackage[$key]
    $pct = if ($p.Total -gt 0) { [math]::Round(100.0 * $p.Covered / $p.Total, 2) } else { 0 }
    Write-Host ("{0,-30} {1,5}/{2,-5}  {3,6}%" -f $key, $p.Covered, $p.Total, $pct)
}

$totalPct = if ($totalLines -gt 0) { [math]::Round(100.0 * $totalCovered / $totalLines, 2) } else { 0 }
Write-Host "------------------------------------------------------------"
Write-Host ("{0,-30} {1,5}/{2,-5}  {3,6}%" -f "TOTAL", $totalCovered, $totalLines, $totalPct)
Write-Host ""
