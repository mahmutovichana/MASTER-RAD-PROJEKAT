# Application/Features

Poslovni use cases / feature handleri organizovani po modulu.

**Preporučena struktura po feature-u:**

```
Features/
  Items/
    Commands/
      CreateItem/
        CreateItemCommand.cs
        CreateItemCommandHandler.cs
        CreateItemCommandValidator.cs
      UpdateItem/
        ...
    Queries/
      GetItemById/
        GetItemByIdQuery.cs
        GetItemByIdQueryHandler.cs
      GetItemsList/
        ...
    DTOs/
      ItemDto.cs
```

Svaki handler sadrži poslovnu logiku za jedan use case. Ne stavlja se logika u Controller/Endpoint.

**Napomena:** Za CQRS pattern preporučuje se MediatR (dodati u RBBH.CollateralAppraisal.Application.csproj).
