# Codebooks — Šifarnici

Ovaj folder sadrži centralnu definiciju Application sloja za upravljanje vrijednostima šifarnika.

## Zašto šifarnici nisu običan CRUD

Vrijednosti šifarnika (tipovi uloga, osnov povezanosti, vrste limita) se koriste u poslovnim
zapisima kao referentni podaci. Ako se vrijednost fizički obriše dok je koriste postojeći zapisi:
- historijski podaci gube značenje,
- relacije u bazi mogu puknuti,
- audit postaje nepouzdan.

**Primarni mehanizam uklanjanja vrijednosti iz novih formi je DEAKTIVACIJA, a ne fizičko brisanje.**

## Struktura

```
Codebooks/
├── CodebookErrorCodes.cs            — mašinski čitljivi kodovi grešaka (za frontend)
├── Interfaces/
│   ├── ICodebookValueService.cs     — sva poslovna pravila za upravljanje vrijednostima
│   ├── ICodebookUsageChecker.cs     — checker za upotrebu jednog šifarnika u jednom modulu
│   ├── ICodebookUsageService.cs     — agregator svih checkera za dati codebookKey
│   └── ICodebookCacheInvalidator.cs — invalidacija cache-a nakon promjena
├── Models/
│   ├── CodebookOptionDto.cs         — lagani DTO za dropdown menije
│   ├── CodebookValueDto.cs          — puni DTO za admin pregled
│   ├── CodebookUsageResult.cs       — rezultat usage checka (IsInUse, IsReliable, Locations)
│   └── CodebookUsageLocation.cs     — jedna lokacija upotrebe (modul, entitet, count)
└── Requests/
    └── DeactivateCodebookValueRequest.cs — request tijelo za deaktivaciju
```

## Stanja vrijednosti

| Stanje | IsActive | DeletedAt | Dropdown | Novi unos | Historijski zapis |
|---|---|---|---|---|---|
| Active | true | null | Da | Da | Da |
| Inactive | false | null | Ne | Ne | Da |
| Deleted | - | postoji | Ne | Ne | Ne* |

*Soft-deleted vrijednosti se automatski isključuju globalnim query filterom.

## Kada je dozvoljeno brisanje

```
IsSystem=true  → brisanje BLOKIRANO (uvijek)
IsInUse=true   → brisanje BLOKIRANO → preporuka: deaktivirati
IsReliable=false (usage check pao) → brisanje BLOKIRANO (fail-safe)
Ostalo         → soft delete dozvoljen
```

## Kada je dozvoljena deaktivacija

```
IsCritical=true → deaktivacija BLOKIRANA
IsActive=false  → već neaktivna → 409 AlreadyInactive
Ostalo          → deaktivacija dozvoljena (čak i ako je u upotrebi)
```

## Kako radi usage check

`ICodebookUsageService` agregira rezultate od svih registrovanih `ICodebookUsageChecker`
implementacija za dati `codebookKey`.

**Fail-safe**: ako neki checker baci grešku, `IsReliable=false` → delete se blokira.

**DELETE endpoint UVIJEK ponavlja usage check** — GET /usage je informativan, DELETE je autoritativan.
Frontend može pozvati /usage i dobiti `canDelete=true`, ali se stanje može promijeniti
prije stvarnog DELETE poziva.

## Kako dodati novi usage checker

```csharp
// 1. Implementirati ICodebookUsageChecker
public sealed class LimitTypeUsageChecker : ICodebookUsageChecker
{
    public string CodebookKey => "limit_types";

    public async Task<CodebookUsageLocation?> CheckAsync(int valueId, CancellationToken ct)
    {
        var count = await _db.LimitRequests
            .CountAsync(x => x.LimitTypeValueId == valueId, ct);

        return count > 0
            ? new CodebookUsageLocation { Module = "Limits", EntityName = "LimitRequest", Count = count }
            : null;
    }
}

// 2. Registrovati u Infrastructure/DependencyInjection.cs:
services.AddScoped<ICodebookUsageChecker, LimitTypeUsageChecker>();
```

Nema potrebe mijenjati `CodebookUsageService` — Open/Closed Principle.

## Kako dropdown koristi samo aktivne vrijednosti

```
GET /api/codebooks/{key}/values/active
→ ICodebookValueService.GetActiveAsync()
→ WHERE codebook_key = '{key}' AND is_active = true AND deleted_at IS NULL
→ ORDER BY sort_order, label
→ CodebookOptionDto[] (id, code, label, sortOrder)
```

## Kako se auditira promjena

Svaka mutacija poziva `IAuditService.RecordAsync(...)` s odgovarajućim `AuditActions.*` konstantama.
Audit greška ne ruši poslovnu operaciju — loguje se i nastavlja.

## Invalidacija cache-a

Nakon svake mutacije poziva se `ICodebookCacheInvalidator.InvalidateAsync(codebookKey)`.
Trenutna implementacija: `NullCodebookCacheInvalidator` (ne radi ništa).
Zamijeniti sa stvarnom implementacijom kad se doda cache.

## Greška u validaciji neaktivne vrijednosti

Ako API prima `codebookValueId` za novi unos, servis mora provjeriti:
```csharp
// Primjer validacije pri kreiranju zapisa
var value = await _db.CodebookValues.FindAsync(request.LimitTypeId);
if (value is null || !value.IsActive)
    throw new ConflictException(
        "Odabrana vrijednost više nije aktivna i ne može se koristiti za nove zapise.",
        CodebookErrorCodes.InactiveForNewRecord);
```

## Permission pravila

| Operacija | Permission |
|---|---|
| GET /values/active | `codebooks.view` |
| GET /values | `codebooks.manage` |
| GET /values/{id} | `codebooks.manage` |
| GET /values/{id}/usage | `codebooks.manage` |
| POST /values/{id}/deactivate | `codebooks.manage` |
| POST /values/{id}/activate | `codebooks.manage` |
| DELETE /values/{id} | `codebooks.manage` |

## Raspodjela odgovornosti

| Odgovornost | Ko |
|---|---|
| Arhitektura, servis, usage checker infrastruktura | Amina ✅ |
| Per-entitet ICodebookUsageChecker implementacije | Hamza (uz definiciju entiteta) |
| Normalized kolone i indeksi za šifarnike ako ih ima | Hamza |
| EF migracija za codebook_values tabelu | Hamza ili DevOps |
| Frontend dropdown logika | Frontend tim |
| QA testovi | QA team |
