using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Opinions;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Opinions.Commands;

public sealed record SubmitOpinionCommand(
    int OrderId,
    OpinionType OpinionType,
    byte[] FileBytes,
    string FileName,
    string? ContentType,
    string? Comment,
    string UserId) : ICommand;

public sealed class SubmitOpinionCommandHandler : IRequestHandler<SubmitOpinionCommand>
{
    private readonly IOpinionService _service;
    public SubmitOpinionCommandHandler(IOpinionService service) => _service = service;
    public Task Handle(SubmitOpinionCommand command, CancellationToken ct)
        => _service.SubmitOpinionAsync(
            command.OrderId, command.OpinionType, new MemoryStream(command.FileBytes),
            command.FileName, command.ContentType, command.Comment, command.UserId, ct);
}
