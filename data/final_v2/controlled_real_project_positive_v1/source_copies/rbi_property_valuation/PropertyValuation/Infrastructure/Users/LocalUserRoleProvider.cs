using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.Users;
using RBBH.CollateralAppraisal.Application.Users.Models;

namespace RBBH.CollateralAppraisal.Infrastructure.Users;

/// <summary>Predvidljivi korisnici za lokalni razvoj bez Keycloak Admin API-ja.</summary>
public sealed class LocalUserRoleProvider : IUserRoleProvider
{
    private static readonly IReadOnlyList<UserRoleSourceItem> Users = AppRoles.All
        .Select((role, index) => new UserRoleSourceItem
        {
            UserId = $"local-user-{index + 1}",
            Username = index == 0 ? "local.admin" : $"local.{index + 1}",
            DisplayName = index == 0 ? "Lokalni administrator" : $"Lokalni korisnik — {role}",
            Email = $"local.{index + 1}@localhost",
            IsActive = true,
            Roles = [role]
        })
        .ToArray();

    public Task<PagedResult<UserRoleSourceItem>> GetUsersWithRolesAsync(
        UserRoleListRequest request,
        CancellationToken cancellationToken = default)
    {
        IEnumerable<UserRoleSourceItem> query = Users;
        if (!string.IsNullOrWhiteSpace(request.NormalizedSearch))
            query = query.Where(user =>
                user.Username.Contains(request.NormalizedSearch, StringComparison.OrdinalIgnoreCase) ||
                (user.DisplayName?.Contains(request.NormalizedSearch, StringComparison.OrdinalIgnoreCase) ?? false));
        if (!string.IsNullOrWhiteSpace(request.Role))
            query = query.Where(user => user.Roles.Contains(request.Role, StringComparer.OrdinalIgnoreCase));
        if (request.IsActive.HasValue)
            query = query.Where(user => user.IsActive == request.IsActive.Value);

        var all = query.ToArray();
        return Task.FromResult(new PagedResult<UserRoleSourceItem>
        {
            Items = all.Skip(request.Offset).Take(request.ValidatedPageSize).ToArray(),
            TotalCount = all.Length,
            Page = request.ValidatedPage,
            PageSize = request.ValidatedPageSize
        });
    }

    public Task<UserRoleSourceItem?> GetUserWithRolesAsync(
        string userId,
        CancellationToken cancellationToken = default) =>
        Task.FromResult(Users.FirstOrDefault(user => user.UserId == userId));
}
