using System.Net;
using RBBH.CollateralAppraisal.Api.Tests.Helpers;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Misc;

/// <summary>
/// Testovi za jednostavne GET endpointe koji vraćaju statičke podatke.
/// Pokriva nepokrivene linije u CodebookImportExportEndpoints i SharedDocumentEndpoints.
/// </summary>
[Collection("ApiTests")]
public sealed class MiscEndpointsTests : IClassFixture<ApiFactory>
{
    private readonly ApiFactory _factory;

    public MiscEndpointsTests(ApiFactory factory) => _factory = factory;

    [Fact]
    public async Task GetCodebookImportTypes_Returns200WithTypes()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var response = await client.GetAsync("/api/codebooks/import-export/types");
        // 200 OK ili 401/403 — ne smije biti 500
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }

    [Fact]
    public async Task GetSharedDocumentCategories_Returns200()
    {
        var client = _factory.CreateAuthenticatedClient("test-admin");
        var response = await client.GetAsync("/api/shared-documents/categories");
        Assert.NotEqual(HttpStatusCode.InternalServerError, response.StatusCode);
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
