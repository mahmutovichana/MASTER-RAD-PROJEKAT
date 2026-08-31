using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Orders.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Orders;

/// <summary>
/// Generira jedinstven broj narudžbe formata PN-{year}-{seq:D6}.
/// Format PN (Protokol Narudžbe) usklađen sa specifikacijom i Excel tabletom.
///
/// Koristi SQL Server MERGE uz HOLDLOCK i OUTPUT radi atomarnog brojača.
/// </summary>
public sealed class OrderNumberGenerator : IOrderNumberGenerator
{
    private readonly ApplicationDbContext _db;

    public OrderNumberGenerator(ApplicationDbContext db) => _db = db;

    public async Task<string> GenerateAsync(CancellationToken ct = default)
    {
        var year = DateTime.UtcNow.Year;

        var sequences = await _db.Database
            .SqlQuery<int>($"""
                MERGE order_number_year_counters WITH (HOLDLOCK) AS target
                USING (SELECT {year} AS [year]) AS source
                ON target.[year] = source.[year]
                WHEN MATCHED THEN UPDATE SET last_sequence = target.last_sequence + 1
                WHEN NOT MATCHED THEN INSERT ([year], last_sequence) VALUES (source.[year], 1)
                OUTPUT inserted.last_sequence;
                """)
            .ToListAsync(ct);

        return $"PN-{year}-{sequences[0]:D6}";
    }
}
