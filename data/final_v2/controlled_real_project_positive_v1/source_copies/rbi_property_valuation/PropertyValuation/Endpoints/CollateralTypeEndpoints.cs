using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Constants;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Shortcut endpointi za dropdown menije narudžbe.
/// Koriste isti servis kao /api/codebooks, ali sa fiksnim ključem šifarnika.
/// </summary>
public static class CollateralTypeEndpoints
{
    private const string CollateralKey         = CodebookKeys.CollateralTypes;
    private const string CombinedCollateralKey = CodebookKeys.CombinedCollateralTypes;

    public static IEndpointRouteBuilder MapCollateralTypeEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/codebooks").WithTags("Codebooks");

        group.MapGet("/collateral-types", GetCollateralTypes)
             .RequireAuthorization(AppPolicies.CodebooksView)
             .WithName("GetCollateralTypes")
             .WithSummary("Aktivni tipovi kolaterala za dropdown (svi tipovi iz šifarnika za FL i PL).");

        group.MapGet("/combined-collateral-types", GetCombinedCollateralTypes)
             .RequireAuthorization(AppPolicies.CodebooksView)
             .WithName("GetCombinedCollateralTypes")
             .WithSummary("Aktivni kombinovani tipovi kolaterala za dropdown.");

        return app;
    }

    private static async Task<IResult> GetCollateralTypes(
        ICodebookValueService service, CancellationToken ct)
    {
        var items = await service.GetActiveAsync(CollateralKey, ct);
        return Results.Ok(items);
    }

    private static async Task<IResult> GetCombinedCollateralTypes(
        ICodebookValueService service, CancellationToken ct)
    {
        var items = await service.GetActiveAsync(CombinedCollateralKey, ct);
        return Results.Ok(items);
    }
}
