using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Servis za upravljanje šifarnicima (kategorije + vrijednosti) i čitanje audit traga.
///
/// Dvije implementacije:
///   <see cref="SifarnikService"/>      — SQL Server backend (production / docker dev).
///   <see cref="MockSifarnikService"/>  — in-memory (kad nema baze).
///
/// Switch se radi u Program.cs preko <c>MockSifarnik:Enabled</c> flag-a u appsettings.
/// Svaka CREATE/UPDATE/DELETE operacija automatski upisuje zapis u audit_log
/// u istoj transakciji — pozivalac samo prosljeđuje <c>actorId</c> i <c>actorName</c>
/// (iz <see cref="Auth.IUserContext"/>).
/// </summary>
public interface ISifarnikService
{
    // ── Kategorije ────────────────────────────────────────────────────────────

    /// <summary>Vraća sve aktivne kategorije šifarnika, sortirano po nazivu.</summary>
    Task<IReadOnlyList<SifarnikKategorijaDto>> GetKategorijeAsync(CancellationToken ct = default);

    /// <summary>
    /// Vraća kategoriju po stabilnom slug-u (npr. "tipovi_rola"). Null ako ne postoji.
    /// Koristiti kad kod treba referencu na fiksnu kategoriju (npr. integracija s TAG-4).
    /// </summary>
    Task<SifarnikKategorijaDto?> GetKategorijaBySlugAsync(string slug, CancellationToken ct = default);

    // ── Vrijednosti ───────────────────────────────────────────────────────────

    /// <summary>
    /// Vraća vrijednosti unutar kategorije, sortirano po <c>redoslijed</c> pa <c>naziv</c>.
    /// <paramref name="onlyActive"/> = true vraća samo aktivne (za dropdownove);
    /// false vraća sve (za admin UI gdje se i neaktivne prikazuju i mogu reaktivirati).
    /// </summary>
    Task<IReadOnlyList<SifarnikVrijednostDto>> GetVrijednostiAsync(
        Guid kategorijaId,
        bool onlyActive = false,
        CancellationToken ct = default);

    /// <summary>Vraća pojedinačnu vrijednost po ID-u, ili null.</summary>
    Task<SifarnikVrijednostDto?> GetVrijednostByIdAsync(Guid id, CancellationToken ct = default);

    /// <summary>
    /// Kreira novu vrijednost u šifarniku i upisuje CREATE audit zapis u istoj transakciji.
    /// Vraća ID nove vrijednosti.
    /// </summary>
    /// <exception cref="InvalidOperationException">Ako naziv duplira postojeću vrijednost u kategoriji (UNIQUE constraint).</exception>
    Task<Guid> CreateVrijednostAsync(
        CreateSifarnikVrijednostRequest request,
        string actorId,
        string actorName,
        CancellationToken ct = default);

    /// <summary>
    /// Mijenja postojeću vrijednost i upisuje UPDATE audit zapis (s old_values + new_values).
    /// </summary>
    /// <exception cref="InvalidOperationException">Ako vrijednost ne postoji ili duplira naziv.</exception>
    Task UpdateVrijednostAsync(
        Guid id,
        UpdateSifarnikVrijednostRequest request,
        string actorId,
        string actorName,
        CancellationToken ct = default);

    /// <summary>
    /// Briše vrijednost (hard delete) uz upis DELETE audit zapisa.
    /// Pozivalac MORA prethodno provjeriti <see cref="IsVrijednostInUseAsync"/> —
    /// ako je u upotrebi, FK constraint na <c>user_role_assignments</c> baci grešku.
    /// </summary>
    Task DeleteVrijednostAsync(
        Guid id,
        string actorId,
        string actorName,
        CancellationToken ct = default);

    // ── Provjera upotrebe ─────────────────────────────────────────────────────

    /// <summary>
    /// Broj aktivnih dodjela rola koje koriste ovu vrijednost kao user_type_id.
    /// Vraća 0 ako vrijednost nije u upotrebi.
    /// </summary>
    Task<int> CountUsagesAsync(Guid vrijednostId, CancellationToken ct = default);

    /// <summary>Shortcut: <c>CountUsagesAsync &gt; 0</c>.</summary>
    Task<bool> IsVrijednostInUseAsync(Guid vrijednostId, CancellationToken ct = default);

    // ── Audit ─────────────────────────────────────────────────────────────────

    /// <summary>
    /// Vraća zadnji audit zapis za zadati entitet (po <c>changed_at DESC</c>).
    /// Null ako nema audit zapisa.
    /// </summary>
    Task<AuditLogEntryDto?> GetLastAuditEntryAsync(
        string entityType,
        Guid entityId,
        CancellationToken ct = default);

    /// <summary>
    /// Batch verzija — jedan query za N entiteta. Vraća mapu id → zadnji zapis.
    /// Entiteti bez audit zapisa nisu u mapi. Koristiti za popunjavanje "Izmijenio" kolone u tabeli.
    /// </summary>
    Task<IReadOnlyDictionary<Guid, AuditLogEntryDto>> GetLastAuditEntriesAsync(
        string entityType,
        IEnumerable<Guid> entityIds,
        CancellationToken ct = default);
}
