using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Domain.Audit;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Audit sink koji pokušava primarni sink, a u slučaju greške automatski prelazi na sekundarni.
///
/// Pattern: DatabaseAuditSink (primarni) → FileAuditSink (fallback)
///
/// Ovo osigurava da audit zapisi nikad nisu potpuno izgubljeni čak i kada baza podataka
/// nije dostupna. Fajl-fallback zapisi mogu se naknadno uvesti u bazu kad se veza uspostavi.
/// </summary>
public sealed class FallbackAuditSink : IAuditSink
{
    private readonly DatabaseAuditSink              _primary;
    private readonly FileAuditSink                  _fallback;
    private readonly ILogger<FallbackAuditSink>     _logger;

    public FallbackAuditSink(
        DatabaseAuditSink          primary,
        FileAuditSink              fallback,
        ILogger<FallbackAuditSink> logger)
    {
        _primary  = primary;
        _fallback = fallback;
        _logger   = logger;
    }

    public async Task WriteAsync(AuditLog log, CancellationToken cancellationToken = default)
    {
        try
        {
            await _primary.WriteAsync(log, cancellationToken);
        }
        catch (Exception primaryEx)
        {
            _logger.LogError(primaryEx,
                "DatabaseAuditSink nije uspio za akciju {Action}. Aktiviran FileAuditSink fallback.",
                log.Action);

            // Fallback — ne smije propagirati grešku, samo logovati
            await _fallback.WriteAsync(log, cancellationToken);
        }
    }
}
