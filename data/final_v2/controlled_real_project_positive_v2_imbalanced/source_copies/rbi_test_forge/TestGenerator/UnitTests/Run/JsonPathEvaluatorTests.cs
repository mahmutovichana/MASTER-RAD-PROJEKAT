using RBBH.TestAutomation.Api.Services.Run;

namespace UnitTests.Run;

/// <summary>
/// Unit testovi za <see cref="JsonPathEvaluator"/> — minimalni JSONPath nad REST odgovorima.
/// Pokriva obrasce koje koriste seed scenariji: $.prop, $.a.b, $[0], $[0].prop.
/// </summary>
public class JsonPathEvaluatorTests
{
    [Theory]
    [InlineData("{\"id\":1}",                         "$.id",        "1")]
    [InlineData("{\"username\":\"Bret\"}",            "$.username",  "Bret")]
    [InlineData("{\"a\":{\"b\":42}}",                 "$.a.b",       "42")]
    [InlineData("[{\"id\":7}]",                       "$[0].id",     "7")]
    [InlineData("[10,20,30]",                          "$[1]",        "20")]
    [InlineData("{\"ok\":true}",                      "$.ok",        "true")]
    [InlineData("{\"data\":[{\"naziv\":\"x\"}]}",    "$.data[0].naziv", "x")]
    public void TryEvaluate_ValidPath_ReturnsValue(string json, string path, string expected)
    {
        var ok = JsonPathEvaluator.TryEvaluate(json, path, out var value);

        Assert.True(ok);
        Assert.Equal(expected, value);
    }

    [Theory]
    [InlineData("{\"id\":1}",   "$.missing")]   // nepostojeće polje
    [InlineData("{\"id\":1}",   "$[0]")]        // indeks nad objektom
    [InlineData("[1,2]",         "$[5]")]        // indeks van granica
    [InlineData("{ not json",   "$.id")]        // nevalidan JSON
    public void TryEvaluate_InvalidPathOrJson_ReturnsFalse(string json, string path)
    {
        var ok = JsonPathEvaluator.TryEvaluate(json, path, out var value);

        Assert.False(ok);
        Assert.Null(value);
    }
}
