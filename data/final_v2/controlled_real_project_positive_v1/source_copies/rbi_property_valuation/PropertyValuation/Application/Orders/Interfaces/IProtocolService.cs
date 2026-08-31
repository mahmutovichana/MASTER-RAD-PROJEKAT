using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Orders.Interfaces;

public interface IProtocolService
{
    Task<ProtocolEntryDto> GetByOrderIdAsync(int orderId, CancellationToken ct = default);
    Task<PagedResult<ProtocolEntryDto>> GetProtocolListAsync(int page = 1, int pageSize = 20, CancellationToken ct = default);
    Task<OrderProtocolEntry> CreateProtocolForOrderAsync(int orderId, CancellationToken ct = default);
}
