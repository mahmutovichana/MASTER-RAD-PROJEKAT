using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;

namespace UnitTests.Scenariji;

/// <summary>
/// Unit testovi za <see cref="MockScenarioService"/>.
///
/// Pokriva data-sloj acceptance kriterija TAG-29:
///   AC1/AC2 — CREATE s REST podacima, GetById vraća isti sadržaj
///   AC3     — CREATE s UI podacima
///   AC5     — CloneAsync: novi Id, naziv s "(kopija)", duboka kopija
///   AC6     — UpdateAsync na nepostojećem baca, audit polja se postavljaju
///
/// Svaki test kreira svoju instancu servisa → potpuna izolacija stanja.
/// </summary>
public class MockScenarioServiceTests
{
    private const string ActorId   = "test-actor-001";
    private const string ActorName = "Test Korisnik";

    private static MockScenarioService CreateSvc() => new();

    private static CreateScenarioRequest RestRequest(string naziv = "Test REST") =>
        new(
            GroupId: null,
            Naziv:   naziv,
            Opis:    null,
            Tip:     TipScenarija.Rest,
            Rest: new RestScenarioDto(
                Metoda:          HttpMetoda.Get,
                Url:             "{{baseUrl}}/api/test",
                Headeri:         [new HeaderDto("Authorization", "Bearer {{token}}")],
                RequestBody:     null,
                OcekivaniStatus: 200,
                ResponseAsserti: [new ResponseAssertDto("$.ok", "true")]
            ),
            Ui: null
        );

    private static CreateScenarioRequest UiRequest(string naziv = "Test UI") =>
        new(
            GroupId: null,
            Naziv:   naziv,
            Opis:    null,
            Tip:     TipScenarija.Ui,
            Rest:    null,
            Ui: new UiScenarioDto(
                UrlStranice: "{{baseUrl}}/login",
                Koraci: [new UiKorakDto(UiAkcija.Klik, "#btn", null, null)]
            )
        );

    // ═══════════════════════════════════════════════════════════════════════════
    // Seed
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetAllAsync_WhenSeeded_ReturnsNineScenarios()
    {
        var svc = CreateSvc();
        var lista = await svc.GetAllAsync();
        Assert.Equal(9, lista.Count);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Create + GetById
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CreateAsync_REST_GetByIdVracaIsteSadrzaj()
    {
        var svc = CreateSvc();
        var req = RestRequest("Moj REST test");

        var id = await svc.CreateAsync(req, ActorId, ActorName);
        var dto = await svc.GetByIdAsync(id);

        Assert.NotNull(dto);
        Assert.Equal("Moj REST test",    dto.Naziv);
        Assert.Equal(TipScenarija.Rest,  dto.Tip);
        Assert.NotNull(dto.Rest);
        Assert.Null(dto.Ui);
        Assert.Equal(HttpMetoda.Get,     dto.Rest.Metoda);
        Assert.Equal("{{baseUrl}}/api/test", dto.Rest.Url);
        Assert.Single(dto.Rest.Headeri);
        Assert.Single(dto.Rest.ResponseAsserti);
    }

    [Fact]
    public async Task CreateAsync_UI_GetByIdVracaIsteSadrzaj()
    {
        var svc = CreateSvc();
        var req = UiRequest("Moj UI test");

        var id = await svc.CreateAsync(req, ActorId, ActorName);
        var dto = await svc.GetByIdAsync(id);

        Assert.NotNull(dto);
        Assert.Equal("Moj UI test",     dto.Naziv);
        Assert.Equal(TipScenarija.Ui,   dto.Tip);
        Assert.Null(dto.Rest);
        Assert.NotNull(dto.Ui);
        Assert.Single(dto.Ui.Koraci);
    }

    [Fact]
    public async Task CreateAsync_PostavljaKreiranOdIKreiranAt()
    {
        var svc  = CreateSvc();
        var prije = DateTime.UtcNow.AddSeconds(-1);

        var id  = await svc.CreateAsync(RestRequest(), ActorId, ActorName);
        var dto = await svc.GetByIdAsync(id);

        Assert.NotNull(dto);
        Assert.Equal(ActorId, dto.KreiranOd);
        Assert.True(dto.KreiranAt >= prije);
        Assert.Null(dto.IzmjenjenOd);
        Assert.Null(dto.IzmjenjenAt);
    }

    [Fact]
    public async Task GetByIdAsync_NaNepostojeci_VracaNull()
    {
        var svc = CreateSvc();
        var dto = await svc.GetByIdAsync(Guid.NewGuid());
        Assert.Null(dto);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Update
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task UpdateAsync_PostavljaIzmjenjenOdIIzmjenjenAt()
    {
        var svc = CreateSvc();
        var id  = await svc.CreateAsync(RestRequest(), ActorId, ActorName);

        var prije = DateTime.UtcNow.AddSeconds(-1);
        var req   = RestRequest("Izmijenjeni naziv");
        await svc.UpdateAsync(id, new UpdateScenarioRequest(req.GroupId, req.Naziv, req.Opis, req.Tip, req.Rest, req.Ui),
                              "editor-001", "Editor");

        var dto = await svc.GetByIdAsync(id);
        Assert.NotNull(dto);
        Assert.Equal("Izmijenjeni naziv", dto.Naziv);
        Assert.Equal("editor-001",        dto.IzmjenjenOd);
        Assert.NotNull(dto.IzmjenjenAt);
        Assert.True(dto.IzmjenjenAt >= prije);
    }

    [Fact]
    public async Task UpdateAsync_NaNepostojeci_BacaInvalidOperationException()
    {
        var svc = CreateSvc();
        var req = RestRequest();
        var update = new UpdateScenarioRequest(req.GroupId, req.Naziv, req.Opis, req.Tip, req.Rest, req.Ui);

        await Assert.ThrowsAsync<InvalidOperationException>(
            () => svc.UpdateAsync(Guid.NewGuid(), update, ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Delete
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task DeleteAsync_UklanjaScenarij()
    {
        var svc = CreateSvc();
        var id  = await svc.CreateAsync(RestRequest(), ActorId, ActorName);

        await svc.DeleteAsync(id, ActorId, ActorName);

        var dto = await svc.GetByIdAsync(id);
        Assert.Null(dto);
    }

    [Fact]
    public async Task DeleteAsync_NaNepostojeci_NeBacaGresuku()
    {
        var svc = CreateSvc();
        // Idempotentna operacija — ne smije baciti iznimku.
        var ex = await Record.ExceptionAsync(() => svc.DeleteAsync(Guid.NewGuid(), ActorId, ActorName));
        Assert.Null(ex);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Clone — AC5
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task CloneAsync_VracaKopijuSNovimIdINazivom()
    {
        var svc = CreateSvc();
        var id  = await svc.CreateAsync(RestRequest("Original"), ActorId, ActorName);

        var kopija = await svc.CloneAsync(id, ActorId, ActorName);

        Assert.NotEqual(id,              kopija.Id);
        Assert.Equal("Original (kopija)", kopija.Naziv);
    }

    [Fact]
    public async Task CloneAsync_KopijaJeUListiScenarija()
    {
        var svc    = CreateSvc();
        var id     = await svc.CreateAsync(RestRequest(), ActorId, ActorName);
        var kopija = await svc.CloneAsync(id, ActorId, ActorName);

        var lista = await svc.GetAllAsync();
        Assert.Contains(lista, s => s.Id == kopija.Id);
    }

    [Fact]
    public async Task CloneAsync_REST_DubokaKopija_MutacijaKopijeneUtjecaNaOriginal()
    {
        var svc = CreateSvc();
        var id  = await svc.CreateAsync(RestRequest(), ActorId, ActorName);
        var kopija = await svc.CloneAsync(id, ActorId, ActorName);

        // Izmjena headera kopije — direktna mutacija nije moguća na IReadOnlyList,
        // ali kroz Update možemo provjeriti da su headeri neovisni objekti.
        var original = await svc.GetByIdAsync(id);
        Assert.NotNull(original);
        Assert.NotNull(kopija.Rest);

        // Kopija i original ne dijele iste reference lista.
        Assert.NotSame(original.Rest!.Headeri, kopija.Rest.Headeri);
        Assert.NotSame(original.Rest.ResponseAsserti, kopija.Rest.ResponseAsserti);
    }

    [Fact]
    public async Task CloneAsync_UI_DubokaKopija_KoraciSuNezavisni()
    {
        var svc = CreateSvc();
        var id  = await svc.CreateAsync(UiRequest(), ActorId, ActorName);
        var kopija = await svc.CloneAsync(id, ActorId, ActorName);

        var original = await svc.GetByIdAsync(id);
        Assert.NotNull(original);
        Assert.NotNull(kopija.Ui);

        Assert.NotSame(original.Ui!.Koraci, kopija.Ui.Koraci);
    }

    [Fact]
    public async Task CloneAsync_PostavljaAuditPolja()
    {
        var svc    = CreateSvc();
        var id     = await svc.CreateAsync(RestRequest(), ActorId, ActorName);
        var prije  = DateTime.UtcNow.AddSeconds(-1);
        var kopija = await svc.CloneAsync(id, "kloner-001", "Kloner");

        Assert.Equal("kloner-001", kopija.KreiranOd);
        Assert.True(kopija.KreiranAt >= prije);
        Assert.Null(kopija.IzmjenjenOd);
    }

    [Fact]
    public async Task CloneAsync_NaNepostojeci_BacaInvalidOperationException()
    {
        var svc = CreateSvc();
        await Assert.ThrowsAsync<InvalidOperationException>(
            () => svc.CloneAsync(Guid.NewGuid(), ActorId, ActorName));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // RunConfig
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetRunConfigAsync_VracaVarijable()
    {
        var svc    = CreateSvc();
        var config = await svc.GetRunConfigAsync();

        Assert.NotEmpty(config.Varijable);
        Assert.Contains(config.Varijable, v => v.Naziv == "baseUrl");
        Assert.Contains(config.Varijable, v => v.Naziv == "token");
    }
}
