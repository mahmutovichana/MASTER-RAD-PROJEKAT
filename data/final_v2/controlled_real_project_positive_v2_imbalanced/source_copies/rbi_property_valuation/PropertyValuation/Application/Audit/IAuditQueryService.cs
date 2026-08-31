using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Roles.Models;
using RBBH.CollateralAppraisal.Application.Roles.Requests;

namespace RBBH.CollateralAppraisal.Application.Audit;

public interface IAuditQueryService
{
    Task<PagedResult<AuditLogDto>> QueryAsync(AuditQueryRequest request, CancellationToken ct = default);
}
