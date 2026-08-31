using MediatR;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.CaDocumentReview.Commands;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za CA pregled dokumentacije (US-91/92) — "Dopuna podataka" ↔
/// "Podaci dopunjeni" / "Završi pregled". Auto-discovery preko IEndpointModule.
/// </summary>
public sealed class CaDocumentReviewEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders/{orderId:int}")
            .WithTags("CA Document Review");

        group.MapPost("/request-correction", RequestCorrection)
            .RequireAuthorization(AppPolicies.OrdersRequestCorrection)
            .WithName("RequestCorrection")
            .WithSummary("CA vraća narudžbu Prodaji na dopunu podataka.");

        group.MapPost("/complete-review", CompleteReview)
            .RequireAuthorization(AppPolicies.OrdersCompleteReview)
            .WithName("CompleteReview")
            .WithSummary("CA završava pregled dokumentacije — dokumentacija je odobrena.");

        group.MapPost("/submit-correction", SubmitCorrection)
            .RequireAuthorization(AppPolicies.OrdersSubmitCorrection)
            .WithName("SubmitCorrection")
            .WithSummary("Prodaja potvrđuje da je dopuna podataka dostavljena.");
    }

    private static async Task<IResult> RequestCorrection(
        int orderId,
        RequestCorrectionRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new RequestCorrectionCommand(orderId, request.ReasonCodeId, request.Comment), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> CompleteReview(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new CompleteDocumentReviewCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SubmitCorrection(
        int orderId,
        SubmitCorrectionRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new SubmitCorrectionCommand(orderId, request.Comment), ct);
        return Results.Ok(result);
    }
}
