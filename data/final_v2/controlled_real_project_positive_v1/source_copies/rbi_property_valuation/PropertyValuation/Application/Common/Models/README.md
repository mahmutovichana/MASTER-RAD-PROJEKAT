# Application/Common/Models

Zajednički modeli koji se koriste kroz Application sloj.

**Preporučeni modeli:**
- `Result<T>` / `Result` — wrapper za uspješan/neuspješan rezultat bez bacanja izuzetaka
- `PaginatedList<T>` — straničenje rezultata
- `PagedRequest` — request za straničene upite

```csharp
// Primjer Result<T>:
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    private Result(T value) { IsSuccess = true; Value = value; }
    private Result(string error) { IsSuccess = false; Error = error; }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);
}
```
