using RBBH.CollateralAppraisal.Infrastructure.Audit;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Audit;

public sealed class AuditValueSanitizerTests
{
    private readonly AuditValueSanitizer _sut = new();

    [Fact]
    public void Sanitize_NullValue_ReturnsNull()
    {
        var result = _sut.Sanitize(null);

        Assert.Null(result);
    }

    [Fact]
    public void Sanitize_StringValue_RedactsPasswordField()
    {
        var json = """{"password":"super-secret","name":"Petar"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"password\":\"***REDACTED***\"", result);
        Assert.Contains("\"name\":\"Petar\"", result);
    }

    [Theory]
    [InlineData("refreshToken")]
    [InlineData("accessToken")]
    [InlineData("apiKey")]
    [InlineData("clientSecret")]
    [InlineData("connectionString")]
    [InlineData("authorizationHeader")]
    [InlineData("privateKey")]
    public void Sanitize_RedactsKnownSensitiveFieldNames(string fieldName)
    {
        var json = $$"""{"{{fieldName}}":"value-123"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains($"\"{fieldName}\":\"***REDACTED***\"", result);
    }

    [Fact]
    public void Sanitize_ObjectValue_SerializesWithCamelCaseAndRedactsSensitiveFields()
    {
        var payload = new SamplePayload("janedoe", "super-secret");

        var result = _sut.Sanitize(payload);

        Assert.Contains("\"username\":\"janedoe\"", result);
        Assert.Contains("\"password\":\"***REDACTED***\"", result);
    }

    [Fact]
    public void Sanitize_EmailField_WithShortLocalPart_MasksWithSingleVisibleChar()
    {
        var json = """{"email":"ab@example.com"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"email\":\"a***@example.com\"", result);
    }

    [Fact]
    public void Sanitize_EmailField_WithLongerLocalPart_MasksWithTwoVisibleChars()
    {
        var json = """{"actorEmail":"johndoe@example.com"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"actorEmail\":\"jo***@example.com\"", result);
    }

    [Fact]
    public void Sanitize_PhoneField_LongEnough_MasksMiddleDigits()
    {
        var json = """{"phoneNumber":"+38761123456"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"phoneNumber\":\"+387***456\"", result);
    }

    [Fact]
    public void Sanitize_PhoneField_TooShort_LeavesValueUnchanged()
    {
        var json = """{"tel":"12345"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"tel\":\"12345\"", result);
    }

    [Fact]
    public void Sanitize_AppliesRedactionBeforeEmailAndPhoneMasking()
    {
        var json = """{"password":"secret","email":"johndoe@example.com","mobile":"+38761123456"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"password\":\"***REDACTED***\"", result);
        Assert.Contains("\"email\":\"jo***@example.com\"", result);
        Assert.Contains("\"mobile\":\"+387***456\"", result);
    }

    // ── JMBG / clientIdentifier maskiranje ───────────────────────────────────

    [Fact]
    public void Sanitize_ClientIdentifierField_MasksJmbg()
    {
        var json = """{"clientIdentifier":"0101985771007"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"clientIdentifier\":\"01*********07\"", result);
    }

    [Theory]
    [InlineData("jmbg")]
    [InlineData("pib")]
    [InlineData("nationalId")]
    [InlineData("taxNumber")]
    public void Sanitize_IdentifierField_MasksNationalId(string fieldName)
    {
        var json = $$"""{"{{fieldName}}":"1234567890123"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains($"\"{fieldName}\":\"12*********23\"", result);
    }

    [Fact]
    public void Sanitize_ShortIdentifier_LeavesUnchanged()
    {
        // Vrijednosti <= 4 znaka se ne maskiraju (nema što sakriti)
        var json = """{"clientIdentifier":"AB1"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"clientIdentifier\":\"AB1\"", result);
    }

    [Fact]
    public void Sanitize_OrderSnapshot_MasksJmbgButPreservesOtherFields()
    {
        var json = """{"clientName":"Haris Hadžić","clientIdentifier":"0101985771007","city":"Sarajevo"}""";

        var result = _sut.Sanitize(json);

        Assert.Contains("\"clientName\":\"Haris Hadžić\"", result);
        Assert.Contains("\"clientIdentifier\":\"01*********07\"", result);
        Assert.Contains("\"city\":\"Sarajevo\"", result);
    }

    private sealed record SamplePayload(string Username, string Password);
}
