using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;
using RBBH.CollateralAppraisal.Application.Common.Models;

namespace RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;

/// <summary>
/// Upravljanje šifarnicima (Codebook) kao cjelinom.
/// Odvojeno od ICodebookValueService koji upravljava vrijednostima unutar šifarnika.
/// </summary>
public interface ICodebookService
{
    Task<PagedResult<CodebookListItemDto>> GetAllAsync(CodebookQueryRequest request, CancellationToken ct = default);
    Task<CodebookDto?> GetByCodeAsync(string code, CancellationToken ct = default);
    Task<CodebookDto> CreateAsync(CreateCodebookRequest request, CancellationToken ct = default);
    Task<CodebookDto> UpdateAsync(string code, UpdateCodebookRequest request, CancellationToken ct = default);
    Task<CodebookDto> DeactivateAsync(string code, CancellationToken ct = default);
    Task<CodebookDto> ActivateAsync(string code, CancellationToken ct = default);
    Task DeleteAsync(string code, CancellationToken ct = default);
}
