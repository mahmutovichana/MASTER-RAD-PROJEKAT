namespace RBBH.TestAutomation.Api.DTO;

/// <summary>Tip test scenarija — određuje koji set polja se koristi.</summary>
public enum TipScenarija
{
    /// <summary>Microservice REST — HTTP poziv s header-ima, body-jem i assert-ima.</summary>
    Rest,

    /// <summary>Blazor/UI — navigacija i interakcija s elementima stranice.</summary>
    Ui,

    /// <summary>bUnit — generisani testovi iz .razor sadržaja komponente.</summary>
    Blazor,
}

/// <summary>HTTP metoda za REST scenarij.</summary>
public enum HttpMetoda { Get, Post, Put, Patch, Delete }

/// <summary>Tip akcije koraka u UI scenariju.</summary>
public enum UiAkcija
{
    /// <summary>Klik na element identifikovan selektorom.</summary>
    Klik,

    /// <summary>Upis teksta u polje (selektor + vrijednost).</summary>
    Upis,

    /// <summary>Provjera da element sadrži očekivani tekst.</summary>
    OcekujTekst,

    /// <summary>Provjera da element postoji u DOM-u.</summary>
    OcekujElement,
}

/// <summary>Jedan HTTP header (ključ/vrijednost). Vrijednost podržava <c>{{token}}</c> tokene.</summary>
public sealed record HeaderDto(string Kljuc, string Vrijednost);

/// <summary>
/// Assert nad JSON response body-jem. <c>JsonPutanja</c> je JSONPath izraz (npr. <c>$.data.id</c>),
/// <c>OcekivanaVrijednost</c> je string s kojim se poredi stringifikovana vrijednost na toj putanji.
/// Izvršavanje (evaluacija) dolazi sa Run engine-om; ovaj DTO samo čuva definiciju.
/// </summary>
public sealed record ResponseAssertDto(string JsonPutanja, string OcekivanaVrijednost);

/// <summary>
/// Jedan korak UI scenarija. Koja polja su relevantna ovisi o <c>Akcija</c>:
/// <list type="bullet">
/// <item><see cref="UiAkcija.Klik"/> — <c>Selektor</c> obavezan</item>
/// <item><see cref="UiAkcija.Upis"/> — <c>Selektor</c> + <c>Vrijednost</c> obavezni</item>
/// <item><see cref="UiAkcija.OcekujTekst"/> / <see cref="UiAkcija.OcekujElement"/> — <c>OcekivaniTekst</c> obavezan</item>
/// </list>
/// </summary>
public sealed record UiKorakDto(
    UiAkcija Akcija,
    string?  Selektor,
    string?  Vrijednost,
    string?  OcekivaniTekst
);

/// <summary>
/// Detalji REST scenarija. <c>RequestBody</c> je sirovi JSON tekst (null = tijelo se ne šalje).
/// URL i header vrijednosti mogu sadržavati <c>{{token}}</c>/<c>{{baseUrl}}</c> tokene.
/// </summary>
public sealed record RestScenarioDto(
    HttpMetoda                       Metoda,
    string                           Url,
    IReadOnlyList<HeaderDto>         Headeri,
    string?                          RequestBody,
    int                              OcekivaniStatus,
    IReadOnlyList<ResponseAssertDto> ResponseAsserti
);

/// <summary>
/// Detalji bUnit scenarija — čuva .razor sadržaj i naziv komponente.
/// Kod generisanja testova koristi <see cref="RBBH.TestAutomation.Core.Generation.BlazorComponentAnalyzer"/>.
/// </summary>
public sealed record BlazorScenarioDto(
    string ComponentName,
    string RazorContent
);

/// <summary>
/// Detalji UI/Blazor scenarija. <c>UrlStranice</c> podržava <c>{{baseUrl}}</c> token.
/// Koraci se izvršavaju redom (Playwright/engine dolazi u kasnijim sprintovima).
/// </summary>
public sealed record UiScenarioDto(
    string                    UrlStranice,
    IReadOnlyList<UiKorakDto> Koraci
);

/// <summary>
/// Puni model test scenarija. Tačno jedno od <c>Rest</c>/<c>Ui</c> je popunjeno,
/// ovisno o <c>Tip</c>. Audit polja (<c>KreiranOd</c>, <c>IzmjenjenOd</c>…) su Keycloak sub claim-ovi.
/// </summary>
public sealed record ScenarioDto(
    Guid                Id,
    Guid?               GroupId,
    string              Naziv,
    string?             Opis,
    TipScenarija        Tip,
    RestScenarioDto?    Rest,
    UiScenarioDto?      Ui,
    BlazorScenarioDto?  Blazor,
    string?             KreiranOd,
    DateTime            KreiranAt,
    string?             IzmjenjenOd,
    DateTime?           IzmjenjenAt,
    bool                RunSequentially = false
);

/// <summary>Ulaz za kreiranje novog scenarija.</summary>
public sealed record CreateScenarioRequest(
    Guid?               GroupId,
    string              Naziv,
    string?             Opis,
    TipScenarija        Tip,
    RestScenarioDto?    Rest,
    UiScenarioDto?      Ui,
    BlazorScenarioDto?  Blazor = null,
    bool                RunSequentially = false
);

/// <summary>Ulaz za izmjenu postojećeg scenarija. ID se ne mijenja kroz ovaj zahtjev.</summary>
public sealed record UpdateScenarioRequest(
    Guid?               GroupId,
    string              Naziv,
    string?             Opis,
    TipScenarija        Tip,
    RestScenarioDto?    Rest,
    UiScenarioDto?      Ui,
    BlazorScenarioDto?  Blazor = null,
    bool                RunSequentially = false
);

/// <summary>Varijabla Run konfiguracije — naziv i konkretna vrijednost (npr. baseUrl = https://api.dev).</summary>
public sealed record RunVariableDto(string Naziv, string Vrijednost);

/// <summary>
/// Run konfiguracija — izvor varijabli za <c>{{token}}</c>/<c>{{baseUrl}}</c> zamjenu.
/// U Sprintu 2 sadrži hardcoded dev vrijednosti; stvarni Run modul dolazi u kasnijim sprintovima.
/// </summary>
public sealed record RunConfigDto(IReadOnlyList<RunVariableDto> Varijable);

/// <summary>Konstante za <c>entity_type</c> kolonu audit zapisa vezanih za scenarije.</summary>
public static class ScenarioAuditEntityTypes
{
    public const string Scenarij = "test_scenarij";
}
