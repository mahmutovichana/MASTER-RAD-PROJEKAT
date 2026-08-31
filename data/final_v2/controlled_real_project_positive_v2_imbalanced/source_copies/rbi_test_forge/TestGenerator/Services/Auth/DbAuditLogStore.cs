using Dapper;
using Microsoft.Data.SqlClient;

namespace RBBH.TestAutomation.Api.Services.Auth;

/// <summary>
/// SQL Server implementacija <see cref="IAuditLogStore"/> — perzistira sigurnosne
/// (login/logout) audit zapise u tabelu <c>security_audit_log</c> da prežive restart
/// aplikacije. Zamjenjuje <see cref="InMemoryAuditLogStore"/> u Keycloak/produkcijskom
/// toku; mock/dev (bez baze) ostaje na in-memory varijanti.
///
/// <para><b>Best-effort:</b> upis ide na zasebnoj Microsoft.Data.SqlClient konekciji i obavijen je u
/// try/catch — ako audit upis padne (npr. baza nedostupna ili tabela ne postoji),
/// greška se loguje kao warning i NE propagira, da nikad ne sruši login/logout
/// korisnika. Čitanje (<see cref="GetRecent"/>) na grešci vraća praznu listu.</para>
///
/// Interfejs je sinhron (Add/GetRecent) pa se koriste sinhroni Dapper pozivi; sigurnosni
/// događaji su rijetki (samo na login/logout) tako da blokiranje nije problem.
/// </summary>
public sealed class DbAuditLogStore : IAuditLogStore
{
    private readonly string _connectionString;
    private readonly ILogger<DbAuditLogStore> _logger;

    public DbAuditLogStore(IConfiguration config, ILogger<DbAuditLogStore> logger)
    {
        _connectionString = config.GetConnectionString("Default")
            ?? throw new InvalidOperationException(
                "ConnectionStrings:Default nije konfigurisan.");
        _logger = logger;
    }

    public void Add(AuditLogEntry entry)
    {
        try
        {
            using var conn = new SqlConnection(_connectionString);
            conn.Open();
            conn.Execute(
                """
                INSERT INTO security_audit_log
                    (timestamp_utc, event_type, username, ip_address, failure_reason)
                VALUES
                    (@TimestampUtc, @EventType, @Username, @IpAddress, @FailureReason);
                """,
                entry);
        }
        catch (Exception ex)
        {
            // Best-effort: audit ne smije srušiti korisničku prijavu/odjavu.
            _logger.LogWarning(ex,
                "Sigurnosni audit upis nije uspio ({EventType} / {Username}).",
                entry.EventType, entry.Username);
        }
    }

    public IReadOnlyList<AuditLogEntry> GetRecent(int max = 100)
    {
        try
        {
            using var conn = new SqlConnection(_connectionString);
            conn.Open();
            return conn.Query<AuditLogEntry>(
                """
                SELECT TOP (@max) timestamp_utc AS TimestampUtc,
                       event_type      AS EventType,
                       username        AS Username,
                       ip_address      AS IpAddress,
                       failure_reason  AS FailureReason
                FROM   security_audit_log
                ORDER  BY timestamp_utc DESC;
                """,
                new { max }).ToList();
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Čitanje sigurnosnog audit loga iz baze nije uspjelo.");
            return [];
        }
    }
}
