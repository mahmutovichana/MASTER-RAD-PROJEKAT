using System.Diagnostics.CodeAnalysis;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;

namespace RBBH.CollateralAppraisal.Application.Documents;

/// <summary>
/// Generisanje Word dokumenata (narudžbenica i izjava) sa podacima iz Protokola narudžbi.
/// Eliminira ručni copy-paste i greške pri prepisivanju.
/// </summary>
public interface IOrderDocumentGenerator
{
    /// <summary>
    /// Generiše narudžbenicu i izjavu za narudžbu procjene.
    /// Dokumenti se snimaju u skladište i kreiraju kao Document entiteti.
    /// </summary>
    Task<OrderDocumentGenerationResult> GenerateAsync(
        int orderId,
        OrderDocumentGenerationRequest request,
        CancellationToken ct = default);
}

[ExcludeFromCodeCoverage]
public sealed record OrderDocumentGenerationRequest(
    decimal? Iznos = null,
    string? ZkOznaka = null);

[ExcludeFromCodeCoverage]
public sealed record OrderDocumentGenerationResult(
    int OrderId,
    string OrderNumber,
    IReadOnlyList<DocumentDto> GeneratedDocuments,
    string Message);
