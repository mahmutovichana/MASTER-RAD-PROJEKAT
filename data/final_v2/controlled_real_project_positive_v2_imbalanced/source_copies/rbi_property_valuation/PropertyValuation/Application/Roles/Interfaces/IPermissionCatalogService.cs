using RBBH.CollateralAppraisal.Application.Roles.Models;

namespace RBBH.CollateralAppraisal.Application.Roles.Interfaces;

public interface IPermissionCatalogService
{
    Task<IReadOnlyList<PermissionDefinitionDto>> GetAllAsync(CancellationToken ct = default);
    Task<IReadOnlyList<PermissionDefinitionDto>> GetByModuleAsync(string module, CancellationToken ct = default);
}
