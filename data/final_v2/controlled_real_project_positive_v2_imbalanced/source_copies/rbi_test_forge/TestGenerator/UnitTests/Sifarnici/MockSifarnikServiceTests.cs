using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;

namespace UnitTests.Sifarnici;

/// <summary>
/// Unit testovi za <see cref="MockSifarnikService"/>.
///
/// Pokriva sva tri acceptance kriterija TAG-6 user storyja:
///   #1 — Izmjene šifarnika odmah se reflektuju u padajućim menijima (GetVrijednostiAsync)
///   #2 — Brisanje vrijednosti koja je u upotrebi prikazuje upozorenje (CountUsagesAsync, Delete)
///   #3 — Sve promjene bilježe korisnika i datum izmjene (audit metode)
///
/// Svaki test kreira svoju instancu servisa → potpuna izolacija stanja.
/// </summary>
public class MockSifarnikServiceTests
{
    // ── Konstante ─────────────────────────────────────────────────────────────

    private const string ActorId   = "test-actor-001";
    private const string ActorName = "Test Korisnik";

    // ── Helpers ───────────────────────────────────────────────────────────────

    /// <summary>Kreira svježu izoliranu instancu servisa s punim seed podacima.</summary>
    private static MockSifarnikService CreateSvc() => new();

    private static async Task<Guid> GetKatIdAsync(MockSifarnikService svc, string slug)
    {
        var kat = await svc.GetKategorijaBySlugAsync(slug);
        return kat!.Id;
    }

    private static async Task<SifarnikVrijednostDto> GetByNazivAsync(
        MockSifarnikService svc, Guid katId, string naziv)
    {
        var rows = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        return rows.First(v => string.Equals(v.Naziv, naziv, StringComparison.OrdinalIgnoreCase));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetKategorijeAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetKategorijeAsync_WhenCalled_ReturnsThreeCategories()
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijeAsync();
        Assert.Equal(3, result.Count);
    }

    [Fact]
    public async Task GetKategorijeAsync_WhenCalled_ReturnsOnlyActiveCategories()
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijeAsync();
        Assert.All(result, k => Assert.True(k.Active));
    }

    [Fact]
    public async Task GetKategorijeAsync_WhenCalled_ReturnsSortedByNaziv()
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijeAsync();
        var names = result.Select(k => k.Naziv).ToList();
        Assert.Equal(names.OrderBy(n => n).ToList(), names);
    }

    [Theory]
    [InlineData("tipovi_rola")]
    [InlineData("osnov_povezanosti")]
    [InlineData("vrste_limita")]
    public async Task GetKategorijeAsync_ContainsExpectedSlugs(string slug)
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijeAsync();
        Assert.Contains(result, k => k.Slug == slug);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetKategorijaBySlugAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetKategorijaBySlugAsync_WhenSlugExists_ReturnsCategory()
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijaBySlugAsync("tipovi_rola");
        Assert.NotNull(result);
        Assert.Equal("tipovi_rola", result.Slug);
    }

    [Fact]
    public async Task GetKategorijaBySlugAsync_WhenSlugDoesNotExist_ReturnsNull()
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijaBySlugAsync("nepostojeci_slug");
        Assert.Null(result);
    }

    [Theory]
    [InlineData("TIPOVI_ROLA")]
    [InlineData("Tipovi_Rola")]
    [InlineData("tipovi_rola")]
    public async Task GetKategorijaBySlugAsync_IsCaseInsensitive(string slug)
    {
        var svc = CreateSvc();
        var result = await svc.GetKategorijaBySlugAsync(slug);
        Assert.NotNull(result);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetVrijednostiAsync  [Acceptance kriterij #1]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetVrijednostiAsync_WhenOnlyActiveFalse_ReturnsAllSeedValues()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var result = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        Assert.Equal(3, result.Count);
    }

    [Fact]
    public async Task GetVrijednostiAsync_WhenOnlyActiveTrue_ReturnsOnlyActiveValues()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");

        // Deaktiviraj Posmatrač
        var posm = await GetByNazivAsync(svc, katId, "Posmatrač");
        await svc.UpdateVrijednostAsync(posm.Id,
            new UpdateSifarnikVrijednostRequest(posm.Naziv, posm.Kod, posm.Redoslijed, Active: false),
            ActorId, ActorName);

        var result = await svc.GetVrijednostiAsync(katId, onlyActive: true);
        Assert.Equal(2, result.Count);
        Assert.DoesNotContain(result, v => v.Naziv == "Posmatrač");
    }

    [Fact]
    public async Task GetVrijednostiAsync_WhenOnlyActiveTrue_AfterCreate_ReflectsNewValue()
    {
        // Acceptance kriterij #1 — izmjene se odmah reflektuju
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");

        await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Supervizor", "SUP", 4, Active: true),
            ActorId, ActorName);

        var result = await svc.GetVrijednostiAsync(katId, onlyActive: true);
        Assert.Contains(result, v => v.Naziv == "Supervizor");
    }

    [Fact]
    public async Task GetVrijednostiAsync_WhenValueDeactivated_DisappearsFromActiveList()
    {
        // Acceptance kriterij #1 — deaktivacija se odmah reflektuje
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest(ver.Naziv, ver.Kod, ver.Redoslijed, Active: false),
            ActorId, ActorName);

        var active = await svc.GetVrijednostiAsync(katId, onlyActive: true);
        Assert.DoesNotContain(active, v => v.Id == ver.Id);
    }

    [Fact]
    public async Task GetVrijednostiAsync_ReturnsSortedByRedoslijedThenNaziv()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var result = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        var sorted = result
            .OrderBy(v => v.Redoslijed)
            .ThenBy(v => v.Naziv)
            .Select(v => v.Id)
            .ToList();
        Assert.Equal(sorted, result.Select(v => v.Id).ToList());
    }

    [Fact]
    public async Task GetVrijednostiAsync_WhenUnknownCategoryId_ReturnsEmpty()
    {
        var svc = CreateSvc();
        var result = await svc.GetVrijednostiAsync(Guid.NewGuid(), onlyActive: false);
        Assert.Empty(result);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CreateVrijednostAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CreateVrijednostAsync_WhenValid_ReturnsNonEmptyGuid()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "vrste_limita");
        var id = await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Godišnji", "GOD", 4, true),
            ActorId, ActorName);
        Assert.NotEqual(Guid.Empty, id);
    }

    [Fact]
    public async Task CreateVrijednostAsync_WhenValid_NewValueAppearsInGetVrijednostiAsync()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "vrste_limita");
        var id = await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Godišnji", "GOD", 4, true),
            ActorId, ActorName);

        var result = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        Assert.Contains(result, v => v.Id == id && v.Naziv == "Godišnji");
    }

    [Fact]
    public async Task CreateVrijednostAsync_WhenValid_SetsKreiranOdAndKreiranAt()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "vrste_limita");
        var before = DateTime.UtcNow;

        var id = await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Godišnji", "GOD", 4, true),
            ActorId, ActorName);

        var v = await svc.GetVrijednostByIdAsync(id);
        Assert.NotNull(v);
        Assert.Equal(ActorId, v.KreiranOd);
        Assert.True(v.KreiranAt >= before);
        Assert.Null(v.IzmjenjenOd);
        Assert.Null(v.IzmjenjenAt);
    }

    [Fact]
    public async Task CreateVrijednostAsync_WhenDuplicateNazivInSameCategory_ThrowsInvalidOperationException()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");

        // "Unosnik" već postoji u seed podacima
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CreateVrijednostAsync(
                new CreateSifarnikVrijednostRequest(katId, "Unosnik", "UNOS2", 10, true),
                ActorId, ActorName));
    }

    [Fact]
    public async Task CreateVrijednostAsync_WhenSameNazivInDifferentCategory_Succeeds()
    {
        // Isti naziv u različitoj kategoriji je dozvoljen
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "vrste_limita");

        // "Unosnik" postoji u tipovi_rola, ali ne u vrste_limita
        var id = await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Unosnik", "UNOS", 5, true),
            ActorId, ActorName);

        Assert.NotEqual(Guid.Empty, id);
    }

    [Fact]
    public async Task CreateVrijednostAsync_WhenDuplicateNazivCaseInsensitive_ThrowsInvalidOperationException()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");

        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.CreateVrijednostAsync(
                new CreateSifarnikVrijednostRequest(katId, "UNOSNIK", "X", 10, true),
                ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // UpdateVrijednostAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task UpdateVrijednostAsync_WhenValid_ChangesValueInList()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator Senior", "VER_SR", 2, true),
            ActorId, ActorName);

        var updated = await svc.GetVrijednostByIdAsync(ver.Id);
        Assert.NotNull(updated);
        Assert.Equal("Verifikator Senior", updated.Naziv);
        Assert.Equal("VER_SR", updated.Kod);
    }

    [Fact]
    public async Task UpdateVrijednostAsync_WhenValid_SetsIzmjenjenOdAndIzmjenjenAt()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");
        var before = DateTime.UtcNow;

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator Senior", "VER_SR", 2, true),
            ActorId, ActorName);

        var updated = await svc.GetVrijednostByIdAsync(ver.Id);
        Assert.NotNull(updated);
        Assert.Equal(ActorId, updated.IzmjenjenOd);
        Assert.NotNull(updated.IzmjenjenAt);
        Assert.True(updated.IzmjenjenAt >= before);
    }

    [Fact]
    public async Task UpdateVrijednostAsync_WhenValueDoesNotExist_ThrowsInvalidOperationException()
    {
        var svc = CreateSvc();
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.UpdateVrijednostAsync(
                Guid.NewGuid(),
                new UpdateSifarnikVrijednostRequest("Novi naziv", null, 0, true),
                ActorId, ActorName));
    }

    [Fact]
    public async Task UpdateVrijednostAsync_WhenDuplicateNazivOnOtherValue_ThrowsInvalidOperationException()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        // Pokušaj preimenovati Verifikator u "Unosnik" koji već postoji
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.UpdateVrijednostAsync(ver.Id,
                new UpdateSifarnikVrijednostRequest("Unosnik", "UNOS", 2, true),
                ActorId, ActorName));
    }

    [Fact]
    public async Task UpdateVrijednostAsync_WhenSameNazivOnSameValue_Succeeds()
    {
        // Edit s nepromijenjenim nazivom ne smije baciti iznimku
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        var ex = await Record.ExceptionAsync(() =>
            svc.UpdateVrijednostAsync(ver.Id,
                new UpdateSifarnikVrijednostRequest("Verifikator", "VER2", 99, true),
                ActorId, ActorName));

        Assert.Null(ex);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // DeleteVrijednostAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task DeleteVrijednostAsync_WhenValueNotInUse_RemovesFromList()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var posm = await GetByNazivAsync(svc, katId, "Posmatrač");

        await svc.DeleteVrijednostAsync(posm.Id, ActorId, ActorName);

        var result = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        Assert.DoesNotContain(result, v => v.Id == posm.Id);
    }

    [Fact]
    public async Task DeleteVrijednostAsync_WhenValueDoesNotExist_ThrowsInvalidOperationException()
    {
        var svc = CreateSvc();
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.DeleteVrijednostAsync(Guid.NewGuid(), ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // CountUsagesAsync + IsVrijednostInUseAsync  [Acceptance kriterij #2]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CountUsagesAsync_WhenUnosnikId_ReturnsOne()
    {
        // Acceptance kriterij #2 — vrijednost koja je u upotrebi
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var unosnik = await GetByNazivAsync(svc, katId, "Unosnik");

        var count = await svc.CountUsagesAsync(unosnik.Id);
        Assert.Equal(1, count);
    }

    [Fact]
    public async Task CountUsagesAsync_WhenValueNotInUse_ReturnsZero()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        var count = await svc.CountUsagesAsync(ver.Id);
        Assert.Equal(0, count);
    }

    [Fact]
    public async Task IsVrijednostInUseAsync_WhenUnosnik_ReturnsTrue()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var unosnik = await GetByNazivAsync(svc, katId, "Unosnik");

        Assert.True(await svc.IsVrijednostInUseAsync(unosnik.Id));
    }

    [Fact]
    public async Task IsVrijednostInUseAsync_WhenValueNotInUse_ReturnsFalse()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var posm = await GetByNazivAsync(svc, katId, "Posmatrač");

        Assert.False(await svc.IsVrijednostInUseAsync(posm.Id));
    }

    [Fact]
    public async Task DeleteVrijednostAsync_WhenValueIsInUse_ThrowsInvalidOperationException()
    {
        // Acceptance kriterij #2 — brisanje u upotrebi mora biti blokirano
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var unosnik = await GetByNazivAsync(svc, katId, "Unosnik");

        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            svc.DeleteVrijednostAsync(unosnik.Id, ActorId, ActorName));
    }

    [Fact]
    public async Task DeleteVrijednostAsync_WhenValueIsInUse_ValueRemainsInList()
    {
        // Acceptance kriterij #2 — brisanje nije izvršeno
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var unosnik = await GetByNazivAsync(svc, katId, "Unosnik");

        try { await svc.DeleteVrijednostAsync(unosnik.Id, ActorId, ActorName); }
        catch (InvalidOperationException) { /* očekivano */ }

        var result = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        Assert.Contains(result, v => v.Id == unosnik.Id);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetLastAuditEntryAsync  [Acceptance kriterij #3]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetLastAuditEntryAsync_WhenNoAuditForId_ReturnsNull()
    {
        var svc = CreateSvc();
        var result = await svc.GetLastAuditEntryAsync(
            AuditEntityTypes.SifarnikVrijednost, Guid.NewGuid());
        Assert.Null(result);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_AfterCreate_ReturnsCreateEntry()
    {
        // Acceptance kriterij #3 — kreiranu promjenu bilježi
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "vrste_limita");
        var id = await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Sedmični", "SED", 4, true),
            ActorId, ActorName);

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, id);

        Assert.NotNull(entry);
        Assert.Equal(AuditActions.Create, entry.Action);
        Assert.Equal(ActorId, entry.ChangedBy);
        Assert.Equal(ActorName, entry.ChangedByName);
        Assert.NotNull(entry.NewValues);
        Assert.Null(entry.OldValues);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_AfterCreate_ChangedAtIsRecent()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "vrste_limita");
        var before = DateTime.UtcNow;
        var id = await svc.CreateVrijednostAsync(
            new CreateSifarnikVrijednostRequest(katId, "Sedmični", "SED", 4, true),
            ActorId, ActorName);

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, id);

        Assert.NotNull(entry);
        Assert.True(entry.ChangedAt >= before);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_AfterUpdate_ReturnsUpdateEntry()
    {
        // Acceptance kriterij #3 — izmjena bilježi UPDATE, ne CREATE
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator Senior", "VER_SR", 2, true),
            ActorId, ActorName);

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, ver.Id);

        Assert.NotNull(entry);
        Assert.Equal(AuditActions.Update, entry.Action);
        Assert.NotNull(entry.OldValues);
        Assert.NotNull(entry.NewValues);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_AfterUpdate_OldValuesContainPreviousNaziv()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator Senior", "VER_SR", 2, true),
            ActorId, ActorName);

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, ver.Id);
        Assert.NotNull(entry);
        Assert.Contains("Verifikator", entry.OldValues);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_AfterDelete_ReturnsDeleteEntry()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var posm = await GetByNazivAsync(svc, katId, "Posmatrač");

        await svc.DeleteVrijednostAsync(posm.Id, ActorId, ActorName);

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, posm.Id);

        Assert.NotNull(entry);
        Assert.Equal(AuditActions.Delete, entry.Action);
        Assert.NotNull(entry.OldValues);
        Assert.Null(entry.NewValues);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_AfterMultipleUpdates_ReturnsLatestEntry()
    {
        // Mora vraćati zadnji (ne prvi) zapis
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator v2", "VER2", 2, true),
            ActorId, ActorName);

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator v3", "VER3", 2, true),
            ActorId, ActorName);

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, ver.Id);
        Assert.NotNull(entry);
        Assert.Contains("Verifikator v3", entry.NewValues);
    }

    [Fact]
    public async Task GetLastAuditEntryAsync_SeedValuesHaveSeedAudit()
    {
        // Seed vrijednosti imaju CREATE audit od inicijalizacije
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var unosnik = await GetByNazivAsync(svc, katId, "Unosnik");

        var entry = await svc.GetLastAuditEntryAsync(AuditEntityTypes.SifarnikVrijednost, unosnik.Id);

        Assert.NotNull(entry);
        Assert.Equal(AuditActions.Create, entry.Action);
        Assert.Equal("Admin (seed)", entry.ChangedByName);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetLastAuditEntriesAsync (batch)  [Acceptance kriterij #3]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetLastAuditEntriesAsync_WhenEmptyInput_ReturnsEmptyDictionary()
    {
        var svc = CreateSvc();
        var result = await svc.GetLastAuditEntriesAsync(
            AuditEntityTypes.SifarnikVrijednost, []);
        Assert.Empty(result);
    }

    [Fact]
    public async Task GetLastAuditEntriesAsync_ReturnsEntryForEachKnownId()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var rows = await svc.GetVrijednostiAsync(katId, onlyActive: false);
        var ids = rows.Select(v => v.Id).ToList();

        var result = await svc.GetLastAuditEntriesAsync(AuditEntityTypes.SifarnikVrijednost, ids);

        Assert.Equal(ids.Count, result.Count);
        foreach (var id in ids)
            Assert.True(result.ContainsKey(id));
    }

    [Fact]
    public async Task GetLastAuditEntriesAsync_WhenIdHasNoAudit_IsAbsentFromResult()
    {
        var svc = CreateSvc();
        var unknownId = Guid.NewGuid();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var unosnik = await GetByNazivAsync(svc, katId, "Unosnik");

        var result = await svc.GetLastAuditEntriesAsync(
            AuditEntityTypes.SifarnikVrijednost, [unosnik.Id, unknownId]);

        Assert.Contains(unosnik.Id, result);
        Assert.DoesNotContain(unknownId, result);
    }

    [Fact]
    public async Task GetLastAuditEntriesAsync_AfterUpdate_ReturnsLatestEntryPerValue()
    {
        // Batch vraća najnoviji (UPDATE), ne stariji (CREATE)
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        await svc.UpdateVrijednostAsync(ver.Id,
            new UpdateSifarnikVrijednostRequest("Verifikator Senior", "VER_SR", 2, true),
            ActorId, ActorName);

        var result = await svc.GetLastAuditEntriesAsync(
            AuditEntityTypes.SifarnikVrijednost, [ver.Id]);

        Assert.True(result.ContainsKey(ver.Id));
        Assert.Equal(AuditActions.Update, result[ver.Id].Action);
    }

    [Fact]
    public async Task GetLastAuditEntriesAsync_ReturnsOneEntryPerIdEvenWithMultipleAudits()
    {
        var svc = CreateSvc();
        var katId = await GetKatIdAsync(svc, "tipovi_rola");
        var ver = await GetByNazivAsync(svc, katId, "Verifikator");

        // Napravi 3 izmjene — batch mora vratiti samo jednu po ID-u
        for (var i = 1; i <= 3; i++)
        {
            await svc.UpdateVrijednostAsync(ver.Id,
                new UpdateSifarnikVrijednostRequest($"Verifikator v{i}", "VER", 2, true),
                ActorId, ActorName);
        }

        var result = await svc.GetLastAuditEntriesAsync(
            AuditEntityTypes.SifarnikVrijednost, [ver.Id]);

        Assert.Single(result); // Samo jedan entry po ID-u
        Assert.Contains("Verifikator v3", result[ver.Id].NewValues); // Zadnji
    }
}
