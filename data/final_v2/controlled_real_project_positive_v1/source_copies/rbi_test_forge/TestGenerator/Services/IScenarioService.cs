using RBBH.TestAutomation.Api.DTO;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Servis za upravljanje test scenarijima: CRUD, kloniranje i dohvat Run konfiguracije.
///
/// Dvije implementacije:
///   <see cref="MockScenarioService"/> — in-memory (dev/demo, bez baze).
///   ScenarioService (SQL Server/EF Core) — dolazi s TAG-36; UI se ne mijenja.
///
/// Switch se radi preko <c>ScenarioServiceRegistration.AddScenarioServices</c>.
/// CREATE/UPDATE/DELETE operacije primaju <c>actorId</c>/<c>actorName</c>
/// (iz <see cref="Auth.IUserContext"/>) radi audit traga.
/// </summary>
public interface IScenarioService
{
    /// <summary>
    /// Vraća sve scenarije, sortirane po nazivu. Koristi <see cref="ScenarioListItemDto"/>
    /// iz <c>GroupDtos.cs</c> — isti tip koji grupe koriste za prikaz scenarija unutar grupe.
    /// </summary>
    Task<IReadOnlyList<ScenarioListItemDto>> GetAllAsync(CancellationToken ct = default);

    /// <summary>Vraća puni scenarij po ID-u, ili null ako ne postoji.</summary>
    Task<ScenarioDto?> GetByIdAsync(Guid id, CancellationToken ct = default);

    /// <summary>
    /// Kreira novi scenarij i vraća njegov ID.
    /// </summary>
    Task<Guid> CreateAsync(CreateScenarioRequest r, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>
    /// Mijenja postojeći scenarij.
    /// </summary>
    /// <exception cref="InvalidOperationException">Ako scenarij s datim ID-om ne postoji.</exception>
    Task UpdateAsync(Guid id, UpdateScenarioRequest r, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>
    /// Briše scenarij. Tiho prolazi ako scenarij ne postoji (idempotentna operacija).
    /// </summary>
    Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>
    /// Klonira scenarij — kreira duboku kopiju s novim ID-om i nazivom koji dobija sufiks "(kopija)".
    /// Vraća kreiranu kopiju. Izvorni scenarij ostaje nepromijenjen.
    /// </summary>
    /// <exception cref="InvalidOperationException">Ako izvorni scenarij ne postoji.</exception>
    Task<ScenarioDto> CloneAsync(Guid id, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>
    /// Vraća Run konfiguraciju s varijablama za <c>{{token}}</c>/<c>{{baseUrl}}</c> zamjenu.
    /// U Sprintu 2 vraća hardcoded dev vrijednosti; stvarni Run modul dolazi u kasnijim sprintovima.
    /// </summary>
    Task<RunConfigDto> GetRunConfigAsync(CancellationToken ct = default);
}
