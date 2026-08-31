using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.Invoice.Queries;

public sealed record GetInvoiceStatusQuery(int OrderId) : IQuery<InvoiceStatusDto>;

public sealed class GetInvoiceStatusQueryHandler
    : IRequestHandler<GetInvoiceStatusQuery, InvoiceStatusDto>
{
    private readonly IInvoiceWorkflowService _service;
    public GetInvoiceStatusQueryHandler(IInvoiceWorkflowService service) => _service = service;
    public Task<InvoiceStatusDto> Handle(GetInvoiceStatusQuery query, CancellationToken ct)
        => _service.GetStatusAsync(query.OrderId, ct);
}
