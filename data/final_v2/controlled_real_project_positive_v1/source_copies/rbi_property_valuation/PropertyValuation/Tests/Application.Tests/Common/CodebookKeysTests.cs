using RBBH.CollateralAppraisal.Application.Common.Constants;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common;

public sealed class CodebookKeysTests
{
    [Fact]
    public void DocumentTypes_HasExpectedValue()
        => Assert.Equal("tipovi_dokumenata", CodebookKeys.DocumentTypes);

    [Fact]
    public void CollateralTypes_HasExpectedValue()
        => Assert.Equal("tipovi_kolaterala", CodebookKeys.CollateralTypes);

    [Fact]
    public void DocumentTypeCodes_FinalAppraisal_HasExpectedValue()
        => Assert.Equal("FINALNA_PROCJENA", DocumentTypeCodes.FinalAppraisal);

    [Fact]
    public void DocumentTypeCodes_ZkExtract_HasExpectedValue()
        => Assert.Equal("ZK", DocumentTypeCodes.ZkExtract);
}
