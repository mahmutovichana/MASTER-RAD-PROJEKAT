using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za pregled korisnika, njihovih rola i suspenziju.
///
/// Permission pravila:
/// - users.view   → pregled liste korisnika i rola
/// - users.suspend → suspenzija / reaktivacija
/// </summary>
public static class UserRoleEndpoints
{
    public static IEndpointRouteBuilder MapUserRoleEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/users").WithTags("Users");

        group.MapGet("", GetUsers)
             .RequireAuthorization(AppPolicies.UsersView)
             .WithName("GetUsers")
             .WithSummary("Paginirana lista korisnika sa rolama i izračunatim permission-ima.");

        group.MapGet("{userId}/roles", GetUserRoles)
             .RequireAuthorization(AppPolicies.UsersView)
             .WithName("GetUserRoles")
             .WithSummary("Detaljan prikaz rola i permission-a za jednog korisnika.");

        group.MapPost("{userId}/suspend", SuspendUser)
             .RequireAuthorization(AppPolicies.UsersSuspend)
             .WithName("SuspendUser")
             .WithSummary("Suspenduje korisnički nalog. Korisnik se ne može prijaviti dok se ne reaktivira.");

        group.MapPost("{userId}/reactivate", ReactivateUser)
             .RequireAuthorization(AppPolicies.UsersSuspend)
             .WithName("ReactivateUser")
             .WithSummary("Reaktivira suspendovani korisnički nalog.");

        return app;
    }

    private static async Task<IResult> GetUsers(
        IUserRoleQueryService service,
        [AsParameters] UserRoleListRequest request,
        CancellationToken ct)
    {
        // Validacija role filtera uklonjena — dozvoliti filtriranje po custom rolama.
        // Keycloak provider prima naziv role i filtrira direktno; backend ne smije
        // blokirati filtere koji nisu u hardkodiranoj listi sistemskih rola.

        var result = await service.GetUsersWithRolesAsync(request, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetUserRoles(
        string userId, IUserRoleQueryService service, CancellationToken ct)
    {
        var result = await service.GetUserRolesAsync(userId, ct);

        if (result is null)
            throw new NotFoundException("Korisnik nije pronađen.", "USER_NOT_FOUND");

        return Results.Ok(result);
    }

    private static async Task<IResult> SuspendUser(
        string userId,
        [FromBody] SuspendUserRequest? request,
        IUserSuspensionService service,
        CancellationToken ct)
    {
        await service.SuspendAsync(userId, request?.Reason, ct);
        return Results.NoContent();
    }

    private static async Task<IResult> ReactivateUser(
        string userId, IUserSuspensionService service, CancellationToken ct)
    {
        await service.ReactivateAsync(userId, ct);
        return Results.NoContent();
    }
}

public sealed record SuspendUserRequest(string? Reason);
