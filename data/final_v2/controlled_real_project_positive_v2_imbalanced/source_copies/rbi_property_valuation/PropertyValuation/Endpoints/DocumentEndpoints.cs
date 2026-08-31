using RBBH.CollateralAppraisal.Api.Middleware;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class DocumentEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var ordersGroup = app.MapGroup("/api/orders/{orderId:int}")
            .WithTags("Documents");

        ordersGroup.MapPost("/documents", UploadDocuments)
            .RequireAuthorization(AppPolicies.DocumentsUpload)
            .AddEndpointFilter<RateLimitEndpointFilter>()
            .DisableAntiforgery()
            .WithName("UploadDocuments")
            .WithSummary("Upload jednog ili više PDF dokumenata za narudžbu procjene.");

        ordersGroup.MapGet("/documents", GetDocumentsByOrder)
            .RequireAuthorization(AppPolicies.DocumentsView)
            .WithName("GetDocumentsByOrder")
            .WithSummary("Vraća listu dokumenata za narudžbu procjene.");

        ordersGroup.MapPost("/documents/generate", GenerateOrderDocuments)
            .RequireAuthorization(AppPolicies.DocumentsUpload)
            .WithName("GenerateOrderDocuments")
            .WithSummary("Generiše narudžbenicu i izjavu iz podataka Protokola narudžbi (Word).");

        var documentsGroup = app.MapGroup("/api/documents")
            .WithTags("Documents");

        documentsGroup.MapGet("/{documentId:int}/download", DownloadDocument)
            .RequireAuthorization(AppPolicies.DocumentsDownload)
            .WithName("DownloadDocument")
            .WithSummary("Preuzima originalni PDF dokument.");

        documentsGroup.MapDelete("/{documentId:int}", DeleteDocument)
            .RequireAuthorization(AppPolicies.DocumentsDelete)
            .WithName("DeleteDocument")
            .WithSummary("Soft delete dokumenta.");

        documentsGroup.MapPost("/{documentId:int}/versions", ReplaceDocument)
            .RequireAuthorization(AppPolicies.DocumentsUpload)
            .DisableAntiforgery()
            .WithName("ReplaceDocument")
            .WithSummary("Zamjenjuje dokument novom verzijom (stara verzija se deaktivira).");

        documentsGroup.MapPost("/{documentId:int}/deactivate", DeactivateDocument)
            .RequireAuthorization(AppPolicies.DocumentsDelete)
            .WithName("DeactivateDocument")
            .WithSummary("Deaktivira dokument bez brisanja.");

        documentsGroup.MapPost("/{documentId:int}/reactivate", ReactivateDocument)
            .RequireAuthorization(AppPolicies.DocumentsDelete)
            .WithName("ReactivateDocument")
            .WithSummary("Ponovo aktivira prethodno deaktiviran dokument.");
    }

    private static async Task<IResult> UploadDocuments(
        int orderId,
        IFormFileCollection files,
        int documentTypeId,
        IDocumentService service,
        CancellationToken ct)
    {
        var uploadFiles = files
            .Select(file => new DocumentUploadFile(
                file.OpenReadStream(),
                file.FileName,
                file.ContentType,
                file.Length))
            .ToList();

        var result = await service.UploadAsync(orderId, documentTypeId, uploadFiles, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetDocumentsByOrder(
        int orderId,
        IDocumentService service,
        CancellationToken ct)
    {
        var result = await service.GetByOrderAsync(orderId, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> DownloadDocument(
        int documentId,
        IDocumentService service,
        CancellationToken ct)
    {
        var result = await service.OpenDownloadAsync(documentId, ct);
        return Results.File(
            result.Content,
            result.ContentType,
            result.FileName);
    }

    private static async Task<IResult> DeleteDocument(
        int documentId,
        IDocumentService service,
        CancellationToken ct)
    {
        await service.DeleteAsync(documentId, ct);
        return Results.NoContent();
    }

    private static async Task<IResult> ReplaceDocument(
        int documentId,
        IFormFile file,
        IDocumentService service,
        CancellationToken ct)
    {
        var uploadFile = new DocumentUploadFile(
            file.OpenReadStream(),
            file.FileName,
            file.ContentType,
            file.Length);

        var result = await service.ReplaceAsync(documentId, uploadFile, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> DeactivateDocument(
        int documentId,
        DeactivateDocumentRequest? request,
        IDocumentService service,
        CancellationToken ct)
    {
        var result = await service.DeactivateAsync(documentId, request?.Reason, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> ReactivateDocument(
        int documentId,
        IDocumentService service,
        CancellationToken ct)
    {
        var result = await service.ReactivateAsync(documentId, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GenerateOrderDocuments(
        int orderId,
        GenerateOrderDocumentsRequest? request,
        IOrderDocumentGenerator generator,
        CancellationToken ct)
    {
        var req = new OrderDocumentGenerationRequest(
            Iznos: request?.Iznos,
            ZkOznaka: request?.ZkOznaka);

        var result = await generator.GenerateAsync(orderId, req, ct);
        return Results.Ok(result);
    }
}

public sealed record DeactivateDocumentRequest(string? Reason);
public sealed record GenerateOrderDocumentsRequest(decimal? Iznos = null, string? ZkOznaka = null);