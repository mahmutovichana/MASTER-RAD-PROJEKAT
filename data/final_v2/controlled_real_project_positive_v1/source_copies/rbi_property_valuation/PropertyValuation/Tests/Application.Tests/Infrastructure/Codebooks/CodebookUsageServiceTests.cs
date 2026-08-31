using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Codebooks.Interfaces;
using RBBH.CollateralAppraisal.Application.Codebooks.Models;
using RBBH.CollateralAppraisal.Infrastructure.Codebooks;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Codebooks;

public sealed class CodebookUsageServiceTests
{
    private static ICodebookUsageChecker CreateChecker(string codebookKey, CodebookUsageLocation? result)
    {
        var checker = Substitute.For<ICodebookUsageChecker>();
        checker.CodebookKey.Returns(codebookKey);
        checker.CheckAsync(Arg.Any<int>(), Arg.Any<CancellationToken>()).Returns(result);
        return checker;
    }

    private static ICodebookUsageChecker CreateThrowingChecker(string codebookKey)
    {
        var checker = Substitute.For<ICodebookUsageChecker>();
        checker.CodebookKey.Returns(codebookKey);
        checker.CheckAsync(Arg.Any<int>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException<CodebookUsageLocation?>(new InvalidOperationException("boom")));
        return checker;
    }

    [Fact]
    public async Task CheckUsageAsync_NoRegisteredCheckers_ReturnsNotInUseAndReliable()
    {
        var sut = new CodebookUsageService([], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.False(result.IsInUse);
        Assert.Equal(0, result.UsageCount);
        Assert.True(result.IsReliable);
        Assert.Empty(result.Locations);
    }

    [Fact]
    public async Task CheckUsageAsync_CheckerReturnsNull_ReturnsNotInUse()
    {
        var checker = CreateChecker("limit_types", null);
        var sut = new CodebookUsageService([checker], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.False(result.IsInUse);
        Assert.Equal(0, result.UsageCount);
        Assert.True(result.IsReliable);
    }

    [Fact]
    public async Task CheckUsageAsync_CheckerReturnsLocationWithCount_ReturnsInUse()
    {
        var checker = CreateChecker("limit_types",
            new CodebookUsageLocation { Module = "Orders", EntityName = "AppraisalOrder", Count = 2 });
        var sut = new CodebookUsageService([checker], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.True(result.IsInUse);
        Assert.Equal(2, result.UsageCount);
        Assert.Single(result.Locations);
        Assert.Equal("Orders", result.Locations[0].Module);
    }

    [Fact]
    public async Task CheckUsageAsync_CheckerReturnsLocationWithZeroCount_IsNotAddedToLocations()
    {
        var checker = CreateChecker("limit_types",
            new CodebookUsageLocation { Module = "Orders", EntityName = "AppraisalOrder", Count = 0 });
        var sut = new CodebookUsageService([checker], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.False(result.IsInUse);
        Assert.Equal(0, result.UsageCount);
        Assert.Empty(result.Locations);
    }

    [Fact]
    public async Task CheckUsageAsync_MultipleCheckersForSameKey_SumsUsageCounts()
    {
        var checker1 = CreateChecker("limit_types",
            new CodebookUsageLocation { Module = "Orders", EntityName = "AppraisalOrder", Count = 2 });
        var checker2 = CreateChecker("limit_types",
            new CodebookUsageLocation { Module = "Orders", EntityName = "WorkflowTask", Count = 3 });
        var sut = new CodebookUsageService([checker1, checker2], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.True(result.IsInUse);
        Assert.Equal(5, result.UsageCount);
        Assert.Equal(2, result.Locations.Count);
    }

    [Fact]
    public async Task CheckUsageAsync_CheckerThrows_ReturnsIsReliableFalse()
    {
        var checker = CreateThrowingChecker("limit_types");
        var sut = new CodebookUsageService([checker], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.False(result.IsReliable);
        Assert.False(result.CanDelete);
    }

    [Fact]
    public async Task CheckUsageAsync_CodebookKeyMatchIsCaseInsensitive()
    {
        var checker = CreateChecker("Limit_Types",
            new CodebookUsageLocation { Module = "Orders", EntityName = "AppraisalOrder", Count = 1 });
        var sut = new CodebookUsageService([checker], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.True(result.IsInUse);
    }

    [Fact]
    public async Task CheckUsageAsync_FiltersOutCheckersForOtherCodebookKeys()
    {
        var matching = CreateChecker("limit_types",
            new CodebookUsageLocation { Module = "Orders", EntityName = "AppraisalOrder", Count = 1 });
        var other = CreateChecker("relation_basis",
            new CodebookUsageLocation { Module = "Orders", EntityName = "AppraisalOrder", Count = 99 });
        var sut = new CodebookUsageService([matching, other], Substitute.For<ILogger<CodebookUsageService>>());

        var result = await sut.CheckUsageAsync("limit_types", 1);

        Assert.Equal(1, result.UsageCount);
    }
}
