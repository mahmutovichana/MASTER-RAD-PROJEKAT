namespace RBBH.CollateralAppraisal.Application.Common.Interfaces;

/// <summary>
/// Apstrakcija za distribuirani rate limiter.
/// Podrazumijevana implementacija je in-memory (per-process) — pogodna za single-instance deploy.
/// Za multi-instance deploy (load balancer, Kubernetes) zamijeniti sa RedisDistributedRateLimiter
/// koji koristi StackExchange.Redis i AtomicIncr/EXPIRE per window.
/// </summary>
public interface IDistributedRateLimiter
{
    /// <summary>
    /// Vraća true ako je zahtjev dozvoljen (unutar limite), false ako je prekoračen.
    /// </summary>
    /// <param name="key">Unikatan ključ za korisnika/akciju (npr. "userId:uploadDocument")</param>
    /// <param name="maxRequests">Maksimalan broj zahtjeva u prozoru</param>
    /// <param name="window">Vremenski prozor</param>
    bool IsAllowed(string key, int maxRequests, TimeSpan window);
}
