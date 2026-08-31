using MediatR;
using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;
using RBBH.CollateralAppraisal.Application.AppraiserAssignment.Queries;
using RBBH.CollateralAppraisal.Application.Appraisers;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.QuoteRequests.Commands;
using RBBH.CollateralAppraisal.Application.QuoteRequests.Queries;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za master-data vještaka (Faza C) i odabir vještaka za narudžbu.
/// Auto-discovery preko IEndpointModule.
/// </summary>
public sealed class AppraiserEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/appraisers").WithTags("Appraisers");

        group.MapGet("/", GetList)
            .RequireAuthorization(AppPolicies.AppraisersView)
            .WithName("GetAppraisers")
            .WithSummary("Pregled liste vještaka sa filterima i brojem aktivnih procjena.");

        group.MapGet("/{id:int}", GetById)
            .RequireAuthorization(AppPolicies.AppraisersView)
            .WithName("GetAppraiserById")
            .WithSummary("Detalji vještaka.");

        group.MapPost("/", Create)
            .RequireAuthorization(AppPolicies.AppraisersManage)
            .WithName("CreateAppraiser")
            .WithSummary("Kreira novog vještaka.");

        group.MapPut("/{id:int}", Update)
            .RequireAuthorization(AppPolicies.AppraisersManage)
            .WithName("UpdateAppraiser")
            .WithSummary("Ažurira podatke vještaka.");

        group.MapPost("/{id:int}/on-leave", SetOnLeave)
            .RequireAuthorization(AppPolicies.AppraisersManage)
            .WithName("SetAppraiserOnLeave")
            .WithSummary("Postavlja/uklanja status godišnjeg odmora (GO) vještaka.");

        group.MapPost("/{id:int}/blacklist", SetBlacklisted)
            .RequireAuthorization(AppPolicies.AppraisersManage)
            .WithName("SetAppraiserBlacklisted")
            .WithSummary("Postavlja/uklanja vještaka sa crne liste.");

        group.MapDelete("/{id:int}", Deactivate)
            .RequireAuthorization(AppPolicies.AppraisersManage)
            .WithName("DeactivateAppraiser")
            .WithSummary("Deaktivira vještaka (soft).");

        app.MapPost("/api/orders/{orderId:int}/select-appraiser/auto", AutoSelectAppraiser)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("Appraisers")
            .WithName("AutoSelectAppraiser")
            .WithSummary("FL — automatski odabir vještaka za narudžbu prema algoritmu.");

        app.MapGet("/api/orders/{orderId:int}/appraiser-candidates", GetCandidates)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("Appraisers")
            .WithName("GetAppraiserCandidates")
            .WithSummary("PL / FL fallback — lista vještaka pogodnih za ručni odabir.");

        app.MapPost("/api/orders/{orderId:int}/select-appraiser/manual", ManualSelectAppraiser)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("Appraisers")
            .WithName("ManualSelectAppraiser")
            .WithSummary("PL / FL fallback — ručni odabir vještaka sa liste kandidata.");

        app.MapPost("/api/orders/{orderId:int}/send-to-appraiser", SendToAppraiser)
            .RequireAuthorization(AppPolicies.OrdersSendToAppraiser)
            .WithTags("Appraisers")
            .WithName("SendToAppraiser")
            .WithSummary("CA šalje narudžbu odabranom vještaku.");

        app.MapGet("/api/orders/{orderId:int}/appraiser-package", GetAppraiserPackage)
            .RequireAuthorization(AppPolicies.OrdersSendToAppraiser)
            .WithTags("Appraisers")
            .WithName("GetAppraiserPackage")
            .WithSummary("Paket dokumenata za odabranog vještaka (download linkovi).");

        app.MapPost("/api/orders/{orderId:int}/accept-by-appraiser", AcceptByAppraiser)
            .RequireAuthorization(AppPolicies.OrdersAccept)
            .WithTags("Appraisers")
            .WithName("AcceptByAppraiser")
            .WithSummary("Vještak prihvata dodijeljenu narudžbu i započinje izradu procjene.");

        app.MapPost("/api/orders/{orderId:int}/reject-by-appraiser", RejectByAppraiser)
            .RequireAuthorization(AppPolicies.OrdersAccept)
            .WithTags("Appraisers")
            .WithName("RejectByAppraiser")
            .WithSummary("Vještak odbija narudžbu s razlogom — sistem automatski dodjeljuje sljedećeg vještaka.");

        app.MapPost("/api/orders/{orderId:int}/request-additional-payment", RequestAdditionalPayment)
            .RequireAuthorization(AppPolicies.OrdersAccept)
            .WithTags("Appraisers")
            .WithName("RequestAdditionalPayment")
            .WithSummary("Vještak traži doplatu — CA prima notifikaciju i potvrđuje uplatu.");

        app.MapPost("/api/orders/{orderId:int}/confirm-additional-payment", ConfirmAdditionalPayment)
            .RequireAuthorization(AppPolicies.OrdersSendToAppraiser)
            .WithTags("Appraisers")
            .WithName("ConfirmAdditionalPayment")
            .WithSummary("CA potvrđuje da je doplata izvršena — vještak dobiva notifikaciju i može nastaviti.");

        app.MapPost("/api/orders/{orderId:int}/submit-appraisal", SubmitAppraisal)
            .RequireAuthorization(AppPolicies.DocumentsUpload)
            .WithTags("Appraisers")
            .WithName("SubmitAppraisal")
            .WithSummary("Vještak dostavlja gotovu procjenu na kolateral oficira.");

        app.MapPost("/api/orders/{orderId:int}/complete-signed-docs", CompleteSignedDocumentImport)
            .RequireAuthorization(AppPolicies.DocumentsUpload)
            .WithTags("Appraisers")
            .WithName("CompleteSignedDocumentImport")
            .WithSummary("Vještak završava import potpisanih dokumenata — notifikacija CA.");

        app.MapPost("/api/orders/{orderId:int}/reject-order", RejectOrder)
            .RequireAuthorization(AppPolicies.OrdersSendToAppraiser)
            .WithTags("Appraisers")
            .WithName("RejectOrder")
            .WithSummary("CA/CO administrativno odbija narudžbu koja je kod vještaka — auto-reassign.");

        app.MapPost("/api/orders/{orderId:int}/quote-requests", SendQuoteRequests)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("QuoteRequests")
            .WithName("SendQuoteRequests")
            .WithSummary("PL — CA šalje zahtjev za ponudu na odabrane vještake.");

        app.MapGet("/api/orders/{orderId:int}/quote-requests", GetQuoteRequests)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("QuoteRequests")
            .WithName("GetQuoteRequests")
            .WithSummary("PL — lista zahtjeva za ponudu za narudžbu.");

        app.MapPost("/api/orders/{orderId:int}/quote-requests/thank-you", SendThankYou)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("QuoteRequests")
            .WithName("SendThankYou")
            .WithSummary("PL — CA šalje zahvalnicu neodabranim vještacima.");

        app.MapPost("/api/orders/{orderId:int}/quote-requests/{quoteId:int}/accept", AcceptQuote)
            .RequireAuthorization(AppPolicies.OrdersSelectAppraiser)
            .WithTags("QuoteRequests")
            .WithName("AcceptQuote")
            .WithSummary("PL — CO/CA prihvata ponudu odabranog vještaka.");
    }

    private sealed record SubmitAppraisalRequest(DateTime? VisitDate);

    private static async Task<IResult> GetList(
        [AsParameters] AppraiserListQuery query,
        IAppraiserService service,
        CancellationToken ct)
    {
        var result = await service.GetListAsync(
            query.Page, query.PageSize, query.Search, query.City,
            query.OnLeave, query.Blacklisted, query.Active, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetById(
        int id, IAppraiserService service, CancellationToken ct)
    {
        var result = await service.GetByIdAsync(id, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Create(
        [FromBody] CreateAppraiserRequest request,
        IAppraiserService service,
        CancellationToken ct)
    {
        var result = await service.CreateAsync(request, ct);
        return Results.Created($"/api/appraisers/{result.Id}", result);
    }

    private static async Task<IResult> Update(
        int id,
        [FromBody] UpdateAppraiserRequest request,
        IAppraiserService service,
        CancellationToken ct)
    {
        var result = await service.UpdateAsync(id, request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SetOnLeave(
        int id,
        [FromBody] SetAppraiserFlagRequest request,
        IAppraiserService service,
        CancellationToken ct)
    {
        var result = await service.SetOnLeaveAsync(id, request.Value, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SetBlacklisted(
        int id,
        [FromBody] SetAppraiserFlagRequest request,
        IAppraiserService service,
        CancellationToken ct)
    {
        var result = await service.SetBlacklistedAsync(id, request.Value, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Deactivate(
        int id, IAppraiserService service, CancellationToken ct)
    {
        await service.DeactivateAsync(id, ct);
        return Results.NoContent();
    }

    // ── Assignment & Quote operations (IMediator) ─────────────────────────────

    private static async Task<IResult> AutoSelectAppraiser(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new AutoSelectAppraiserCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetCandidates(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new GetCandidatesForOrderQuery(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ManualSelectAppraiser(
        int orderId,
        [FromBody] ManualSelectAppraiserRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new ManualSelectAppraiserCommand(orderId, request.AppraiserId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SendToAppraiser(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new SendToAppraiserCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetAppraiserPackage(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new GetAppraiserPackageQuery(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> AcceptByAppraiser(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new AcceptByAppraiserCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> RejectByAppraiser(
        int orderId,
        [FromBody] RejectByAppraiserRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new RejectByAppraiserCommand(orderId, request.Reason, request.Comment), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> RequestAdditionalPayment(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new RequestAdditionalPaymentCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ConfirmAdditionalPayment(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new ConfirmAdditionalPaymentCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SubmitAppraisal(
        int orderId,
        [FromBody] SubmitAppraisalRequest? request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new SubmitAppraisalCommand(orderId, request?.VisitDate), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> CompleteSignedDocumentImport(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new CompleteSignedDocumentImportCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> RejectOrder(
        int orderId,
        [FromBody] RejectOrderRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new RejectOrderCommand(orderId, request.Reason, request.Comment), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SendQuoteRequests(
        int orderId,
        [FromBody] SendQuoteRequestsApiRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(
            new SendQuoteRequestsCommand(orderId, request.AppraiserIds, request.Deadline), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetQuoteRequests(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new GetQuoteRequestsQuery(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SendThankYou(
        int orderId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new SendThankYouCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> AcceptQuote(
        int orderId, int quoteId, IMediator mediator, CancellationToken ct)
    {
        var result = await mediator.Send(new AcceptQuoteCommand(orderId, quoteId), ct);
        return Results.Ok(result);
    }
}

public sealed record ManualSelectAppraiserRequest(int AppraiserId);
public sealed record RejectOrderRequest(string Reason, string? Comment = null);
public sealed record SendQuoteRequestsApiRequest(List<int> AppraiserIds, DateTime Deadline);
public sealed record SubmitAppraisalRequest(DateTime? VisitDate = null);
public sealed record RejectByAppraiserRequest(AppraiserDeclineReason Reason, string? Comment = null);
