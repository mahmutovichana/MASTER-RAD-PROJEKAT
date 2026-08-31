# SQL Server, SSMS i EF Core migracije

Jedini vanjski način konfiguracije baze je:

```text
Database__ServerName=SQL-SERVER-ILI-SERVER,1433
Database__Name=TestGenerator
Database__IntegratedSecurity=false
Database__User=<OCP Secret>
Database__Password=<OCP Secret>
```

Za lokalni SSMS/Windows identitet koristite `localhost\SQLEXPRESS`, naziv
`TestGenerator_Local` i `Database__IntegratedSecurity=true`. Prazni ServerName
i Name u Developmentu biraju seedovanu InMemory bazu. Djelimična konfiguracija
je greška, a Production bez SQL konfiguracije ne starta. Enkripcija je uvijek
uključena; nepouzdani certifikat se prihvata samo u Developmentu.

Nakon izmjene EF modela generišite i commitujte migraciju:

```powershell
$env:Database__ServerName='localhost\SQLEXPRESS'
$env:Database__Name='TestGenerator_Local'
$env:Database__IntegratedSecurity='true'
dotnet ef migrations add NazivPromjene `
  --project TestGenerator/Core/RBBH.TestAutomation.Core.csproj `
  --startup-project TestGenerator/TestGenerator.csproj `
  --context TestForgeDbContext
```

Backend pri startupu automatski poziva `MigrateAsync()` i izvršava samo
neprimijenjene migracije. Demo seed radi samo u Development/Staging okruženju;
produkcijski podaci ostaju pod kontrolom aplikacije i SSMS procesa. Prije
produkcijske migracije obavezni su pregled SQL-a i backup.
