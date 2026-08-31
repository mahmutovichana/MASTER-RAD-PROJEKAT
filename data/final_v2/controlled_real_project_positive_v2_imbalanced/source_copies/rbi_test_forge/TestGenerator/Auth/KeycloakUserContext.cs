using System.Security.Claims;
using Microsoft.AspNetCore.Components.Authorization;

namespace RBBH.TestAutomation.Api.Auth;

public sealed class KeycloakUserContext : IUserContext
{
    private readonly AuthenticationStateProvider _authState;

    public KeycloakUserContext(AuthenticationStateProvider authState) =>
        _authState = authState;

    // GetAuthenticationStateAsync() je već resolved Task u Blazor Server circuitu
    // (RevalidatingServerAuthenticationStateProvider ga kešira tokom SSR faze),
    // pa .GetAwaiter().GetResult() ne može uzrokovati deadlock.
    private ClaimsPrincipal User =>
        _authState.GetAuthenticationStateAsync().GetAwaiter().GetResult().User;

    public string UserId =>
        User.FindFirst("sub")?.Value
        ?? User.FindFirst(ClaimTypes.NameIdentifier)?.Value
        ?? string.Empty;

    public string FullName =>
        User.FindFirst(ClaimTypes.Name)?.Value
        ?? User.FindFirst("name")?.Value
        ?? User.FindFirst("preferred_username")?.Value
        ?? string.Empty;

    public string Email =>
        User.FindFirst(ClaimTypes.Email)?.Value
        ?? User.FindFirst("email")?.Value
        ?? string.Empty;

    public string[] Roles =>
        User.FindAll(ClaimTypes.Role)
            .Select(c => c.Value)
            .ToArray();

    public bool IsAuthenticated => User.Identity?.IsAuthenticated ?? false;

    public string Initials => BuildInitials(FullName);

    public bool HasRole(string role) => AppRoles.HasRole(Roles, role);

    public bool HasAnyRole(params string[] roles) => AppRoles.HasAnyRole(Roles, roles);

    public bool CanAccess(string module) => AppModules.CanAccess(module, Roles);

    private static string BuildInitials(string fullName)
    {
        var parts = fullName.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        return parts.Length switch
        {
            0 => "?",
            1 => parts[0][..1].ToUpperInvariant(),
            _ => $"{parts[0][0]}{parts[^1][0]}".ToUpperInvariant()
        };
    }
}
