namespace RBBH.TestAutomation.Api.DTO;

public sealed record ScheduleConfigDto(
    Guid   Id,
    Guid   GroupId,
    string GroupNaziv,
    string CronExpression,
    bool   IsActive,
    string Timezone
);

public sealed record CreateScheduleRequest(
    Guid   GroupId,
    string CronExpression,
    string Timezone,
    bool   IsActive
);

public sealed record UpdateScheduleRequest(
    string CronExpression,
    string Timezone,
    bool   IsActive
);

/// <summary>
/// Rezultat dijaloga pri kreiranju — isti Cron raspored može biti dodijeljen
/// više grupa odjednom. Stranica kreira po jedan <see cref="CreateScheduleRequest"/>
/// za svaku grupu iz <see cref="GroupIds"/>.
/// </summary>
public sealed record ScheduleCreateDraft(
    IReadOnlyList<Guid> GroupIds,
    string              CronExpression,
    string              Timezone,
    bool                IsActive
);
