using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Reports;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Izvještaji (kućica "Izvještaji"):
///  • GET /api/reports/concentration — koncentracija vještaka, 5 opcija (US 9)
///  • GET /api/reports/timeline      — pregled svih narudžbi + 7 vremenskih kolona (US 10)
/// Oba vraćaju Excel (xlsx) na klik. Zaštita: reports.generate (CA/CO/CM/Administrator).
/// </summary>
public sealed class ReportEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        app.MapGet("/api/reports/concentration", GenerateConcentration)
            .RequireAuthorization(AppPolicies.ReportsGenerate)
            .WithTags("Reports")
            .WithName("ConcentrationReport")
            .WithSummary("Izvještaj koncentracije vještaka (5 opcija) — Excel.");

        app.MapGet("/api/reports/timeline", GenerateTimeline)
            .RequireAuthorization(AppPolicies.ReportsGenerate)
            .WithTags("Reports")
            .WithName("OrdersTimeReport")
            .WithSummary("Pregled svih narudžbi + 7 vremenskih kolona — Excel.");

    }

    private static async Task<IResult> GenerateConcentration(
        int option,
        DateTime? asOfDate,
        IReportService service,
        CancellationToken ct)
    {
        var file = await service.GenerateConcentrationAsync(option, asOfDate, ct);
        return Results.File(file.Content, file.ContentType, file.FileName);
    }

    private static async Task<IResult> GenerateTimeline(
        DateTime? endDate,
        IReportService service,
        CancellationToken ct)
    {
        var file = await service.GenerateOrdersTimeReportAsync(endDate, ct);
        return Results.File(file.Content, file.ContentType, file.FileName);
    }

}
