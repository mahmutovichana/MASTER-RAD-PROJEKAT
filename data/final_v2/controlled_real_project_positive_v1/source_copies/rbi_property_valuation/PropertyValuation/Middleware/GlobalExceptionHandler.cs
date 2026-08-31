using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Api.Middleware;

/// <summary>
/// Centralni handler za izuzetke aplikacije.
/// Registruje se kao Singleton — scoped servisi (IAuditService) se dohvataju
/// putem IServiceScopeFactory, ne direktnom injekcijom.
/// </summary>
public sealed class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    private readonly IServiceScopeFactory _scopeFactory;

    public GlobalExceptionHandler(
        ILogger<GlobalExceptionHandler> logger,
        IServiceScopeFactory scopeFactory)
    {
        _logger       = logger;
        _scopeFactory = scopeFactory;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext       httpContext,
        Exception         exception,
        CancellationToken cancellationToken)
    {
        if (exception is OperationCanceledException && httpContext.RequestAborted.IsCancellationRequested)
            return true;

        var (statusCode, title, detail, errorCode) = exception switch
        {
            NotFoundException e                  => (404, "Not Found",            e.Message,                                              e.ErrorCode),
            ConflictException e                  => (409, "Conflict",             e.Message,                                              e.ErrorCode),
            InvalidStateTransitionException e    => (409, "Invalid State",        e.Message,                                              (string?)null),
            ForbiddenException e                 => (403, "Forbidden",            e.Message,                                              e.ErrorCode),
            ValidationException _                => (400, "Validation Error",     "Jedan ili više uslova validacije nisu ispunjeni.",     (string?)null),
            BadHttpRequestException e            => (e.StatusCode, "Bad Request", "Zahtjev nije ispravan. Provjerite format i sadržaj.",  (string?)null),
            _                                    => (500, "Internal Server Error", "Neočekivana greška servera.",                         (string?)null)
        };

        if (statusCode == 500)
            _logger.LogError(exception,
                "Neočekivana greška: {Message} | Path: {Path}",
                exception.Message, httpContext.Request.Path);

        // Audit 403 — kreiramo kratkotrajan scope da dohvatimo Scoped IAuditService
        if (statusCode == 403)
            await RecordSecurityAuditSafeAsync(exception.Message, httpContext.Request.Path.Value, cancellationToken);

        var problemDetails = new ProblemDetails
        {
            Status   = statusCode,
            Title    = title,
            Detail   = detail,
            Instance = httpContext.Request.Path,
            Type     = statusCode switch
            {
                400 => "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                403 => "https://tools.ietf.org/html/rfc7231#section-6.5.3",
                404 => "https://tools.ietf.org/html/rfc7231#section-6.5.4",
                409 => "https://tools.ietf.org/html/rfc7231#section-6.5.8",
                _   => "https://tools.ietf.org/html/rfc7231#section-6.6.1"
            }
        };

        if (!string.IsNullOrEmpty(errorCode))
            problemDetails.Extensions["errorCode"] = errorCode;

        var correlationId = httpContext.Items[HttpHeaders.CorrelationId] as string
                         ?? httpContext.TraceIdentifier;
        problemDetails.Extensions["correlationId"] = correlationId;

        if (exception is ValidationException ve)
        {
            if (ve.FieldErrors is { Count: > 0 })
                problemDetails.Extensions["fieldErrors"] = ve.FieldErrors;
            else if (ve.Errors is { Count: > 0 })
                problemDetails.Extensions["errors"] = ve.Errors;
        }

        httpContext.Response.StatusCode  = statusCode;
        httpContext.Response.ContentType = "application/problem+json";

        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);
        return true;
    }

    private async Task RecordSecurityAuditSafeAsync(
        string reason, string? requestPath, CancellationToken ct)
    {
        try
        {
            // Singleton handler ne može direktno injectovati Scoped servis —
            // kreiramo kratkotrajan scope samo za ovaj audit upis.
            await using var scope  = _scopeFactory.CreateAsyncScope();
            var auditService = scope.ServiceProvider.GetRequiredService<IAuditService>();

            await auditService.RecordAsync(new AuditEvent
            {
                Action            = AuditActions.PermissionDenied,
                OperationType     = AuditOperationTypes.AccessDenied,
                Module            = AuditModules.Security,
                EntityType        = "Endpoint",
                EntityKey         = requestPath,
                EntityDisplayName = requestPath,
                Status            = AuditStatuses.Forbidden,
                Severity          = AuditSeverity.Security,
                Reason            = reason
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Audit nije zapisao PERMISSION_DENIED za putanju {Path}.", requestPath);
        }
    }
}
