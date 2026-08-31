using MediatR;
using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Api.Middleware;
using RBBH.CollateralAppraisal.Application.OrderApproval.Commands;
using RBBH.CollateralAppraisal.Application.OrderApproval.Queries;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class OrderApprovalEndpoints
{
    public static IEndpointRouteBuilder MapOrderApprovalEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders/{orderId:int}").WithTags("Order Approval");

        group.MapPost("/approve-final", ApproveFinalAppraisal)
             .RequireAuthorization(AppPolicies.OrdersApproveFinal)
             .AddEndpointFilter<RateLimitEndpointFilter>()
             .WithName("ApproveFinalAppraisal")
             .WithSummary("CO odobrava finalnu procjenu i označava da može dalje u proceduru.");

        group.MapPost("/return-for-rework", ReturnForRework)
             .RequireAuthorization(AppPolicies.OrdersApproveFinal)
             .AddEndpointFilter<RateLimitEndpointFilter>()
             .WithName("ReturnForRework")
             .WithSummary("CO vraća procjenu na doradu — vještak prima email s komentarom.");

        group.MapGet("/final-appraisal", GetFinalAppraisal)
             .RequireAuthorization(AppPolicies.OrdersDownloadAppraisal)
             .WithName("GetFinalAppraisal")
             .WithSummary("Vraća metapodatke finalne procjene i link na download endpoint.");

        return app;
    }

    private static async Task<IResult> ApproveFinalAppraisal(
        int orderId,
        [FromBody] ApproveFinalRequest? request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new ApproveFinalAppraisalCommand(orderId, request?.AppraiserRating), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetFinalAppraisal(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetFinalAppraisalQuery(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ReturnForRework(
        int orderId,
        [FromBody] ReturnForReworkRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new ReturnForReworkCommand(orderId, request.Category, request.Comment), ct);
        return Results.Ok(result);
    }
}

public sealed record ApproveFinalRequest(int? AppraiserRating = null);
public sealed record ReturnForReworkRequest(string Category, string Comment);
