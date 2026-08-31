# Domain/Entities

Ovdje se dodaju poslovni entiteti projekta.

**Smjernice:**
- Svaki entitet nasljeđuje `BaseEntity`.
- Konstruktori su privatni ili protected — kreirajte factory metode `Create(...)`.
- Entiteti ne poznaju EF Core, ne sadrže `[Key]` atribute itd.
- Validaciona pravila su u samom entitetu (domain validation), ne u Application sloju.

```csharp
// Primjer:
public class Item : BaseEntity
{
    public string Name { get; private set; } = string.Empty;

    private Item() { }

    public static Item Create(string name) => new() { Name = name };
}
```
