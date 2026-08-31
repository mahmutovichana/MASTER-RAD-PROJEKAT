using System.Reflection;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Domain.Codebooks;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

/// <summary>
/// Idempotentno popunjava šifarnike (Codebook + CodebookValue) iz ugrađenog JSON-a.
/// Pokreće se pri startupu nakon migracija.
///
/// Idempotentnost:
/// - Codebook: ako Code ne postoji → kreiraj; ako postoji → preskoči (ne briše izmjene admina)
/// - CodebookValue: ako (CodebookKey, Code) ne postoji → kreiraj; ako postoji → preskoči
/// - Vrijednosti uklonjene iz codebooks.json se ne brišu, već deaktiviraju (IsActive = false)
/// Višestruko pokretanje ne pravi duplikate niti briše korisničke izmjene.
/// </summary>
public static class CodebookSeeder
{
    private const string ResourceName = "RBBH.CollateralAppraisal.Infrastructure.Seed.codebooks.json";
    private const string SeedUserId   = "system-seed";

    private sealed record SeedCodebook(
        string Key, string Label, string? Description, string? Category,
        bool IsSystem, List<SeedValue> Values);

    private sealed record SeedValue(
        string Code, string Label, string? Description,
        int SortOrder, bool IsSystem, bool IsCritical);

    public static async Task SeedAsync(
        ApplicationDbContext db,
        ILogger? logger = null,
        CancellationToken ct = default)
    {
        var codebooks = LoadFromEmbeddedResource();
        if (codebooks.Count == 0) return;

        var now            = DateTime.UtcNow;
        var addedCodebooks = 0;
        var addedValues    = 0;

        // ── 1. Seed Codebook tabele ───────────────────────────────────────────
        var existingCodes = await db.Codebooks
            .IgnoreQueryFilters()
            .Select(c => c.Code)
            .ToListAsync(ct);

        var existingCodeSet = new HashSet<string>(existingCodes, StringComparer.OrdinalIgnoreCase);

        foreach (var cb in codebooks)
        {
            if (existingCodeSet.Contains(cb.Key))
                continue;

            var entity = cb.IsSystem
                ? Codebook.CreateSystem(cb.Key, cb.Label, cb.Description, cb.Category)
                : Codebook.CreateCustom(cb.Key, cb.Label, cb.Description, cb.Category, SeedUserId);

            db.Codebooks.Add(entity);
            addedCodebooks++;
        }

        if (addedCodebooks > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("Codebook seed: dodano {Count} novih šifarnika.", addedCodebooks);
        }

        // ── 2. Seed CodebookValue tabele ──────────────────────────────────────
        foreach (var cb in codebooks)
        {
            var existingValueCodes = await db.CodebookValues
                .IgnoreQueryFilters()
                .Where(v => v.CodebookKey == cb.Key)
                .Select(v => v.Code)
                .ToListAsync(ct);

            var existingValues = new HashSet<string>(existingValueCodes, StringComparer.OrdinalIgnoreCase);

            foreach (var v in cb.Values)
            {
                if (existingValues.Contains(v.Code))
                    continue;

                var entity = CodebookValue.Create(
                    codebookKey:     cb.Key,
                    code:            v.Code,
                    label:           v.Label,
                    description:     v.Description,
                    sortOrder:       v.SortOrder,
                    createdByUserId: SeedUserId,
                    isSystem:        v.IsSystem,
                    isCritical:      v.IsCritical);

                db.CodebookValues.Add(entity);
                addedValues++;
            }
        }

        if (addedValues > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("Codebook seed: dodano {Count} novih vrijednosti šifarnika.", addedValues);
        }

        // ── 3. Deaktiviraj vrijednosti uklonjene iz specifikacije ──────────────
        await DeactivateRemovedValuesAsync(db, now, logger, ct);
    }

    /// <summary>
    /// Deaktivira CodebookValue zapise koji su uklonjeni iz codebooks.json nakon što
    /// su već bili seedani u postojeće baze (npr. "SP" iz tipovi_klijenata —
    /// samostalni poduzetnik ne postoji u FL/PL specifikaciji). Ne briše red niti
    /// pokreće migraciju — koristi postojeći IsActive/Deactivate mehanizam, pa
    /// historijski podaci ostaju netaknuti.
    /// </summary>
    private static async Task DeactivateRemovedValuesAsync(
        ApplicationDbContext db, DateTime now, ILogger? logger, CancellationToken ct)
    {
        (string CodebookKey, string Code)[] removed =
        [
            ("tipovi_klijenata",               "SP"),
            ("razlozi_dopune_dokumentacije",   "NEDOSTAJE_DATUM"),
            ("razlozi_dopune_dokumentacije",   "NEDOSTAJE_TERETNI_LIST"),
            ("tipovi_kolaterala",              "APP_STAN"),
            ("tipovi_kolaterala",              "GARAZA"),
            ("tipovi_kolaterala",              "OSTAVA"),
        ];

        var deactivated = 0;
        foreach (var (codebookKey, code) in removed)
        {
            var value = await db.CodebookValues
                .FirstOrDefaultAsync(v => v.CodebookKey == codebookKey && v.Code == code && v.IsActive, ct);

            if (value is null)
                continue;

            value.Deactivate(now, SeedUserId, "Uklonjeno iz specifikacije (nije FL ni PL).");
            deactivated++;
        }

        if (deactivated > 0)
        {
            await db.SaveChangesAsync(ct);
            logger?.LogInformation("Codebook seed: deaktivirano {Count} uklonjenih vrijednosti šifarnika.", deactivated);
        }
    }

    private static List<SeedCodebook> LoadFromEmbeddedResource()
    {
        var assembly = Assembly.GetExecutingAssembly();
        using var stream = assembly.GetManifestResourceStream(ResourceName);
        if (stream is null)
            return [];

        using var reader = new StreamReader(stream);
        var json = reader.ReadToEnd();

        var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
        return JsonSerializer.Deserialize<List<SeedCodebook>>(json, options) ?? [];
    }
}
