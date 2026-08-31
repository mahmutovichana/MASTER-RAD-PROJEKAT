# Api/Middleware

ASP.NET Core middleware komponente.

| Middleware | Svrha |
|-----------|-------|
| `CorrelationIdMiddleware` | Dodaje X-Correlation-ID header na svaki request/response |

**Registracija u Program.cs:**
```csharp
app.UseMiddleware<CorrelationIdMiddleware>();
```
