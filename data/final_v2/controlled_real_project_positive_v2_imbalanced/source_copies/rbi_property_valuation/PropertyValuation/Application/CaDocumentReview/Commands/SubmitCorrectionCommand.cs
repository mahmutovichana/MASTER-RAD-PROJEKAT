using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.CaDocumentReview.Commands;

public sealed record SubmitCorrectionCommand(int OrderId, string? Comment) : ICommand<CaDocumentReviewResultDto>;

public sealed class SubmitCorrectionCommandHandler
    : IRequestHandler<SubmitCorrectionCommand, CaDocumentReviewResultDto>
{
    private readonly ICaDocumentReviewService _service;
    public SubmitCorrectionCommandHandler(ICaDocumentReviewService service) => _service = service;
    public Task<CaDocumentReviewResultDto> Handle(SubmitCorrectionCommand command, CancellationToken ct)
        => _service.SubmitCorrectionAsync(command.OrderId, command.Comment, ct);
}
