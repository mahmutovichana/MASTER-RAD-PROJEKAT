# Infrastructure/ExternalSources

Implementacije konektora na vanjske izvore podataka.

## Kreiranje novog konektora

1. Kreirajte DTO klasu za podatke iz izvora
2. Implementirajte `IExternalDataConnector<TDto>`
3. Registrujte u `DependencyInjection.cs`

```csharp
// Primjer: konektor na vanjski REST API
public class PaymentApiConnector : IExternalDataConnector<PaymentDto>
{
    private readonly HttpClient _http;

    public ExternalSourceContext Context => new()
    {
        SourceSystem = "PAYMENT_GATEWAY",
        SourceConnectionName = "payment_api_v2",
        SourceTable = "payments/v2/transactions"
    };

    public async Task<IEnumerable<PaymentDto>> FetchAsync(CancellationToken ct)
    {
        var response = await _http.GetFromJsonAsync<IEnumerable<PaymentDto>>("payments/v2/transactions", ct);
        return response ?? Enumerable.Empty<PaymentDto>();
    }

    public async Task<bool> IsAvailableAsync(CancellationToken ct)
    {
        var response = await _http.GetAsync("health", ct);
        return response.IsSuccessStatusCode;
    }
}
```

## TODO

- Definisati konkretne vanjske izvore sa timom
- Dodati connection string konfiguraciju za svaki izvor
- Razmotriti retry politiku (Polly) za nestabilne izvore
