namespace RBBH.TestAutomation.Api.DTO;

/// <summary>
/// Tip (kategorija) test grupe — određuje namjenu skupa testova.
/// </summary>
public enum TestTag
{
    /// <summary>Brzi "smoke" testovi — osnovna provjera da sistem uopće radi.</summary>
    Smoke,

    /// <summary>Regresijski testovi — provjera da nove izmjene nisu pokvarile postojeće.</summary>
    Regression,

    /// <summary>Puni skup — kompletna test suita.</summary>
    Full,
}

/// <summary>
/// Test grupa (suite). Može imati nadređenu grupu preko <see cref="ParentGroupId"/> —
/// hijerarhija je ograničena na ≤2 nivoa (root + jedan nivo podgrupa).
/// <c>KreiranOd</c>/<c>IzmjenjenOd</c> su Keycloak sub claim-ovi (UserId).
/// </summary>
public sealed record GroupDto(
    Guid Id,
    string Naziv,
    string? Opis,
    string? Boja,
    TestTag Tag,
    int Prioritet,
    Guid? ParentGroupId,
    string? KreiranOd,
    DateTime KreiranAt,
    string? IzmjenjenOd,
    DateTime? IzmjenjenAt
);

/// <summary>
/// Agregirani sažetak grupe za prikaz na kartici. Sve vrijednosti su pred-izračunate
/// u jednom prolazu (bez N+1 poziva po grupi).
/// <c>LastRunAt</c>/<c>LastPassRate</c> su null ako grupa nikad nije izvršena (null-state prikaz).
/// </summary>
public sealed record GroupSummaryDto(
    int ScenarioCount,
    DateTime? LastRunAt,
    double? LastPassRate,
    int ActiveScheduleCount
);

/// <summary>
/// Čvor stabla grupa — grupa + njen sažetak + podgrupe. Dubina ≤2 (podgrupe nemaju svoje podgrupe).
/// </summary>
public sealed record GroupTreeNodeDto(
    GroupDto Group,
    GroupSummaryDto Summary,
    IReadOnlyList<GroupTreeNodeDto> Children
);

/// <summary>
/// Stavka liste scenarija unutar grupe. <c>Redoslijed</c> definiše poredak koji drag&amp;drop mijenja.
/// </summary>
public sealed record ScenarioListItemDto(
    Guid Id,
    Guid GroupId,
    string Naziv,
    string Tip,
    int Redoslijed
)
{
    public bool RunSequentially { get; init; }
}

/// <summary>
/// Ulaz za kreiranje nove grupe. <c>ParentGroupId</c> = null za root grupu, ili ID roota za podgrupu.
/// </summary>
public sealed record CreateGroupRequest(
    string Naziv,
    string? Opis,
    string? Boja,
    TestTag Tag,
    int Prioritet,
    Guid? ParentGroupId
);

/// <summary>
/// Ulaz za izmjenu postojeće grupe. Hijerarhija (parent) se ne mijenja kroz ovaj zahtjev.
/// </summary>
public sealed record UpdateGroupRequest(
    string Naziv,
    string? Opis,
    string? Boja,
    TestTag Tag,
    int Prioritet
);

/// <summary>
/// Konstante za <c>entity_type</c> kolonu audit zapisa vezanih za grupe.
/// </summary>
public static class GroupAuditEntityTypes
{
    public const string Grupa = "test_grupa";
}
