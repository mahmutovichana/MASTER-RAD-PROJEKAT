using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Branches;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Branches;

public sealed class BranchQueryService : IBranchQueryService
{
    private readonly ApplicationDbContext _db;

    public BranchQueryService(ApplicationDbContext db) => _db = db;

    public async Task<IReadOnlyList<CityDto>> GetCitiesAsync(CancellationToken ct = default)
        => await _db.Cities
            .OrderBy(c => c.Name)
            .Select(c => new CityDto(c.Id, c.Name))
            .ToListAsync(ct);

    public async Task<IReadOnlyList<BranchDto>> GetBranchesAsync(int? cityId = null, CancellationToken ct = default)
    {
        var query = _db.Branches.Include(b => b.City).AsQueryable();
        if (cityId.HasValue)
            query = query.Where(b => b.CityId == cityId.Value);
        return await query
            .OrderBy(b => b.Name)
            .Select(b => new BranchDto(b.Id, b.Code, b.Name, b.Address, b.CityId, b.City.Name))
            .ToListAsync(ct);
    }

    public async Task<BranchDto?> GetBranchByIdAsync(int id, CancellationToken ct = default)
        => await _db.Branches
            .Include(b => b.City)
            .Where(b => b.Id == id)
            .Select(b => new BranchDto(b.Id, b.Code, b.Name, b.Address, b.CityId, b.City.Name))
            .FirstOrDefaultAsync(ct);
}
