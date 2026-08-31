using RBBH.CollateralAppraisal.Application.Reports.Dtos;

namespace RBBH.CollateralAppraisal.Application.Reports;

public interface IOrdersTimeReportService
{
    /// <summary>
    /// Vraća listu svih protokol narudžbi + 7 vremenskih kolona.
    /// <paramref name="endDate"/> filtrira narudžbe s datumom prijema ≤ endDate.
    /// </summary>
    Task<List<OrdersTimeReportRowDto>> GetReportAsync(DateTime? endDate = null, CancellationToken ct = default);

    /// <summary>
    /// Vraća Excel (.xlsx) izvještaj kao stream spreman za download.
    /// </summary>
    Task<(Stream Stream, string ContentType, string FileName)> GetReportXlsxAsync(DateTime? endDate = null, CancellationToken ct = default);
}
