using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Application.Users.Models;

/// <summary>
/// Request za paginiranu listu korisnika i njihovih rola.
/// Validacija: Page >= 1, PageSize 1-100, Role mora biti iz AppRoles.All (ako je proslijeđena).
/// </summary>
public sealed class UserRoleListRequest
{
    /// <summary>Pretraga po username, displayName, email. Case-insensitive, trimovan.</summary>
    public string? Search { get; init; }

    /// <summary>Filter po roli. Mora biti poznata rola iz AppRoles.All — nepoznata rola → 400.</summary>
    public string? Role { get; init; }

    /// <summary>true=aktivni, false=neaktivni, null=svi.</summary>
    public bool? IsActive { get; init; }

    public int Page { get; init; } = 1;
    public int PageSize { get; init; } = 20;

    public int ValidatedPage => Page < 1 ? 1 : Page;
    public int ValidatedPageSize => PageSize is < 1 or > 100 ? 20 : PageSize;
    public int Offset => (ValidatedPage - 1) * ValidatedPageSize;
    public string? NormalizedSearch => string.IsNullOrWhiteSpace(Search) ? null : Search.Trim();

    /// <summary>
    /// Vraća true ako je Role filter proslijeđen ali nije poznata rola.
    /// Endpoint treba vratiti 400 ako je ovo true.
    /// </summary>
    public bool HasUnknownRoleFilter =>
        !string.IsNullOrWhiteSpace(Role) && !AppRoles.All.Contains(Role);
}
