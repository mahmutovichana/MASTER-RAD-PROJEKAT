using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Common.Exceptions;

public sealed class NotFoundExceptionTests
{
    // ── Constructor with entity name and key ──────────────────────────────────

    [Fact]
    public void Constructor_WithNameAndKey_FormatsMessageCorrectly()
    {
        var ex = new NotFoundException("AppraisalOrder", 42);

        Assert.Equal("Entity 'AppraisalOrder' with key '42' was not found.", ex.Message);
        Assert.Null(ex.ErrorCode);
    }

    [Fact]
    public void Constructor_WithNameAndStringKey_FormatsMessageCorrectly()
    {
        // Cast to object to force the (string, object, string?) overload
        var ex = new NotFoundException("User", (object)"user-abc-123");

        Assert.Equal("Entity 'User' with key 'user-abc-123' was not found.", ex.Message);
        Assert.Null(ex.ErrorCode);
    }

    [Fact]
    public void Constructor_WithNameKeyAndErrorCode_StoresErrorCode()
    {
        var ex = new NotFoundException("AppraisalOrder", 42, "ORDER_NOT_FOUND");

        Assert.Equal("Entity 'AppraisalOrder' with key '42' was not found.", ex.Message);
        Assert.Equal("ORDER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public void Constructor_WithNameAndGuidKey_FormatsMessageCorrectly()
    {
        var guid = Guid.NewGuid();
        var ex = new NotFoundException("Document", guid);

        Assert.Equal($"Entity 'Document' with key '{guid}' was not found.", ex.Message);
        Assert.Null(ex.ErrorCode);
    }

    // ── Constructor with custom message ──────────────────────────────────────

    [Fact]
    public void Constructor_WithMessage_StoresCustomMessage()
    {
        var ex = new NotFoundException("Narudzba nije pronadjena.");

        Assert.Equal("Narudzba nije pronadjena.", ex.Message);
        Assert.Null(ex.ErrorCode);
    }

    [Fact]
    public void Constructor_WithMessageAndErrorCode_StoresBoth()
    {
        var ex = new NotFoundException("Korisnik nije pronadjen.", "USER_NOT_FOUND");

        Assert.Equal("Korisnik nije pronadjen.", ex.Message);
        Assert.Equal("USER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public void Constructor_WithMessageAndNullErrorCode_ErrorCodeIsNull()
    {
        var ex = new NotFoundException("Nema entiteta.", (string?)null);

        Assert.Equal("Nema entiteta.", ex.Message);
        Assert.Null(ex.ErrorCode);
    }

    [Fact]
    public void Constructor_TwoStrings_ResolvesToMessageOverload()
    {
        // With two string arguments, C# resolves to (string message, string? errorCode)
        // because string is more specific than object
        var ex = new NotFoundException("Poruka", "KOD");

        Assert.Equal("Poruka", ex.Message);
        Assert.Equal("KOD", ex.ErrorCode);
    }

    // ── Inheritance ──────────────────────────────────────────────────────────

    [Fact]
    public void NotFoundException_IsException()
    {
        var ex = new NotFoundException("Test", 1);

        Assert.IsAssignableFrom<Exception>(ex);
    }

    [Fact]
    public void NotFoundException_CanBeCaughtAsException()
    {
        Exception? caught = null;

        try
        {
            throw new NotFoundException("Entity", (object)"key-1");
        }
        catch (Exception ex)
        {
            caught = ex;
        }

        Assert.NotNull(caught);
        Assert.IsType<NotFoundException>(caught);
        Assert.Equal("Entity 'Entity' with key 'key-1' was not found.", caught.Message);
    }

    // ── Edge cases ───────────────────────────────────────────────────────────

    [Fact]
    public void Constructor_WithEmptyName_FormatsMessageWithEmptyName()
    {
        var ex = new NotFoundException("", 0);

        Assert.Equal("Entity '' with key '0' was not found.", ex.Message);
    }

    [Fact]
    public void Constructor_WithEmptyMessage_StoresEmptyMessage()
    {
        var ex = new NotFoundException("");

        Assert.Equal("", ex.Message);
    }

    [Theory]
    [InlineData("ORDER_NOT_FOUND")]
    [InlineData("USER_NOT_FOUND")]
    [InlineData("DOCUMENT_NOT_FOUND")]
    [InlineData("CODEBOOK_NOT_FOUND")]
    public void Constructor_ErrorCode_AcceptsVariousValues(string errorCode)
    {
        var ex = new NotFoundException("Entity", 1, errorCode);

        Assert.Equal(errorCode, ex.ErrorCode);
    }

    [Theory]
    [InlineData(1)]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(int.MaxValue)]
    public void Constructor_WithVariousIntKeys_FormatsCorrectly(int key)
    {
        var ex = new NotFoundException("Entity", key);

        Assert.Contains(key.ToString(), ex.Message);
    }
}
