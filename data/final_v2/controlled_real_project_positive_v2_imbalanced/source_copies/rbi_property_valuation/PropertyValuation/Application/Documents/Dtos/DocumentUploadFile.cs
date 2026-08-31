namespace RBBH.CollateralAppraisal.Application.Documents.Dtos;

public sealed record DocumentUploadFile(
    Stream Content,
    string FileName,
    string? ContentType,
    long Length);