# Application/Audit

Generički audit scaffold. Nije vezan za konkretne poslovne tabele.

## Principi dizajna

- `AuditEvent` — DTO koji opisuje šta se desilo
- `IAuditService` — jedini ulaz za logovanje; distribuira na sve Sink-ove
- `IAuditSink` — implementira se u Infrastructure (baza, datoteka, SIEM...)
- `IAuditValueSanitizer` — maskira PII/osjetljive podatke prije upisa
- Konstante (`AuditActions`, `AuditModules`, `AuditOperationTypes`, `AuditStatuses`, `AuditSeverity`) — standardizovani vokabular

## Korištenje

```csharp
await _auditService.LogAsync(new AuditEvent
{
    UserId      = currentUser.UserId,
    UserName    = currentUser.UserName,
    Action      = AuditActions.Create,
    Module      = AuditModules.Users,
    OperationType = AuditOperationTypes.UserInitiated,
    Status      = AuditStatuses.Success,
    Severity    = AuditSeverity.Low,
    EntityType  = "User",
    EntityKey   = newUserId.ToString()
});
```

## Proširenje

Za novi modul ili akciju — dodajte konstantu u odgovarajuću klasu, ne mijenjajte AuditEvent.

Za novi izvor podataka (vanjska baza) — implementirajte `IAuditSink` u Infrastructure/Audit.
