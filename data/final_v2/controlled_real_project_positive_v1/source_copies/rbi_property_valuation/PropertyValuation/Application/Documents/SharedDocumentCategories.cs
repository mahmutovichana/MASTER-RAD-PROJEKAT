namespace RBBH.CollateralAppraisal.Application.Documents;

public static class SharedDocumentCategories
{
    public const string Cjenovnik     = "Cjenovnik";
    public const string Dokumentacija = "Lista dokumentacije";
    public const string Ostalo        = "Ostalo";

    public static readonly IReadOnlyList<string> All =
    [
        Cjenovnik,
        Dokumentacija,
        Ostalo
    ];
}
