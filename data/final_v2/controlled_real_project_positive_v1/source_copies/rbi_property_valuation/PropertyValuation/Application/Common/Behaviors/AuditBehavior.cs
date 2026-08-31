using MediatR;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.CQRS;

namespace RBBH.CollateralAppraisal.Application.Common.Behaviors;

/// <summary>
/// Pipeline behavior za automatski audit log.
/// Primjenjuje se samo na komande koje implementuju IAuditableCommand.
///
/// NAPOMENA O DIZAJNU:
/// Postojeće komande delegiraju na servise koji interno audiraju s bogatijim kontekstom
/// (EntityDisplayName, OldValues, NewValues, višestruki eventi po operaciji).
/// AuditBehavior koristiti za buduće komande koje direktno implementiraju logiku u handleru.
/// </summary>
public sealed class AuditBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly IAuditService _audit;
    private readonly ILogger<AuditBehavior<TRequest, TResponse>> _logger;

    public AuditBehavior(IAuditService audit, ILogger<AuditBehavior<TRequest, TResponse>> logger)
    {
        _audit  = audit;
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (request is not IAuditableCommand auditCmd)
            return await next();

        var result = await next();

        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action        = auditCmd.AuditAction,
                EntityType    = auditCmd.AuditEntityType,
                EntityKey     = auditCmd.AuditEntityKey,
                Module        = auditCmd.AuditModule,
                OperationType = auditCmd.AuditOperationType,
                Status        = AuditStatuses.Success,
                Severity      = auditCmd.AuditSeverity
            }, cancellationToken);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "AuditBehavior greška za {Request}", typeof(TRequest).Name);
        }

        return result;
    }
}
