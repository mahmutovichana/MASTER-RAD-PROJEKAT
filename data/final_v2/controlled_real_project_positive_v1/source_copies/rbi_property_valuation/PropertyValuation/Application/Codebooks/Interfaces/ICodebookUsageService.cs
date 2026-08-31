using RBBH.CollateralAppraisal.Application.Codebooks.Models;

namespace RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;

/// <summary>
/// Agregator za provjeru upotrebe vrijednosti šifarnika.
/// Prikuplja rezultate od svih registrovanih <see cref="ICodebookUsageChecker"/> implementacija
/// za dati codebookKey i vraća konsolidovani <see cref="CodebookUsageResult"/>.
///
/// Ako nijedan checker nije registrovan za codebookKey, rezultat je IsInUse=false, IsReliable=true.
/// Ako neki checker baci grešku, IsReliable se postavlja na false (fail-safe: delete se blokira).
/// </summary>
public interface ICodebookUsageService
{
    /// <summary>
    /// Provjerava da li se vrijednost s ID-om <paramref name="valueId"/> koristi u poslovnim zapisima.
    /// </summary>
    Task<CodebookUsageResult> CheckUsageAsync(
        string codebookKey,
        int    valueId,
        CancellationToken cancellationToken = default);
}
