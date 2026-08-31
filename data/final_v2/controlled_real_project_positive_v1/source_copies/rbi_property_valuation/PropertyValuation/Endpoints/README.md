# Api/Endpoints

Minimal API endpoints organizovani po domenu.

**Konvencija:**

```csharp
// Svaki modul ima svoju statičku klasu sa Map... extension metodom
public static class ItemEndpoints
{
    public static IEndpointRouteBuilder MapItemEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/items").RequireAuthorization();

        group.MapGet("/", GetAllItems);
        group.MapGet("/{id:int}", GetItemById);
        group.MapPost("/", CreateItem);
        group.MapPut("/{id:int}", UpdateItem);
        group.MapDelete("/{id:int}", DeleteItem);

        return app;
    }

    private static async Task<IResult> GetAllItems(ISender sender)
    {
        // TODO: Delegirati na Application handler
        throw new NotImplementedException();
    }
    // ...
}
```

Pozivajte iz `WebApplicationExtensions.MapAllEndpoints()`.
