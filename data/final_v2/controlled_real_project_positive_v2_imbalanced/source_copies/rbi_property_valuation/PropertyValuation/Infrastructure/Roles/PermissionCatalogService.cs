using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Roles.Models;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Roles;

public sealed class PermissionCatalogService : IPermissionCatalogService
{
    private readonly ApplicationDbContext _db;

    public PermissionCatalogService(ApplicationDbContext db) => _db = db;

    public async Task<IReadOnlyList<PermissionDefinitionDto>> GetAllAsync(CancellationToken ct = default)
        => await _db.PermissionDefinitions
            .AsNoTracking()
            .Where(p => p.IsActive)
            .OrderBy(p => p.Module).ThenBy(p => p.DisplayName)
            .Select(p => new PermissionDefinitionDto(p.Id, p.Code, p.DisplayName, p.Description, p.Module, p.IsActive))
            .ToListAsync(ct);

    public async Task<IReadOnlyList<PermissionDefinitionDto>> GetByModuleAsync(
        string module, CancellationToken ct = default)
        => await _db.PermissionDefinitions
            .AsNoTracking()
            .Where(p => p.IsActive && p.Module == module)
            .OrderBy(p => p.DisplayName)
            .Select(p => new PermissionDefinitionDto(p.Id, p.Code, p.DisplayName, p.Description, p.Module, p.IsActive))
            .ToListAsync(ct);
}
