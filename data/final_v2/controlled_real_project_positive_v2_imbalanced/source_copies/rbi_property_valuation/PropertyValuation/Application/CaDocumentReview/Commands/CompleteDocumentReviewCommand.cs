using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.CaDocumentReview.Commands;

public sealed record CompleteDocumentReviewCommand(int OrderId) : ICommand<CaDocumentReviewResultDto>;

public sealed class CompleteDocumentReviewCommandHandler
    : IRequestHandler<CompleteDocumentReviewCommand, CaDocumentReviewResultDto>
{
    private readonly ICaDocumentReviewService _service;
    public CompleteDocumentReviewCommandHandler(ICaDocumentReviewService service) => _service = service;
    public Task<CaDocumentReviewResultDto> Handle(CompleteDocumentReviewCommand command, CancellationToken ct)
        => _service.CompleteReviewAsync(command.OrderId, ct);
}
