# Arhitektura

Tok zahtjeva je `Browser → React (src/Web) → isti HTTPS origin → .NET API (TestGenerator) → Core (TestGenerator/Core) → EF Core → SQL Server`.

- **React/Web** prikazuje RBI komponente, validira unos radi boljeg UX-a, drži server state kroz React Query i koristi jedan HTTP klijent. Ne sadrži tajne niti direktno pristupa bazi ili Keycloaku.
- **.NET API** je sigurnosna i poslovna granica. Validira svaki zahtjev, vraća standardni Problem Details format, provjerava CSRF, upravlja cookie/OIDC prijavom i izlaže OpenAPI ugovor.
- **Core** sadrži modele, parsere, generatore i ugovore koji nisu vezani za prikaz ili hosting.
- **SQL Server/EF Core** je trajno spremište. Development bez connection stringa koristi seedovanu InMemory bazu istog EF modela.
- **Keycloak** izdaje identitet i role; tajne i tokeni ostaju na serveru. Bez konfiguracije se samo u Development režimu koristi jasno označen mock identitet.

Frontend poziva relativne `/api` rute. Lokalno ih Webpack Dev Server prosljeđuje API-ju, a na IIS-u server/reverse proxy prosljeđuje OCP backendu. Zbog toga stvarni URL nije ugrađen u JavaScript build i isti ZIP može prolaziti kroz okruženja. Frontend nema Vite/Nitro/esbuild zavisnosti.

OCP artefakt je backend kontejnerska slika. IIS artefakt su statički frontend fajlovi.
