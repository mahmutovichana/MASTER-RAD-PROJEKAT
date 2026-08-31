using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Roles.Models;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Audit;

public sealed class AuditQueryService : IAuditQueryService
{
    private readonly ApplicationDbContext _db;

    public AuditQueryService(ApplicationDbContext db) => _db = db;

    public async Task<PagedResult<AuditLogDto>> QueryAsync(
        AuditQueryRequest request, CancellationToken ct = default)
    {
        var query = _db.AuditLogs.AsNoTracking().AsQueryable();

        // ── Točni filteri (indeksirani stupci) ────────────────────────────────
        if (!string.IsNullOrWhiteSpace(request.ActorUserId))
            query = query.Where(a => a.ActorUserId == request.ActorUserId);

        if (!string.IsNullOrWhiteSpace(request.ActorUsername))
            query = query.Where(a => a.ActorUsername.Contains(request.ActorUsername));

        if (!string.IsNullOrWhiteSpace(request.ActorRole))
            query = query.Where(a =>
                a.ActiveRole == request.ActorRole || a.ActorRole == request.ActorRole);

        if (!string.IsNullOrWhiteSpace(request.Module))
            query = query.Where(a => a.Module == request.Module);

        if (!string.IsNullOrWhiteSpace(request.Action))
            query = query.Where(a => a.Action == request.Action);

        if (!string.IsNullOrWhiteSpace(request.EntityType))
            query = query.Where(a => a.EntityType == request.EntityType);

        if (!string.IsNullOrWhiteSpace(request.EntityKey))
            query = query.Where(a => a.EntityKey == request.EntityKey);

        if (!string.IsNullOrWhiteSpace(request.Status))
            query = query.Where(a => a.Status == request.Status);

        if (!string.IsNullOrWhiteSpace(request.Severity))
            query = query.Where(a => a.Severity == request.Severity);

        // ── Datum ─────────────────────────────────────────────────────────────
        if (request.From.HasValue)
            query = query.Where(a => a.TimestampUtc >= request.From.Value);

        if (request.To.HasValue)
            query = query.Where(a => a.TimestampUtc <= request.To.Value);

        // ── Globalna pretraga (full-text po ključnim tekstualnim poljima) ──────
        if (!string.IsNullOrWhiteSpace(request.Search))
        {
            var s = request.Search.Trim().ToLower();
            query = query.Where(a =>
                a.Action.ToLower().Contains(s)              ||
                a.ActorUsername.ToLower().Contains(s)       ||
                (a.EntityDisplayName != null && a.EntityDisplayName.ToLower().Contains(s)) ||
                (a.Reason            != null && a.Reason.ToLower().Contains(s))            ||
                (a.EntityKey         != null && a.EntityKey.ToLower().Contains(s))         ||
                (a.CorrelationId     != null && a.CorrelationId.ToLower().Contains(s)));
        }

        var total = await query.CountAsync(ct);
        var page  = Math.Max(1, request.Page);
        var size  = Math.Clamp(request.PageSize, 1, 200);

        var items = await query
            .OrderByDescending(a => a.TimestampUtc)
            .Skip((page - 1) * size)
            .Take(size)
            .Select(a => new AuditLogDto(
                a.Id, a.TimestampUtc,
                a.ActorUserId, a.ActorUsername, a.ActorEmail, a.ActorFullName, a.ActorRole, a.ActiveRole,
                a.Action, a.OperationType, a.Module,
                a.EntityType, a.EntityKey, a.EntityDisplayName,
                a.OldValuesJson, a.NewValuesJson, a.ChangedFieldsJson,
                a.Status, a.Severity, a.Reason,
                a.CorrelationId, a.RequestPath,
                a.IpAddress, a.UserAgent))
            .ToListAsync(ct);

        return new PagedResult<AuditLogDto>
        {
            Items      = items,
            TotalCount = total,
            Page       = page,
            PageSize   = size
        };
    }
}
