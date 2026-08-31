using MediatR;
using RBBH.CollateralAppraisal.Application.Appraisers.Dtos;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.AppraiserAssignment.Commands;

public sealed record AutoSelectAppraiserCommand(int OrderId) : ICommand<AppraiserAssignmentResultDto>;

public sealed class AutoSelectAppraiserCommandHandler
    : IRequestHandler<AutoSelectAppraiserCommand, AppraiserAssignmentResultDto>
{
    private readonly IAppraiserAssignmentService _service;
    public AutoSelectAppraiserCommandHandler(IAppraiserAssignmentService service) => _service = service;
    public Task<AppraiserAssignmentResultDto> Handle(AutoSelectAppraiserCommand command, CancellationToken ct)
        => _service.AutoSelectAppraiserAsync(command.OrderId, ct);
}
