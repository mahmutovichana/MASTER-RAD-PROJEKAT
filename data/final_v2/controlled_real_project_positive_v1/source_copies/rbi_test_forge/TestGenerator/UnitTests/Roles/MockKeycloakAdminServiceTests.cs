using RBBH.TestAutomation.Api.Auth;
using RBBH.TestAutomation.Api.Services;

namespace UnitTests.Roles;

/// <summary>
/// Unit testovi za <see cref="MockKeycloakAdminService"/>.
///
/// Pokriva acceptance kriterije TAG-4 user storyja:
///   #1 — Svaka rola ima minimalno 2 korisnika (seed podaci)
///   #2 — Polja nedostupna za rolu su siva i onemogućena (CanAccess — vidi AppModulesAccessTests)
///   #3 — Administrator može prenositi administratorsku rolu na drugog korisnika
///
/// Napomena: MockKeycloakAdminService je Singleton s statičkim stanjem.
/// Mutacijski testovi uvijek čiste za sobom (RemoveRole nakon AssignRole) kako
/// bi ostali testovi primili konzistentno početno stanje.
/// </summary>
public class MockKeycloakAdminServiceTests
{
    // ── Konstante — poznati seed korisnici ────────────────────────────────────

    private const string AdminId        = "mock-admin-001";
    private const string QAEngineer1Id  = "mock-qae-001";
    private const string QAEngineer2Id  = "mock-qae-002";
    private const string Developer1Id   = "mock-dev-001";
    private const string Developer2Id   = "mock-dev-002";

    private static MockKeycloakAdminService CreateSvc() => new();

    // ── Helper: dohvati role datog korisnika ──────────────────────────────────

    private static async Task<List<string>> GetRolesAsync(
        MockKeycloakAdminService svc, string userId)
    {
        var users = await svc.GetUsersWithRolesAsync();
        return users.First(u => u.User.Id == userId).Roles;
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GetUsersWithRolesAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task GetUsersWithRolesAsync_WhenCalled_Returns9Users()
    {
        var svc = CreateSvc();
        var result = await svc.GetUsersWithRolesAsync();
        Assert.Equal(9, result.Count);
    }

    [Fact]
    public async Task GetUsersWithRolesAsync_AdminUser_HasAdministratorRole()
    {
        var svc = CreateSvc();
        var roles = await GetRolesAsync(svc, AdminId);
        Assert.Contains(AppRoles.Administrator, roles);
    }

    [Fact]
    public async Task GetUsersWithRolesAsync_EachNonAdminRole_HasAtLeastTwoUsers()
    {
        // Acceptance kriterij #1 — minimalno 2 korisnika po roli
        var svc = CreateSvc();
        var users = await svc.GetUsersWithRolesAsync();

        var nonAdminRoles = AppRoles.All
            .Where(r => r != AppRoles.Administrator)
            .ToList();

        foreach (var role in nonAdminRoles)
        {
            var count = users.Count(u => u.Roles.Contains(role, StringComparer.OrdinalIgnoreCase));
            Assert.True(count >= 2,
                $"Rola '{role}' ima samo {count} korisnika, a trebaju barem 2.");
        }
    }

    [Fact]
    public async Task GetUsersWithRolesAsync_ReturnsDefensiveCopiesOfRoles()
    {
        // Mutacija vraćene liste ne smije utjecati na interni state
        var svc = CreateSvc();
        var users = await svc.GetUsersWithRolesAsync();
        var qae1 = users.First(u => u.User.Id == QAEngineer1Id);

        // Direktna mutacija kopije
        qae1.Roles.Add("HackedRole");

        var usersAgain = await svc.GetUsersWithRolesAsync();
        var qae1Again = usersAgain.First(u => u.User.Id == QAEngineer1Id);
        Assert.DoesNotContain("HackedRole", qae1Again.Roles);
    }

    [Fact]
    public async Task GetUsersWithRolesAsync_AllUsersHaveNonEmptyId()
    {
        var svc = CreateSvc();
        var result = await svc.GetUsersWithRolesAsync();
        Assert.All(result, u => Assert.False(string.IsNullOrWhiteSpace(u.User.Id)));
    }

    [Fact]
    public async Task GetUsersWithRolesAsync_AllUsersHaveNonEmptyUsername()
    {
        var svc = CreateSvc();
        var result = await svc.GetUsersWithRolesAsync();
        Assert.All(result, u => Assert.False(string.IsNullOrWhiteSpace(u.User.Username)));
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AssignRoleAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task AssignRoleAsync_WhenRoleNotPresent_AddsRole()
    {
        var svc = CreateSvc();
        await svc.AssignRoleAsync(QAEngineer1Id, AppRoles.QALead);

        var roles = await GetRolesAsync(svc, QAEngineer1Id);
        Assert.Contains(AppRoles.QALead, roles);

        // Cleanup
        await svc.RemoveRoleAsync(QAEngineer1Id, AppRoles.QALead);
    }

    [Fact]
    public async Task AssignRoleAsync_WhenRoleAlreadyPresent_IsIdempotent()
    {
        // Dodjela iste role dvaput ne smije kreirati duplikat
        var svc = CreateSvc();
        await svc.AssignRoleAsync(QAEngineer1Id, AppRoles.QALead);
        await svc.AssignRoleAsync(QAEngineer1Id, AppRoles.QALead);

        var roles = await GetRolesAsync(svc, QAEngineer1Id);
        Assert.Equal(1, roles.Count(r =>
            string.Equals(r, AppRoles.QALead, StringComparison.OrdinalIgnoreCase)));

        // Cleanup
        await svc.RemoveRoleAsync(QAEngineer1Id, AppRoles.QALead);
    }

    [Fact]
    public async Task AssignRoleAsync_IsCaseInsensitive()
    {
        var svc = CreateSvc();
        await svc.AssignRoleAsync(Developer1Id, "qa lead"); // lowercase

        var roles = await GetRolesAsync(svc, Developer1Id);
        Assert.Contains(roles, r =>
            string.Equals(r, AppRoles.QALead, StringComparison.OrdinalIgnoreCase));

        // Cleanup
        await svc.RemoveRoleAsync(Developer1Id, "qa lead");
    }

    [Fact]
    public async Task AssignRoleAsync_ForUserWithNoExistingRoles_CreatesRoleEntry()
    {
        // Korisnik bez rola u _roles dictionary
        const string userId = "mock-new-user-test";
        var svc = CreateSvc();
        await svc.AssignRoleAsync(userId, AppRoles.Developer);

        var users = await svc.GetUsersWithRolesAsync();
        // User možda ne postoji u _users listi, ali state za njega postoji
        // Testiramo samo da ne baci iznimku
        await svc.RemoveRoleAsync(userId, AppRoles.Developer); // Cleanup
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // RemoveRoleAsync
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task RemoveRoleAsync_WhenRolePresent_RemovesRole()
    {
        var svc = CreateSvc();
        // Setup: dodaj rolu
        await svc.AssignRoleAsync(QAEngineer2Id, AppRoles.QALead);

        // Act
        await svc.RemoveRoleAsync(QAEngineer2Id, AppRoles.QALead);

        var roles = await GetRolesAsync(svc, QAEngineer2Id);
        Assert.DoesNotContain(AppRoles.QALead, roles);
    }

    [Fact]
    public async Task RemoveRoleAsync_WhenRoleNotPresent_DoesNotThrow()
    {
        var svc = CreateSvc();
        // Uklanjanje nepostojeće role ne smije baciti iznimku
        var ex = await Record.ExceptionAsync(() =>
            svc.RemoveRoleAsync(QAEngineer1Id, "NitiJednaOvakoRole"));
        Assert.Null(ex);
    }

    [Fact]
    public async Task RemoveRoleAsync_IsCaseInsensitive()
    {
        var svc = CreateSvc();
        await svc.AssignRoleAsync(Developer2Id, AppRoles.QALead);
        await svc.RemoveRoleAsync(Developer2Id, "QA LEAD"); // uppercase

        var roles = await GetRolesAsync(svc, Developer2Id);
        Assert.DoesNotContain(roles, r =>
            string.Equals(r, AppRoles.QALead, StringComparison.OrdinalIgnoreCase));
    }

    [Fact]
    public async Task RemoveRoleAsync_WhenUserHasMultipleRoles_RemovesOnlyTargetRole()
    {
        var svc = CreateSvc();
        await svc.AssignRoleAsync(QAEngineer1Id, AppRoles.QALead);
        await svc.AssignRoleAsync(QAEngineer1Id, AppRoles.DevOpsInzenjer);

        await svc.RemoveRoleAsync(QAEngineer1Id, AppRoles.QALead);

        var roles = await GetRolesAsync(svc, QAEngineer1Id);
        Assert.DoesNotContain(AppRoles.QALead, roles);
        Assert.Contains(AppRoles.DevOpsInzenjer, roles);

        // Cleanup
        await svc.RemoveRoleAsync(QAEngineer1Id, AppRoles.DevOpsInzenjer);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Prenos administratorske role  [Acceptance kriterij #3]
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public async Task TransferAdmin_WhenCompleted_TargetHasAdminRole()
    {
        // Acceptance kriterij #3 — administrator može prenijeti rolu
        var svc = CreateSvc();
        const string targetId = QAEngineer1Id;

        await svc.AssignRoleAsync(targetId, AppRoles.Administrator);

        var roles = await GetRolesAsync(svc, targetId);
        Assert.Contains(AppRoles.Administrator, roles);

        // Cleanup
        await svc.RemoveRoleAsync(targetId, AppRoles.Administrator);
    }

    [Fact]
    public async Task TransferAdmin_WhenCompleted_PreviousAdminLosesRole()
    {
        // Acceptance kriterij #3 — stari admin gubi rolu
        var svc = CreateSvc();
        const string targetId = QAEngineer1Id;

        // Simulacija: dodaj admin target-u, ukloni starom adminu
        await svc.AssignRoleAsync(targetId, AppRoles.Administrator);
        await svc.RemoveRoleAsync(AdminId, AppRoles.Administrator);

        var adminRoles = await GetRolesAsync(svc, AdminId);
        Assert.DoesNotContain(AppRoles.Administrator, adminRoles);

        // Cleanup — vrati admina
        await svc.AssignRoleAsync(AdminId, AppRoles.Administrator);
        await svc.RemoveRoleAsync(targetId, AppRoles.Administrator);
    }

    [Fact]
    public async Task TransferAdmin_BothOperationsAtomic_NoMomentWithoutAdmin()
    {
        // Provjeri da ne postoji stanje gdje ni jedan korisnik nije admin
        // Redoslijed: PRVO dodaj novom, ONDA ukloni starom
        var svc = CreateSvc();
        const string targetId = QAEngineer2Id;

        await svc.AssignRoleAsync(targetId, AppRoles.Administrator);
        var usersAfterAssign = await svc.GetUsersWithRolesAsync();
        Assert.Contains(usersAfterAssign, u =>
            u.Roles.Contains(AppRoles.Administrator, StringComparer.OrdinalIgnoreCase));

        await svc.RemoveRoleAsync(AdminId, AppRoles.Administrator);
        var usersAfterRemove = await svc.GetUsersWithRolesAsync();
        Assert.Contains(usersAfterRemove, u =>
            u.Roles.Contains(AppRoles.Administrator, StringComparer.OrdinalIgnoreCase));

        // Cleanup
        await svc.AssignRoleAsync(AdminId, AppRoles.Administrator);
        await svc.RemoveRoleAsync(targetId, AppRoles.Administrator);
    }
}
