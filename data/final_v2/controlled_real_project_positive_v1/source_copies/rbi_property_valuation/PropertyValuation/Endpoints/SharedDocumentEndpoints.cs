using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class SharedDocumentEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/shared-documents").WithTags("SharedDocuments");

        group.MapGet("/", GetAll)
            .RequireAuthorization(AppPolicies.SharedDocumentsView)
            .WithName("GetSharedDocuments")
            .WithSummary("Lista dijeljenih dokumenata (cjenovnik, lista dokumentacije...).");

        group.MapGet("/categories", GetCategories)
            .RequireAuthorization(AppPolicies.SharedDocumentsView)
            .WithName("GetSharedDocumentCategories")
            .WithSummary("Dostupne kategorije dijeljenih dokumenata.");

        group.MapPost("/", Upload)
            .RequireAuthorization(AppPolicies.SharedDocumentsManage)
            .DisableAntiforgery()
            .WithName("UploadSharedDocument")
            .WithSummary("Upload dijeljenog dokumenta (samo CA).");

        group.MapGet("/{id:int}/download", Download)
            .RequireAuthorization(AppPolicies.SharedDocumentsView)
            .WithName("DownloadSharedDocument")
            .WithSummary("Download dijeljenog dokumenta.");

        group.MapDelete("/{id:int}", Delete)
            .RequireAuthorization(AppPolicies.SharedDocumentsManage)
            .WithName("DeleteSharedDocument")
            .WithSummary("Brisanje dijeljenog dokumenta (samo CA).");
    }

    private static async Task<IResult> GetAll(
        ISharedDocumentService service, CancellationToken ct)
    {
        var result = await service.GetAllAsync(ct);
        return Results.Ok(result);
    }

    private static IResult GetCategories() =>
        Results.Ok(SharedDocumentCategories.All);

    private static async Task<IResult> Upload(
        IFormFile file,
        [FromForm] string title,
        [FromForm] string category,
        ISharedDocumentService service,
        CancellationToken ct)
    {
        var uploadFile = new DocumentUploadFile(
            file.OpenReadStream(),
            file.FileName,
            file.ContentType,
            file.Length);

        var result = await service.UploadAsync(title, category, uploadFile, ct);
        return Results.Created($"/api/shared-documents/{result.Id}/download", result);
    }

    private static async Task<IResult> Download(
        int id, ISharedDocumentService service, CancellationToken ct)
    {
        var result = await service.DownloadAsync(id, ct);
        return Results.File(result.Content, result.ContentType, result.FileName);
    }

    private static async Task<IResult> Delete(
        int id, ISharedDocumentService service, CancellationToken ct)
    {
        await service.DeleteAsync(id, ct);
        return Results.NoContent();
    }
}
