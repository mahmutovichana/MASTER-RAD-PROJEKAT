using ClosedXML.Excel;
using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.Import.Mappers;

/// <summary>
/// Import vještaka iz Excel-a sa multi-sheet formatom:
/// Svaki sheet = jedan vještak (ime sheet-a = naziv vještaka).
/// Red 2 sadrži sumarne podatke (email, tip nekretnine, firma/individualni).
/// Ostali redovi = gradovi koje vještak pokriva.
/// </summary>
[ExcludeFromCodeCoverage]
public sealed class AppraiserMapper : ICodebookMapper
{
    public string CodebookType => "vjestaci";

    public string? DuplicateKeyColumn => "Naziv";

    public IReadOnlyList<ColumnDef> Columns =>
    [
        new("Naziv", "Naziv vještaka (ime sheet-a)", Required: false),
        new("Opstina/Grad", "Grad", Required: false),
        new("Grad", "Grad (alias)", Required: false),
        new("Tip nekretnine", "Tip nekretnine", Required: false),
        new("E mail", "Email", Required: false),
        new("Polisa", "Polisa", Required: false),
        new("Opcija Firma/Individualni vještak", "Firma/Individualni", Required: false),
    ];

    public Task<IReadOnlyList<ImportRowError>> ValidateRowAsync(ParsedRow row, ImportContext ctx, CancellationToken ct)
        => Task.FromResult<IReadOnlyList<ImportRowError>>([]);

    public Task<RowAction> ClassifyRowAsync(ParsedRow row, ImportContext ctx, CancellationToken ct)
        => Task.FromResult(RowAction.Skip);

    public Task ApplyRowAsync(ParsedRow row, RowAction action, ImportContext ctx, CancellationToken ct)
        => Task.CompletedTask;

    public Task<int> DeactivateMissingAsync(IReadOnlyList<ParsedRow> rows, ImportContext ctx, CancellationToken ct)
        => Task.FromResult(0);

    /// <summary>
    /// Specijalni import: ćita direktno XLSX sa multi-sheet formatom.
    /// Poziva se iz CodebookImportExportService umjesto standardnog row-by-row flow-a.
    /// </summary>
    public static async Task<(int Created, int Updated, int Skipped, List<string> Errors)> ImportFromMultiSheetAsync(
        Stream content, ApplicationDbContext db, string? userId, CancellationToken ct)
    {
        content.Position = 0;
        using var workbook = new XLWorkbook(content);

        int created = 0, updated = 0, skipped = 0;
        var errors = new List<string>();
        var now = DateTime.UtcNow;

        foreach (var ws in workbook.Worksheets)
        {
            var name = ws.Name.Trim();
            if (string.IsNullOrWhiteSpace(name)) { skipped++; continue; }

            var lastRow = ws.LastRowUsed()?.RowNumber() ?? 0;
            if (lastRow < 2) { skipped++; continue; }

            var row2 = ws.Row(2);
            var email = FindCellValue(ws, 2, "E mail");
            var propertyTypes = FindCellValue(ws, 2, "Tip nekretnine");
            var legalFormStr = FindCellValue(ws, 2, "Opcija Firma/Individualni vještak");
            var polisa = FindCellValue(ws, 2, "Polisa");

            var legalForm = legalFormStr?.ToUpperInvariant().Contains("FIRMA") == true
                ? AppraiserLegalForm.Firm
                : AppraiserLegalForm.Individual;

            // Gradove ćitamo iz kolone A (redovi 3+)
            var cities = new List<string>();
            var gradCol = FindColumnIndex(ws, "Opstina/Grad") ?? FindColumnIndex(ws, "Grad") ?? 1;
            for (int r = 3; r <= lastRow; r++)
            {
                var city = ws.Row(r).Cell(gradCol).GetString().Trim();
                if (!string.IsNullOrWhiteSpace(city) && !city.Contains("Teritorija", StringComparison.OrdinalIgnoreCase))
                    cities.Add(city);
            }

            var supportedCities = cities.Count > 0 ? string.Join(",", cities.Distinct(StringComparer.OrdinalIgnoreCase)) : null;
            var primaryCity = cities.FirstOrDefault();

            try
            {
                var existing = await db.Appraisers.FirstOrDefaultAsync(a => a.Name == name, ct);
                if (existing is not null)
                {
                    existing.UpdateDetails(name, primaryCity, legalForm, email, null, polisa, now,
                        supportedPropertyTypes: propertyTypes, supportedCities: supportedCities);
                    updated++;
                }
                else
                {
                    var appraiser = Appraiser.Create(name, primaryCity, legalForm, email, null, polisa,
                        supportedPropertyTypes: propertyTypes, supportedCities: supportedCities);
                    db.Appraisers.Add(appraiser);
                    created++;
                }

                await db.SaveChangesAsync(ct);
            }
            catch (Exception ex)
            {
                // Unwrap EF Core DbUpdateException do stvarnog DB errora (npr. unique constraint)
                errors.Add($"Sheet '{name}': {UnwrapMessage(ex)}");
                db.ChangeTracker.Clear(); // resetuj kontekst da sljedeći sheet može nastaviti
                skipped++;
            }
        }

        return (created, updated, skipped, errors);
    }

    private static string? FindCellValue(IXLWorksheet ws, int row, string headerName)
    {
        var lastCol = ws.LastColumnUsed()?.ColumnNumber() ?? 0;
        var headerRow = ws.Row(1);
        for (int c = 1; c <= lastCol; c++)
        {
            if (headerRow.Cell(c).GetString().Trim().Equals(headerName, StringComparison.OrdinalIgnoreCase))
                return ws.Row(row).Cell(c).GetString().Trim();
        }
        return null;
    }

    private static int? FindColumnIndex(IXLWorksheet ws, string headerName)
    {
        var lastCol = ws.LastColumnUsed()?.ColumnNumber() ?? 0;
        var headerRow = ws.Row(1);
        for (int c = 1; c <= lastCol; c++)
        {
            if (headerRow.Cell(c).GetString().Trim().Equals(headerName, StringComparison.OrdinalIgnoreCase))
                return c;
        }
        return null;
    }

    public async Task<IReadOnlyList<Dictionary<string, string?>>> ExportRowsAsync(
        bool includeInactive, ImportContext ctx, CancellationToken ct)
    {
        var db = (ApplicationDbContext)ctx.DbContext;
        var query = db.Appraisers.AsNoTracking().AsQueryable();
        if (!includeInactive) query = query.Where(a => a.IsActive);

        var list = await query.OrderBy(a => a.Name).ToListAsync(ct);
        return list.Select(a => new Dictionary<string, string?>
        {
            ["Naziv"] = a.Name,
            ["Grad"] = a.City,
            ["Gradovi"] = a.SupportedCities,
            ["Tip nekretnine"] = a.SupportedPropertyTypes,
            ["Firma/Individualni"] = a.LegalForm == AppraiserLegalForm.Firm ? "Firma" : "Individualni",
            ["GO"] = a.IsOnLeave ? "Da" : "Ne",
            ["Aktivan"] = a.IsActive ? "Da" : "Ne",
            ["Email"] = a.ContactEmail,
            ["Telefon"] = a.ContactPhone,
        }).ToList();
    }

    /// <summary>
    /// Unwrapa Exception lanac do korijenskog uzroka.
    /// EF Core DbUpdateException ima generičku poruku u Message;
    /// stvarna SQL greška (npr. unique constraint, null violation) je u InnerException lancu.
    /// </summary>
    private static string UnwrapMessage(Exception ex)
    {
        var root = ex;
        while (root.InnerException is not null)
            root = root.InnerException;

        // Skratimo dugu SQL Server poruku na ključni dio (sve do prve "." ili newline)
        var msg = root.Message;
        var nl  = msg.IndexOfAny(['\n', '\r']);
        if (nl > 0) msg = msg[..nl].Trim();

        // Engleski EF poruka → prevedemo u razumljivu bosansku
        if (msg.Contains("unique", StringComparison.OrdinalIgnoreCase) ||
            msg.Contains("duplicate", StringComparison.OrdinalIgnoreCase))
            return $"Vještak s tim nazivom već postoji u bazi (duplikat). Originalna greška: {msg}";

        if (msg.Contains("null value", StringComparison.OrdinalIgnoreCase) ||
            msg.Contains("NOT NULL", StringComparison.OrdinalIgnoreCase))
            return $"Obavezno polje nije popunjeno u Excel fajlu. Originalna greška: {msg}";

        return msg;
    }

    private static bool ParseBool(string? value, bool defaultVal = false) => value switch
    {
        null or "" => defaultVal,
        "Da" or "da" or "DA" or "Yes" or "yes" or "1" or "true" => true,
        _ => false
    };
}
