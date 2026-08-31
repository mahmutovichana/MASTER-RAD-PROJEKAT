using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za S3-15: Reminder vještaku za dostavu procjene.
///
/// GET  /api/reports/appraiser-reminders         → lista zakašnjelih narudžbi (> N radnih dana)
/// POST /api/reports/appraiser-reminders/{orderId}/send → šalje reminder vještaku
///
/// Ovlaštenje: isključivo CA (OrdersRemindAppraiser permission).
/// Filter: status "u obradi" + OrderSentToAppraiserAt > minDays radnih dana.
/// </summary>
public sealed class AppraiserReminderReportEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/reports/appraiser-reminders")
            .WithTags("Reports")
            .RequireAuthorization(AppPolicies.OrdersRemindAppraiser);

        group.MapGet("/", GetOverdueAppraisals)
            .WithName("GetOverdueAppraisals")
            .WithSummary("Lista narudžbi kod vještaka koje su prekoračile rok (> N radnih dana).");

        group.MapPost("/{orderId:int}/send", SendReminder)
            .WithName("SendAppraisalDeliveryReminder")
            .WithSummary("Šalje email vještaku: 'U kojem je statusu izrada procjene za klijenta XY?'");
    }

    private static async Task<IResult> GetOverdueAppraisals(
        IAppraiserDeliveryReminderService service,
        int?  appraiserId          = null,
        int   minBusinessDaysOverdue = 5,
        int   page                 = 1,
        int   pageSize             = 50,
        CancellationToken ct       = default)
    {
        if (minBusinessDaysOverdue < 1) minBusinessDaysOverdue = 1;
        if (pageSize > 200)             pageSize               = 200;

        var result = await service.GetOverdueAppraisalsAsync(
            appraiserId, minBusinessDaysOverdue, page, pageSize, ct);

        return Results.Ok(result);
    }

    private static async Task<IResult> SendReminder(
        int orderId,
        IAppraiserDeliveryReminderService service,
        CancellationToken ct = default)
    {
        var result = await service.SendAppraisalStatusReminderAsync(orderId, ct);
        return Results.Ok(result);
    }
}
