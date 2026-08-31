using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Opinions.Commands;
using RBBH.CollateralAppraisal.Application.Opinions.Queries;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Orders;
using MediatR;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za mišljenja CO i Pravne službe (US 94).
/// Auto-discovery preko IEndpointModule — ne treba mijenjati WebApplicationExtensions.
/// </summary>
public sealed class OpinionEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders/{orderId:int}").WithTags("Opinions");

        group.MapPost("/opinions/request", RequestOpinions)
             .RequireAuthorization(AppPolicies.OpinionsRequest)
             .WithName("RequestOpinions")
             .WithSummary("AM/SM/UB šalje zahtjev za mišljenje CO i Pravne.");

        group.MapPost("/opinions/{type}", SubmitOpinion)
             .RequireAuthorization()
             .WithName("SubmitOpinion")
             .WithSummary("CO ili Pravna importuju PDF mišljenja.")
             .DisableAntiforgery();

        group.MapGet("/opinions", GetOpinions)
             .RequireAuthorization(AppPolicies.OpinionsView)
             .WithName("GetOpinions")
             .WithSummary("Vraća status mišljenja za UI.");
    }

    private static async Task<IResult> RequestOpinions(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        await mediator.Send(new RequestOpinionsCommand(orderId), ct);
        return Results.Ok(new { message = "Zahtjev za mišljenje poslan CO i Pravnoj službi." });
    }

    private static async Task<IResult> SubmitOpinion(
        int orderId,
        string type,
        IFormFile file,
        [FromForm] string? comment,
        IMediator mediator,
        ICurrentUserService currentUser,
        CancellationToken ct)
    {
        var (opinionType, requiredRole) = type switch
        {
            "CO"     => (OpinionType.CO, AppRoles.KolateralOficir),
            "Pravna" => (OpinionType.Pravna, AppRoles.PravnaSluzba),
            _        => ((OpinionType?)null, (string?)null)
        };

        if (opinionType is null || requiredRole is null)
            return Results.BadRequest(new { message = "Nepoznat tip mišljenja. Dozvoljeno: CO, Pravna." });

        if (!currentUser.Roles.Contains(requiredRole))
            return Results.Forbid();

        if (currentUser.UserId is null)
            return Results.Unauthorized();

        await using var stream = file.OpenReadStream();
        using var ms = new MemoryStream();
        await stream.CopyToAsync(ms, ct);
        await mediator.Send(new SubmitOpinionCommand(
            orderId, opinionType.Value, ms.ToArray(),
            file.FileName, file.ContentType, comment,
            currentUser.UserId), ct);

        return Results.Ok(new { message = "Mišljenje uspješno importovano." });
    }

    private static async Task<IResult> GetOpinions(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetOpinionsQuery(orderId), ct);
        return Results.Ok(result);
    }
}
