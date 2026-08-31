using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Orders;

namespace RBBH.CollateralAppraisal.Application.QuoteRequests.Queries;

public sealed record GetQuoteRequestsQuery(int OrderId) : IQuery<IReadOnlyList<QuoteRequestDto>>;

public sealed class GetQuoteRequestsQueryHandler
    : IRequestHandler<GetQuoteRequestsQuery, IReadOnlyList<QuoteRequestDto>>
{
    private readonly IQuoteRequestService _service;
    public GetQuoteRequestsQueryHandler(IQuoteRequestService service) => _service = service;
    public Task<IReadOnlyList<QuoteRequestDto>> Handle(GetQuoteRequestsQuery query, CancellationToken ct)
        => _service.GetByOrderAsync(query.OrderId, ct);
}
