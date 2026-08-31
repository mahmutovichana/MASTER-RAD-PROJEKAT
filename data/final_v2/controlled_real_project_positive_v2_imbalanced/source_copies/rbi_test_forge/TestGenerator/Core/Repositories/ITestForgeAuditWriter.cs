namespace RBBH.TestAutomation.Core.Repositories;

/// <summary>
/// Apstrakcija za upis u dijeljenu <c>audit_log</c> tabelu. Implementacija je Dapper-om
/// u RBBH.TestAutomation.Api (<c>DapperTestForgeAuditWriter</c>) — <c>audit_log</c> ostaje u vlasništvu
/// Dapper sloja i NE mapira se kroz EF (vidi koordinacijski dokument: dvije schema vlasti,
/// jedna baza). TestForge repozitoriji/servisi audit-uju isključivo kroz ovaj interfejs.
/// </summary>
public interface ITestForgeAuditWriter
{
    /// <summary>
    /// Upisuje jedan audit zapis. Implementacija je <b>best-effort</b>: greška pri upisu
    /// se loguje, ali se ne propagira (EF write je u tom trenutku već commitan).
    /// </summary>
    /// <param name="entityType">Vidi <see cref="TestForgeAuditEntities"/>.</param>
    /// <param name="action">Vidi <see cref="TestForgeAuditActions"/>.</param>
    /// <param name="actorId">Keycloak <c>sub</c> korisnika (<c>changed_by</c>).</param>
    /// <param name="actorName">Display name korisnika (<c>changed_by_name</c>).</param>
    /// <param name="oldValues">Stanje prije promjene (serijalizuje se u <c>old_values</c> jsonb); null za CREATE.</param>
    /// <param name="newValues">Stanje nakon promjene (serijalizuje se u <c>new_values</c> jsonb); null za DELETE.</param>
    Task WriteAsync(
        string entityType,
        Guid entityId,
        string action,
        string actorId,
        string actorName,
        object? oldValues,
        object? newValues,
        CancellationToken ct = default);
}

/// <summary><c>entity_type</c> vrijednosti za TestForge entitete u <c>audit_log</c>.</summary>
public static class TestForgeAuditEntities
{
    public const string Group = "test_group";
    public const string Scenario = "test_scenario";
}

/// <summary>
/// <c>action</c> vrijednosti — moraju odgovarati CHECK constraint-u <c>audit_log</c> tabele
/// (<c>init.sql</c>: <c>action IN ('CREATE','UPDATE','DELETE')</c>).
/// </summary>
public static class TestForgeAuditActions
{
    public const string Create = "CREATE";
    public const string Update = "UPDATE";
    public const string Delete = "DELETE";
}
