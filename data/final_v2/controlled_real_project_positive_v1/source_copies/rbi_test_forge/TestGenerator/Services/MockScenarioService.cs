using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// In-memory dev implementacija servisa scenarija — radi bez baze. Registruje se kao Singleton
/// da promjene opstaju između navigacija u toku jedne sesije procesa.
///
/// Polja su instancna (ne statička) kako bi unit testovi mogli kreirati izoliranu
/// instancu po testu bez međusobnog zagađivanja stanja.
///
/// Seed (vidi konstruktor): 3 scenarija — 2 REST i 1 UI — koji demonstriraju obje vrste
/// te korištenje {{baseUrl}}/{{token}} varijabli.
/// </summary>
public sealed class MockScenarioService : IScenarioService
{
    private const string SeedActor = "mock-admin-001";

    private readonly List<ScenarioDto> _scenariji;
    private readonly Lock _lock = new();

    private static readonly RunConfigDto SeedRunConfig = new(
    [
        new RunVariableDto("baseUrl", "http://localhost:5187"),
        new RunVariableDto("token",   "ey_mock_jwt_token_dev"),
        new RunVariableDto("userId",  "42"),
    ]);

    public MockScenarioService()
    {
        var now = DateTime.UtcNow;

        _scenariji =
        [
            // REST — health check bez autentikacije
            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000001"),
                GroupId:     null,
                Naziv:       "Health check",
                Opis:        "Provjerava da API uopće odgovara.",
                Tip:         TipScenarija.Rest,
                Rest: new RestScenarioDto(
                    Metoda:          HttpMetoda.Get,
                    Url:             "{{baseUrl}}/health",
                    Headeri:         [],
                    RequestBody:     null,
                    OcekivaniStatus: 200,
                    ResponseAsserti: []
                ),
                Ui:          null,
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-10),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),

            // REST — login s body-jem i header-om s tokenom
            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000002"),
                GroupId:     null,
                Naziv:       "Login korisnika",
                Opis:        "Namjerni negativni smoke test za prikaz response detalja.",
                Tip:         TipScenarija.Rest,
                Rest: new RestScenarioDto(
                    Metoda:          HttpMetoda.Get,
                    Url:             "{{baseUrl}}/health",
                    Headeri:         [],
                    RequestBody:     null,
                    OcekivaniStatus: 201,
                    ResponseAsserti: []
                ),
                Ui:          null,
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-8),
                IzmjenjenOd: null,
                IzmjenjenAt: null,
                RunSequentially: true
            ),

            // UI — login forma u Blazor aplikaciji
            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000003"),
                GroupId:     null,
                Naziv:       "UI login forma",
                Opis:        "Otvori /login, unesi kredencijale, klikni dugme, očekuj Dashboard.",
                Tip:         TipScenarija.Ui,
                Rest:        null,
                Ui: new UiScenarioDto(
                    UrlStranice: "{{baseUrl}}/login",
                    Koraci:
                    [
                        new UiKorakDto(UiAkcija.Upis,         "#username",     "test@example.com", null),
                        new UiKorakDto(UiAkcija.Upis,         "#password",     "TestPass123",      null),
                        new UiKorakDto(UiAkcija.Klik,         "#btn-login",    null,               null),
                        new UiKorakDto(UiAkcija.OcekujTekst,  ".page-title",   null,               "Dashboard"),
                    ]
                ),
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-5),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),

            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000004"),
                GroupId:     null,
                Naziv:       "Kreiranje korisnika",
                Opis:        "Kreira testnog korisnika kroz REST API.",
                Tip:         TipScenarija.Rest,
                Rest: new RestScenarioDto(
                    Metoda:          HttpMetoda.Post,
                    Url:             "{{baseUrl}}/api/users",
                    Headeri:         [new HeaderDto("Authorization", "Bearer {{token}}")],
                    RequestBody:     "{\"email\":\"new.user@example.com\",\"name\":\"New User\"}",
                    OcekivaniStatus: 201,
                    ResponseAsserti: [new ResponseAssertDto("$.email", "new.user@example.com")]
                ),
                Ui:          null,
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-4),
                IzmjenjenOd: null,
                IzmjenjenAt: null,
                RunSequentially: true
            ),

            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000005"),
                GroupId:     null,
                Naziv:       "Brisanje korisnika",
                Opis:        "Brise testnog korisnika kroz REST API.",
                Tip:         TipScenarija.Rest,
                Rest: new RestScenarioDto(
                    Metoda:          HttpMetoda.Delete,
                    Url:             "{{baseUrl}}/api/users/{{userId}}",
                    Headeri:         [new HeaderDto("Authorization", "Bearer {{token}}")],
                    RequestBody:     null,
                    OcekivaniStatus: 204,
                    ResponseAsserti: []
                ),
                Ui:          null,
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-4),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),

            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000006"),
                GroupId:     null,
                Naziv:       "Validacija forme",
                Opis:        "Provjerava klijentsku validaciju login forme.",
                Tip:         TipScenarija.Ui,
                Rest:        null,
                Ui: new UiScenarioDto(
                    UrlStranice: "{{baseUrl}}/login",
                    Koraci:
                    [
                        new UiKorakDto(UiAkcija.Klik, "#btn-login", null, null),
                        new UiKorakDto(UiAkcija.OcekujTekst, ".validation-message", null, "Obavezno polje"),
                    ]
                ),
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-4),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),

            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000007"),
                GroupId:     null,
                Naziv:       "GET /users paginacija",
                Opis:        "Provjerava paginiranu listu korisnika.",
                Tip:         TipScenarija.Rest,
                Rest: new RestScenarioDto(
                    Metoda:          HttpMetoda.Get,
                    Url:             "{{baseUrl}}/api/users?page=1&pageSize=10",
                    Headeri:         [new HeaderDto("Authorization", "Bearer {{token}}")],
                    RequestBody:     null,
                    OcekivaniStatus: 200,
                    ResponseAsserti: [new ResponseAssertDto("$.page", "1")]
                ),
                Ui:          null,
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-3),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),

            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000008"),
                GroupId:     null,
                Naziv:       "POST /users vraca 400",
                Opis:        "Provjerava validaciju losih podataka.",
                Tip:         TipScenarija.Rest,
                Rest: new RestScenarioDto(
                    Metoda:          HttpMetoda.Post,
                    Url:             "{{baseUrl}}/api/users",
                    Headeri:         [new HeaderDto("Authorization", "Bearer {{token}}")],
                    RequestBody:     "{\"email\":\"\"}",
                    OcekivaniStatus: 400,
                    ResponseAsserti: []
                ),
                Ui:          null,
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-3),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),

            new ScenarioDto(
                Id:          Guid.Parse("29000000-0000-0000-0000-000000000009"),
                GroupId:     null,
                Naziv:       "End-to-end checkout",
                Opis:        "Demo E2E tok kroz UI runner.",
                Tip:         TipScenarija.Ui,
                Rest:        null,
                Ui: new UiScenarioDto(
                    UrlStranice: "{{baseUrl}}/checkout",
                    Koraci:
                    [
                        new UiKorakDto(UiAkcija.OcekujTekst, ".page-title", null, "Checkout"),
                    ]
                ),
                Blazor:      null,
                KreiranOd:   SeedActor,
                KreiranAt:   now.AddDays(-2),
                IzmjenjenOd: null,
                IzmjenjenAt: null
            ),
        ];
    }

    // ── Čitanje ───────────────────────────────────────────────────────────────

    public Task<IReadOnlyList<ScenarioListItemDto>> GetAllAsync(CancellationToken ct = default)
    {
        lock (_lock)
        {
            IReadOnlyList<ScenarioListItemDto> result = _scenariji
                .OrderBy(s => s.Naziv, StringComparer.OrdinalIgnoreCase)
                .Select((s, i) => ToListItem(s, i))
                .ToList();
            return Task.FromResult(result);
        }
    }

    public Task<ScenarioDto?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        lock (_lock)
        {
            return Task.FromResult(_scenariji.FirstOrDefault(s => s.Id == id));
        }
    }

    // ── Mutacije ──────────────────────────────────────────────────────────────

    public Task<Guid> CreateAsync(CreateScenarioRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var dto = new ScenarioDto(
                Id:          Guid.NewGuid(),
                GroupId:     r.GroupId,
                Naziv:       r.Naziv,
                Opis:        r.Opis,
                Tip:         r.Tip,
                Rest:        r.Rest,
                Ui:          r.Ui,
                Blazor:      r.Blazor,
                KreiranOd:   actorId,
                KreiranAt:   DateTime.UtcNow,
                IzmjenjenOd: null,
                IzmjenjenAt: null,
                RunSequentially: r.RunSequentially);

            _scenariji.Add(dto);
            return Task.FromResult(dto.Id);
        }
    }

    public Task UpdateAsync(Guid id, UpdateScenarioRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var idx = _scenariji.FindIndex(s => s.Id == id);
            if (idx < 0)
                throw new InvalidOperationException($"Scenarij s ID {id} ne postoji.");

            _scenariji[idx] = _scenariji[idx] with
            {
                GroupId     = r.GroupId,
                Naziv       = r.Naziv,
                Opis        = r.Opis,
                Tip         = r.Tip,
                Rest        = r.Rest,
                Ui          = r.Ui,
                Blazor      = r.Blazor,
                IzmjenjenOd = actorId,
                IzmjenjenAt = DateTime.UtcNow,
                RunSequentially = r.RunSequentially,
            };

            return Task.CompletedTask;
        }
    }

    public Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            _scenariji.RemoveAll(s => s.Id == id);
            return Task.CompletedTask;
        }
    }

    /// <summary>
    /// Kreira duboku kopiju scenarija. Novi ID, naziv s nastavkom "(kopija)",
    /// audit polja postavljene na trenutnog actor-a. Headeri, koraci i asserti su
    /// nezavisne kopije — mutacija kopije ne utječe na original.
    /// </summary>
    public Task<ScenarioDto> CloneAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var source = _scenariji.FirstOrDefault(s => s.Id == id)
                ?? throw new InvalidOperationException($"Scenarij s ID {id} ne postoji.");

            var kopija = new ScenarioDto(
                Id:          Guid.NewGuid(),
                GroupId:     source.GroupId,
                Naziv:       $"{source.Naziv} (kopija)",
                Opis:        source.Opis,
                Tip:         source.Tip,
                Rest:        source.Rest   is null ? null : DeepCopyRest(source.Rest),
                Ui:          source.Ui     is null ? null : DeepCopyUi(source.Ui),
                Blazor:      source.Blazor is null ? null : new BlazorScenarioDto(source.Blazor.ComponentName, source.Blazor.RazorContent),
                KreiranOd:   actorId,
                KreiranAt:   DateTime.UtcNow,
                IzmjenjenOd: null,
                IzmjenjenAt: null,
                RunSequentially: source.RunSequentially);

            _scenariji.Add(kopija);
            return Task.FromResult(kopija);
        }
    }

    public Task<RunConfigDto> GetRunConfigAsync(CancellationToken ct = default)
        => Task.FromResult(SeedRunConfig);

    // ── Duboko kopiranje (čuva nezavisnost kopije od originala) ──────────────

    private static RestScenarioDto DeepCopyRest(RestScenarioDto src) => new(
        Metoda:          src.Metoda,
        Url:             src.Url,
        Headeri:         src.Headeri.Select(h => new HeaderDto(h.Kljuc, h.Vrijednost)).ToList(),
        RequestBody:     src.RequestBody,
        OcekivaniStatus: src.OcekivaniStatus,
        ResponseAsserti: src.ResponseAsserti.Select(a => new ResponseAssertDto(a.JsonPutanja, a.OcekivanaVrijednost)).ToList()
    );

    private static UiScenarioDto DeepCopyUi(UiScenarioDto src) => new(
        UrlStranice: src.UrlStranice,
        Koraci:      src.Koraci.Select(k => new UiKorakDto(k.Akcija, k.Selektor, k.Vrijednost, k.OcekivaniTekst)).ToList()
    );

    private static ScenarioListItemDto ToListItem(ScenarioDto s, int index) =>
        new(s.Id, s.GroupId ?? Guid.Empty, s.Naziv, s.Tip.ToString(), index)
        {
            RunSequentially = s.RunSequentially,
        };
}
