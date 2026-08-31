# RBBH Test Automation

Poslovna aplikacija za upravljanje testnim scenarijima, grupama, šifarnicima, rasporedima i izvršavanjima te generisanje automatizovanih REST, bUnit i Playwright testova. React interfejs koristi RBI design-core komponente i semantičke boje, dok .NET API čuva poslovna pravila i jedini pristupa bazi i Keycloaku.

## Mogućnosti

- kreiranje, kloniranje, brisanje i neposredno pokretanje REST/UI scenarija;
- hijerarhijske grupe testova, rasporedi, historija i trendovi izvršavanja;
- OpenAPI/Swagger analiza i generisanje xUnit REST test projekta;
- analiza `.razor`/`.razor.cs` komponenti i generisanje bUnit ili Playwright testova;
- šifarnici u bazi, API ključevi za CI/CD, korisnici i role iz Keycloaka te audit;
- bosanski, engleski i njemački jezik, light/dark tema i pristupačne RBI komponente.

## Struktura

- `TestGenerator/TestGenerator.csproj` — glavni .NET/OCP servis.
- `TestGenerator/Core` — domenski modeli, parseri, generatori i repozitorijski ugovori.
- `TestGenerator/` — sav backend kod, konfiguracija, Dockerfile i backend testovi.
- `src/Web` — React aplikacija i tipizirani HTTP sloj.
- `TestGenerator/UnitTests` i `TestGenerator/E2ETests` — automatske provjere.

## Lokalno pokretanje

Preduvjeti su .NET SDK 10, Node.js i pnpm 9. Docker nije potreban niti se koristi za lokalno pokretanje.

```powershell
# Terminal 1
cd src/Web
pnpm install
pnpm dev:api

# Terminal 2, isti src/Web folder
pnpm dev
```

Otvorite `http://localhost:8081`. API je na `http://127.0.0.1:5001`. Bez lokalnih tajni `dev:api` koristi Development režim, seedovanu InMemory bazu i lokalnog korisnika.

Frontend koristi isti Webpack obrazac kao Registar povezanih lica. Vite,
Nitro i esbuild nisu instalirani niti se pokreće dodatni izvršni fajl.
`pnpm dev` generiše javnu runtime konfiguraciju, pokreće SPA server i
prosljeđuje relativne API/autentifikacijske rute na port 5001. Za privremene
portove koriste se `WEB_PORT` i `API_PROXY_TARGET`.

Port `8081` je frontend aplikacije, a port `5001` je isključivo API. Otvaranje API početne adrese u Development režimu preusmjerava na frontend.

Bez SQL Server konfiguracije Development koristi seedovanu InMemory bazu i in-memory adaptere. Bez Keycloak konfiguracije koristi se razvojna autentifikacija uz warning. Produkcija nema nesiguran fallback.

Lokalni korisnik je `admin`; lozinka se ne traži jer razvojni režim simulira prijavu. Dodatni seedovani identiteti su `qalead1`, `qalead2`, `qaengineer1`, `qaengineer2`, `developer1`, `developer2`, `devops1` i `devops2`. Aktivni identitet se bira kroz `MockAuth__ActiveUser`.

## SQL Server

```powershell
$env:Database__ServerName='localhost\SQLEXPRESS'
$env:Database__Name='TestGenerator_Local'
$env:Database__IntegratedSecurity='true'
```

Ovo je jedini konfiguracijski oblik. Za OCP/SQL korisnika postavite
`Database__IntegratedSecurity=false`, a User/Password držite u OCP Secretu.
Backend automatski primjenjuje commitovane EF migracije pri startupu.

## Keycloak

Za stvarnu prijavu postaviti deployment varijable `OpenIDConnectSettings__Authority`, `OpenIDConnectSettings__ClientId` i `OpenIDConnectSettings__ClientSecret`. Ovo je serverski OIDC/cookie tok kao u DataProductsPortal-u: frontend ne dobija client secret, a profil prijavljenog korisnika i njegove role čita preko zaštićenog API-ja. U Keycloaku još moraju biti dozvoljeni tačni callback/logout URL-ovi OCP servisa. Za ekran upravljanja korisnicima potreban je zaseban service-account klijent kroz `KeycloakAdmin__ClientId` i `KeycloakAdmin__ClientSecret`, sa minimalnim potrebnim ovlastima. Zato client ID i secret bez Authority/realm adrese, redirect URL-ova i rola nisu potpuna konfiguracija.

Realm treba sadržavati role `Administrator`, `QA Lead`, `QA Inzenjer`, `Developer` i `DevOps Inzenjer`. Jedan korisnik može imati više rola.

OpenAPI tipovi se generišu tek nakon pokretanja API-ja:

```powershell
cd src/Web
pnpm openapi:generate
```

## Provjera i isporuka

```powershell
dotnet build TestGenerator/TestGenerator.slnx --configuration Release
dotnet test TestGenerator/TestGenerator.slnx --configuration Release
cd src/Web
pnpm localization:validate
pnpm typecheck
pnpm lint
pnpm test
pnpm build
```

Backend ide na OCP, frontend kao statički IIS paket. Više: [arhitektura](docs/architecture/README.md), [lokalni razvoj](docs/development/LOCAL-DEVELOPMENT.md), [SQL Server i migracije](docs/database/SQL-SERVER.md), [varijable](docs/configuration/ENVIRONMENT-VARIABLES.md), [konvencije](docs/CONVENTIONS.md) i [deployment](docs/deployment/OCP-IIS.md).

GitHub Environment koristi `PROJECT_PATH=TestGenerator`, `SOLUTION_PATH=TestGenerator.csproj` i `NUGET_CONFIG_PATH=nuget.config`.
