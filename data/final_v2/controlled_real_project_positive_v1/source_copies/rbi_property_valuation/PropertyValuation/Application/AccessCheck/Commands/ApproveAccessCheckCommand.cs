using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.AccessCheck.Commands;

public sealed record ApproveAccessCheckCommand(int OrderId, string? Comment) : ICommand<CaDocumentReviewResultDto>;

public sealed class ApproveAccessCheckCommandHandler
    : IRequestHandler<ApproveAccessCheckCommand, CaDocumentReviewResultDto>
{
    private readonly IAccessCheckService _service;
    public ApproveAccessCheckCommandHandler(IAccessCheckService service) => _service = service;
    public Task<CaDocumentReviewResultDto> Handle(ApproveAccessCheckCommand command, CancellationToken ct)
        => _service.ApproveAccessAsync(command.OrderId, command.Comment, ct);
}
