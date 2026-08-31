using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za upravljanje vrijednostima šifarnika.
///
/// Permission pravila:
/// - codebooks.view  → čitanje aktivnih vrijednosti za dropdown
/// - codebooks.manage → admin pregled, usage check, deaktivacija, aktivacija, brisanje
///
/// Poslovna pravila su u CodebookValueService, ne ovdje.
/// </summary>
public static class CodebookEndpoints
{
    public static IEndpointRouteBuilder MapCodebookEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/codebooks/{codebookKey}")
                       .WithTags("Codebooks");

        // Dropdown za novi unos — samo aktivne vrijednosti, lagani DTO
        group.MapGet("/values/active", GetActiveValues)
             .RequireAuthorization(AppPolicies.CodebooksView)
             .WithName("GetActiveCodebookValues")
             .WithSummary("Vraća aktivne vrijednosti za dropdown meni.");

        // Admin pregled svih vrijednosti (aktivne + neaktivne, bez deleted)
        group.MapGet("/values", GetAllValues)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("GetAllCodebookValues")
             .WithSummary("Admin pregled svih vrijednosti šifarnika.");

        // Jedna vrijednost po ID-u
        group.MapGet("/values/{id:int}", GetValueById)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("GetCodebookValueById");

        // Usage check — informativan endpoint; DELETE uvijek ponavlja vlastitu provjeru
        group.MapGet("/values/{id:int}/usage", GetUsage)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("GetCodebookValueUsage")
             .WithSummary("Provjera da li je vrijednost u upotrebi. Informativan — DELETE uvijek ponavlja.");

        // Kreiranje nove vrijednosti
        group.MapPost("/values", Create)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("CreateCodebookValue")
             .WithSummary("Kreira novu vrijednost šifarnika. Code mora biti jedinstven unutar šifarnika.");

        // Uređivanje Label, Description, SortOrder — Code se ne može mijenjati
        group.MapPut("/values/{id:int}", Update)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("UpdateCodebookValue")
             .WithSummary("Uređuje Label, Description i SortOrder. Code nije moguće promijeniti.");

        // Deaktivacija
        group.MapPost("/values/{id:int}/deactivate", Deactivate)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("DeactivateCodebookValue")
             .WithSummary("Deaktivira vrijednost. Deaktivirana vrijednost se ne nudi za nove unose.");

        // Aktivacija (reaktivacija)
        group.MapPost("/values/{id:int}/activate", Activate)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("ActivateCodebookValue")
             .WithSummary("Reaktivira prethodno deaktiviranu vrijednost.");

        // Brisanje (soft delete) — blokira se ako je vrijednost u upotrebi
        group.MapDelete("/values/{id:int}", Delete)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("DeleteCodebookValue")
             .WithSummary("Soft delete. Blokira se ako je vrijednost u upotrebi ili je sistemska.");

        return app;
    }

    private static async Task<IResult> Create(
        string codebookKey,
        [FromBody] CreateCodebookValueRequest request,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var result = await service.CreateAsync(codebookKey, request, ct);
        return Results.Created($"/api/codebooks/{codebookKey}/values/{result.Id}", result);
    }

    private static async Task<IResult> Update(
        string codebookKey,
        int id,
        [FromBody] UpdateCodebookValueRequest request,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var result = await service.UpdateAsync(codebookKey, id, request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetActiveValues(
        string codebookKey,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var items = await service.GetActiveAsync(codebookKey, ct);
        return Results.Ok(items);
    }

    private static async Task<IResult> GetAllValues(
        string codebookKey,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var items = await service.GetAllAsync(codebookKey, ct);
        return Results.Ok(items);
    }

    private static async Task<IResult> GetValueById(
        string codebookKey,
        int id,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var item = await service.GetByIdAsync(codebookKey, id, ct);
        return Results.Ok(item);
    }

    private static async Task<IResult> GetUsage(
        string codebookKey,
        int id,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var usage = await service.CheckUsageAsync(codebookKey, id, ct);
        return Results.Ok(usage);
    }

    private static async Task<IResult> Deactivate(
        string codebookKey,
        int id,
        [FromBody] DeactivateCodebookValueRequest? request,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var result = await service.DeactivateAsync(codebookKey, id, request ?? new(), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Activate(
        string codebookKey,
        int id,
        ICodebookValueService service,
        CancellationToken ct)
    {
        var result = await service.ActivateAsync(codebookKey, id, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Delete(
        string codebookKey,
        int id,
        ICodebookValueService service,
        CancellationToken ct)
    {
        await service.DeleteAsync(codebookKey, id, ct);
        return Results.NoContent();
    }
}
