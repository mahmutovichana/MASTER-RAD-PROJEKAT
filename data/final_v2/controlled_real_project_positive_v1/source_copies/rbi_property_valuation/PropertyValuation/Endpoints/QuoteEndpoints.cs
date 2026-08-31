using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za vještaka — odgovor na zahtjev za ponudu (PL, AC 5).
/// Auto-discovery preko IEndpointModule.
/// </summary>
public sealed class QuoteEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders/{orderId:int}/quote-requests")
            .WithTags("QuoteRequests");

        group.MapPost("/{quoteRequestId:int}/respond", RespondToQuote)
             .RequireAuthorization(AppPolicies.OrdersView)
             .WithName("RespondToQuote")
             .WithSummary("Vještak odgovara na zahtjev za ponudu — šalje cijenu i rok izrade (PL).");
    }

    private static async Task<IResult> RespondToQuote(
        int orderId,
        int quoteRequestId,
        [FromBody] RespondToQuoteCommand command,
        IQuoteRequestService service,
        CancellationToken ct)
    {
        var result = await service.RespondToQuoteAsync(orderId, quoteRequestId, command, ct);
        return Results.Ok(result);
    }
}