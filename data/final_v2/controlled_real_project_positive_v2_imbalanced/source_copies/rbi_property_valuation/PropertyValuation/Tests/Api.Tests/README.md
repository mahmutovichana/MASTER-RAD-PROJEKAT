# Api.Tests

Integracijski testovi za Api projekt.

Koriste `WebApplicationFactory<Program>` za pokretanje cijele aplikacije u memoriji.

```csharp
public class HealthEndpointTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public HealthEndpointTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Health_ReturnsOk()
    {
        var response = await _client.GetAsync("/health");
        response.EnsureSuccessStatusCode();
    }
}
```

**Zavisnosti:** Microsoft.AspNetCore.Mvc.Testing
