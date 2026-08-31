using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Models;

namespace RBBH.CollateralAppraisal.Infrastructure.Codebooks;

/// <summary>
/// Agregator koji pronalazi sve registrovane <see cref="ICodebookUsageChecker"/> implementacije
/// za dati codebookKey, poziva ih i sabira rezultate.
///
/// Fail-safe: ako bilo koji checker baci grešku, IsReliable se postavlja na false.
/// U tom slučaju <see cref="CodebookUsageResult.CanDelete"/> = false — brisanje je blokirano.
///
/// Proširivanje: dodaj novi checker registrujući ga u DI:
///   services.AddScoped&lt;ICodebookUsageChecker, LimitTypeUsageChecker&gt;()
/// Nije potrebno mijenjati ovaj servis.
/// </summary>
public sealed class CodebookUsageService : ICodebookUsageService
{
    private readonly IEnumerable<ICodebookUsageChecker> _checkers;
    private readonly ILogger<CodebookUsageService>      _logger;

    public CodebookUsageService(
        IEnumerable<ICodebookUsageChecker> checkers,
        ILogger<CodebookUsageService>      logger)
    {
        _checkers = checkers;
        _logger   = logger;
    }

    public async Task<CodebookUsageResult> CheckUsageAsync(
        string codebookKey,
        int    valueId,
        CancellationToken cancellationToken = default)
    {
        var relevantCheckers = _checkers
            .Where(c => string.Equals(c.CodebookKey, codebookKey, StringComparison.OrdinalIgnoreCase))
            .ToList();

        // Nema registrovanih checkera — vrijednost sigurno nije referencirana
        if (relevantCheckers.Count == 0)
            return new CodebookUsageResult { IsInUse = false, UsageCount = 0, IsReliable = true };

        var locations  = new List<CodebookUsageLocation>();
        var isReliable = true;

        foreach (var checker in relevantCheckers)
        {
            try
            {
                var location = await checker.CheckAsync(valueId, cancellationToken);
                if (location is not null && location.Count > 0)
                    locations.Add(location);
            }
            catch (Exception ex)
            {
                // Ako checker padne, ne možemo biti sigurni — fail-safe blokira delete
                _logger.LogError(ex,
                    "Usage checker {Checker} pao za codebookKey={Key}, valueId={Id}. " +
                    "Brisanje će biti blokirano (fail-safe).",
                    checker.GetType().Name, codebookKey, valueId);
                isReliable = false;
            }
        }

        return new CodebookUsageResult
        {
            IsInUse    = locations.Count > 0,
            UsageCount = locations.Sum(l => l.Count),
            Locations  = locations,
            IsReliable = isReliable
        };
    }
}
