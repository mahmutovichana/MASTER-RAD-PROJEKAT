namespace RBBH.CollateralAppraisal.Application.Branches;

public interface IBranchQueryService
{
    Task<IReadOnlyList<CityDto>>   GetCitiesAsync(CancellationToken ct = default);
    Task<IReadOnlyList<BranchDto>> GetBranchesAsync(int? cityId = null, CancellationToken ct = default);
    Task<BranchDto?>               GetBranchByIdAsync(int id, CancellationToken ct = default);
}
