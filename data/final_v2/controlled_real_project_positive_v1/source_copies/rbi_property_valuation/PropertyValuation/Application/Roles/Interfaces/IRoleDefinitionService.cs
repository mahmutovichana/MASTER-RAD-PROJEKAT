using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Roles.Models;
using RBBH.CollateralAppraisal.Application.Roles.Requests;

namespace RBBH.CollateralAppraisal.Application.Roles.Interfaces;

public interface IRoleDefinitionService
{
    Task<PagedResult<RoleDefinitionListItemDto>> GetAllAsync(RoleQueryRequest request, CancellationToken ct = default);
    Task<RoleDefinitionDto>  GetByIdAsync(int id, CancellationToken ct = default);
    Task<RoleDefinitionDto>  CreateAsync(CreateRoleRequest request, CancellationToken ct = default);
    Task<RoleDefinitionDto>  UpdateAsync(int id, UpdateRoleRequest request, CancellationToken ct = default);
    Task<RoleDefinitionDto>  DeactivateAsync(int id, CancellationToken ct = default);
    Task<RoleDefinitionDto>  ActivateAsync(int id, CancellationToken ct = default);
    Task                     DeleteAsync(int id, CancellationToken ct = default);
    Task<RoleDefinitionDto>  AddPermissionAsync(int roleId, int permissionId, CancellationToken ct = default);
    Task<RoleDefinitionDto>  RemovePermissionAsync(int roleId, int permissionId, CancellationToken ct = default);

    /// <summary>Vraća permissione custom role prema imenu — za PermissionClaimsTransformation.</summary>
    Task<IReadOnlyList<string>> GetPermissionCodesForRoleAsync(string roleName, CancellationToken ct = default);
}
