using RBBH.CollateralAppraisal.Application.Opinions.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Opinions;

/// <summary>
/// Servis za upravljanje mišljenjima CO i Pravne službe (US 94).
/// </summary>
public interface IOpinionService
{
    /// <summary>AM/SM/UB šalje zahtjev — kreira Opinion redove za CO i Pravnu.</summary>
    Task RequestOpinionsAsync(int appraisalOrderId, CancellationToken ct = default);

    /// <summary>CO ili Pravna importuju PDF mišljenja sa komentarom.</summary>
    Task SubmitOpinionAsync(int appraisalOrderId, OpinionType opinionType, Stream fileStream,
        string fileName, string? contentType, string? comment, string userId,
        CancellationToken ct = default);

    /// <summary>Vraća status mišljenja za UI.</summary>
    Task<List<OpinionDto>> GetOpinionsAsync(int appraisalOrderId, CancellationToken ct = default);
}