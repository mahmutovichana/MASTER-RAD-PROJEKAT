using RBBH.CollateralAppraisal.Application.Documents.Dtos;

namespace RBBH.CollateralAppraisal.Application.Documents;

public interface ISharedDocumentService
{
    Task<IReadOnlyList<SharedDocumentDto>> GetAllAsync(CancellationToken ct = default);

    Task<SharedDocumentDto> UploadAsync(
        string title,
        string category,
        DocumentUploadFile file,
        CancellationToken ct = default);

    Task<DocumentDownloadDto> DownloadAsync(int id, CancellationToken ct = default);

    Task DeleteAsync(int id, CancellationToken ct = default);
}
