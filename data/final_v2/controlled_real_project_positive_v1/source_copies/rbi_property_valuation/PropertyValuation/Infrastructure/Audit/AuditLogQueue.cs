using System.Threading.Channels;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// In-memory bounded queue (System.Threading.Channels) — singleton, dijeli se kroz
/// cijelu aplikaciju. Kapacitet je velik (10000) jer je drain (AuditLogQueueWorker)
/// brz; ako se ikad napuni (npr. baza nedostupna duže vrijeme), najstariji neobrađeni
/// zapisi se odbacuju (DropOldest) — namjerno: pisanje audit zapisa NIKAD ne smije
/// blokirati niti baciti grešku pozivaocu (download/upload mora proći).
///
/// NAPOMENA: ovo je in-memory red — nije durable kroz restart/crash procesa. Za potpunu
/// durability (garantovano nula gubitka i kod pada procesa) bila bi potrebna prava
/// poruka-broker/outbox tabela — vidi README/izvještaj za preporuku.
/// </summary>
public sealed class AuditLogQueue : IAuditLogQueue
{
    private readonly Channel<AuditLog> _channel;
    private readonly ILogger<AuditLogQueue> _logger;

    public AuditLogQueue(ILogger<AuditLogQueue> logger)
    {
        _logger = logger;
        _channel = Channel.CreateBounded<AuditLog>(new BoundedChannelOptions(10_000)
        {
            FullMode     = BoundedChannelFullMode.DropOldest,
            SingleReader = true,
            SingleWriter = false
        });
    }

    public ChannelReader<AuditLog> Reader => _channel.Reader;

    public ValueTask EnqueueAsync(AuditLog log, CancellationToken ct = default)
    {
        if (!_channel.Writer.TryWrite(log))
            _logger.LogWarning("Audit queue je pun — zapis za akciju {Action} je odbačen.", log.Action);

        return ValueTask.CompletedTask;
    }
}
