using RBBH.CollateralAppraisal.Application.Codebooks.Models;

namespace RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;

/// <summary>
/// Checker za upotrebu jedne specifične vrijednosti šifarnika u konkretnom modulu/entitetu.
///
/// Za svaki šifarnik koji se koristi u poslovnim entitetima registruje se poseban checker.
/// Primjeri: RoleTypeUsageChecker, LimitTypeUsageChecker, RelationBasisUsageChecker.
///
/// Registry pattern: <see cref="ICodebookUsageService"/> pronalazi sve checkere
/// koji odgovaraju datom codebookKey i sabira njihove rezultate.
/// Time se poštuje Open/Closed Principle — novi šifarnik = novi checker, bez promjene postojećeg koda.
///
/// Kako dodati novi checker:
/// 1. Implementirati ovaj interfejs (npr. LimitTypeUsageChecker).
/// 2. Registrovati u DI: services.AddScoped&lt;ICodebookUsageChecker, LimitTypeUsageChecker&gt;()
/// 3. Nema potrebe mijenjati CodebookUsageService.
/// </summary>
public interface ICodebookUsageChecker
{
    /// <summary>
    /// Ključ šifarnika za koji je ovaj checker odgovoran (npr. "limit_types").
    /// Mora se podudarati s CodebookValue.CodebookKey.
    /// </summary>
    string CodebookKey { get; }

    /// <summary>
    /// Provjeri da li se vrijednost s datim ID-om koristi u ovom modulu/entitetu.
    /// Vraća null ako nema upotrebe, ili <see cref="CodebookUsageLocation"/> s brojem referenci.
    /// Baca izuzetak ako provjera nije bila moguća — caller će postaviti IsReliable=false.
    /// </summary>
    Task<CodebookUsageLocation?> CheckAsync(int valueId, CancellationToken cancellationToken = default);
}
