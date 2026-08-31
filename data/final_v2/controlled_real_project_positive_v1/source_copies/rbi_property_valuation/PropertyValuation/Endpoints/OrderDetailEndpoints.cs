using MediatR;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Orders.Queries;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class OrderDetailEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders")
            .WithTags("Orders");

        group.MapGet("/{orderId:int}/detail", GetById)
            .RequireAuthorization(AppPolicies.OrdersView)
            .WithName("GetOrderDetailById")
            .WithSummary("Vraća detalje narudžbe procjene, sa Capabilities za trenutnog korisnika (US 92/93/94).");
    }

    private static async Task<IResult> GetById(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetOrderDetailQuery(orderId), ct);
        return Results.Ok(result);
    }
}
