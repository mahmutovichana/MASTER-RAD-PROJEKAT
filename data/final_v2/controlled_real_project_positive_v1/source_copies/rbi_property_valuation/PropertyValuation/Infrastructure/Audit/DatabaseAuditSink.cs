using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

/// <summary>
/// Sink koji čuva audit zapise u SQL Server bazi podataka.
/// Prima gotov AuditLog entitet — ne vrši nikakvu transformaciju.
/// </summary>
public sealed class DatabaseAuditSink : IAuditSink
{
    private readonly ApplicationDbContext _db;

    public DatabaseAuditSink(ApplicationDbContext db)
    {
        _db = db;
    }

    public async Task WriteAsync(AuditLog log, CancellationToken cancellationToken = default)
    {
        _db.AuditLogs.Add(log);
        await _db.SaveChangesAsync(cancellationToken);
    }
}
