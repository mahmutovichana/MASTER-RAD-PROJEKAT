# Api/Contracts

Request i Response modeli koji su dio API ugovora (public API contract).

**Konvencija:**
```
Contracts/
  Items/
    CreateItemRequest.cs
    UpdateItemRequest.cs
    ItemResponse.cs
    ItemListResponse.cs
```

Ovi modeli se ne koriste unutar Application/Domain — mapiraju se na/sa Application DTO-ove u Endpoint handleru.
