using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// Servis za upravljanje grupama testova: CRUD, hijerarhija ≤2 nivoa, scenariji unutar grupe,
/// reorder (drag&amp;drop), kopiranje scenarija i pauziranje/aktiviranje rasporeda.
///
/// Dvije implementacije:
///   <see cref="MockGroupService"/> — in-memory (dev/demo, bez baze).
///   GroupService (SQL Server/EF Core) — tanki adapter, dolazi sa #3 (TAG-36); UI se ne mijenja.
///
/// Switch se radi preko <c>MockGroups:Enabled</c> flag-a (fallback na <c>MockAuth:Enabled</c>),
/// vidi <see cref="Groups.GroupServiceRegistration.AddGroupServices"/>.
/// CREATE/UPDATE/DELETE operacije prosljeđuju <c>actorId</c>/<c>actorName</c>
/// (iz <see cref="Auth.IUserContext"/>) radi audit traga.
/// </summary>
public interface IGroupService
{
    /// <summary>
    /// Vraća cijelo stablo grupa (≤2 nivoa) sa pred-izračunatim <see cref="DTO.GroupSummaryDto"/>
    /// na svakom čvoru. Sažeci se računaju u jednom prolazu — bez N+1 poziva po grupi.
    /// </summary>
    Task<IReadOnlyList<GroupTreeNodeDto>> GetGroupsTreeAsync(CancellationToken ct = default);

    /// <summary>Vraća grupu po ID-u, ili null ako ne postoji.</summary>
    Task<GroupDto?> GetByIdAsync(Guid id, CancellationToken ct = default);

    /// <summary>
    /// Vraća root grupe (bez parenta), sortirano po prioritetu (desc) pa nazivu.
    /// Koristi se za parent-dropdown pri kreiranju podgrupe.
    /// </summary>
    Task<IReadOnlyList<GroupDto>> GetRootGroupsAsync(CancellationToken ct = default);

    /// <summary>
    /// Kreira novu grupu i vraća njen ID.
    /// </summary>
    /// <exception cref="InvalidOperationException">
    /// Ako bi grupa prekršila pravilo ≤2 nivoa (zadati parent već ima svog parenta).
    /// </exception>
    Task<Guid> CreateAsync(CreateGroupRequest r, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>Mijenja postojeću grupu (naziv, opis, boja, tag, prioritet).</summary>
    /// <exception cref="InvalidOperationException">Ako grupa s datim ID-om ne postoji.</exception>
    Task UpdateAsync(Guid id, UpdateGroupRequest r, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>Briše grupu i kaskadno njene scenarije, rasporede i run rezultate.</summary>
    /// <exception cref="InvalidOperationException">
    /// Ako grupa ima podgrupe — prvo ih treba obrisati ili premjestiti.
    /// </exception>
    Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>Vraća scenarije grupe sortirane po <c>Redoslijed</c>.</summary>
    Task<IReadOnlyList<ScenarioListItemDto>> GetScenariosAsync(Guid groupId, CancellationToken ct = default);

    /// <summary>
    /// Postavlja redoslijed scenarija grupe prema poziciji svakog ID-a u <paramref name="orderedIds"/>.
    /// </summary>
    Task ReorderScenariosAsync(Guid groupId, IReadOnlyList<Guid> orderedIds, CancellationToken ct = default);

    /// <summary>
    /// Kopira scenarij u drugu grupu (kopija ide na kraj liste ciljne grupe, naziv dobije sufiks "(kopija)").
    /// Vraća kreiranu kopiju. Izvorni scenarij ostaje nepromijenjen.
    /// </summary>
    /// <exception cref="InvalidOperationException">Ako izvorni scenarij ili ciljna grupa ne postoje.</exception>
    Task<ScenarioListItemDto> CopyScenarioAsync(Guid scenarioId, Guid targetGroupId, string actorId, string actorName, CancellationToken ct = default);

    /// <summary>
    /// Pauzira (false) ili aktivira (true) rasporede grupe.
    /// Stub za Sprint 2 — stvarni engine izvršavanja dolazi u Sprint 3.
    /// </summary>
    Task SetScheduleActiveAsync(Guid groupId, bool isActive, CancellationToken ct = default);

    Task<NotificationConfig?> GetNotificationConfigAsync(Guid groupId, CancellationToken ct = default);
    Task SaveNotificationConfigAsync(Guid groupId, NotificationConfig config, CancellationToken ct = default);
}
