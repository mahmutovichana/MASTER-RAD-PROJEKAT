# Security — Role, Permission, Policy

Ovaj folder sadrži centralnu definiciju sigurnosnog modela aplikacije.

## Struktura

```
Security/
├── AppRoles.cs              — konstante za role
├── AppPermissions.cs        — konstante za permission-e
├── AppPolicies.cs           — konstante za policy nazive
├── RolePermissionMatrix.cs  — mapa rola → permission-i
├── Models/
│   ├── FieldVisibility.cs       — Hidden | ReadOnly | Editable
│   ├── RecordCapabilities.cs    — capabilities za konkretni zapis
│   └── UserPermissionsResponse.cs — response za GET /api/me/permissions
├── Interfaces/
│   ├── IUserPermissionService.cs
│   ├── IRoleManagementService.cs
│   ├── IRecordAuthorizationService.cs
│   └── IFieldAuthorizationService.cs
└── DTOs/
    ├── AssignRoleRequest.cs
    ├── RemoveRoleRequest.cs
    └── TransferAdminRoleRequest.cs
```

---

## Kako dodati novu rolu

1. Dodaj konstantu u `AppRoles.cs` i u `AppRoles.All` niz.
2. Dodaj permissions za novu rolu u `RolePermissionMatrix.PermissionsByRole`.
3. Ako rola zahtijeva nove permission-e, dodaj ih u `AppPermissions.cs`.
4. Dokumentuj rolu u `docs/backend/role-permission-rules.md`.
5. Kreiraj rolu u Keycloak realm-u.

---

## Kako dodati novu permission

1. Dodaj konstantu u `AppPermissions.cs`.
2. Dodaj permission u `AppPermissions.All` niz — policy se **automatski** registruje.
3. Dodaj permission odgovarajućoj roli u `RolePermissionMatrix.PermissionsByRole`.
4. Zaštiti endpoint (vidi ispod).

---

## Kako zaštititi endpoint

### Minimal API
```csharp
app.MapPost("/api/roles/assign", handler)
   .RequireAuthorization(AppPolicies.RolesAssign);
```

### Controller
```csharp
[Authorize(Policy = AppPolicies.RolesAssign)]
public IActionResult AssignRole([FromBody] AssignRoleRequest request) { ... }
```

### NIKAD ne pisati
```csharp
[Authorize(Roles = "Administrator")]           // hardkodovan string
.RequireAuthorization(p => p.RequireRole("Administrator"))  // zaobilazi permission model
```

---

## Kako funkcioniše permission model

```
JWT token → uloge (roles) → PermissionClaimsTransformation
                         ↓
                  RolePermissionMatrix
                         ↓
               "permission" claim-ovi u ClaimsPrincipal
                         ↓
         Policy: RequireClaim("permission", "roles.assign")
```

1. Keycloak šalje role u JWT tokenu.
2. `PermissionClaimsTransformation` čita role i dodaje `permission` claim-ove.
3. `AddPermissionPolicies()` registruje policy za svaki permission iz `AppPermissions.All`.
4. Endpoint koristi `.RequireAuthorization(AppPolicies.XYZ)` → provjera permission claim-a.

---

## Zašto ne hardkodovati role stringove po endpointima

- Promjena naziva role ne zahtijeva promjenu svakog endpointa.
- Dodavanje nove role ne zahtijeva ažuriranje endpointa — samo ažurirati matricu.
- Permission model je čitljiviji od role modela za kompleksna pravila.
- SOLID Open/Closed Principle: sistem se proširuje bez mijenjanja postojećeg koda.

---

## Zašto frontend hidden/readOnly/disabled nije sigurnosna zaštita

Frontend može sakriti dugme ili onemogućiti polje, ali:
- Korisnik može direktno pozvati API.
- API mora uvijek provjeriti dozvole, status zapisa i vlasništvo.
- Backend je jedini sigurnosni sloj.

---

## Capabilities model

`RecordCapabilities` opisuje šta korisnik smije raditi na konkretnom zapisu.
Vraća se kao dio response-a ili posebnim endpointom `GET /api/records/{id}/capabilities`.

```json
{
  "recordId": "123",
  "status": "PendingVerification",
  "capabilities": {
    "canEdit": false,
    "canSubmitForVerification": false,
    "canApprove": true,
    "canReject": true
  },
  "fields": {
    "title": "ReadOnly",
    "verificationComment": "Editable"
  }
}
```

---

## GET /api/me/permissions

Endpoint vraća role i permission-e trenutnog korisnika.
Frontend koristi ovo za inicijalni prikaz — **nije zamjena za backend provjere**.

```json
{
  "roles": ["Unosnik"],
  "permissions": [
    "records.create",
    "records.view-own",
    "records.update-own-draft",
    "records.submit-for-verification",
    "codebooks.view"
  ]
}
```
