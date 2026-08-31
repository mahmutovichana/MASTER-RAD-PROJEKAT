using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users.Models;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Endpointi za profil i role context trenutno prijavljenog korisnika.
/// </summary>
public static class MeEndpoints
{
    public static IEndpointRouteBuilder MapMeEndpoints(this IEndpointRouteBuilder app)
    {
        app.MapGet("/api/me", GetMe)
           .RequireAuthorization()
           .WithTags("Me")
           .WithName("GetMe")
           .WithSummary("Profil korisnika: roles, permissions, modules, userStatus.");

        // ── Role context ──────────────────────────────────────────────────────
        app.MapPost("/api/me/active-role", SetActiveRole)
           .RequireAuthorization()
           .WithTags("Me")
           .WithName("SetActiveRole")
           .WithSummary("Validira i prihvata izbor aktivne uloge. Vraća dashboardRoute za redirect.");

        return app;
    }

    // ── GET /api/me ───────────────────────────────────────────────────────────

    private static async Task<IResult> GetMe(
        ICurrentUserService currentUser,
        IAuditService       auditService,
        CancellationToken   ct)
    {
        // Vrati samo aplikativne role — filtriraj Keycloak sistemske role
        // (default-roles-*, offline_access, uma_authorization) da ne zagađuju UI.
        var roles       = currentUser.Roles
            .Where(r => AppRoles.All.Contains(r, StringComparer.OrdinalIgnoreCase))
            .ToList();
        var permissions = currentUser.Permissions;

        var (status, defaultRoute, modules) = ResolveNavigationContext(roles);

        if (status == "NoRole" && currentUser.IsAuthenticated)
        {
            try
            {
                await auditService.RecordAsync(new AuditEvent
                {
                    Action            = AuditActions.UnknownRoleDetected,
                    OperationType     = AuditOperationTypes.Login,
                    Module            = AuditModules.Security,
                    EntityType        = "User",
                    EntityKey         = currentUser.UserId,
                    EntityDisplayName = currentUser.Username,
                    Status            = AuditStatuses.Forbidden,
                    Severity          = AuditSeverity.Warning,
                    Reason            = "Korisnik se prijavio bez dodijeljene role."
                }, ct);
            }
            catch { /* Audit greška ne smije blokirati ME endpoint */ }
        }

        return Results.Ok(new MeDto(
            UserId:           currentUser.UserId,
            Username:         currentUser.Username,
            DisplayName:      currentUser.FullName,
            Email:            currentUser.Email,
            Roles:            roles,
            Permissions:      permissions,
            DefaultRoute:     defaultRoute,
            AvailableModules: modules,
            UserStatus:       status
        ));
    }

    // ── POST /api/me/active-role ──────────────────────────────────────────────

    /// <summary>
    /// Validira da korisnik stvarno posjeduje traženu rolu, vraća dashboard rutu.
    ///
    /// Sigurnost:
    /// - Korisnik može izabrati SAMO rolu iz svog Keycloak JWT tokena.
    /// - Nepostojeća ili tuđa rola → 403 + audit INVALID_ACTIVE_ROLE_SELECTION.
    /// - Neaktivna (unknown) rola → 400 + audit.
    /// </summary>
    private static async Task<IResult> SetActiveRole(
        [FromBody] ActiveRoleRequest request,
        ICurrentUserService          currentUser,
        IAuditService                auditService,
        CancellationToken            ct)
    {
        var roleCode = request.RoleCode?.Trim();

        if (string.IsNullOrWhiteSpace(roleCode))
            return Results.BadRequest(new { error = "RoleCode je obavezan." });

        var userRoles = currentUser.Roles;

        // ── Sigurnosna provjera: korisnik mora posjedovati tu rolu ────────────
        if (!userRoles.Contains(roleCode, StringComparer.OrdinalIgnoreCase))
        {
            await RecordAuditSafe(auditService, new AuditEvent
            {
                Action            = AuditActions.InvalidActiveRoleSelection,
                OperationType     = AuditOperationTypes.AccessDenied,
                Module            = AuditModules.Security,
                EntityType        = "User",
                EntityKey         = currentUser.UserId,
                EntityDisplayName = currentUser.Username,
                NewValues         = new { RequestedRole = roleCode, UserRoles = userRoles },
                Status            = AuditStatuses.Forbidden,
                Severity          = AuditSeverity.Security,
                Reason            = $"Korisnik pokušao preuzeti rolu '{roleCode}' koju ne posjeduje."
            }, ct);

            return Results.Forbid();
        }

        // ── Provjera da je rola poznata aplikaciji ────────────────────────────
        var dashboardRoute = DashboardRoutes.GetRoute(roleCode);
        if (dashboardRoute is null)
        {
            await RecordAuditSafe(auditService, new AuditEvent
            {
                Action            = AuditActions.UnknownRoleDetected,
                OperationType     = AuditOperationTypes.AccessDenied,
                Module            = AuditModules.Security,
                EntityType        = "User",
                EntityKey         = currentUser.UserId,
                EntityDisplayName = currentUser.Username,
                NewValues         = new { RequestedRole = roleCode },
                Status            = AuditStatuses.Failed,
                Severity          = AuditSeverity.Warning,
                Reason            = $"Rola '{roleCode}' nije poznata aplikaciji."
            }, ct);

            return Results.BadRequest(new { error = $"Rola '{roleCode}' nema definisanu dashboard rutu." });
        }

        // ── Uspješan izbor — auditiranje ──────────────────────────────────────
        await RecordAuditSafe(auditService, new AuditEvent
        {
            Action            = AuditActions.ActiveRoleSelected,
            OperationType     = AuditOperationTypes.Login,
            Module            = AuditModules.Security,
            EntityType        = "User",
            EntityKey         = currentUser.UserId,
            EntityDisplayName = currentUser.Username,
            NewValues         = new { ActiveRole = roleCode, DashboardRoute = dashboardRoute, AllRoles = userRoles },
            Status            = AuditStatuses.Success,
            Severity          = AuditSeverity.Security
        }, ct);

        return Results.Ok(new ActiveRoleResponse(roleCode, dashboardRoute));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private static (string status, string? defaultRoute, IReadOnlyList<string> modules)
        ResolveNavigationContext(IReadOnlyList<string> roles)
    {
        if (roles.Count == 0)
            return ("NoRole", null, []);

        // Filtriraj samo poznate role
        var knownRoles = roles.Where(DashboardRoutes.IsKnownRole).ToList();
        if (knownRoles.Count == 0)
            return ("UnknownRole", null, []);

        var modules = new List<string> { "notifications" };

        // 2+ validnih rola → UI treba pokazati /select-role
        // API ne odlučuje; defaultRoute ostaje null a status označava "SelectRole"
        if (knownRoles.Count >= 2)
        {
            // Uključujemo module svih rola korisnika
            foreach (var r in knownRoles)
                modules.AddRange(GetModulesForRole(r));

            return ("SelectRole", DashboardRoutes.SelectRole, modules.Distinct().ToList());
        }

        // Tačno jedna validna rola
        var single = knownRoles[0];
        modules.AddRange(GetModulesForRole(single));

        return ("Active", DashboardRoutes.GetRoute(single), modules.Distinct().ToList());
    }

    private static string[] GetModulesForRole(string role) => role switch
    {
        AppRoles.Administrator           => ["access-management", "codebooks", "audit", "health", "orders", "tasks"],
        AppRoles.Verifikator              => ["orders", "tasks"],
        AppRoles.Unosnik                  => ["orders"],
        AppRoles.AM                       => ["orders"],
        AppRoles.SM                       => ["orders"],
        AppRoles.UB                       => ["orders"],
        AppRoles.KolateralAdministrator   => ["orders", "tasks"],
        _                                 => ["orders"]
    };

    private static async Task RecordAuditSafe(IAuditService audit, AuditEvent evt, CancellationToken ct)
    {
        try { await audit.RecordAsync(evt, ct); }
        catch { /* Audit greška ne smije blokirati korisnički zahtjev */ }
    }
}

public sealed record ActiveRoleRequest(string? RoleCode);
public sealed record ActiveRoleResponse(string RoleCode, string DashboardRoute);
