using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

public sealed class AuditService : IAuditService
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = false,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    private readonly IEnumerable<IAuditSink> _sinks;
    private readonly IAuditLogQueue          _queue;
    private readonly IAuditValueSanitizer    _sanitizer;
    private readonly ICurrentUserService     _currentUser;
    private readonly IHttpContextAccessor    _httpContextAccessor;
    private readonly ILogger<AuditService>   _logger;

    public AuditService(
        IEnumerable<IAuditSink> sinks,
        IAuditLogQueue          queue,
        IAuditValueSanitizer    sanitizer,
        ICurrentUserService     currentUser,
        IHttpContextAccessor    httpContextAccessor,
        ILogger<AuditService>   logger)
    {
        _sinks               = sinks;
        _queue               = queue;
        _sanitizer           = sanitizer;
        _currentUser         = currentUser;
        _httpContextAccessor = httpContextAccessor;
        _logger              = logger;
    }

    /// <summary>
    /// Izgrađuje AuditLog SINHRONO (mora čitati HttpContext/ICurrentUserService dok su
    /// dostupni — request je još u toku), a zatim ga stavlja u red za asinhrono pisanje
    /// (vidi <see cref="IAuditLogQueue"/>/AuditLogQueueWorker). Stvarni DB/file upis se
    /// dešava u pozadini — download/upload NE čeka taj I/O (zahtjev: "audit log ne smije
    /// usporavati download").
    ///
    /// Pouzdanost: ako enqueue iz nekog razloga ne uspije (npr. CancellationToken),
    /// pada se na direktan upis kroz sinkove kao sigurnosna mreža — audit zapis se
    /// nikad tiho ne gubi.
    /// </summary>
    public async Task RecordAsync(AuditEvent auditEvent, CancellationToken cancellationToken = default)
    {
        AuditLog log;
        try
        {
            log = BuildAuditLog(auditEvent);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Neuspješna izgradnja AuditLog objekta za akciju {Action}", auditEvent.Action);
            return;
        }

        try
        {
            await _queue.EnqueueAsync(log, cancellationToken);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit queue enqueue nije uspio za akciju {Action} — pokušaj direktnog upisa.",
                auditEvent.Action);

            foreach (var sink in _sinks)
            {
                try
                {
                    await sink.WriteAsync(log, cancellationToken);
                }
                catch (Exception sinkEx)
                {
                    _logger.LogError(sinkEx,
                        "Audit sink {Sink} nije uspio (direktan fallback upis) za akciju {Action}",
                        sink.GetType().Name, auditEvent.Action);
                }
            }
        }
    }

    private AuditLog BuildAuditLog(AuditEvent evt)
    {
        var http = _httpContextAccessor.HttpContext;

        var data = new AuditLogData(
            TimestampUtc:          DateTime.UtcNow,
            ActorUserId:           _currentUser.UserId   ?? "system",
            ActorUsername:         _currentUser.Username ?? "system",
            ActorEmail:            _currentUser.Email,
            ActorFullName:         _currentUser.FullName,
            ActorRole:             _currentUser.Role,
            ActiveRole:            ResolveActiveRole(http),
            Action:                evt.Action,
            OperationType:         evt.OperationType,
            Module:                evt.Module,
            SourceSystem:          evt.SourceSystem,
            SourceConnectionName:  evt.SourceConnectionName,
            SourceDatabase:        evt.SourceDatabase,
            SourceSchema:          evt.SourceSchema,
            SourceTable:           evt.SourceTable,
            EntityType:            evt.EntityType,
            EntityKey:             evt.EntityKey,
            EntityDisplayName:     evt.EntityDisplayName,
            OldValuesJson:         _sanitizer.Sanitize(evt.OldValues),
            NewValuesJson:         _sanitizer.Sanitize(evt.NewValues),
            ChangedFieldsJson:     evt.ChangedFields is not null
                                       ? JsonSerializer.Serialize(evt.ChangedFields, JsonOptions)
                                       : null,
            Status:                evt.Status,
            Severity:              evt.Severity,
            Reason:                evt.Reason,
            IntegrationDirection:  evt.IntegrationDirection,
            ExternalRequestId:     evt.ExternalRequestId,
            ExternalResponseStatus: evt.ExternalResponseStatus,
            CorrelationId:         ResolveCorrelationId(http, evt),
            RequestPath:           http?.Request.Path.Value,
            HttpMethod:            http?.Request.Method,
            IpAddress:             ResolveIpAddress(http),
            UserAgent:             http?.Request.Headers.UserAgent.ToString()
        );

        return AuditLog.Create(data);
    }

    private static string? ResolveCorrelationId(HttpContext? http, AuditEvent evt)
    {
        if (evt.CorrelationId is not null)
            return evt.CorrelationId;

        // Čitamo iz Items — CorrelationIdMiddleware uvijek upiše vrijednost (ili GUID ili header)
        return http?.Items[HttpHeaders.CorrelationId] as string;
    }

    private static string? ResolveIpAddress(HttpContext? http)
    {
        if (http is null) return null;

        var forwarded = http.Request.Headers["X-Forwarded-For"].ToString();
        if (!string.IsNullOrWhiteSpace(forwarded))
            return forwarded.Split(',')[0].Trim();

        return http.Connection.RemoteIpAddress?.ToString();
    }

    /// <summary>
    /// Aktivna rola pod kojom je korisnik izvršio akciju. Frontend šalje X-Active-Role
    /// header (vidi BaseApiService) postavljen iz ActiveRoleState — bitno za korisnike
    /// sa više rola gdje ActorRole (prva rola iz tokena) ne mora biti rola koju je
    /// korisnik stvarno odabrao za tu sesiju. Fallback na ActorRole ako header nedostaje
    /// (npr. poziv van browsera, stariji klijent, korisnik sa samo jednom rolom).
    /// </summary>
    private string? ResolveActiveRole(HttpContext? http)
    {
        var header = http?.Request.Headers[HttpHeaders.ActiveRole].ToString();
        return !string.IsNullOrWhiteSpace(header) ? header : _currentUser.Role;
    }
}
