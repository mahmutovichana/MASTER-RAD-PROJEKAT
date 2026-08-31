# OCP backend i IIS frontend

Backend i frontend su dva nezavisna deployment artefakta. OCP image sadrži samo backend iz `TestGenerator/`, dok se statički React paket gradi iz `src/Web` i predaje IIS administratoru kao ZIP.

Tri fajla u `.github/workflows` ostaju byte-po-byte jednaka DataProducts workflowima. U svakom GitHub Environmentu postavite:

| Varijabla | Vrijednost |
|---|---|
| `PROJECT_PATH` | `TestGenerator` |
| `SOLUTION_PATH` | `TestGenerator.csproj` |
| `NUGET_CONFIG_PATH` | `nuget.config` |

Build workflow koristi `TestGenerator/Dockerfile` sa korijenom repozitorija kao Docker contextom. CodeQL izvršava restore i build nad `TestGenerator/TestGenerator.csproj`. Connection string, Keycloak, data-protection lokacija, GitHub token, SMTP i ostale tajne dolaze iz OCP Secret/ConfigMap resursa i ne upisuju se u image ili Git.

Frontend paket se pravi komandom `pnpm publish:iis` iz `src/Web`. IIS raspakuje ZIP, nudi HTTPS i SPA fallback te prosljeđuje relativne `/api`, `/authentication`, `/health` i `/openapi` rute prema OCP servisu. Keycloak redirect URI mora odgovarati javnom IIS URL-u i `/signin-oidc` putanji.

ZIP nema `.dll`: IIS vraća statički HTML/CSS/JavaScript, fontove, slike i
lokalizacije. `.NET` proces i njegove `.dll` datoteke postoje samo u OCP imageu.
IIS ARR mora proslijediti `/authentication`, `/signin-oidc`, `/signout-callback-oidc`
i `/api`; browser zatim dobija samo HttpOnly/Secure session cookie. Na IIS-u
nisu potrebni Node, pnpm ni .NET runtime.

```text
Browser → IIS → auth/API putanje kroz ARR → OCP TestGenerator
                                           ├→ Keycloak
                                           └→ SQL Server
```

OCP database ConfigMap/Secret koristi `Database__ServerName`,
`Database__Name`, `Database__IntegratedSecurity`, `Database__User` i
`Database__Password`.
