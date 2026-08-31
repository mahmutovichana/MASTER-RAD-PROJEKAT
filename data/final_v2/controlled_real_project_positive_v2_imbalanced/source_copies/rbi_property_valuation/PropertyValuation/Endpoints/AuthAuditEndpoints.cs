using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpoint za auditiranje autentifikacijskih događaja (login, logout, login failed).
/// Poziva se iz Web OIDC event handlera gdje direktni IAuditService nije dostupan.
///
/// USER_LOGIN_FAILED je AllowAnonymous jer korisnik još nije autentificiran.
/// Ostali eventi zahtijevaju autentifikaciju.
/// </summary>
public static class AuthAuditEndpoints
{
    public static IEndpointRouteBuilder MapAuthAuditEndpoints(this IEndpointRouteBuilder app)
    {
        // Uspješni autentifikacijski događaji — zahtijevaju autentifikaciju
        app.MapPost("/api/audit/auth-events", RecordAuthEvent)
           .RequireAuthorization()
           .WithTags("Audit")
           .WithName("RecordAuthEvent")
           .WithSummary("Evidentira autentifikacijski događaj (login/logout) u audit log.");

        // Neuspješni login — AllowAnonymous jer korisnik nije autentificiran
        app.MapPost("/api/audit/auth-events/failed", RecordFailedAuthEvent)
           .AllowAnonymous()
           .WithTags("Audit")
           .WithName("RecordFailedAuthEvent")
           .WithSummary("Evidentira neuspješan pokušaj prijave u audit log.");

        return app;
    }

    private static async Task<IResult> RecordAuthEvent(
        AuthEventRequest    request,
        IAuditService       auditService,
        ICurrentUserService currentUser,
        CancellationToken   ct)
    {
        if (!string.Equals(request.UserId, currentUser.UserId, StringComparison.Ordinal) ||
            !string.Equals(request.Username, currentUser.Username, StringComparison.OrdinalIgnoreCase))
        {
            throw new ForbiddenException(
                "UserId/Username u zahtjevu ne odgovaraju autentificiranom korisniku.",
                "AUTH_EVENT_IDENTITY_MISMATCH");
        }

        var action = request.Action switch
        {
            "USER_LOGGED_IN"  => AuditActions.UserLoggedIn,
            "USER_LOGGED_OUT" => AuditActions.UserLoggedOut,
            "TOKEN_REFRESHED" => AuditActions.TokenRefreshed,
            _                 => request.Action ?? string.Empty
        };

        await auditService.RecordAsync(new AuditEvent
        {
            Action            = action,
            OperationType     = action == AuditActions.UserLoggedOut
                                    ? AuditOperationTypes.Logout
                                    : AuditOperationTypes.Login,
            Module            = AuditModules.Security,
            EntityType        = "User",
            EntityKey         = request.UserId,
            EntityDisplayName = request.Username,
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Security,
            Reason            = request.Reason
        }, ct);

        return Results.Ok();
    }

    private static async Task<IResult> RecordFailedAuthEvent(
        AuthEventRequest  request,
        IAuditService     auditService,
        CancellationToken ct)
    {
        await auditService.RecordAsync(new AuditEvent
        {
            Action            = AuditActions.UserLoginFailed,
            OperationType     = AuditOperationTypes.Login,
            Module            = AuditModules.Security,
            EntityType        = "User",
            EntityKey         = request.UserId,
            EntityDisplayName = request.Username,
            Status            = AuditStatuses.Failed,
            Severity          = AuditSeverity.Security,
            Reason            = request.Reason ?? "OIDC authentication failed"
        }, ct);

        return Results.Ok();
    }
}

[System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage]
public sealed record AuthEventRequest(
    string?  Action,
    string?  UserId,
    string?  Username,
    string?  Reason = null);
