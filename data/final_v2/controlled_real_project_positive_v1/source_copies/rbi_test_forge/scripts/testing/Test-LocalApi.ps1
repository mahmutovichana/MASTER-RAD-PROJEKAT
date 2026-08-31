param(
    [string]$BaseUrl = "http://127.0.0.1:5001",
    [switch]$IncludeCrud
)
$ErrorActionPreference = "Stop"
$webSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$checks = @(
    @{ Name = "Health"; Path = "/health"; Contains = "Healthy" },
    @{ Name = "Profil"; Path = "/api/frontend/profile"; Contains = "fullName" },
    @{ Name = "Grupe"; Path = "/api/frontend/groups/"; Contains = "Smoke" },
    @{ Name = "Scenariji"; Path = "/api/frontend/scenarios/"; Contains = "naziv" },
    @{ Name = "Rasporedi"; Path = "/api/frontend/schedules/"; Contains = "[" },
    @{ Name = "Historija"; Path = "/api/frontend/history"; Contains = "status" },
    @{ Name = "Šifrarnici"; Path = "/api/frontend/code-lists/"; Contains = "scenario-types" },
    @{ Name = "Audit"; Path = "/api/frontend/audit"; Contains = "[" }
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

if (-not $IncludeCrud) {
    Write-Host "Osnovna API provjera je uspješna. Za izolovani CRUD test dodajte -IncludeCrud." -ForegroundColor Cyan
    return
}

function Invoke-ApiJson {
    param([string]$Method, [string]$Path, [object]$Body)
    $arguments = @{ Method = $Method; Uri = $BaseUrl + $Path; UseBasicParsing = $true; TimeoutSec = 30; WebSession = $webSession }
    if ($null -ne $Body) {
        $arguments.ContentType = "application/json"
        $arguments.Body = $Body | ConvertTo-Json -Depth 12 -Compress
    }
    if ($Method -notin @("GET", "HEAD", "OPTIONS")) {
        if (-not $script:csrfToken) {
            $csrf = Invoke-WebRequest -UseBasicParsing -Uri ($BaseUrl + "/api/security/csrf") -WebSession $webSession -TimeoutSec 15
            $script:csrfToken = ($csrf.Content | ConvertFrom-Json).token
        }
        $arguments.Headers = @{ "X-CSRF-TOKEN" = $script:csrfToken }
    }
    $response = Invoke-WebRequest @arguments
    if ([string]::IsNullOrWhiteSpace($response.Content)) { return $null }
    return $response.Content | ConvertFrom-Json
}

$suffix = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$groupId = $null
$scenarioId = $null
$scheduleId = $null
$apiKeyId = $null
$codeValueId = $null
$categoryId = $null
try {
    $group = Invoke-ApiJson POST "/api/frontend/groups/" @{
        naziv = "Codex CRUD $suffix"; opis = "Privremena automatizovana provjera"; boja = "#fee600"
        tag = "Smoke"; prioritet = 25; parentGroupId = $null
    }
    $groupId = $group.id
    if (-not $groupId) { throw "Kreiranje grupe nije vratilo ID." }
    Write-Host "[OK] Kreiranje grupe" -ForegroundColor Green

    try {
        Invoke-ApiJson POST "/api/frontend/scenarios/" @{
            groupId = $null; naziv = "Neispravan scenarij"; opis = $null; tip = "Rest"; runSequentially = $false
            rest = @{ metoda = "Get"; url = "nije-url"; headeri = @(); requestBody = $null; ocekivaniStatus = 99; responseAsserti = @() }
            ui = $null; blazor = $null
        } | Out-Null
        throw "Neispravan scenarij je neočekivano prihvaćen."
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 400) { throw }
        Write-Host "[OK] Odbijanje scenarija bez grupe i ispravnog URL-a" -ForegroundColor Green
    }

    $scenario = Invoke-ApiJson POST "/api/frontend/scenarios/" @{
        groupId = $groupId; naziv = "Lokalni health $suffix"; opis = "Provjera lokalnog API-ja"; tip = "Rest"; runSequentially = $false
        rest = @{ metoda = "Get"; url = "$BaseUrl/health"; headeri = @(); requestBody = $null; ocekivaniStatus = 200; responseAsserti = @() }
        ui = $null; blazor = $null
    }
    $scenarioId = $scenario.id
    Write-Host "[OK] Kreiranje REST scenarija" -ForegroundColor Green

    Invoke-ApiJson PUT "/api/frontend/scenarios/$scenarioId" @{
        groupId = $groupId; naziv = "Lokalni health izmijenjen $suffix"; opis = "PUT provjera"; tip = "Rest"; runSequentially = $true
        rest = @{ metoda = "Get"; url = "$BaseUrl/health"; headeri = @(); requestBody = $null; ocekivaniStatus = 200; responseAsserti = @() }
        ui = $null; blazor = $null
    } | Out-Null
    Write-Host "[OK] Izmjena scenarija" -ForegroundColor Green

    $run = Invoke-ApiJson POST "/api/frontend/scenarios/$scenarioId/run" $null
    if ($run.status -notin @("Passed", 2)) { throw "Pokretanje scenarija nije završilo uspješno." }
    Write-Host "[OK] Pokretanje scenarija" -ForegroundColor Green

    $schedule = Invoke-ApiJson POST "/api/frontend/schedules/" @{
        groupId = $groupId; cronExpression = "0 8 * * 1-5"; timezone = "Europe/Sarajevo"; isActive = $true
    }
    $scheduleId = $schedule.id
    Invoke-ApiJson PUT "/api/frontend/schedules/$scheduleId" @{
        cronExpression = "30 8 * * 1-5"; timezone = "Europe/Sarajevo"; isActive = $false
    } | Out-Null
    Write-Host "[OK] Kreiranje i izmjena rasporeda" -ForegroundColor Green

    $key = Invoke-ApiJson POST "/api/frontend/api-keys/" @{ name = "Codex $suffix"; expiresAt = (Get-Date).ToUniversalTime().AddDays(7).ToString("o") }
    $apiKeyId = $key.key.id
    if ([string]::IsNullOrWhiteSpace($key.rawKey)) { throw "API ključ nije prikazan nakon kreiranja." }
    Write-Host "[OK] Kreiranje API ključa i jednokratni secret" -ForegroundColor Green

    $categories = Invoke-ApiJson GET "/api/frontend/code-lists/" $null
    $categoryId = $categories[0].id
    $codeValue = Invoke-ApiJson POST "/api/frontend/code-lists/$categoryId/values" @{
        name = "Codex vrijednost $suffix"; code = "CDX$suffix"; order = 999; active = $true
    }
    $codeValueId = $codeValue.id
    Invoke-ApiJson PUT "/api/frontend/code-lists/$categoryId/values/$codeValueId" @{
        name = "Codex izmijenjeno $suffix"; code = "CDX$suffix"; order = 998; active = $false
    } | Out-Null
    Write-Host "[OK] Kreiranje i izmjena vrijednosti šifarnika" -ForegroundColor Green

    try {
        Invoke-ApiJson POST "/api/frontend/generator/rest" @{
            className = "nije validno"; httpMethod = "INVALID"; routePath = "api/test"; expectedStatus = 99; requestBodyJson = "{"; requiresAuth = $false
        } | Out-Null
        throw "Neispravna generator konfiguracija je neočekivano prihvaćena."
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 400) { throw }
        Write-Host "[OK] Odbijanje neispravne generator konfiguracije" -ForegroundColor Green
    }
    $generated = Invoke-ApiJson POST "/api/frontend/generator/rest" @{
        className = "HealthCheck"; httpMethod = "GET"; routePath = "/health"; expectedStatus = 200; requestBodyJson = $null; requiresAuth = $false
    }
    if ($generated.files.Count -lt 4) { throw "Generator nije vratio očekivane testne fajlove." }
    Write-Host "[OK] Generisanje xUnit test projekta" -ForegroundColor Green
} finally {
    if ($codeValueId -and $categoryId) { try { Invoke-ApiJson DELETE "/api/frontend/code-lists/$categoryId/values/$codeValueId" $null | Out-Null } catch {} }
    if ($scheduleId) { try { Invoke-ApiJson DELETE "/api/frontend/schedules/$scheduleId" $null | Out-Null } catch {} }
    if ($scenarioId) { try { Invoke-ApiJson DELETE "/api/frontend/scenarios/$scenarioId" $null | Out-Null } catch {} }
    if ($apiKeyId) { try { Invoke-ApiJson DELETE "/api/frontend/api-keys/$apiKeyId" $null | Out-Null } catch {} }
    if ($groupId) { try { Invoke-ApiJson DELETE "/api/frontend/groups/$groupId" $null | Out-Null } catch {} }
}
Write-Host "Sve CRUD provjere su uspješne, a privremeni podaci su uklonjeni." -ForegroundColor Cyan
