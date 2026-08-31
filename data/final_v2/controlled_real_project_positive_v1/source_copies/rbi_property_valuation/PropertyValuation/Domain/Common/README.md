# Domain/Common

Ovdje se nalaze bazne klase koje koriste sve domenske entitete.

- `BaseEntity.cs` — apstraktna klasa sa `Id`, `CreatedAt`, `UpdatedAt` koja je zajednička osnova svih entiteta.

**Pravila:**
- Domain ne smije imati reference na EF Core, ASP.NET, Keycloak ili bilo koji infrastrukturni paket.
- Domain ne referencira nijedan drugi projekat u ovom solution-u.
