using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Codebooks.Import;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class CodebookImportExportEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/codebooks/import-export").WithTags("Codebook Import/Export");

        group.MapGet("/types", GetSupportedTypes)
            .RequireAuthorization(AppPolicies.CodebooksExport)
            .WithName("GetSupportedImportExportTypes")
            .WithSummary("Lista podržanih šifarnika za import/export.");

        group.MapPost("/preview", PreviewImport)
            .RequireAuthorization(AppPolicies.CodebooksImport)
            .DisableAntiforgery()
            .WithName("PreviewCodebookImport")
            .WithSummary("Upload fajla i preview importa (validacija bez upisa).");

        group.MapPost("/confirm", ConfirmImport)
            .RequireAuthorization(AppPolicies.CodebooksImport)
            .WithName("ConfirmCodebookImport")
            .WithSummary("Potvrda importa nakon preview-a (transakcijski upis).");

        group.MapGet("/export", Export)
            .RequireAuthorization(AppPolicies.CodebooksExport)
            .WithName("ExportCodebook")
            .WithSummary("Export šifarnika u CSV ili XLSX format.");
    }

    private static IResult GetSupportedTypes(ICodebookImportExportService service) =>
        Results.Ok(service.SupportedCodebookTypes);

    private static async Task<IResult> PreviewImport(
        IFormFile file,
        string codebookType,
        int mode,
        ICodebookImportExportService service,
        CancellationToken ct)
    {
        using var stream = new MemoryStream();
        await file.CopyToAsync(stream, ct);
        stream.Position = 0;

        var request = new ImportPreviewRequest(codebookType, file.FileName, stream, (ImportMode)mode);
        var result = await service.PreviewImportAsync(request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ConfirmImport(
        ImportConfirmRequest request,
        ICodebookImportExportService service,
        CancellationToken ct)
    {
        var result = await service.ConfirmImportAsync(request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Export(
        string codebookType,
        string format,
        bool includeInactive,
        ICodebookImportExportService service,
        CancellationToken ct)
    {
        var fmt = format.Equals("csv", StringComparison.OrdinalIgnoreCase)
            ? ExportFormat.Csv : ExportFormat.Xlsx;

        var request = new ExportRequest(codebookType, fmt, includeInactive);
        var result = await service.ExportAsync(request, ct);
        return Results.File(result.Content, result.ContentType, result.FileName);
    }
}
