using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Orders;
using ApplicationAppRoles = RBBH.CollateralAppraisal.Application.Security.AppRoles;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Centralizirani authorization guard za narudžbe — eliminacija dupliciranog auth koda.
/// Koristi se u svim servisima koji pristupaju narudžbama.
/// </summary>
public sealed class OrderAuthorizationGuard
{
    private readonly ICurrentUserService _currentUser;
    private readonly IAuditService _audit;

    public OrderAuthorizationGuard(ICurrentUserService currentUser, IAuditService audit)
    {
        _currentUser = currentUser;
        _audit = audit;
    }

    public async Task EnsureCanViewAsync(AppraisalOrder order, CancellationToken ct)
    {
        var isOwner      = order.CreatedByUserId == _currentUser.UserId;
        var hasAllAccess = _currentUser.Roles.Any(ApplicationAppRoles.OrderViewerRoles.Contains);

        if (!isOwner && !hasAllAccess)
            await DenyAccessAsync(order, "Nemate pristup ovoj narudžbi.", ct);
    }

    public async Task EnsureOwnerAsync(AppraisalOrder order, CancellationToken ct)
    {
        if (order.CreatedByUserId != _currentUser.UserId &&
            !_currentUser.Roles.Contains(ApplicationAppRoles.Administrator))
            await DenyAccessAsync(order, "Samo kreator narudžbe ili administrator mogu izvršiti ovu akciju.", ct);
    }

    private async Task DenyAccessAsync(AppraisalOrder order, string message, CancellationToken ct)
    {
        await _audit.RecordAsync(new AuditEvent
        {
            Action            = AuditActions.UnauthorizedOrderAccess,
            OperationType     = AuditOperationTypes.AccessDenied,
            Module            = AuditModules.AppraisalOrders,
            EntityType        = "AppraisalOrder",
            EntityKey         = order.Id.ToString(),
            EntityDisplayName = order.Title,
            Status            = AuditStatuses.Forbidden,
            Severity          = AuditSeverity.Security
        }, ct);
        throw new ForbiddenException(message);
    }
}
