# Konvencije

- Namespace i projekti počinju sa `RBBH.TestAutomation`.
- `TestGenerator/TestGenerator.csproj` je host, `TestGenerator/Core` poslovno jezgro, a `src/Web` odvojeni React klijent.
- OpenAPI i zajednički HTTP klijent su jedini frontend/backend ugovor.
- SQL Server je jedini trajni provider; InMemory je razvojni fallback.
- Tajne nisu u appsettings datotekama pod verzioniranjem.
- Lokalna autentifikacija nikada nije dostupna u Production okruženju.
