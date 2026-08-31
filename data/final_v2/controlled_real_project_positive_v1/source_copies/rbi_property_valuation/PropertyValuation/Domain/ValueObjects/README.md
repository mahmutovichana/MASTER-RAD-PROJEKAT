# Domain/ValueObjects

Value Objects nemaju identitet — dva value objecta su jednaka ako su sve vrijednosti jednake.

```csharp
// Primjer:
public record Money(decimal Amount, string Currency);
public record Email(string Value);
```
