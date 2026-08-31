namespace RBBH.CollateralAppraisal.Application.Orders.Requests;

public sealed record OrderListRequest(
    string?   Search      = null,
    string?   Status      = null,
    string?   City        = null,
    int?      CollateralTypeId = null,
    string?   AppraisalType = null,
    DateTime? CreatedFrom = null,
    DateTime? CreatedTo   = null,
    string?   SortBy         = null,
    bool      SortDescending = true,
    int       Page        = 1,
    int       PageSize    = 20
);
