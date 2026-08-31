# RBBH Collateral Appraisal

Poslovna aplikacija za kompletan tok procjene kolaterala: kreiranje naloga, dodjelu procjenitelja, dokumentaciju, mišljenja, odobravanje, fakture, protokol, izvještaje, šifarnike i audit.

## Struktura

- `PropertyValuation/PropertyValuation.csproj` — glavni .NET/OCP servis.
- `PropertyValuation/Domain` — poslovni entiteti i pravila bez infrastrukturnih zavisnosti.
- `PropertyValuation/Application` — use-case ugovori, komande, upiti i validacija.
- `PropertyValuation/Infrastructure` — EF Core, SQL Server, dokumenti, audit, Keycloak adapteri i seed.
- `PropertyValuation/` — sav backend kod, konfiguracija, Dockerfile i backend testovi.
- `src/Web` — React frontend, dizajn sistem, lokalizacija i jedinstveni HTTP klijent.
- `PropertyValuation/Tests` — domenske, aplikacijske, infrastrukturne, API i E2E provjere.

## Lokalno pokretanje

Preduvjeti su .NET SDK 10, Node.js i pnpm 9. Docker nije potreban.

```powershell
# Terminal 1
cd src/Web
pnpm install
pnpm dev:api

# Terminal 2, isti src/Web folder
pnpm dev
```

Otvorite `http://localhost:8082`. API je na `http://127.0.0.1:5002`. Bez lokalnih tajni `dev:api` koristi Development režim, seedovanu InMemory bazu i lokalnog korisnika; Keycloak sinhronizacija se tada uredno preskače.

Frontend koristi isti Webpack obrazac kao Registar povezanih lica. Vite,
Nitro i esbuild nisu instalirani niti se pokreće `esbuild.exe`. `pnpm dev`
generiše runtime konfiguraciju i prosljeđuje relativne API rute na port 5002.
Za privremene portove koriste se `WEB_PORT` i `API_PROXY_TARGET`.

Development bez SQL Server postavki koristi seedovanu InMemory bazu. Bez Keycloak postavki koristi se lokalni identitet uz upozorenje. Produkcija zahtijeva stvarnu bazu i autentifikaciju.

Frontend uključuje Keycloak samo kada je `KEYCLOAK_ENABLED=true` i kada su
`KEYCLOAK_URL`, `KEYCLOAK_REALM` i `KEYCLOAK_CLIENT_ID` popunjeni. Vrijednosti
se čitaju iz runtime `app-config.js`, pa se mogu postaviti na IIS-u bez novog
builda. Client secret nikada ne pripada browseru. Kada konfiguracija nedostaje,
Development nastavlja sa lokalnim identitetom uz warning; Production zahtijeva
stvarnu autentifikaciju.

## SQL Server

```powershell
$env:Database__ServerName='localhost\SQLEXPRESS'
$env:Database__Name='PropertyValuation_Local'
$env:Database__IntegratedSecurity='true'
```

Ovo je jedini konfiguracijski oblik. Za OCP/SQL korisnika postavite
`Database__IntegratedSecurity=false`, a User/Password držite u OCP Secretu.
Backend automatski primjenjuje commitovane EF migracije pri startupu.

## Keycloak

API validira bearer token kroz `Keycloak__Enabled`, `Keycloak__Authority` i
`Keycloak__Audience`. React koristi javne runtime vrijednosti
`KEYCLOAK_ENABLED`, `KEYCLOAK_URL`, `KEYCLOAK_REALM` i `KEYCLOAK_CLIENT_ID` uz
PKCE. Secret se ne smije staviti u frontend. Admin base URL i realm izvode se
iz `Keycloak__Authority`; samo opcioni service-account ClientId/ClientSecret
ostaju dodatne backend tajne za upravljanje rolama.

## Provjera i isporuka

```powershell
dotnet build PropertyValuation/PropertyValuation.slnx --configuration Release
dotnet test PropertyValuation/PropertyValuation.slnx --configuration Release
cd src/Web
pnpm lint
pnpm build
```

Backend ide na OCP, frontend kao statički IIS paket. Više: [arhitektura](docs/architecture/README.md), [lokalni razvoj](docs/development/LOCAL-DEVELOPMENT.md), [SQL Server i migracije](docs/database/SQL-SERVER.md), [varijable](docs/configuration/ENVIRONMENT-VARIABLES.md), [konvencije](docs/CONVENTIONS.md) i [deployment](docs/deployment/OCP-IIS.md).

GitHub Environment koristi `PROJECT_PATH=PropertyValuation`, `SOLUTION_PATH=PropertyValuation.csproj` i `NUGET_CONFIG_PATH=nuget.config`.
