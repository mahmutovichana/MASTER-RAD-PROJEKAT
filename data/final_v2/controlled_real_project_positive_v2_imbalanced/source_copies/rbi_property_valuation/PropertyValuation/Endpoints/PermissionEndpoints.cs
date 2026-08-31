using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class PermissionEndpoints
{
    public static IEndpointRouteBuilder MapPermissionEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/admin/permissions").WithTags("Permissions");

        group.MapGet("/", GetAll)
             .RequireAuthorization(AppPolicies.RolesView)
             .WithName("GetPermissions")
             .WithSummary("Lista Permission Catalog-a. Admin bira iz ovog kataloga pri dodjeli permissiona roli.");

        group.MapGet("/by-module/{module}", GetByModule)
             .RequireAuthorization(AppPolicies.RolesView)
             .WithName("GetPermissionsByModule");

        return app;
    }

    private static async Task<IResult> GetAll(
        IPermissionCatalogService service, CancellationToken ct)
    {
        var result = await service.GetAllAsync(ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetByModule(
        string module, IPermissionCatalogService service, CancellationToken ct)
    {
        var result = await service.GetByModuleAsync(module, ct);
        return Results.Ok(result);
    }
}
