using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services.Groups;
using RBBH.TestAutomation.Core.Domain;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>
/// In-memory dev implementacija servisa grupa — radi bez baze. Registruje se kao Singleton
/// da promjene opstaju između navigacija u toku jedne sesije procesa.
///
/// Polja su instancna (ne statička) kako bi unit testovi mogli kreirati izoliranu
/// instancu po testu bez međusobnog zagađivanja stanja.
///
/// Seed (vidi konstruktor): 3 root grupe (Smoke, Regression, Full Suite) + 1 podgrupa pod
/// Regression (demonstrira nesting ≤2), scenariji u svakoj, run rezultati koji pokrivaju
/// sve pragove pass-rate-a i null-state (Full Suite bez run-a), te po jedan raspored.
/// </summary>
public sealed class MockGroupService : IGroupService
{
    // ── Stabilni ID-evi za seed (samo konstante, ne mutabilno stanje) ─────────

    private static readonly Guid _grpSmoke      = Guid.Parse("10000000-0000-0000-0000-000000000001");
    private static readonly Guid _grpRegression = Guid.Parse("10000000-0000-0000-0000-000000000002");
    private static readonly Guid _grpFullSuite  = Guid.Parse("10000000-0000-0000-0000-000000000003");
    private static readonly Guid _grpRegApi      = Guid.Parse("10000000-0000-0000-0000-000000000004"); // podgrupa pod Regression
    private static readonly Guid _scenarioHealth = Guid.Parse("29000000-0000-0000-0000-000000000001");
    private static readonly Guid _scenarioLogin  = Guid.Parse("29000000-0000-0000-0000-000000000002");
    private static readonly Guid _scenarioUi     = Guid.Parse("29000000-0000-0000-0000-000000000003");
    private static readonly Guid _scenarioCreateUser = Guid.Parse("29000000-0000-0000-0000-000000000004");
    private static readonly Guid _scenarioDeleteUser = Guid.Parse("29000000-0000-0000-0000-000000000005");
    private static readonly Guid _scenarioFormValidation = Guid.Parse("29000000-0000-0000-0000-000000000006");
    private static readonly Guid _scenarioUsersPaging = Guid.Parse("29000000-0000-0000-0000-000000000007");
    private static readonly Guid _scenarioUsersBadRequest = Guid.Parse("29000000-0000-0000-0000-000000000008");
    private static readonly Guid _scenarioCheckout = Guid.Parse("29000000-0000-0000-0000-000000000009");

    private const string _seedActor = "mock-admin-001";

    // ── Instancno mutabilno stanje (izolirano po instanci) ────────────────────

    private readonly List<GroupDto>           _groups;
    private readonly List<ScenarioListItemDto> _scenariji;
    private readonly List<(Guid GroupId, DateTime At, double PassRate)> _runs;
    private readonly List<(Guid GroupId, bool IsActive)> _schedules;
    private readonly IScenarioService _scenarioSvc;
    private readonly Lock _lock = new();

    // ── Konstruktor — inicijalizacija seed podataka ───────────────────────────

    public MockGroupService() : this(new MockScenarioService())
    {
    }

    public MockGroupService(IScenarioService scenarioSvc)
    {
        _scenarioSvc = scenarioSvc;
        var now = DateTime.UtcNow;

        _groups =
        [
            new(_grpSmoke,      "Smoke",       "Brze osnovne provjere da sistem uopće radi.", "#43a047",
                TestTag.Smoke,      100, null,            _seedActor, now.AddDays(-20), null, null),
            new(_grpRegression, "Regression",  "Provjera da nove izmjene nisu pokvarile postojeće.", "#1e88e5",
                TestTag.Regression,  50, null,            _seedActor, now.AddDays(-20), null, null),
            new(_grpFullSuite,  "Full Suite",  "Kompletan skup testova prije release-a.", "#8e24aa",
                TestTag.Full,        10, null,            _seedActor, now.AddDays(-20), null, null),
            new(_grpRegApi,     "Regresija - API", "API regresijski podskup.", "#3949ab",
                TestTag.Regression,  50, _grpRegression,  _seedActor, now.AddDays(-15), null, null),
        ];

        _scenariji =
        [
            // Smoke
            new(_scenarioHealth, _grpSmoke, "Health check",    "REST", 0),
            new(_scenarioLogin,  _grpSmoke, "Login korisnika", "REST", 1) { RunSequentially = true },
            // Regression (root)
            new(_scenarioCreateUser, _grpRegression, "Kreiranje korisnika", "REST", 0),
            new(_scenarioDeleteUser, _grpRegression, "Brisanje korisnika",  "REST", 1),
            new(_scenarioFormValidation, _grpRegression, "Validacija forme", "UI", 2) { RunSequentially = true },
            // Regresija - API (podgrupa)
            new(_scenarioUsersPaging, _grpRegApi, "GET /users paginacija", "REST", 0),
            new(_scenarioUsersBadRequest, _grpRegApi, "POST /users vraća 400", "REST", 1),
            // Full Suite
            new(_scenarioCheckout, _grpFullSuite, "End-to-end checkout", "UI", 0),
        ];

        _runs =
        [
            (_grpSmoke,      now.AddHours(-3),  92.0),  // Success (≥80)
            (_grpRegression, now.AddHours(-6),  68.0),  // Warning (≥50)
            (_grpRegApi,     now.AddHours(-8),  45.0),  // Error   (<50)
            // Full Suite: namjerno bez run-a → null-state ("—")
        ];

        _schedules =
        [
            (_grpSmoke,      true),   // aktivan → ActiveScheduleCount = 1
            (_grpFullSuite,  false),  // neaktivan → ne broji se
        ];
    }

    // ── Čitanje ───────────────────────────────────────────────────────────────

    public Task<IReadOnlyList<GroupTreeNodeDto>> GetGroupsTreeAsync(CancellationToken ct = default)
    {
        lock (_lock)
        {
            // Sažeci u JEDNOM prolazu — bez N+1 poziva po grupi.
            var scenarioCounts = _scenariji
                .GroupBy(s => s.GroupId)
                .ToDictionary(g => g.Key, g => g.Count());

            var lastRuns = _runs
                .GroupBy(r => r.GroupId)
                .ToDictionary(g => g.Key, g => g.OrderByDescending(r => r.At).First());

            var activeScheduleCounts = _schedules
                .Where(s => s.IsActive)
                .GroupBy(s => s.GroupId)
                .ToDictionary(g => g.Key, g => g.Count());

            var summaries = _groups.ToDictionary(
                g => g.Id,
                g =>
                {
                    DateTime? lastAt = null;
                    double? lastRate = null;
                    if (lastRuns.TryGetValue(g.Id, out var run))
                    {
                        lastAt = run.At;
                        lastRate = run.PassRate;
                    }

                    return new GroupSummaryDto(
                        ScenarioCount:       scenarioCounts.GetValueOrDefault(g.Id),
                        LastRunAt:           lastAt,
                        LastPassRate:        lastRate,
                        ActiveScheduleCount: activeScheduleCounts.GetValueOrDefault(g.Id));
                });

            return Task.FromResult(GroupTreeBuilder.Build(_groups, summaries));
        }
    }

    public Task<GroupDto?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        lock (_lock)
        {
            return Task.FromResult(_groups.FirstOrDefault(g => g.Id == id));
        }
    }

    public Task<IReadOnlyList<GroupDto>> GetRootGroupsAsync(CancellationToken ct = default)
    {
        lock (_lock)
        {
            IReadOnlyList<GroupDto> roots = _groups
                .Where(g => g.ParentGroupId is null)
                .OrderByDescending(g => g.Prioritet)
                .ThenBy(g => g.Naziv, StringComparer.OrdinalIgnoreCase)
                .ToList();
            return Task.FromResult(roots);
        }
    }

    public async Task<IReadOnlyList<ScenarioListItemDto>> GetScenariosAsync(Guid groupId, CancellationToken ct = default)
    {
        List<ScenarioListItemDto> assigned;
        lock (_lock)
        {
            assigned = _scenariji
                .Where(s => s.GroupId == groupId)
                .OrderBy(s => s.Redoslijed)
                .ToList();
        }

        var result = new List<ScenarioListItemDto>(assigned.Count);
        foreach (var item in assigned)
        {
            var latest = await _scenarioSvc.GetByIdAsync(item.Id, ct);
            result.Add(latest is null
                ? item
                : item with
                {
                    Naziv = latest.Naziv,
                    Tip = latest.Tip.ToString(),
                    RunSequentially = latest.RunSequentially,
                });
        }

        return result;
    }

    // ── Mutacije grupa ──────────────────────────────────────────────────────

    public Task<Guid> CreateAsync(CreateGroupRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            // Depth guard — ≤2 nivoa: parent ne smije sam imati parenta.
            if (r.ParentGroupId is Guid parentId)
            {
                var parent = _groups.FirstOrDefault(g => g.Id == parentId)
                    ?? throw new InvalidOperationException("Nadređena grupa ne postoji.");

                if (parent.ParentGroupId is not null)
                    throw new InvalidOperationException("Maksimalna dubina grupa je 2 nivoa.");
            }

            var dto = new GroupDto(
                Id:            Guid.NewGuid(),
                Naziv:         r.Naziv,
                Opis:          r.Opis,
                Boja:          r.Boja,
                Tag:           r.Tag,
                Prioritet:     r.Prioritet,
                ParentGroupId: r.ParentGroupId,
                KreiranOd:     actorId,
                KreiranAt:     DateTime.UtcNow,
                IzmjenjenOd:   null,
                IzmjenjenAt:   null);

            _groups.Add(dto);
            return Task.FromResult(dto.Id);
        }
    }

    public Task UpdateAsync(Guid id, UpdateGroupRequest r, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var idx = _groups.FindIndex(g => g.Id == id);
            if (idx < 0)
                throw new InvalidOperationException($"Grupa s ID {id} ne postoji.");

            _groups[idx] = _groups[idx] with
            {
                Naziv       = r.Naziv,
                Opis        = r.Opis,
                Boja        = r.Boja,
                Tag         = r.Tag,
                Prioritet   = r.Prioritet,
                IzmjenjenOd = actorId,
                IzmjenjenAt = DateTime.UtcNow,
            };

            return Task.CompletedTask;
        }
    }

    public Task DeleteAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var idx = _groups.FindIndex(g => g.Id == id);
            if (idx < 0)
                throw new InvalidOperationException($"Grupa s ID {id} ne postoji.");

            if (_groups.Any(g => g.ParentGroupId == id))
                throw new InvalidOperationException(
                    "Grupa ima podgrupe. Prvo obrišite ili premjestite podgrupe.");

            _groups.RemoveAt(idx);
            // Kaskadno uklanjanje vezanih zapisa.
            _scenariji.RemoveAll(s => s.GroupId == id);
            _runs.RemoveAll(r => r.GroupId == id);
            _schedules.RemoveAll(s => s.GroupId == id);

            return Task.CompletedTask;
        }
    }

    // ── Scenariji unutar grupe ────────────────────────────────────────────────

    public Task ReorderScenariosAsync(Guid groupId, IReadOnlyList<Guid> orderedIds, CancellationToken ct = default)
    {
        lock (_lock)
        {
            for (var i = 0; i < orderedIds.Count; i++)
            {
                var idx = _scenariji.FindIndex(s => s.Id == orderedIds[i] && s.GroupId == groupId);
                if (idx >= 0)
                    _scenariji[idx] = _scenariji[idx] with { Redoslijed = i };
            }

            return Task.CompletedTask;
        }
    }

    public Task<ScenarioListItemDto> CopyScenarioAsync(Guid scenarioId, Guid targetGroupId, string actorId, string actorName, CancellationToken ct = default)
    {
        lock (_lock)
        {
            var source = _scenariji.FirstOrDefault(s => s.Id == scenarioId)
                ?? throw new InvalidOperationException("Scenarij za kopiranje ne postoji.");

            if (_groups.All(g => g.Id != targetGroupId))
                throw new InvalidOperationException("Ciljna grupa ne postoji.");

            var sourceBaseName = NormalizeScenarioName(source.Naziv);
            if (_scenariji.Any(s => s.GroupId == targetGroupId &&
                                    NormalizeScenarioName(s.Naziv).Equals(sourceBaseName, StringComparison.OrdinalIgnoreCase)))
            {
                throw new InvalidOperationException("Scenarij je vec dodijeljen odabranoj grupi.");
            }

            var maxOrder = _scenariji
                .Where(s => s.GroupId == targetGroupId)
                .Select(s => (int?)s.Redoslijed)
                .Max() ?? -1;

            var copy = source with
            {
                Id         = Guid.NewGuid(),
                GroupId    = targetGroupId,
                Naziv      = $"{source.Naziv} (kopija)",
                Redoslijed = maxOrder + 1,
            };

            _scenariji.Add(copy);
            return Task.FromResult(copy);
        }
    }

    private static string NormalizeScenarioName(string naziv)
    {
        var normalized = naziv.Trim();
        const string copySuffix = " (kopija)";

        while (normalized.EndsWith(copySuffix, StringComparison.OrdinalIgnoreCase))
            normalized = normalized[..^copySuffix.Length].TrimEnd();

        return normalized;
    }

    // ── Rasporedi (stub — engine izvršavanja dolazi u Sprint 3) ────────────────

    public Task SetScheduleActiveAsync(Guid groupId, bool isActive, CancellationToken ct = default)
    {
        lock (_lock)
        {
            for (var i = 0; i < _schedules.Count; i++)
            {
                if (_schedules[i].GroupId == groupId)
                    _schedules[i] = (groupId, isActive);
            }

            return Task.CompletedTask;
        }
    }

    private readonly Dictionary<Guid, NotificationConfig> _notifConfigs = new();

    public Task<NotificationConfig?> GetNotificationConfigAsync(Guid groupId, CancellationToken ct = default)
    {
        lock (_lock)
        {
            _notifConfigs.TryGetValue(groupId, out var cfg);
            return Task.FromResult(cfg);
        }
    }

    public Task SaveNotificationConfigAsync(Guid groupId, NotificationConfig config, CancellationToken ct = default)
    {
        lock (_lock)
        {
            _notifConfigs[groupId] = config;
            return Task.CompletedTask;
        }
    }
}
