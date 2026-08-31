using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Opinions.Dtos;

public sealed record OpinionDto(
    OpinionType   OpinionType,
    OpinionStatus Status,
    string?       ImportedByUserId,
    DateTime?     ImportedAt,
    string?       Comment,
    int?          DocumentId
);