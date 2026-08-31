# Application/Common/Interfaces

Interfejsi koje Application sloj definiše, a Infrastructure implementira.

| Interfejs | Svrha |
|-----------|-------|
| `ICurrentUserService` | Pristup podacima trenutno prijavljenog korisnika (UserID, UserName) |
| `IDateTimeProvider` | Apstrakcija za `DateTime.UtcNow` — olakšava testiranje |

**Dodajte ovdje:**
- `IRepository<T>` ako koristite Repository Pattern
- `IUnitOfWork` ako koristite Unit of Work
- `IEmailService`, `INotificationService`, itd.
