namespace RBBH.CollateralAppraisal.Domain.Audit;

/// <summary>
/// Generički application audit zapis.
/// Ne vezan za konkretnu poslovnu tabelu — koristi EntityType/EntityKey umjesto OrderId, ClientId, itd.
/// Jedan isti mehanizam pokriva sve module: raspodjelu naloga, integracije, korisnike, šifarnike...
/// </summary>
public class AuditLog
{
    public long Id { get; private set; }
    public DateTime TimestampUtc { get; private set; }

    // ── Ko je pokrenuo akciju ────────────────────────────────────────────────
    public string ActorUserId { get; private set; } = string.Empty;
    public string ActorUsername { get; private set; } = string.Empty;
    public string? ActorEmail { get; private set; }
    /// <summary>Puno ime aktora u trenutku akcije (Keycloak "name" claim — vidi ICurrentUserService.FullName).</summary>
    public string? ActorFullName { get; private set; }
    /// <summary>Primarna rola aktora (prva iz Roles claim-a) — za korisnike sa jednom rolom, isto kao ActiveRole.</summary>
    public string? ActorRole { get; private set; }
    /// <summary>
    /// Aktivna rola odabrana kroz /select-role mehanizam u trenutku akcije (vidi X-Active-Role header,
    /// BaseApiService.cs). Bitno za korisnike sa više rola — ActorRole je samo "prva" rola iz tokena,
    /// ActiveRole je rola pod kojom je korisnik STVARNO radio akciju. Fallback na ActorRole ako header nije poslan.
    /// </summary>
    public string? ActiveRole { get; private set; }

    // ── Šta se desilo ────────────────────────────────────────────────────────
    /// <summary>Poslovna akcija (npr. ORDER_ASSIGNED_BY_SYSTEM). Vidi AuditActions.</summary>
    public string Action { get; private set; } = string.Empty;
    /// <summary>Tip operacije (npr. Assign, Update). Vidi AuditOperationTypes.</summary>
    public string OperationType { get; private set; } = string.Empty;
    /// <summary>Modul aplikacije (npr. OrderDistribution). Vidi AuditModules.</summary>
    public string Module { get; private set; } = string.Empty;

    // ── Izvor podataka ───────────────────────────────────────────────────────
    /// <summary>Naziv vanjskog sistema (npr. "ExternalOrdersDb", "SAP"). Nullable za interne akcije.</summary>
    public string? SourceSystem { get; private set; }
    /// <summary>Logički alias konekcije prema vanjskom sistemu.</summary>
    public string? SourceConnectionName { get; private set; }
    public string? SourceDatabase { get; private set; }
    public string? SourceSchema { get; private set; }
    /// <summary>Tabela ili endpoint u izvoru (npr. "public.orders", "payments/v2").</summary>
    public string? SourceTable { get; private set; }

    // ── Nad kojim entitetom ──────────────────────────────────────────────────
    /// <summary>Tip entiteta (npr. "Order", "User", "ExternalSync"). NIKAD konkretni ID kolumni.</summary>
    public string EntityType { get; private set; } = string.Empty;
    /// <summary>Ključ entiteta kao string. Može biti UUID, int, eksterni kod...</summary>
    public string? EntityKey { get; private set; }
    /// <summary>Čitljiv naziv za audit pregled (npr. "Nalog #123 — Zagreb").</summary>
    public string? EntityDisplayName { get; private set; }

    // ── Podaci o promjeni ────────────────────────────────────────────────────
    /// <summary>JSON stare vrijednosti (sanitizirane).</summary>
    public string? OldValuesJson { get; private set; }
    /// <summary>JSON novih vrijednosti (sanitizirane).</summary>
    public string? NewValuesJson { get; private set; }
    /// <summary>JSON lista promijenjenih polja (npr. ["AssignedAgent", "Status"]).</summary>
    public string? ChangedFieldsJson { get; private set; }

    // ── Ishod ────────────────────────────────────────────────────────────────
    /// <summary>Status izvršenja. Vidi AuditStatuses.</summary>
    public string Status { get; private set; } = string.Empty;
    /// <summary>Ozbiljnost eventa. Vidi AuditSeverity.</summary>
    public string Severity { get; private set; } = string.Empty;
    /// <summary>Obrazloženje akcije (npr. "Dodijeljen prema lokaciji i dostupnosti").</summary>
    public string? Reason { get; private set; }

    // ── Integracija ──────────────────────────────────────────────────────────
    /// <summary>Smjer integracije: Inbound | Outbound | Internal. Vidi AuditIntegrationDirection.</summary>
    public string? IntegrationDirection { get; private set; }
    /// <summary>ID zahtjeva prema vanjskom sistemu.</summary>
    public string? ExternalRequestId { get; private set; }
    /// <summary>HTTP status ili kod odgovora vanjskog sistema (npr. "200", "Timeout", "404").</summary>
    public string? ExternalResponseStatus { get; private set; }

    // ── HTTP kontekst zahtjeva ───────────────────────────────────────────────
    public string? CorrelationId { get; private set; }
    public string? RequestPath { get; private set; }
    public string? HttpMethod { get; private set; }
    public string? IpAddress { get; private set; }
    public string? UserAgent { get; private set; }

    private AuditLog() { }

    public static AuditLog Create(AuditLogData data) => new()
    {
        TimestampUtc          = data.TimestampUtc,
        ActorUserId           = data.ActorUserId,
        ActorUsername         = data.ActorUsername,
        ActorEmail            = data.ActorEmail,
        ActorFullName         = data.ActorFullName,
        ActorRole             = data.ActorRole,
        ActiveRole            = data.ActiveRole,
        Action                = data.Action,
        OperationType         = data.OperationType,
        Module                = data.Module,
        SourceSystem          = data.SourceSystem,
        SourceConnectionName  = data.SourceConnectionName,
        SourceDatabase        = data.SourceDatabase,
        SourceSchema          = data.SourceSchema,
        SourceTable           = data.SourceTable,
        EntityType            = data.EntityType,
        EntityKey             = data.EntityKey,
        EntityDisplayName     = data.EntityDisplayName,
        OldValuesJson         = data.OldValuesJson,
        NewValuesJson         = data.NewValuesJson,
        ChangedFieldsJson     = data.ChangedFieldsJson,
        Status                = data.Status,
        Severity              = data.Severity,
        Reason                = data.Reason,
        IntegrationDirection  = data.IntegrationDirection,
        ExternalRequestId     = data.ExternalRequestId,
        ExternalResponseStatus = data.ExternalResponseStatus,
        CorrelationId         = data.CorrelationId,
        RequestPath           = data.RequestPath,
        HttpMethod            = data.HttpMethod,
        IpAddress             = data.IpAddress,
        UserAgent             = data.UserAgent,
    };
}

/// <summary>
/// Podaci potrebni za kreiranje audit zapisa.
/// Odvojeno od entiteta kako bi se izbjegao konstruktor sa 28 parametara.
/// Gradi se u AuditService, a ne u poslovnoj logici — tamo se šalje samo AuditEvent.
/// </summary>
public sealed record AuditLogData(
    DateTime TimestampUtc,
    string   ActorUserId,
    string   ActorUsername,
    string?  ActorEmail,
    string?  ActorFullName,
    string?  ActorRole,
    string?  ActiveRole,
    string   Action,
    string   OperationType,
    string   Module,
    string?  SourceSystem,
    string?  SourceConnectionName,
    string?  SourceDatabase,
    string?  SourceSchema,
    string?  SourceTable,
    string   EntityType,
    string?  EntityKey,
    string?  EntityDisplayName,
    string?  OldValuesJson,
    string?  NewValuesJson,
    string?  ChangedFieldsJson,
    string   Status,
    string   Severity,
    string?  Reason,
    string?  IntegrationDirection,
    string?  ExternalRequestId,
    string?  ExternalResponseStatus,
    string?  CorrelationId,
    string?  RequestPath,
    string?  HttpMethod,
    string?  IpAddress,
    string?  UserAgent
);
