using System.Text.Json;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Transactional outbox implementacija IAuditLogQueue.
/// Serializira AuditLog u JSON i upisuje u AuditOutbox tabelu.
/// AuditLogQueueWorker čita i prosljeđuje sinkovima u pozadini.
///
/// Zašto singleton + IServiceScopeFactory: IAuditLogQueue mora biti singleton
/// (injectuje se u AuditService koji je scoped, ali i u singleton middleware-ove).
/// Scope se kreira per-enqueue da dohvati scoped ApplicationDbContext.
/// </summary>
public sealed class DbAuditLogQueue : IAuditLogQueue
{
    private static readonly JsonSerializerOptions JsonOpts = new()
    {
        WriteIndented            = false,
        PropertyNamingPolicy     = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true
    };

    private readonly IServiceScopeFactory      _scopeFactory;
    private readonly ILogger<DbAuditLogQueue>  _logger;

    public DbAuditLogQueue(IServiceScopeFactory scopeFactory, ILogger<DbAuditLogQueue> logger)
    {
        _scopeFactory = scopeFactory;
        _logger       = logger;
    }

    public async ValueTask EnqueueAsync(AuditLog log, CancellationToken ct = default)
    {
        string json;
        try
        {
            json = JsonSerializer.Serialize(log, JsonOpts);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit outbox: neuspješna serializacija za akciju {Action}", log.Action);
            return;
        }

        try
        {
            using var scope = _scopeFactory.CreateScope();
            var db          = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
            db.AuditOutbox.Add(AuditOutboxEntry.Create(json));
            // CancellationToken.None — audit ne smije biti otkazan zajedno s HTTP zahtjevom
            await db.SaveChangesAsync(CancellationToken.None);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit outbox: DB upis nije uspio za akciju {Action}", log.Action);
            // Ne bacamo dalje — AuditService ima vlastiti fallback na direktan sink upis
        }
    }
}
