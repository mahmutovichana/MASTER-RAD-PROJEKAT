namespace RBBH.CollateralAppraisal.Application.Documents.Dtos;

public sealed record DocumentDownloadDto(
    Stream Content,
    string FileName,
    string ContentType);