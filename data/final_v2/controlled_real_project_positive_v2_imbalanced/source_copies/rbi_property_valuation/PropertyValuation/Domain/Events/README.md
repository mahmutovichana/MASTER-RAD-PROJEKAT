# Domain/Events

Domenski eventi opisuju šta se desilo u domeni (past tense).

```csharp
// Primjer:
public record ItemCreatedEvent(int ItemId, string Name, DateTime OccurredAt);
```

Koristite za event-driven komunikaciju između agregata ili za triggering Application logike.
