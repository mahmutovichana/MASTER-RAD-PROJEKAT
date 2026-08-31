using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Domain.Orders;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common;

public sealed class ExceptionTests
{
    [Fact]
    public void ForbiddenException_DefaultConstructor_HasDefaultMessage()
    {
        var ex = new ForbiddenException();
        Assert.Contains("permission", ex.Message, StringComparison.OrdinalIgnoreCase);
        Assert.Null(ex.ErrorCode);
    }

    [Fact]
    public void ForbiddenException_MessageAndErrorCode_SetsProperties()
    {
        var ex = new ForbiddenException("Zabranjeno", "FORBIDDEN_OP");
        Assert.Equal("Zabranjeno", ex.Message);
        Assert.Equal("FORBIDDEN_OP", ex.ErrorCode);
    }
}

public sealed class AppraisalOrderDomainTests
{
    private static AppraisalOrder MakeOrder() => AppraisalOrder.Create(
        "PN-001", "Test", "Klijent", "FL", null,
        null, null, null, null, null, null, null,
        null, null, "user-1", "AM", null, null, null);

    [Fact]
    public void SetCityReference_UpdatesCityId()
    {
        var order = MakeOrder();
        order.SetCityReference(5, DateTime.UtcNow);
        Assert.Equal(5, order.CityId);
    }

    [Fact]
    public void SetBranchReference_UpdatesBranchId()
    {
        var order = MakeOrder();
        order.SetBranchReference(3, DateTime.UtcNow);
        Assert.Equal(3, order.BranchId);
    }
}

public sealed class AuditOutboxTests
{
    [Fact]
    public void AuditOutboxEntry_Create_HasPayloadAndCreatedAt()
    {
        var entry = AuditOutboxEntry.Create("{\"action\":\"TEST\"}");
        Assert.Equal("{\"action\":\"TEST\"}", entry.Payload);
        Assert.NotEqual(default, entry.CreatedAt);
        Assert.Null(entry.ProcessedAt);
    }

    [Fact]
    public void AuditOutboxEntry_MarkProcessed_SetsProcessedAt()
    {
        var entry = AuditOutboxEntry.Create("{}");
        entry.MarkProcessed();
        Assert.NotNull(entry.ProcessedAt);
    }
}
