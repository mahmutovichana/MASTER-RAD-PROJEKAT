using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Application.Codebooks.Requests;

namespace RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;

/// <summary>
/// Servis za upravljanje vrijednostima šifarnika.
/// Sadrži sva poslovna pravila za kreiranje, uređivanje, deaktivaciju, aktivaciju, brisanje i usage check.
/// Endpointi pozivaju ovaj servis — nikada ne implementiraju poslovna pravila direktno.
/// </summary>
public interface ICodebookValueService
{
    /// <summary>
    /// Kreira novu vrijednost šifarnika.
    /// Baca ValidationException ako su podaci neispravni.
    /// Baca ConflictException ako Code već postoji u datom šifarniku.
    /// </summary>
    Task<CodebookValueDto> CreateAsync(
        string codebookKey, CreateCodebookValueRequest request, CancellationToken ct = default);

    /// <summary>
    /// Uređuje Label, Description i SortOrder postojeće vrijednosti.
    /// Code se ne može mijenjati — stabilan je tehnički identifikator.
    /// Baca ValidationException ako su podaci neispravni.
    /// Baca NotFoundException ako vrijednost ne postoji.
    /// </summary>
    Task<CodebookValueDto> UpdateAsync(
        string codebookKey, int id, UpdateCodebookValueRequest request, CancellationToken ct = default);

    /// <summary>
    /// Vraća aktivne, neobrisane vrijednosti za padajući meni.
    /// Sortirano po SortOrder ASC, Label ASC.
    /// Poziva se za svaki dropdown novi unos — uvijek čita trenutno stanje iz baze.
    /// </summary>
    Task<IReadOnlyList<CodebookOptionDto>> GetActiveAsync(
        string codebookKey, CancellationToken ct = default);

    /// <summary>
    /// Admin endpoint: vraća sve vrijednosti (aktivne i neaktivne), isključuje soft-deleted.
    /// </summary>
    Task<IReadOnlyList<CodebookValueDto>> GetAllAsync(
        string codebookKey, CancellationToken ct = default);

    /// <summary>
    /// Vraća jednu vrijednost po ID-u. Uključuje neaktivne, isključuje soft-deleted.
    /// Baca NotFoundException ako ne postoji ili ne pripada datom codebookKey-u.
    /// </summary>
    Task<CodebookValueDto> GetByIdAsync(
        string codebookKey, int id, CancellationToken ct = default);

    /// <summary>
    /// Provjerava upotrebu vrijednosti. Baca NotFoundException ako vrijednost ne postoji.
    /// Rezultat je informativan — DELETE endpoint uvijek sam ponavlja usage check.
    /// </summary>
    Task<CodebookUsageResult> CheckUsageAsync(
        string codebookKey, int id, CancellationToken ct = default);

    /// <summary>
    /// Deaktivira vrijednost. Deaktivirana vrijednost se ne nudi u novim dropdownima.
    /// Baca ConflictException ako je već neaktivna ili je kritična sistemska vrijednost.
    /// </summary>
    Task<CodebookValueDto> DeactivateAsync(
        string codebookKey, int id, DeactivateCodebookValueRequest request, CancellationToken ct = default);

    /// <summary>
    /// Reaktivira prethodno deaktiviranu vrijednost.
    /// Baca ConflictException ako je već aktivna.
    /// </summary>
    Task<CodebookValueDto> ActivateAsync(
        string codebookKey, int id, CancellationToken ct = default);

    /// <summary>
    /// Soft delete vrijednosti. Dozvoljeno samo ako vrijednost nije u upotrebi i nije sistemska.
    /// DELETE endpoint UVIJEK ponavlja usage check — stanje se moglo promijeniti
    /// nakon što je frontend ranije pozvao /usage endpoint.
    /// </summary>
    Task DeleteAsync(string codebookKey, int id, CancellationToken ct = default);
}
