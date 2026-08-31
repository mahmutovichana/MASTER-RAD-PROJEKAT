using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class ProtocolEndpoints
{
    public static IEndpointRouteBuilder MapProtocolEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/protocol").WithTags("Protocol");

        group.MapGet("/orders", GetProtocolList)
             .RequireAuthorization(AppPolicies.ProtocolView)
             .WithName("GetProtocolOrders")
             .WithSummary("Lista svih protokolnih unosa narudžbi.");

        group.MapGet("/orders/{orderId:int}", GetByOrder)
             .RequireAuthorization(AppPolicies.ProtocolView)
             .WithName("GetProtocolByOrder")
             .WithSummary("Protokolni unos za konkretnu narudžbu.");

        return app;
    }

    private static async Task<IResult> GetProtocolList(
        IProtocolService service,
        int page     = 1,
        int pageSize = 20,
        CancellationToken ct = default)
    {
        var result = await service.GetProtocolListAsync(page, pageSize, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetByOrder(
        int orderId,
        IProtocolService service,
        CancellationToken ct)
    {
        var result = await service.GetByOrderIdAsync(orderId, ct);
        return Results.Ok(result);
    }
}
