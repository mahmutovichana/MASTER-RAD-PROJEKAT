using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Common.Constants;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks.UsageCheckers;

public sealed class DocumentTypeUsageChecker : ICodebookUsageChecker
{
    private readonly ApplicationDbContext _db;
    public DocumentTypeUsageChecker(ApplicationDbContext db) => _db = db;

    public string CodebookKey => CodebookKeys.DocumentTypes;

    public async Task<CodebookUsageLocation?> CheckAsync(int valueId, CancellationToken ct = default)
    {
        var count = await _db.Documents
            .IgnoreQueryFilters()
            .CountAsync(d => d.DocumentTypeId == valueId, ct);

        return count > 0
            ? new CodebookUsageLocation { Module = "Dokumenti", EntityName = "Document", Count = count }
            : null;
    }
}
