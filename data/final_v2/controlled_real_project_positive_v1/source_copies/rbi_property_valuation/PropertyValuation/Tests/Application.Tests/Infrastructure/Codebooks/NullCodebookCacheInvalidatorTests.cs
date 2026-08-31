using RBBH.CollateralAppraisal.Infrastructure.Codebooks;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Codebooks;

public sealed class NullCodebookCacheInvalidatorTests
{
    [Fact]
    public async Task InvalidateAsync_CompletesWithoutError()
    {
        var sut = new NullCodebookCacheInvalidator();

        await sut.InvalidateAsync("any_key");
    }
}
