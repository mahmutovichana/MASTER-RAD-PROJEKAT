using System.Text.Json;
using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// In-memory dev implementacija — radi bez baze. Registruje se kao Singleton da
/// promjene opstaju između navigacija u toku jedne sesije procesa.
///
/// Polja su instancna (ne statička) kako bi unit testovi mogli kreirati izoliranu
/// instancu po testu bez međusobnog zagađivanja stanja.
/// </summary>
public sealed class MockSifarnikService : ISifarnikService
{
    // ── Stabilni ID-evi za seed (samo konstante, ne mutabilno stanje) ─────────

    private static readonly Guid _katTipoviRola       = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid _katOsnovPovezanosti = Guid.Parse("22222222-2222-2222-2222-222222222222");
    private static readonly Guid _katVrsteLimita      = Guid.Parse("33333333-3333-3333-3333-333333333333");

    // Unosnik — hard-coded kao "u upotrebi" radi testiranja warning dialoga u UI-ju
    // i unit testova koji pokrivaju acceptance kriterij #2.
    private static readonly Guid _vrijUnosnik = Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa");

    // ── Instancno mutabilno stanje (izolirano po instanci) ────────────────────

    private readonly List<SifarnikKategorijaDto>  _kategorije;
    private readonly List<SifarnikVrijednostDto>  _vrijednosti;
    private readonly List<AuditLogEntryDto>       _audit;
    private readonly Lock                         _lock = new();

    private static readonly JsonSerializerOptions _jsonOpts = new() { WriteIndented = false };

    // ── Konstruktor — inicijalizacija seed podataka ───────────────────────────

    public MockSifarnikService()
    {
        _kategorije =
        [
            new(_katTipoviRola,       "Tipovi rola",       "tipovi_rola",
                "Sub-tip korisnika unutar role (npr. Unosnik, Verifikator).", true, DateTime.UtcNow.AddDays(-30)),
            new(_katOsnovPovezanosti, "Osnov povezanosti", "osnov_povezanosti",
                "Vrste povezanosti — pravna, ekonomska, lična.",              true, DateTime.UtcNow.AddDays(-30)),
            new(_katVrsteLimita,      "Vrste limita",      "vrste_limita",
                "Tipovi limita — kreditni, transakcijski, dnevni.",           true, DateTime.UtcNow.AddDays(-30)),
        ];

        _vrijednosti =
        [
            // Tipovi rola
            new(_vrijUnosnik,
                _katTipoviRola, "Unosnik",     "UNOS", 1, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-30), null, null),
            new(Guid.NewGuid(),
                _katTipoviRola, "Verifikator", "VER",  2, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-30), null, null),
            new(Guid.NewGuid(),
                _katTipoviRola, "Posmatrač",   "POSM", 3, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-30), null, null),

            // Osnov povezanosti
            new(Guid.NewGuid(),
                _katOsnovPovezanosti, "Pravna",    "PRAV", 1, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-25), null, null),
            new(Guid.NewGuid(),
                _katOsnovPovezanosti, "Ekonomska", "EKON", 2, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-25), null, null),
            new(Guid.NewGuid(),
                _katOsnovPovezanosti, "Lična",     "LICN", 3, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-25), null, null),

            // Vrste limita
            new(Guid.NewGuid(),
                _katVrsteLimita, "Kreditni",      "KRED", 1, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-20), null, null),
            new(Guid.NewGuid(),
                _katVrsteLimita, "Transakcijski", "TRAN", 2, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-20), null, null),
            new(Guid.NewGuid(),
                _katVrsteLimita, "Dnevni",        "DNEV", 3, true,
                "mock-admin-001", DateTime.UtcNow.AddDays(-20), null, null),
        ];

        _audit = [];

        // Seed CREATE audit zapisi za sve seed vrijednosti
        foreach (var v in _vrijednosti)
        {
            _audit.Add(new AuditLogEntryDto(
                Guid.NewGuid(),
                AuditEntityTypes.SifarnikVrijednost,
                v.Id,
                AuditActions.Create,
                v.KreiranOd ?? "mock-admin-001",
                "Admin (seed)",
                v.KreiranAt,
                OldValues: null,
                NewValues: JsonSerializer.Serialize(v, _jsonOpts)));
        }
    }

    // ── Kategorije ────────────────────────────────────────────────────────────

    public Task<IReadOnlyList<SifarnikKategorijaDto>> GetKategorijeAsync(CancellationToken ct = default)
    {
        lock (_lock)
        {
            IReadOnlyList<SifarnikKategorijaDto> result = _kategorije
                .Where(k => k.Active)
                .OrderBy(k => k.Naziv)
                .ToList();
            return Task.FromResult(result);
        }
    }

    public Task<SifarnikKategorijaDto?> GetKategorijaBySlugAsync(string slug, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var k = _kategorije.FirstOrDefault(x =>
                string.Equals(x.Slug, slug, StringComparison.OrdinalIgnoreCase));
            return Task.FromResult(k);
        }
    }

    // ── Vrijednosti ───────────────────────────────────────────────────────────

    public Task<IReadOnlyList<SifarnikVrijednostDto>> GetVrijednostiAsync(
        Guid kategorijaId,
        bool onlyActive = false,
        CancellationToken ct = default)
    {
        lock (_lock)
        {
            IReadOnlyList<SifarnikVrijednostDto> result = _vrijednosti
                .Where(v => v.KategorijaId == kategorijaId && (!onlyActive || v.Active))
                .OrderBy(v => v.Redoslijed).ThenBy(v => v.Naziv)
                .ToList();
            return Task.FromResult(result);
        }
    }

    public Task<SifarnikVrijednostDto?> GetVrijednostByIdAsync(Guid id, CancellationToken ct = default)
    {
        lock (_lock)
        {
            return Task.FromResult(_vrijednosti.FirstOrDefault(v => v.Id == id));
        }
    }

    public Task<Guid> CreateVrijednostAsync(
        CreateSifarnikVrijednostRequest request,
        string actorId,
        string actorName,
        CancellationToken ct = default)
    {
        lock (_lock)
        {
            // UNIQUE (kategorija_id, naziv)
            if (_vrijednosti.Any(v =>
                    v.KategorijaId == request.KategorijaId
                    && string.Equals(v.Naziv, request.Naziv, StringComparison.OrdinalIgnoreCase)))
            {
                throw new InvalidOperationException(
                    $"Vrijednost \"{request.Naziv}\" već postoji u ovoj kategoriji.");
            }

            var now = DateTime.UtcNow;
            var dto = new SifarnikVrijednostDto(
                Id:           Guid.NewGuid(),
                KategorijaId: request.KategorijaId,
                Naziv:        request.Naziv,
                Kod:          request.Kod,
                Redoslijed:   request.Redoslijed,
                Active:       request.Active,
                KreiranOd:    actorId,
                KreiranAt:    now,
                IzmjenjenOd:  null,
                IzmjenjenAt:  null);

            _vrijednosti.Add(dto);
            AppendAudit(AuditActions.Create, dto.Id, actorId, actorName, oldValues: null, newValues: dto);

            return Task.FromResult(dto.Id);
        }
    }

    public Task UpdateVrijednostAsync(
        Guid id,
        UpdateSifarnikVrijednostRequest request,
        string actorId,
        string actorName,
        CancellationToken ct = default)
    {
        lock (_lock)
        {
            var idx = _vrijednosti.FindIndex(v => v.Id == id);
            if (idx < 0)
                throw new InvalidOperationException($"Vrijednost s ID {id} ne postoji.");

            var old = _vrijednosti[idx];

            // UNIQUE (kategorija_id, naziv) — dozvoli isti naziv ako je isti entitet
            if (_vrijednosti.Any(v =>
                    v.Id != id
                    && v.KategorijaId == old.KategorijaId
                    && string.Equals(v.Naziv, request.Naziv, StringComparison.OrdinalIgnoreCase)))
            {
                throw new InvalidOperationException(
                    $"Vrijednost \"{request.Naziv}\" već postoji u ovoj kategoriji.");
            }

            var updated = old with
            {
                Naziv       = request.Naziv,
                Kod         = request.Kod,
                Redoslijed  = request.Redoslijed,
                Active      = request.Active,
                IzmjenjenOd = actorId,
                IzmjenjenAt = DateTime.UtcNow,
            };

            _vrijednosti[idx] = updated;
            AppendAudit(AuditActions.Update, id, actorId, actorName, oldValues: old, newValues: updated);

            return Task.CompletedTask;
        }
    }

    public Task DeleteVrijednostAsync(
        Guid id,
        string actorId,
        string actorName,
        CancellationToken ct = default)
    {
        lock (_lock)
        {
            // Simulacija FK constraint — Unosnik je hard-coded kao "u upotrebi"
            if (id == _vrijUnosnik)
            {
                throw new InvalidOperationException(
                    "Ova vrijednost se koristi u aktivnim dodjelama rola. " +
                    "Prvo uklonite dodijeljene role pa pokušajte ponovo.");
            }

            var idx = _vrijednosti.FindIndex(v => v.Id == id);
            if (idx < 0)
                throw new InvalidOperationException($"Vrijednost s ID {id} ne postoji.");

            var old = _vrijednosti[idx];
            _vrijednosti.RemoveAt(idx);
            AppendAudit(AuditActions.Delete, id, actorId, actorName, oldValues: old, newValues: null);

            return Task.CompletedTask;
        }
    }

    // ── Provjera upotrebe ─────────────────────────────────────────────────────

    public Task<int> CountUsagesAsync(Guid vrijednostId, CancellationToken ct = default)
    {
        // Mock: samo Unosnik je u upotrebi (1 dodjela) — za testiranje warning flow-a
        return Task.FromResult(vrijednostId == _vrijUnosnik ? 1 : 0);
    }

    public async Task<bool> IsVrijednostInUseAsync(Guid vrijednostId, CancellationToken ct = default)
        => await CountUsagesAsync(vrijednostId, ct) > 0;

    // ── Audit ─────────────────────────────────────────────────────────────────

    public Task<AuditLogEntryDto?> GetLastAuditEntryAsync(
        string entityType,
        Guid entityId,
        CancellationToken ct = default)
    {
        lock (_lock)
        {
            var entry = _audit
                .Where(a => a.EntityType == entityType && a.EntityId == entityId)
                .OrderByDescending(a => a.ChangedAt)
                .FirstOrDefault();
            return Task.FromResult(entry);
        }
    }

    public Task<IReadOnlyDictionary<Guid, AuditLogEntryDto>> GetLastAuditEntriesAsync(
        string entityType,
        IEnumerable<Guid> entityIds,
        CancellationToken ct = default)
    {
        lock (_lock)
        {
            var idsSet = new HashSet<Guid>(entityIds);
            IReadOnlyDictionary<Guid, AuditLogEntryDto> map = _audit
                .Where(a => a.EntityType == entityType
                            && a.EntityId.HasValue
                            && idsSet.Contains(a.EntityId.Value))
                .GroupBy(a => a.EntityId!.Value)
                .ToDictionary(
                    g => g.Key,
                    g => g.OrderByDescending(a => a.ChangedAt).First());
            return Task.FromResult(map);
        }
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private void AppendAudit(
        string action,
        Guid entityId,
        string actorId,
        string actorName,
        SifarnikVrijednostDto? oldValues,
        SifarnikVrijednostDto? newValues)
    {
        _audit.Add(new AuditLogEntryDto(
            Id:            Guid.NewGuid(),
            EntityType:    AuditEntityTypes.SifarnikVrijednost,
            EntityId:      entityId,
            Action:        action,
            ChangedBy:     actorId,
            ChangedByName: actorName,
            ChangedAt:     DateTime.UtcNow,
            OldValues:     oldValues is null ? null : JsonSerializer.Serialize(oldValues, _jsonOpts),
            NewValues:     newValues is null ? null : JsonSerializer.Serialize(newValues, _jsonOpts)));
    }
}
