# Application/ExternalSources

Apstrakcija za vanjske izvore podataka (vanjske baze, API-jevi, ERP sistemi...).

## Komponente

- `ExternalSourceContext` — opisuje izvor (sistem, konekcija, baza, shema, tabela)
- `IExternalDataConnector<TResult>` — generički interfejs koji Infrastructure implementira

## Primjer implementacije (u Infrastructure)

```csharp
// Infrastructure/ExternalSources/SapItemConnector.cs
public class SapItemConnector : IExternalDataConnector<SapItemDto>
{
    public ExternalSourceContext Context => new()
    {
        SourceSystem = "SAP",
        SourceConnectionName = "SAP_PRODUCTION",
        SourceDatabase = "SAPDB",
        SourceTable = "MARA"
    };

    public async Task<IEnumerable<SapItemDto>> FetchAsync(CancellationToken ct)
    {
        // TODO: implementacija
        throw new NotImplementedException();
    }

    public Task<bool> IsAvailableAsync(CancellationToken ct)
        => Task.FromResult(false); // TODO
}
```
