using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Application.Codebooks.Import;

/// <summary>
/// Per-codebook mapper: definiše kolone, validira redove, kreira/ažurira entitete.
/// Svaki šifarnik registruje svoju implementaciju.
/// </summary>
public interface ICodebookMapper
{
    string CodebookType { get; }
    IReadOnlyList<ColumnDef> Columns { get; }

    /// <summary>
    /// Naziv kolone za duplikat provjeru. Null = nema duplikat provjere (npr. narudžbe gdje isti vještak ima više redova).
    /// Default: prva kolona iz Columns.
    /// </summary>
    [ExcludeFromCodeCoverage]
    string? DuplicateKeyColumn => Columns[0].Name;

    /// <summary>Validira jedan red i vraća greške (prazan ako OK).</summary>
    Task<IReadOnlyList<ImportRowError>> ValidateRowAsync(ParsedRow row, ImportContext context, CancellationToken ct);

    /// <summary>Klasificira red: New, Update, Skip.</summary>
    Task<RowAction> ClassifyRowAsync(ParsedRow row, ImportContext context, CancellationToken ct);

    /// <summary>Primjenjuje red na bazu (insert ili update).</summary>
    Task ApplyRowAsync(ParsedRow row, RowAction action, ImportContext context, CancellationToken ct);

    /// <summary>Deaktivira zapise koji nisu u importovanom setu (za Mode=DeactivateMissing).</summary>
    Task<int> DeactivateMissingAsync(IReadOnlyList<ParsedRow> importedRows, ImportContext context, CancellationToken ct);

    /// <summary>Generiše export redove za sve zapise.</summary>
    Task<IReadOnlyList<Dictionary<string, string?>>> ExportRowsAsync(bool includeInactive, ImportContext context, CancellationToken ct);
}

[ExcludeFromCodeCoverage]
public sealed record ColumnDef(string Name, string Label, bool Required);

public enum RowAction { New, Update, Skip }

/// <summary>Dijeljeni kontekst za import sesiju — DB access, cached lookups.</summary>
[ExcludeFromCodeCoverage]
public sealed class ImportContext
{
    public required object DbContext { get; init; }
    public required string? UserId { get; init; }
    public Dictionary<string, object> Cache { get; } = new();
}
