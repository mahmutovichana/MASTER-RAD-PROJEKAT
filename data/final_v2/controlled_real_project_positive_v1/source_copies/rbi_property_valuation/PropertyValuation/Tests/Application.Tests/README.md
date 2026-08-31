# Application.Tests

Unit testovi za Application sloj.

Testiraju poslovnu logiku, exception scenarije i validacije — bez baze i HTTP-a.

```csharp
public class NotFoundException_Tests
{
    [Fact]
    public void Constructor_WithNameAndKey_SetsMessage()
    {
        var ex = new NotFoundException("Item", 42);
        Assert.Contains("Item", ex.Message);
        Assert.Contains("42", ex.Message);
    }
}
```

Mockujte `ICurrentUserService`, `IAuditService` i ostale interfejse — baza se ne dirá.
