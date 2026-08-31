# Konfiguracija okruženja

Lokalno kopirajte `.env.example` u `.env`. Fajl `.env` je gitignored, a
`scripts/dev-api.cmd` ga učitava prije pokretanja backenda. Stvarne lozinke ne
upisujte u `appsettings.json`, dokumentaciju ni primjer konfiguracije.

## Backend/OCP

| Varijabla | Obavezna | Svrha |
|---|---:|---|
| `ASPNETCORE_ENVIRONMENT` | da | `Development`, `Staging` ili `Production`. |
| `Database__ServerName` | produkcija | SQL Server/instance. |
| `Database__Name` | produkcija | Naziv baze, npr. `PropertyValuation`. |
| `Database__IntegratedSecurity` | ne | `true` za Windows identitet; na OCP obično `false`. |
| `Database__User` / `Database__Password` | SQL auth | OCP Secret. |
| `Keycloak__Enabled` | produkcija | Uključuje JWT bearer validaciju. |
| `Keycloak__Authority` | uz Keycloak | Realm URL; iz njega se izvode admin base URL i realm. |
| `Keycloak__Audience` | uz Keycloak | Očekivani API audience. |
| `KeycloakAdmin__ClientId` / `ClientSecret` | admin funkcije | Least-privilege service account za role/korisnike. |

## Frontend/IIS

`KEYCLOAK_ENABLED`, `KEYCLOAK_URL`, `KEYCLOAK_REALM` i
`KEYCLOAK_CLIENT_ID` su javne PKCE postavke. Browser ih mora znati, ali među
njima nema secreta. Backend ima Authority/Audience jer validira token; to je
druga odgovornost, ne kopija client secreta. `API_BASE_URL` ostavite prazan uz
IIS ARR same-origin proxy. Frontend koristi Webpack runtime `app-config.js` i
nema `VITE_*` varijabli.

```text
Browser → IIS statički frontend → Keycloak PKCE (public client)
Browser → /api preko IIS ARR → OCP backend → validacija tokena → SQL Server
```

GitHub koristi `PROJECT_PATH=PropertyValuation` i
`SOLUTION_PATH=PropertyValuation.csproj` samo za build putanju. Baza i Keycloak
vrijednosti postavljaju se na OCP kroz ConfigMap/Secret.
