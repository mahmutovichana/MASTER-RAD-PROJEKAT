using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Upravljanje definicijama rola (CRUD) + dodjela/uklanjanje permissiona.
/// Sve akcije zahtijevaju roles.manage permission (samo Administrator).
/// </summary>
public static class RoleDefinitionEndpoints
{
    public static IEndpointRouteBuilder MapRoleDefinitionEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/admin/roles").WithTags("Role Definitions");

        group.MapGet("/", GetAll)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("GetRoleDefinitions")
             .WithSummary("Lista svih definicija rola (sistemske + custom).");

        group.MapGet("/{id:int}", GetById)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("GetRoleDefinition");

        group.MapPost("/", Create)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("CreateRoleDefinition")
             .WithSummary("Kreira novu custom rolu i sinhronizuje s Keycloak-om.");

        group.MapPut("/{id:int}", Update)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("UpdateRoleDefinition");

        group.MapPost("/{id:int}/deactivate", Deactivate)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("DeactivateRoleDefinition");

        group.MapPost("/{id:int}/activate", Activate)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("ActivateRoleDefinition");

        group.MapDelete("/{id:int}", Delete)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("DeleteRoleDefinition")
             .WithSummary("Soft delete custom role. Blokira se ako je rola u upotrebi.");

        group.MapPost("/{id:int}/permissions", AddPermission)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("AddPermissionToRole");

        group.MapDelete("/{id:int}/permissions/{permissionId:int}", RemovePermission)
             .RequireAuthorization(AppPolicies.RolesManage)
             .WithName("RemovePermissionFromRole");

        return app;
    }

    private static async Task<IResult> GetAll(
        [AsParameters] RoleQueryRequest request,
        IRoleDefinitionService service,
        CancellationToken ct)
    {
        var result = await service.GetAllAsync(request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetById(
        int id, IRoleDefinitionService service, CancellationToken ct)
    {
        var result = await service.GetByIdAsync(id, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Create(
        [FromBody] CreateRoleRequest request,
        IRoleDefinitionService service,
        CancellationToken ct)
    {
        var result = await service.CreateAsync(request, ct);
        return Results.Created($"/api/admin/roles/{result.Id}", result);
    }

    private static async Task<IResult> Update(
        int id,
        [FromBody] UpdateRoleRequest request,
        IRoleDefinitionService service,
        CancellationToken ct)
    {
        var result = await service.UpdateAsync(id, request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Deactivate(
        int id, IRoleDefinitionService service, CancellationToken ct)
    {
        var result = await service.DeactivateAsync(id, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Activate(
        int id, IRoleDefinitionService service, CancellationToken ct)
    {
        var result = await service.ActivateAsync(id, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Delete(
        int id, IRoleDefinitionService service, CancellationToken ct)
    {
        await service.DeleteAsync(id, ct);
        return Results.NoContent();
    }

    private static async Task<IResult> AddPermission(
        int id,
        [FromBody] AddPermissionToRoleRequest request,
        IRoleDefinitionService service,
        CancellationToken ct)
    {
        var result = await service.AddPermissionAsync(id, request.PermissionDefinitionId, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> RemovePermission(
        int id, int permissionId,
        IRoleDefinitionService service,
        CancellationToken ct)
    {
        var result = await service.RemovePermissionAsync(id, permissionId, ct);
        return Results.Ok(result);
    }
}
