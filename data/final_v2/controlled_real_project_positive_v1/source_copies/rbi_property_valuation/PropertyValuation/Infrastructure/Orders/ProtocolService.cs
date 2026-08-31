using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

public sealed class ProtocolService : IProtocolService
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService _currentUser;

    public ProtocolService(ApplicationDbContext db, ICurrentUserService currentUser)
    {
        _db = db;
        _currentUser = currentUser;
    }

    public async Task<OrderProtocolEntry> CreateProtocolForOrderAsync(int orderId, CancellationToken ct = default)
    {
        var order = await _db.AppraisalOrders.FindAsync([orderId], ct)
            ?? throw new NotFoundException($"Narudžba s ID-om {orderId} nije pronađena.");

        // Ako protokolni unos već postoji za ovu narudžbu, vrati ga bez kreiranja duplikata.
        var existing = await _db.OrderProtocolEntries
            .AsNoTracking()
            .FirstOrDefaultAsync(p => p.OrderId == orderId, ct);
        if (existing is not null)
            return existing;

        var now  = DateTime.UtcNow;
        var year = now.Year;

        // SQL Server atomarni brojač uz HOLDLOCK sprečava duplikate.
        var sequences = await _db.Database
            .SqlQuery<int>($"""
                MERGE protocol_year_counters WITH (HOLDLOCK) AS target
                USING (SELECT {year} AS [year]) AS source
                ON target.[year] = source.[year]
                WHEN MATCHED THEN UPDATE SET last_sequence = target.last_sequence + 1
                WHEN NOT MATCHED THEN INSERT ([year], last_sequence) VALUES (source.[year], 1)
                OUTPUT inserted.last_sequence;
                """)
            .ToListAsync(ct);

        var sequence = sequences[0];

        var protocol = OrderProtocolEntry.Create(
            order.Id,
            year,
            sequence,
            _currentUser.UserId ?? "unknown",
            now);

        _db.OrderProtocolEntries.Add(protocol);
        await _db.SaveChangesAsync(ct);
        return protocol;
    }

    public async Task<ProtocolEntryDto> GetByOrderIdAsync(int orderId, CancellationToken ct = default)
    {
        var entry = await _db.OrderProtocolEntries
            .Include(p => p.Order)
            .FirstOrDefaultAsync(p => p.OrderId == orderId, ct)
            ?? throw new NotFoundException($"Protokolni unos za narudžbu {orderId} nije pronađen.");

        var context = await BuildMappingContextAsync([entry], ct);
        return MapToDto(entry, context);
    }

    public async Task<PagedResult<ProtocolEntryDto>> GetProtocolListAsync(
        int page = 1, int pageSize = 20, CancellationToken ct = default)
    {
        var query = _db.OrderProtocolEntries
            .Include(p => p.Order)
            .OrderByDescending(p => p.GeneratedAt);

        var total   = await query.CountAsync(ct);
        var entries = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);

        var context = await BuildMappingContextAsync(entries, ct);

        return new PagedResult<ProtocolEntryDto>
        {
            Items      = entries.Select(e => MapToDto(e, context)).ToList(),
            TotalCount = total,
            Page       = page,
            PageSize   = pageSize
        };
    }

    private async Task<MappingContext> BuildMappingContextAsync(
        IReadOnlyList<Domain.Orders.OrderProtocolEntry> entries, CancellationToken ct)
    {
        var orderIds = entries.Select(e => e.OrderId).Distinct().ToList();

        var collateralLabels = await GetCollateralLabelsAsync(entries, ct);

        var coComments = await _db.TaskItems
            .AsNoTracking()
            .Where(t => orderIds.Contains(t.AppraisalOrderId)
                     && t.TaskType == Domain.Orders.TaskItemType.ApproveFinalAppraisal
                     && t.Status == Domain.Orders.TaskItemStatus.Completed)
            .GroupBy(t => t.AppraisalOrderId)
            .Select(g => new { OrderId = g.Key, Comment = g.OrderByDescending(t => t.CompletedAt).First().Comment })
            .ToDictionaryAsync(x => x.OrderId, x => x.Comment, ct);

        var appraiserIds = entries
            .Where(e => e.Order?.AppraiserId.HasValue == true)
            .Select(e => e.Order!.AppraiserId!.Value)
            .Distinct()
            .ToList();

        var appraiserNames = appraiserIds.Count == 0
            ? new Dictionary<int, string>()
            : await _db.Appraisers
                .AsNoTracking()
                .Where(a => appraiserIds.Contains(a.Id))
                .ToDictionaryAsync(a => a.Id, a => a.Name, ct);

        return new MappingContext(collateralLabels, coComments, appraiserNames);
    }

    private async Task<Dictionary<int, string>> GetCollateralLabelsAsync(
        IEnumerable<Domain.Orders.OrderProtocolEntry> entries, CancellationToken ct)
    {
        var typeIds = entries
            .SelectMany(e => new[] { e.Order?.CollateralTypeId, e.Order?.CombinedCollateralTypeId })
            .Where(id => id.HasValue)
            .Select(id => id!.Value)
            .Distinct()
            .ToList();

        return typeIds.Count == 0
            ? new Dictionary<int, string>()
            : await _db.CodebookValues
                .Where(v => typeIds.Contains(v.Id))
                .ToDictionaryAsync(v => v.Id, v => v.Label, ct);
    }

    private static ProtocolEntryDto MapToDto(Domain.Orders.OrderProtocolEntry p, MappingContext ctx)
    {
        var coComment = ctx.CoComments.GetValueOrDefault(p.OrderId);
        var appraiserName = p.Order?.AppraiserId is int aid ? ctx.AppraiserNames.GetValueOrDefault(aid) : null;

        return new(
            p.Id,
            p.OrderId,
            p.Order?.OrderNumber ?? string.Empty,
            p.Order?.Title       ?? string.Empty,
            p.ProtocolNumber,
            p.ProtocolYear,
            p.ProtocolSequence,
            p.Status.ToString(),
            p.GeneratedAt,
            p.GeneratedByUserId,
            p.Order?.ClientName ?? string.Empty,
            p.Order?.City,
            p.Order?.Branch,
            p.Order?.Status.ToString() ?? string.Empty,
            p.Order is not null ? (int)p.Order.Status : 0,
            p.Order?.CollateralTypeId.HasValue == true ? ctx.CollateralLabels.GetValueOrDefault(p.Order.CollateralTypeId!.Value) : null,
            p.Order?.CombinedCollateralTypeId.HasValue == true ? ctx.CollateralLabels.GetValueOrDefault(p.Order.CombinedCollateralTypeId!.Value) : null,
            p.Order?.ClientType,
            p.Order?.ClientIdentifier,
            p.Order?.ContactName,
            p.Order?.ContactPhone,
            p.Order?.PropertyAddress,
            p.Order?.BranchAddress,
            p.Order?.CreatedByName,
            p.Order?.CreatedByRole,
            p.Order?.DeliveryContactName,
            p.Order?.AmRecipientName,
            p.Order?.RequestReceivedAt,
            p.Order?.RequestSentAt,
            p.Order?.InvoiceSentDate,
            p.Order?.InvoiceReceivedDate,
            p.Order?.PaymentConsentStatus,
            coComment,
            appraiserName,
            p.Order?.AppraiserRating,
            p.Order?.EsgCertificate,
            p.Order?.AppraiserVisitDate,
            p.Order?.AppraisalFee,
            p.Order?.CollateralStatus,
            p.Order?.SubmittedAt,
            p.Order?.OrderSentToAppraiserAt,
            p.Order?.SignedDocumentsReceivedAt,
            p.Order?.DocumentationSupplementAt,
            p.Order?.CoApprovedAt,
            p.Order?.AppraisalDeliveredToCoAt,
            p.Order?.CorrectionRequestedAt,
            p.Order?.CorrectedAppraisalReceivedAt,
            p.Order?.ReadyForProcedureAt,
            p.Order?.OriginalReceivedAt,
            p.Order?.CoApprovedByUserId,
            p.Order?.AcceptedByCAName,
            p.Order?.DocumentationReviewStatus is { } drs
                ? DocumentationReviewStatusConverter.ToDbValue(drs)
                : null
        );
    }

    private sealed record MappingContext(
        Dictionary<int, string> CollateralLabels,
        Dictionary<int, string?> CoComments,
        Dictionary<int, string> AppraiserNames);
}
