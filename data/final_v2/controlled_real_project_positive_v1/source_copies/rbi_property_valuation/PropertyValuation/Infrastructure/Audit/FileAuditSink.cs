using System.Text.Json;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Fallback audit sink koji upisuje audit zapise u JSON fajlove na disku.
///
/// Koristi se kao sekundarni sink za otpornost sistema:
///   - Automatski se aktivira kada DatabaseAuditSink ne uspije (fan-out pattern u AuditService).
///   - Fajlovi se organizuju po datumu: /audit-logs/audit-2026-06-08.jsonl
///   - Format je JSONL (jedan JSON objekt po liniji) — čitljivo i pogodno za uvoz u SIEM sisteme.
///
/// U produkciji preporučiti rotaciju fajlova i arhiviranje starih logova.
/// </summary>
public sealed class FileAuditSink : IAuditSink
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented        = false,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    private readonly string _logDirectory;
    private readonly ILogger<FileAuditSink> _logger;

    private static readonly SemaphoreSlim _writeLock = new(1, 1);

    public FileAuditSink(ILogger<FileAuditSink> logger)
    {
        _logger = logger;
        _logDirectory = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
            "audit-logs");
    }

    public async Task WriteAsync(AuditLog log, CancellationToken cancellationToken = default)
    {
        try
        {
            Directory.CreateDirectory(_logDirectory);

            var fileName = $"audit-{log.TimestampUtc:yyyy-MM-dd}.jsonl";
            var filePath = Path.Combine(_logDirectory, fileName);

            var entry = new
            {
                id                   = log.Id,
                timestampUtc         = log.TimestampUtc,
                actorUserId          = log.ActorUserId,
                actorUsername        = log.ActorUsername,
                actorEmail           = log.ActorEmail,
                actorRole            = log.ActorRole,
                action               = log.Action,
                operationType        = log.OperationType,
                module               = log.Module,
                entityType           = log.EntityType,
                entityKey            = log.EntityKey,
                entityDisplayName    = log.EntityDisplayName,
                oldValuesJson        = log.OldValuesJson,
                newValuesJson        = log.NewValuesJson,
                changedFieldsJson    = log.ChangedFieldsJson,
                status               = log.Status,
                severity             = log.Severity,
                reason               = log.Reason,
                correlationId        = log.CorrelationId,
                requestPath          = log.RequestPath,
                httpMethod           = log.HttpMethod,
                ipAddress            = log.IpAddress,
                userAgent            = log.UserAgent,
                sourceSystem         = log.SourceSystem,
                integrationDirection = log.IntegrationDirection
            };

            var line = JsonSerializer.Serialize(entry, JsonOptions) + Environment.NewLine;

            // SemaphoreSlim osigurava thread-safe pristup fajlu bez blokiranja async konteksta
            await _writeLock.WaitAsync(cancellationToken);
            try
            {
                await File.AppendAllTextAsync(filePath, line, cancellationToken);
            }
            finally
            {
                _writeLock.Release();
            }
        }
        catch (Exception ex)
        {
            // FileAuditSink je sam po sebi fallback — greška ovdje se samo loguje
            _logger.LogError(ex,
                "FileAuditSink nije uspio upisati audit zapis za akciju {Action}.", log.Action);
        }
    }
}
