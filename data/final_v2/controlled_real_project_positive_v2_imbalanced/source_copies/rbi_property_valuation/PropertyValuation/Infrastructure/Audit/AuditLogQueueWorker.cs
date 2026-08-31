using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Pozadinski worker koji prazni in-memory AuditLogQueue i upisuje zapise kroz
/// IAuditSink implementacije (DatabaseAuditSink → FileAuditSink fallback).
///
/// AuditService.RecordAsync stavlja AuditLog u in-memory channel; ovaj worker
/// čita iz tog istog channela i persistira u bazu/fajl u pozadini.
/// Time-to-persist: zanemarivo (mikrosekunde za enqueue + async drain).
/// </summary>
[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed class AuditLogQueueWorker : BackgroundService
{
    private readonly AuditLogQueue               _queue;
    private readonly IServiceScopeFactory        _scopeFactory;
    private readonly ILogger<AuditLogQueueWorker> _logger;

    public AuditLogQueueWorker(
        AuditLogQueue                queue,
        IServiceScopeFactory         scopeFactory,
        ILogger<AuditLogQueueWorker> logger)
    {
        _queue        = queue;
        _scopeFactory = scopeFactory;
        _logger       = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var log in _queue.Reader.ReadAllAsync(stoppingToken))
        {
            await ProcessAsync(log, stoppingToken);
        }
    }

    private async Task ProcessAsync(AuditLog log, CancellationToken ct)
    {
        try
        {
            using var scope = _scopeFactory.CreateScope();
            var sinks = scope.ServiceProvider.GetServices<IAuditSink>();
            foreach (var sink in sinks)
            {
                try   { await sink.WriteAsync(log, ct); }
                catch (Exception ex)
                {
                    _logger.LogError(ex,
                        "AuditLogQueueWorker: sink {Sink} nije uspio za akciju {Action}.",
                        sink.GetType().Name, log.Action);
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "AuditLogQueueWorker: neočekivana greška pri obradi akcije {Action}.", log.Action);
        }
    }
}
