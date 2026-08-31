using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Opinions;

namespace RBBH.CollateralAppraisal.Application.Opinions.Commands;

public sealed record RequestOpinionsCommand(int OrderId) : ICommand;

public sealed class RequestOpinionsCommandHandler : IRequestHandler<RequestOpinionsCommand>
{
    private readonly IOpinionService _service;
    public RequestOpinionsCommandHandler(IOpinionService service) => _service = service;
    public Task Handle(RequestOpinionsCommand command, CancellationToken ct)
        => _service.RequestOpinionsAsync(command.OrderId, ct);
}
