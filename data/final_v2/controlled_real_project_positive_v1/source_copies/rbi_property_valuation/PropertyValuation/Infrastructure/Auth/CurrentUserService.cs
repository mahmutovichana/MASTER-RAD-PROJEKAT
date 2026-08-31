using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Auth;

public class CurrentUserService : ICurrentUserService
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CurrentUserService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    private ClaimsPrincipal? User => _httpContextAccessor.HttpContext?.User;

    public string? UserId =>
        User?.FindFirst(ClaimTypes.NameIdentifier)?.Value
        ?? User?.FindFirst("sub")?.Value;

    public string? Username =>
        User?.FindFirst("preferred_username")?.Value
        ?? User?.FindFirst(ClaimTypes.Name)?.Value;

    public string? Email =>
        User?.FindFirst(ClaimTypes.Email)?.Value
        ?? User?.FindFirst("email")?.Value;

    // Puno ime — "name" claim (Keycloak oidc-full-name-mapper), fallback na
    // given_name+family_name, pa na Username (login username, ne puno ime).
    public string? FullName
    {
        get
        {
            var name = User?.FindFirst("name")?.Value;
            if (!string.IsNullOrWhiteSpace(name))
                return name;

            var given  = User?.FindFirst("given_name")?.Value;
            var family = User?.FindFirst("family_name")?.Value;
            var composed = $"{given} {family}".Trim();
            if (!string.IsNullOrWhiteSpace(composed))
                return composed;

            return Username;
        }
    }

    // Primarna rola — koristi se za audit log
    public string? Role => Roles.FirstOrDefault();

    // Sve role — sabiru se za izračun permission-a
    public IReadOnlyList<string> Roles =>
        User?.GetRoles() ?? Array.Empty<string>();

    // Permission-e dodane od PermissionClaimsTransformation
    public IReadOnlyList<string> Permissions =>
        User?.FindAll("permission").Select(c => c.Value).OrderBy(p => p).ToList()
        ?? (IReadOnlyList<string>)Array.Empty<string>();

    public bool IsAuthenticated =>
        User?.Identity?.IsAuthenticated == true;
}
