using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za upravljanje šifarnicima (Codebook container) — CRUD nad šifarnikom kao cjelinom.
///
/// Odvojeni od CodebookEndpoints koji upravlja vrijednostima unutar šifarnika.
/// Svi endpointi zahtijevaju codebooks.manage permission (samo Administrator).
/// </summary>
public static class CodebookAdminEndpoints
{
    public static IEndpointRouteBuilder MapCodebookAdminEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/admin/codebooks")
                       .WithTags("Codebooks Admin");

        group.MapGet("/", GetAll)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("GetAllCodebooks")
             .WithSummary("Pregled svih šifarnika sa brojem vrijednosti, filterima i sortiranjem.");

        group.MapGet("/{code}", GetByCode)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("GetCodebookByCode")
             .WithSummary("Detalji šifarnika po kodu.");

        group.MapPost("/", Create)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("CreateCodebook")
             .WithSummary("Kreira novi šifarnik. Code mora biti jedinstven.");

        group.MapPut("/{code}", Update)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("UpdateCodebook")
             .WithSummary("Ažurira naziv, opis i kategoriju šifarnika.");

        group.MapPost("/{code}/deactivate", Deactivate)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("DeactivateCodebook")
             .WithSummary("Deaktivira šifarnik. Šifarnik ostaje vidljiv, ali se ne nudi za nove unose.");

        group.MapPost("/{code}/activate", Activate)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("ActivateCodebook")
             .WithSummary("Reaktivira prethodno deaktiviran šifarnik.");

        group.MapDelete("/{code}", Delete)
             .RequireAuthorization(AppPolicies.CodebooksManage)
             .WithName("DeleteCodebook")
             .WithSummary("Soft delete šifarnika. Blokira se ako ima aktivne vrijednosti ili je sistemski.");

        return app;
    }

    private static async Task<IResult> GetAll(
        [AsParameters] CodebookQueryRequest request,
        ICodebookService service,
        CancellationToken ct)
    {
        var result = await service.GetAllAsync(request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetByCode(
        string code,
        ICodebookService service,
        CancellationToken ct)
    {
        var result = await service.GetByCodeAsync(code, ct);
        return result is null ? Results.NotFound() : Results.Ok(result);
    }

    private static async Task<IResult> Create(
        [FromBody] CreateCodebookRequest request,
        ICodebookService service,
        CancellationToken ct)
    {
        var result = await service.CreateAsync(request, ct);
        return Results.Created($"/api/admin/codebooks/{result.Code}", result);
    }

    private static async Task<IResult> Update(
        string code,
        [FromBody] UpdateCodebookRequest request,
        ICodebookService service,
        CancellationToken ct)
    {
        var result = await service.UpdateAsync(code, request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Deactivate(
        string code,
        ICodebookService service,
        CancellationToken ct)
    {
        var result = await service.DeactivateAsync(code, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Activate(
        string code,
        ICodebookService service,
        CancellationToken ct)
    {
        var result = await service.ActivateAsync(code, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Delete(
        string code,
        ICodebookService service,
        CancellationToken ct)
    {
        await service.DeleteAsync(code, ct);
        return Results.NoContent();
    }
}
