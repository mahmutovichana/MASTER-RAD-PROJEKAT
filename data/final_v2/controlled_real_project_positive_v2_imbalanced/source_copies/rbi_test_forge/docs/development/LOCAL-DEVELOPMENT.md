# Lokalni razvoj

API i Web rade u dva terminala prema koracima u korijenskom README-u. `pnpm dev:api` pokreće API na `5001`, a `pnpm dev` React na `8081`. OpenAPI tipovi se generišu tek kada API radi.

Ako SQL Server nije konfigurisan, Development automatski puni InMemory bazu grupama, scenarijima, rasporedima, historijom, API ključevima i svim šifarnicima. Podaci se brišu pri restartu. Za trajnost postaviti connection string i pregledati bazu kroz SSMS; migracije se primjenjuju pri pokretanju.

Ako Keycloak nije konfigurisan, aplikacija ispisuje warning i koristi `MockAuth__ActiveUser=admin`. To nije dostupno u Production okruženju. Za provjeru drugog seta ovlasti prije pokretanja API-ja postaviti, na primjer, `$env:MockAuth__ActiveUser='developer1'`.
