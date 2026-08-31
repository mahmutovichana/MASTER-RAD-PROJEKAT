namespace RBBH.CollateralAppraisal.Application.Common.Interfaces;

/// <summary>
/// Distribuirani lock za background job koordinaciju između više instanci servisa.
/// SQL Server implementacija koristi pg_try_advisory_lock (session-level).
/// Mora biti Scoped — lock je vezan za DB konekciju iz istog scope-a.
/// </summary>
public interface IDistributedJobLock
{
    /// <summary>Pokušaj zauzeti lock; vraća false ako ga drži drugi čvor.</summary>
    Task<bool> TryAcquireAsync(long lockKey, CancellationToken ct = default);

    /// <summary>Oslobodi lock eksplicitno (ne čekaj zatvaranje konekcije).</summary>
    Task ReleaseAsync(long lockKey, CancellationToken ct = default);
}
