using RBBH.CollateralAppraisal.Application.Branches;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class BranchEndpoints
{
    public static IEndpointRouteBuilder MapBranchEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/branches").WithTags("Branches");

        group.MapGet("/cities", GetCities)
             .RequireAuthorization()
             .WithName("GetCities")
             .WithSummary("Vraća listu gradova za dropdown.");

        group.MapGet("/", GetBranches)
             .RequireAuthorization()
             .WithName("GetBranches")
             .WithSummary("Vraća poslovnice, opcionalno filtrirane po gradu.");

        group.MapGet("/{id:int}", GetBranchById)
             .RequireAuthorization()
             .WithName("GetBranchById")
             .WithSummary("Vraća poslovnicu po ID-u.");

        return app;
    }

    private static async Task<IResult> GetCities(
        IBranchQueryService service,
        CancellationToken ct)
    {
        var cities = await service.GetCitiesAsync(ct);
        return Results.Ok(cities);
    }

    private static async Task<IResult> GetBranches(
        IBranchQueryService service,
        int? cityId,
        CancellationToken ct)
    {
        var branches = await service.GetBranchesAsync(cityId, ct);
        return Results.Ok(branches);
    }

    private static async Task<IResult> GetBranchById(
        int id,
        IBranchQueryService service,
        CancellationToken ct)
    {
        var branch = await service.GetBranchByIdAsync(id, ct);
        return branch is null ? Results.NotFound() : Results.Ok(branch);
    }
}
