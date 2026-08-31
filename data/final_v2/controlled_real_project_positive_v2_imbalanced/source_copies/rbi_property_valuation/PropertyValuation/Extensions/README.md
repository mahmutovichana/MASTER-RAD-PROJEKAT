# Api/Extensions

Extension metode koje drže Program.cs čistim.

| Klasa | Metoda | Svrha |
|-------|--------|-------|
| `ServiceCollectionExtensions` | `AddApiServices` | Registruje sve servise (Application, Infrastructure, Auth, CORS, HealthChecks) |
| `WebApplicationExtensions` | `ConfigurePipeline` | Konfigurira middleware pipeline i mapira sve endpoint-e |
