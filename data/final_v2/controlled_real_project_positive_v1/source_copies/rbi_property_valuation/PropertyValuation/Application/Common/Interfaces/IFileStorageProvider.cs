namespace RBBH.CollateralAppraisal.Application.Common.Interfaces;

/// <summary>
/// Apstrakcija za skladište fajlova (dokumentacija narudžbi procjene, US 92).
/// Implementacija: <c>LocalFileStorageProvider</c> (lokalni disk). Kasnije se može
/// zamijeniti S3/MinIO implementacijom bez promjene pozivatelja.
///
/// <see cref="StoragePath"/> koji vraća <see cref="SaveAsync"/> je relativna putanja
/// (npr. "appraisal-orders/123/3f2e1d4c-....pdf") koja se čuva u
/// <c>Document.StoragePath</c> i prosljeđuje nazad providerima za čitanje/brisanje.
/// Provider je odgovoran za sigurno mapiranje relativne putanje na fizičku lokaciju
/// (zaštita od path traversal-a).
/// </summary>
public interface IFileStorageProvider
{
    /// <summary>
    /// Snima sadržaj struma kao novi fajl unutar zadanog logičkog pod-direktorija
    /// (npr. "appraisal-orders/123"). Generiše jedinstveno ime fajla na disku.
    /// </summary>
    /// <returns>Relativna putanja fajla unutar skladišta i veličina u bajtovima.</returns>
    Task<FileStorageResult> SaveAsync(
        Stream content,
        string originalFileName,
        string subPath,
        CancellationToken ct = default);

    /// <summary>Otvara fajl za čitanje (download). Baca <see cref="FileNotFoundException"/> ako ne postoji.</summary>
    Task<Stream> OpenReadAsync(string storagePath, CancellationToken ct = default);

    /// <summary>Briše fajl sa diska. Idempotentno — ne baca grešku ako fajl ne postoji.</summary>
    Task DeleteAsync(string storagePath, CancellationToken ct = default);

    /// <summary>Provjerava da li fajl postoji u skladištu.</summary>
    Task<bool> ExistsAsync(string storagePath, CancellationToken ct = default);
}

/// <summary>Rezultat snimanja fajla u skladište.</summary>
/// <param name="StoragePath">Relativna putanja fajla unutar skladišta — čuva se u <c>Document.StoragePath</c>.</param>
/// <param name="FileSize">Veličina snimljenog fajla u bajtovima.</param>
public sealed record FileStorageResult(string StoragePath, long FileSize);
