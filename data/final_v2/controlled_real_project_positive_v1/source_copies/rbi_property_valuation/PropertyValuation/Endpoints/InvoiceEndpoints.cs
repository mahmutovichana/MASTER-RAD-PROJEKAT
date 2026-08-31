using MediatR;
using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Api.Middleware;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Invoice.Commands;
using RBBH.CollateralAppraisal.Application.Invoice.Queries;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class InvoiceEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        // US-F1: Protokol uploaduje fakturu
        app.MapPost("/api/orders/{orderId:int}/invoice/upload", UploadInvoice)
            .RequireAuthorization(AppPolicies.InvoiceUpload)
            .AddEndpointFilter<RateLimitEndpointFilter>()
            .WithTags("Invoice")
            .WithName("UploadInvoice")
            .WithSummary("Protokol uploaduje fakturu vještaka za narudžbu.");

        // US-F2: CA šalje fakturu na plaćanje
        app.MapPost("/api/orders/{orderId:int}/invoice/send-for-payment", SendForPayment)
            .RequireAuthorization(AppPolicies.InvoiceSendForPayment)
            .AddEndpointFilter<RateLimitEndpointFilter>()
            .WithTags("Invoice")
            .WithName("SendInvoiceForPayment")
            .WithSummary("CA šalje fakturu na plaćanje — status → 'u obradi'.");

        // US-F3: Likvidatura potvrđuje plaćanje
        app.MapPost("/api/orders/{orderId:int}/invoice/confirm-paid", ConfirmPaid)
            .RequireAuthorization(AppPolicies.InvoiceConfirmPayment)
            .AddEndpointFilter<RateLimitEndpointFilter>()
            .WithTags("Invoice")
            .WithName("ConfirmInvoicePaid")
            .WithSummary("Likvidatura/Računovodstvo potvrđuje plaćanje fakture — status → 'plaćeno'.");

        // Status fakture (read-only)
        app.MapGet("/api/orders/{orderId:int}/invoice/status", GetStatus)
            .RequireAuthorization(AppPolicies.InvoiceView)
            .WithTags("Invoice")
            .WithName("GetInvoiceStatus")
            .WithSummary("Trenutni status fakture za narudžbu (ko je uploadovao, poslao, platio).");
    }

    private static async Task<IResult> UploadInvoice(
        int orderId,
        [FromBody] UploadInvoiceRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new UploadInvoiceCommand(orderId, request.DocumentId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SendForPayment(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new SendInvoiceForPaymentCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ConfirmPaid(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new ConfirmInvoicePaidCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetStatus(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetInvoiceStatusQuery(orderId), ct);
        return Results.Ok(result);
    }
}

public sealed record UploadInvoiceRequest(int DocumentId);
