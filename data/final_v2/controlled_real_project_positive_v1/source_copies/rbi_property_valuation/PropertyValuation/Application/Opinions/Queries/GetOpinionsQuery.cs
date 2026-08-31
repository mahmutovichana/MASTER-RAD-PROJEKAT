using MediatR;
using RBBH.CollateralAppraisal.Application.Common.CQRS;
using RBBH.CollateralAppraisal.Application.Opinions;
using RBBH.CollateralAppraisal.Application.Opinions.Dtos;

namespace RBBH.CollateralAppraisal.Application.Opinions.Queries;

public sealed record GetOpinionsQuery(int OrderId) : IQuery<List<OpinionDto>>;

public sealed class GetOpinionsQueryHandler : IRequestHandler<GetOpinionsQuery, List<OpinionDto>>
{
    private readonly IOpinionService _service;
    public GetOpinionsQueryHandler(IOpinionService service) => _service = service;
    public Task<List<OpinionDto>> Handle(GetOpinionsQuery query, CancellationToken ct)
        => _service.GetOpinionsAsync(query.OrderId, ct);
}
