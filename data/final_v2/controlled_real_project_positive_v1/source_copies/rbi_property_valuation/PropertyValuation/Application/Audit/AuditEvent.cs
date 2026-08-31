namespace RBBH.CollateralAppraisal.Application.Audit;

/// <summary>
/// DTO koji poslovna logika šalje audit sistemu.
/// AuditService ga pretvara u AuditLog entitet koji se fizički čuva.
///
/// OldValues i NewValues su <c>object?</c> — primamo bilo koji C# objekat
/// (anonimni tip, DTO, string, broj...) i serijalizujemo ga u JSON u AuditService.
/// Tako poslovna logika ne mora znati ništa o serijalizaciji ili storage-u.
/// </summary>
public sealed class AuditEvent
{
    // ── Šta se desilo ────────────────────────────────────────────────────────
    /// <summary>Poslovna akcija. Koristiti konstante iz <see cref="AuditActions"/>.</summary>
    public required string Action { get; init; }

    /// <summary>Tip operacije. Koristiti konstante iz <see cref="AuditOperationTypes"/>.</summary>
    public required string OperationType { get; init; }

    /// <summary>Modul aplikacije. Koristiti konstante iz <see cref="AuditModules"/>.</summary>
    public required string Module { get; init; }

    // ── Izvor podataka ───────────────────────────────────────────────────────
    /// <summary>Naziv vanjskog sistema (npr. "ExternalOrdersDb"). Null za interne akcije.</summary>
    public string? SourceSystem { get; init; }

    /// <summary>Logički alias konekcije (npr. "OrdersConnection").</summary>
    public string? SourceConnectionName { get; init; }

    /// <summary>Naziv baze u vanjskom sistemu.</summary>
    public string? SourceDatabase { get; init; }

    /// <summary>Shema u bazi izvora (npr. "public", "dbo").</summary>
    public string? SourceSchema { get; init; }

    /// <summary>Tabela ili endpoint u izvoru (npr. "orders", "payments/v2/transactions").</summary>
    public string? SourceTable { get; init; }

    // ── Nad kojim entitetom ──────────────────────────────────────────────────
    /// <summary>
    /// Tip entiteta. Uvijek koristiti generički naziv — NIKAD OrderId, ClientId itd.
    /// Primjeri: "Order", "User", "Request", "ExternalSync", "RoleAssignment"
    /// </summary>
    public required string EntityType { get; init; }

    /// <summary>
    /// Ključ entiteta kao string. Konvertovati int/Guid/string prema potrebi.
    /// Nullable — nije uvijek poznat (npr. bulk operacije, sinhronizacijski job).
    /// </summary>
    public string? EntityKey { get; init; }

    /// <summary>Čitljiv opis za audit pregled (npr. "Nalog #123 — Zagreb, Ilica 5").</summary>
    public string? EntityDisplayName { get; init; }

    // ── Podaci o promjeni ────────────────────────────────────────────────────
    /// <summary>
    /// Stare vrijednosti — bilo koji C# objekat (anonimni tip, DTO...).
    /// AuditService serijalizuje i sanitizuje prije upisa.
    /// </summary>
    public object? OldValues { get; init; }

    /// <summary>
    /// Nove vrijednosti — bilo koji C# objekat.
    /// AuditService serijalizuje i sanitizuje prije upisa.
    /// </summary>
    public object? NewValues { get; init; }

    /// <summary>Lista naziva polja koja su promijenjena (npr. ["AssignedAgent", "Status"]).</summary>
    public IReadOnlyList<string>? ChangedFields { get; init; }

    // ── Ishod ────────────────────────────────────────────────────────────────
    /// <summary>Status izvršenja. Koristiti konstante iz <see cref="AuditStatuses"/>.</summary>
    public required string Status { get; init; }

    /// <summary>Ozbiljnost. Koristiti konstante iz <see cref="AuditSeverity"/>.</summary>
    public required string Severity { get; init; }

    /// <summary>Obrazloženje akcije ili razlog greške.</summary>
    public string? Reason { get; init; }

    // ── Integracija ──────────────────────────────────────────────────────────
    /// <summary>
    /// Smjer integracije. Koristiti konstante iz <see cref="AuditIntegrationDirection"/>.
    /// Primjeri: "Inbound", "Outbound", "Internal"
    /// </summary>
    public string? IntegrationDirection { get; init; }

    /// <summary>ID zahtjeva prema vanjskom sistemu (ako je dostupan).</summary>
    public string? ExternalRequestId { get; init; }

    /// <summary>HTTP status ili kod odgovora vanjskog sistema (npr. "200", "Timeout").</summary>
    public string? ExternalResponseStatus { get; init; }

    // ── HTTP / Tracing kontekst ───────────────────────────────────────────────
    /// <summary>
    /// Korelacijski ID za praćenje zahtjeva kroz sistem.
    /// Postavi eksplicitno u background jobovima koji nemaju HTTP kontekst.
    /// Za HTTP zahtjeve, AuditService čita X-Correlation-Id header automatski.
    /// </summary>
    public string? CorrelationId { get; init; }
}
