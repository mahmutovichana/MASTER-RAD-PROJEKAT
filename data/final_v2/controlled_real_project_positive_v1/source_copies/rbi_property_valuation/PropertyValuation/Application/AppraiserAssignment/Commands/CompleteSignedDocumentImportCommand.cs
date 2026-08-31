using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record CompleteSignedDocumentImportCommand(int OrderId) : ICommand<SendToAppraiserResultDto>;

public sealed class CompleteSignedDocumentImportCommandHandler
    : IRequestHandler<CompleteSignedDocumentImportCommand, SendToAppraiserResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public CompleteSignedDocumentImportCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<SendToAppraiserResultDto> Handle(CompleteSignedDocumentImportCommand command, CancellationToken ct)
        => _service.CompleteSignedDocumentImportAsync(command.OrderId, ct);
}
