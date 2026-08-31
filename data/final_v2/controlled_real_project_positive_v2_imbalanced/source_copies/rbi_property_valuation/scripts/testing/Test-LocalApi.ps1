param([string]$BaseUrl = "http://127.0.0.1:5002")
$ErrorActionPreference = "Stop"
$checks = @(
    @{ Name = "Health"; Path = "/health"; Contains = "Healthy" },
    @{ Name = "Profil i moduli"; Path = "/api/me"; Contains = "availableModules" },
    @{ Name = "Narudžbe"; Path = "/api/orders"; Contains = "items" },
    @{ Name = "Vještaci"; Path = "/api/appraisers"; Contains = "Mirza" },
    @{ Name = "Poslovnice"; Path = "/api/branches"; Contains = "[" },
    @{ Name = "Šifrarnici"; Path = "/api/admin/codebooks"; Contains = "items" },
    @{ Name = "Notifikacije"; Path = "/api/notifications/mine"; Contains = "[" },
    @{ Name = "Audit"; Path = "/api/audit"; Contains = "items" }
)
$failed = 0
foreach ($check in $checks) {
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri ($BaseUrl + $check.Path) -TimeoutSec 15
        if ($response.StatusCode -ne 200 -or $response.Content -notmatch [regex]::Escape($check.Contains)) { throw "Neočekivan odgovor ili nedostaje seed podatak." }
        Write-Host "[OK] $($check.Name)" -ForegroundColor Green
    } catch { $failed++; Write-Host "[FAIL] $($check.Name): $($_.Exception.Message)" -ForegroundColor Red }
}
if ($failed -gt 0) { throw "$failed API provjera nije prošlo." }
