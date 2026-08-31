using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Configurations;

/// <summary>
/// Mapira DocumentationReviewStatus enum na/od bosanskih naziva koji se čuvaju u bazi.
/// Ovo osigurava backward kompatibilnost s postojećim podacima u koloni documentation_review_status.
/// </summary>
internal static class DocumentationReviewStatusConverter
{
    public static string ToDbValue(DocumentationReviewStatus status) => status switch
    {
        DocumentationReviewStatus.NijePregledano => "Nije pregledano",
        DocumentationReviewStatus.UToku          => "U toku",
        DocumentationReviewStatus.Vraceno        => "Vraćeno",
        DocumentationReviewStatus.Odobreno       => "Odobreno",
        _                                        => throw new ArgumentOutOfRangeException(nameof(status), status, null)
    };

    public static DocumentationReviewStatus FromDbValue(string value) => value switch
    {
        "Nije pregledano" => DocumentationReviewStatus.NijePregledano,
        "U toku"          => DocumentationReviewStatus.UToku,
        "Vraćeno"         => DocumentationReviewStatus.Vraceno,
        "Odobreno"        => DocumentationReviewStatus.Odobreno,
        _                 => DocumentationReviewStatus.NijePregledano
    };
}
