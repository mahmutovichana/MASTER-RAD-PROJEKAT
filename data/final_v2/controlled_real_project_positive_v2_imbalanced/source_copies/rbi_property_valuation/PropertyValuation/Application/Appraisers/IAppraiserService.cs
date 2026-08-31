using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Appraisers;

/// <summary>Master-data CRUD za vještake (Faza C) — koristi CA admin stranica.</summary>
public interface IAppraiserService
{
    Task<PagedResult<AppraiserDto>> GetListAsync(
        int page, int pageSize, string? search = null, string? city = null,
        bool? onLeave = null, bool? blacklisted = null, bool? active = null,
        CancellationToken ct = default);

    Task<AppraiserDto> GetByIdAsync(int id, CancellationToken ct = default);

    Task<AppraiserDto> CreateAsync(CreateAppraiserRequest request, CancellationToken ct = default);

    Task<AppraiserDto> UpdateAsync(int id, UpdateAppraiserRequest request, CancellationToken ct = default);

    Task<AppraiserDto> SetOnLeaveAsync(int id, bool value, CancellationToken ct = default);

    Task<AppraiserDto> SetBlacklistedAsync(int id, bool value, CancellationToken ct = default);

    Task DeactivateAsync(int id, CancellationToken ct = default);
}
