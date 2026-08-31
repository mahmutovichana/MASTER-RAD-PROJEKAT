using MediatR;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.OriginalAppraisal.Commands;
using RBBH.CollateralAppraisal.Application.SalesConsent.Commands;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class OriginalAppraisalEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders/{orderId:int}")
            .WithTags("Original Appraisal");

        group.MapPost("/deliver-original", DeliverOriginalToOffice)
            .RequireAuthorization(AppPolicies.OrdersAccept)
            .WithName("DeliverOriginalToOffice")
            .WithSummary("AC6: Vještak označava da je original dostavljen u poslovnicu.");

        group.MapPost("/confirm-original", ConfirmOriginalReceived)
            .RequireAuthorization(AppPolicies.OrdersConfirmOriginal)
            .WithName("ConfirmOriginalReceived")
            .WithSummary("Prodaja potvrđuje preuzimanje fizičkog originala procjene u poslovnici.");

        group.MapPost("/remind-appraiser", SendAppraiserReminder)
            .RequireAuthorization(AppPolicies.OrdersRemindAppraiser)
            .WithName("SendAppraiserReminder")
            .WithSummary("Šalje podsjetnik vještaku za dostavu originala procjene.");

        group.MapPost("/sign-consent", SignSalesConsent)
            .RequireAuthorization(AppPolicies.OrdersSignConsent)
            .WithName("SignSalesConsent")
            .WithSummary("Prodaja (AM/SM/UB) evidentira potpisanu saglasnost klijenta — samo PL narudžbe.");
    }

    private static async Task<IResult> DeliverOriginalToOffice(
        int orderId,
        IOriginalAppraisalService service,
        CancellationToken ct)
    {
        var result = await service.DeliverOriginalToOfficeAsync(orderId, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ConfirmOriginalReceived(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new ConfirmOriginalReceivedCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SendAppraiserReminder(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new SendAppraiserReminderCommand(orderId), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> SignSalesConsent(
        int orderId,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new SignSalesConsentCommand(orderId), ct);
        return Results.Ok(result);
    }
}