# Testni podaci i scenariji — Generator automatizovanih testova

## Pokretanje

- API: `src/Web/pnpm dev:api`, port 5001.
- Web: `src/Web/pnpm dev`, port 8081.
- Lokalni fallback auth i InMemory baza rade bez Keycloaka/SQL Servera; podešena infrastruktura ih automatski zamjenjuje.
- Profil provjeriti na `GET /api/frontend/profile`.

## Seed sadržaj

Seed daje Smoke, Regression i Full grupe, REST/UI/Blazor scenarije, aktivne rasporede, Passed/Failed historiju, API ključeve/metapodatke, audit i šifrarnike: vrste scenarija, HTTP metode, tagovi grupa, statusi izvršavanja i vremenske zone.

## Validni testni podaci

- Grupa: naziv `Kreditni API smoke`, opis `Kritični tokovi`, prioritet 10, tag Smoke.
- REST scenarij: `GET health`, URL `http://127.0.0.1:5001/health`, metoda GET, očekivani status 200.
- UI scenarij: naziv `Otvaranje pregleda`, početni URL `http://127.0.0.1:8081/app`, koraci navigate + assertion.
- Raspored: cron `0 8 * * 1-5`, zona `Europe/Sarajevo`, aktivan.
- API ključ: naziv `Lokalna CI provjera`, datum isteka u budućnosti. Sirovi ključ se mora prikazati samo jednom.
- Šifrarnik: naziv `PATCH`, kod `PATCH`, redoslijed 3, aktivan.

## Negativni scenariji

- Grupa bez naziva, naziv >200, prioritet -1 ili 1001.
- REST scenarij bez REST konfiguracije ili status 99/600; UI bez koraka; Blazor bez sadržaja.
- Raspored bez cron izraza ili neispravan cron/timezone.
- API ključ bez naziva ili s istekom u prošlosti.
- Nepoznata/duplirana korisnička rola; update mora zamijeniti skup bez duplikata.
- Šifrarnik bez naziva, duplikat koda i brisanje vrijednosti u upotrebi.
- OpenAPI: prazan, sintaksno pogrešan, random Excel/tekst ili dokument >5 MB.
- Blazor analiza: bez fajlova, nepodržana ekstenzija, >250 fajlova ili >5 MB.

## API matrica

- Groups: GET list/detail, POST, PUT, DELETE, POST `/{id}/run`.
- Scenarios: GET list/detail, POST, PUT, DELETE, clone, run.
- Schedules: GET, POST, PUT, DELETE, run-now; provjeriti promjenu historije.
- History: lista, dashboard i trend za 1, 30 i 365 dana; vrijednosti izvan raspona se ograničavaju.
- Generator: REST generisanje, component analyze, bUnit/Playwright generisanje.
- API import: validan OpenAPI JSON/YAML daje parsirane endpoint-e; greška je korisnički čitljiva.
- Users/roles, code lists, API keys i audit: svi CRUD/dozvoljeni tokovi te 401/403 bez prava.
- CI: pokretanje grupe/taga, status posla i izvještaj u podržanom formatu.

## UI i validacija

- Nakon create/update/delete/run, React Query invalidacija mora osvježiti ekran bez ručnog Refresh-a.
- Svako obavezno polje ima label, required stanje i field-level poruku; submit je zaštićen i server validacijom.
- Light/dark header, modali, dropdowni, inputi i textarea su neprozirni; light logo je crni, dark žuti.
- Testirati tastaturu, Escape, fokus, loading/empty/error i duge nazive na 320–1920 px.

## Automatizovani testovi

- `dotnet test TestGenerator/TestGenerator.slnx --configuration Release`: 414 unit + 9 E2E/API testa, svi prolaze.
- `cd src/Web; pnpm test; pnpm build`: vizuelni ugovor i production bundle.
- Dok API radi: `powershell -ExecutionPolicy Bypass -File scripts/testing/Test-LocalApi.ps1 -IncludeCrud` izvršava health i potpuni create/update/run/delete tok nad privremenom grupom, scenarijem, rasporedom i API ključem. Privremeni zapisi se uklanjaju u `finally` bloku čak i kada test ne prođe.
- Testovi pokrivaju generatore, parser, repozitorije, validatore, grupe, scenarije, šifrarnike i HTTP tokove.
