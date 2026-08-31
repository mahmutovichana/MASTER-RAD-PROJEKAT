using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class AuditEndpoints
{
    public static IEndpointRouteBuilder MapAuditEndpoints(this IEndpointRouteBuilder app)
    {
        app.MapGet("/api/audit", Query)
           .RequireAuthorization(AppPolicies.AuditViewSecurity)
           .WithTags("Audit")
           .WithName("QueryAuditLog")
           .WithSummary("Pregled audit loga sa filtriranjem po aktoru, modulu, akciji, statusu i datumu.");

        return app;
    }

    private static async Task<IResult> Query(
        [AsParameters] AuditQueryRequest request,
        IAuditQueryService service,
        CancellationToken ct)
    {
        var result = await service.QueryAsync(request, ct);
        return Results.Ok(result);
    }
}
