# SQL Server, SSMS i EF Core migracije

Jedini vanjski način konfiguracije baze je:

```text
Database__ServerName=SQL-SERVER-ILI-SERVER,1433
Database__Name=PropertyValuation
Database__IntegratedSecurity=false
Database__User=<OCP Secret>
Database__Password=<OCP Secret>
```

Za lokalni SSMS/Windows identitet koristite `localhost\SQLEXPRESS`, naziv
`PropertyValuation_Local` i `Database__IntegratedSecurity=true`. Prazni
ServerName i Name u Developmentu biraju seedovanu InMemory bazu. Djelimična
konfiguracija je greška, a Production bez SQL konfiguracije ne starta.

Nakon izmjene EF modela generišite i commitujte migraciju:

```powershell
$env:Database__ServerName='localhost\SQLEXPRESS'
$env:Database__Name='PropertyValuation_Local'
$env:Database__IntegratedSecurity='true'
dotnet ef migrations add NazivPromjene `
  --project PropertyValuation/Infrastructure/RBBH.CollateralAppraisal.Infrastructure.csproj `
  --startup-project PropertyValuation/PropertyValuation.csproj `
  --output-dir Persistence/Migrations `
  --context ApplicationDbContext
```

Backend pri startupu primjenjuje sve neprimijenjene migracije. Referentni
šifrarnici i definicije rola pune se idempotentno; demo vještaci i narudžbe
samo u Development/Staging okruženju. Produkcija se ne puni demo podacima.
Enkripcija veze je uvijek uključena, a prije produkcijske migracije obavezni su
pregled generisanog SQL-a i backup.
