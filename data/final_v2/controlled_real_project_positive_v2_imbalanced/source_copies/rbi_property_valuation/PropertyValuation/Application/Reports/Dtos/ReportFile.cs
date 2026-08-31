namespace RBBH.CollateralAppraisal.Application.Reports.Dtos;

/// <summary>Generisani izvještaj spreman za download (bajtovi + ime fajla + content-type).</summary>
public sealed record ReportFile(byte[] Content, string FileName, string ContentType);
