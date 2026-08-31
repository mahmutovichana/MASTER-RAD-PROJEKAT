using RBBH.CollateralAppraisal.Application.Common.Models;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Models;

public sealed class PagedResultTests
{
    [Fact]
    public void TotalPages_ComputesCeilingOfTotalCountOverPageSize()
    {
        var result = new PagedResult<int>
        {
            Items      = [1, 2, 3],
            TotalCount = 25,
            Page       = 1,
            PageSize   = 10
        };

        Assert.Equal(3, result.TotalPages);
    }

    [Fact]
    public void TotalPages_PageSizeZero_ReturnsZero()
    {
        var result = new PagedResult<int>
        {
            Items      = [],
            TotalCount = 25,
            Page       = 1,
            PageSize   = 0
        };

        Assert.Equal(0, result.TotalPages);
    }

    [Theory]
    [InlineData(1, false)]
    [InlineData(2, true)]
    public void HasPreviousPage_TrueWhenPageGreaterThanOne(int page, bool expected)
    {
        var result = new PagedResult<int>
        {
            Items      = [],
            TotalCount = 25,
            Page       = page,
            PageSize   = 10
        };

        Assert.Equal(expected, result.HasPreviousPage);
    }

    [Theory]
    [InlineData(1, true)]
    [InlineData(3, false)]
    public void HasNextPage_TrueWhenPageLessThanTotalPages(int page, bool expected)
    {
        var result = new PagedResult<int>
        {
            Items      = [],
            TotalCount = 25,
            Page       = page,
            PageSize   = 10
        };

        Assert.Equal(expected, result.HasNextPage);
    }

    [Fact]
    public void Empty_ReturnsResultWithNoItemsAndZeroTotalCount()
    {
        var result = PagedResult<string>.Empty(page: 2, pageSize: 15);

        Assert.Empty(result.Items);
        Assert.Equal(0, result.TotalCount);
        Assert.Equal(2, result.Page);
        Assert.Equal(15, result.PageSize);
        Assert.True(result.HasPreviousPage);
        Assert.False(result.HasNextPage);
    }
}
