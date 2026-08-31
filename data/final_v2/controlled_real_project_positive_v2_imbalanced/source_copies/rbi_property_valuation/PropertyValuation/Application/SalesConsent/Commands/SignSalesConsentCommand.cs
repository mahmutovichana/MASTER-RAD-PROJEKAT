using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;

namespace RBBH.CollateralAppraisal.Application.SalesConsent.Commands;

public sealed record SignSalesConsentCommand(int OrderId) : ICommand<SignConsentResultDto>;

public sealed class SignSalesConsentCommandHandler
    : IRequestHandler<SignSalesConsentCommand, SignConsentResultDto>
{
    private readonly IOriginalAppraisalService _service;
    public SignSalesConsentCommandHandler(IOriginalAppraisalService service) => _service = service;
    public Task<SignConsentResultDto> Handle(SignSalesConsentCommand command, CancellationToken ct)
        => _service.SignSalesConsentAsync(command.OrderId, ct);
}
