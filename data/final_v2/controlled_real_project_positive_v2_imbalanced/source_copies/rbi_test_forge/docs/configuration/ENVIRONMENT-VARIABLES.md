# Konfiguracija okruženja

Lokalno kopirajte `.env.example` u `.env`. Fajl `.env` je gitignored, a
`scripts/dev-api.cmd` ga učitava prije pokretanja backenda. Stvarne lozinke ne
upisujte u `appsettings.json`, dokumentaciju ni primjer konfiguracije.

## Backend/OCP

| Varijabla | Obavezna | Svrha |
|---|---:|---|
| `ASPNETCORE_ENVIRONMENT` | da | `Development`, `Staging` ili `Production`. |
| `Database__ServerName` | produkcija | SQL Server/instance. |
| `Database__Name` | produkcija | Naziv baze, npr. `TestGenerator`. |
| `Database__IntegratedSecurity` | ne | `true` za Windows identitet; na OCP obično `false`. |
| `Database__User` / `Database__Password` | SQL auth | OCP Secret. |
| `OpenIDConnectSettings__Authority` | produkcija | Keycloak realm URL. |
| `OpenIDConnectSettings__ClientId` / `ClientSecret` | produkcija | Povjerljivi serverski OIDC client. Secret ostaje na backendu. |
| `KeycloakAdmin__ClientId` / `ClientSecret` | opciono | Zaseban least-privilege service account za upravljanje korisnicima; ako nije postavljen koristi OIDC client. |
| `MockAuth__Enabled` / `MockAuth__ActiveUser` | samo lokalno | Razvojni identitet; Production ga odbija. |

Tema 2 koristi isti BFF/cookie obrazac kao Data Products: browser nikada ne
dobija Keycloak token ni client secret. Zbog toga frontend nema Keycloak
varijable. `API_BASE_URL` je jedina javna runtime opcija i preporučeno ostaje
prazna, tako da IIS/webpack prosljeđuje relativne rute backendu. Nema `VITE_*`
varijabli jer frontend koristi Webpack, ne Vite.

```text
Browser → IIS → /authentication/login kroz ARR → OCP backend → Keycloak
Browser ← HttpOnly/Secure cookie
Browser → /api kroz isti origin → OCP backend → SQL Server
```

GitHub koristi `PROJECT_PATH=TestGenerator` i
`SOLUTION_PATH=TestGenerator.csproj` samo za pronalazak backend projekta.
