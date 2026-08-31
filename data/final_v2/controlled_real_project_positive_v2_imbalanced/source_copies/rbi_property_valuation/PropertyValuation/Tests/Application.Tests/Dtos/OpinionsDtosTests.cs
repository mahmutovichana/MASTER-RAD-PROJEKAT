using RBBH.CollateralAppraisal.Application.Opinions.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Dtos;

public sealed class OpinionsDtosTests
{
    [Fact]
    public void OpinionDto_AllFieldsPopulated_StoresCorrectValues()
    {
        var importedAt = new DateTime(2026, 6, 10, 12, 0, 0, DateTimeKind.Utc);

        var dto = new OpinionDto(
            OpinionType: OpinionType.CO,
            Status: OpinionStatus.Imported,
            ImportedByUserId: "co-user-1",
            ImportedAt: importedAt,
            Comment: "CO misljenje uvezeno",
            DocumentId: 42);

        Assert.Equal(OpinionType.CO, dto.OpinionType);
        Assert.Equal(OpinionStatus.Imported, dto.Status);
        Assert.Equal("co-user-1", dto.ImportedByUserId);
        Assert.Equal(importedAt, dto.ImportedAt);
        Assert.Equal("CO misljenje uvezeno", dto.Comment);
        Assert.Equal(42, dto.DocumentId);
    }

    [Fact]
    public void OpinionDto_NullOptionalFields_StoresNull()
    {
        var dto = new OpinionDto(
            OpinionType: OpinionType.Pravna,
            Status: OpinionStatus.Requested,
            ImportedByUserId: null,
            ImportedAt: null,
            Comment: null,
            DocumentId: null);

        Assert.Equal(OpinionType.Pravna, dto.OpinionType);
        Assert.Equal(OpinionStatus.Requested, dto.Status);
        Assert.Null(dto.ImportedByUserId);
        Assert.Null(dto.ImportedAt);
        Assert.Null(dto.Comment);
        Assert.Null(dto.DocumentId);
    }

    [Theory]
    [InlineData(OpinionType.CO, 0)]
    [InlineData(OpinionType.Pravna, 1)]
    public void OpinionDto_OpinionType_HasExpectedIntValue(OpinionType type, int expectedInt)
    {
        var dto = new OpinionDto(
            OpinionType: type,
            Status: OpinionStatus.Requested,
            ImportedByUserId: null,
            ImportedAt: null,
            Comment: null,
            DocumentId: null);

        Assert.Equal(expectedInt, (int)dto.OpinionType);
    }

    [Theory]
    [InlineData(OpinionStatus.Requested, 0)]
    [InlineData(OpinionStatus.Imported, 1)]
    public void OpinionDto_OpinionStatus_HasExpectedIntValue(OpinionStatus status, int expectedInt)
    {
        var dto = new OpinionDto(
            OpinionType: OpinionType.CO,
            Status: status,
            ImportedByUserId: null,
            ImportedAt: null,
            Comment: null,
            DocumentId: null);

        Assert.Equal(expectedInt, (int)dto.Status);
    }

    [Fact]
    public void OpinionDto_PravnaType_WithImportedStatus_StoresCorrectly()
    {
        var now = DateTime.UtcNow;

        var dto = new OpinionDto(
            OpinionType: OpinionType.Pravna,
            Status: OpinionStatus.Imported,
            ImportedByUserId: "pravna-user-1",
            ImportedAt: now,
            Comment: "Pravno misljenje kompletno",
            DocumentId: 100);

        Assert.Equal(OpinionType.Pravna, dto.OpinionType);
        Assert.Equal(OpinionStatus.Imported, dto.Status);
        Assert.Equal("pravna-user-1", dto.ImportedByUserId);
        Assert.Equal(now, dto.ImportedAt);
        Assert.Equal("Pravno misljenje kompletno", dto.Comment);
        Assert.Equal(100, dto.DocumentId);
    }

    [Fact]
    public void OpinionDto_COType_WithRequestedStatus_NoDocumentId()
    {
        var dto = new OpinionDto(
            OpinionType: OpinionType.CO,
            Status: OpinionStatus.Requested,
            ImportedByUserId: null,
            ImportedAt: null,
            Comment: "Ceka se CO misljenje",
            DocumentId: null);

        Assert.Equal(OpinionType.CO, dto.OpinionType);
        Assert.Equal(OpinionStatus.Requested, dto.Status);
        Assert.Equal("Ceka se CO misljenje", dto.Comment);
        Assert.Null(dto.DocumentId);
    }
}
