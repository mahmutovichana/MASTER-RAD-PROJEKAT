namespace RBBH.TestAutomation.Api.Services.Auth;

/// <summary>
/// Apstrakcija nad pohranom audit zapisa.
///
/// Buduća API/DB verzija: zamijeniti in-memory implementaciju s ApiAuditLogStore
/// koji piše u SQL Server preko backend API-ja — consumeri (SecurityEventLogger,
/// AuditLog stranica) ostaju nepromijenjeni.
/// </summary>
public interface IAuditLogStore
{
    /// <summary>Dodaje novi zapis.</summary>
    void Add(AuditLogEntry entry);

    /// <summary>Vraća najnovije zapise (od najnovijeg prema starijem).</summary>
    IReadOnlyList<AuditLogEntry> GetRecent(int max = 100);
}
