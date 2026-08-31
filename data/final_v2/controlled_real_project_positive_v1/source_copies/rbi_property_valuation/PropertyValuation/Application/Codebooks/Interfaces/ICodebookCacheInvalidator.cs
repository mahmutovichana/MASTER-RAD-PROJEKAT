namespace RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;

/// <summary>
/// Invalidira cache za šifarnik nakon svake promjene.
/// Implementacija u Infrastructure-u — null implementacija (NullCodebookCacheInvalidator)
/// koristi se dok cache nije implementiran.
///
/// VAŽNO: Ako cache invalidacija ne uspije, dropdown može prikazivati zastarjele vrijednosti.
/// Greška se ne smije tiho ignorisati — mora se logovati.
/// </summary>
public interface ICodebookCacheInvalidator
{
    /// <summary>
    /// Invalidira sve keširane vrijednosti za dati codebookKey.
    /// Poziva se nakon create/update/deactivate/activate/delete operacija.
    /// </summary>
    Task InvalidateAsync(string codebookKey, CancellationToken cancellationToken = default);
}
