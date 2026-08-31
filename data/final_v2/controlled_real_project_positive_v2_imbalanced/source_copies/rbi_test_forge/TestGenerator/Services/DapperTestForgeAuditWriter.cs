using System.Text.Json;
using Dapper;
using Microsoft.Data.SqlClient;
using RBBH.TestAutomation.Core.Repositories;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Dapper/Microsoft.Data.SqlClient implementacija <see cref="ITestForgeAuditWriter"/> — upisuje TestForge
/// audit zapise u dijeljenu <c>audit_log</c> tabelu (ista tabela i isti obrazac kao
/// <see cref="SifarnikService"/>).
///
/// <para><b>Best-effort:</b> upis u <c>audit_log</c> ide na zasebnoj Microsoft.Data.SqlClient konekciji
/// (ne dijeli EF transakciju, jer repozitoriji pišu kroz EF Core). Ako audit upis padne,
/// greška se loguje kao warning i ne propagira — korisnička operacija (EF write koji je
/// već commitan) ostaje uspješna.</para>
/// </summary>
public sealed class DapperTestForgeAuditWriter : ITestForgeAuditWriter
{
    private readonly string _connectionString;
    private readonly ILogger<DapperTestForgeAuditWriter> _logger;

    private static readonly JsonSerializerOptions _jsonOpts = new() { WriteIndented = false };

    public DapperTestForgeAuditWriter(IConfiguration config, ILogger<DapperTestForgeAuditWriter> logger)
    {
        _connectionString = config.GetConnectionString("Default")
            ?? throw new InvalidOperationException(
                "ConnectionStrings:Default nije konfigurisan.");
        _logger = logger;
    }

    public async Task WriteAsync(
        string entityType,
        Guid entityId,
        string action,
        string actorId,
        string actorName,
        object? oldValues,
        object? newValues,
        CancellationToken ct = default)
    {
        try
        {
            var oldJson = oldValues is null ? null : JsonSerializer.Serialize(oldValues, _jsonOpts);
            var newJson = newValues is null ? null : JsonSerializer.Serialize(newValues, _jsonOpts);

            await using var conn = new SqlConnection(_connectionString);
            await conn.OpenAsync(ct);
            await conn.ExecuteAsync(new CommandDefinition(
                """
                INSERT INTO audit_log
                    (entity_type, entity_id, action, changed_by, changed_by_name, old_values, new_values)
                VALUES
                    (@entityType, @entityId, @action, @actorId, @actorName,
                     @oldJson, @newJson);
                """,
                new { entityType, entityId, action, actorId, actorName, oldJson, newJson },
                cancellationToken: ct));
        }
        catch (Exception ex)
        {
            // Best-effort: audit ne smije srušiti korisničku operaciju.
            _logger.LogWarning(ex,
                "TestForge audit zapis nije uspio za {EntityType} {EntityId} ({Action}).",
                entityType, entityId, action);
        }
    }
}
