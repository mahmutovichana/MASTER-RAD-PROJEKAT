# Shared Komponente — TAG Aplikacija

Sve komponente u ovom folderu su **automatski dostupne** na svakoj `.razor` stranici
jer je `@using RBBH.TestAutomation.Api.Components.Shared` dodan u `Components/_Imports.razor`.

**Pravilo tima:** Nikad ne kopirati isti markup na dvije stranice. Ako nešto ponavljaš,
napravi shared komponentu.

---

## Sadržaj

| Komponenta | Namjena | Gdje se koristi |
|---|---|---|
| [`RbiAppBarBrand`](#rbiappbarbrand) | Logo + naziv u AppBar-u | `MainLayout.razor` |
| [`PageHeader`](#pageheader) | Naslov + subtitle + divider | Svaka stranica |
| [`StatusBadge`](#statusbadge) | Chip za role i statuse | Tablice, liste, kartice |
| [`LoadingButton`](#loadingbutton) | Dugme sa spinner stanjem | Login, sve forme |
| [`ErrorAlert`](#erroralert) | Error poruka s animacijom | Ispod formi, API greške |
| [`NavItem`](#navitem) | Nav link s disabled logikom | `MainLayout.razor` navigacija |

---

## `RbiAppBarBrand`

Logo RBI + naziv "Test Automation Generator" u MudAppBar-u.
Responsive: puni naziv na ≥576px, skraćenica "TAG" na mobilnom.

```razor
<RbiAppBarBrand />
```

**Parametri:** Nema — sve je hardcoded (brand je fiksni identitet).

---

## `PageHeader`

Standardni naslov svake stranice. Uvijek ide kao **prva komponenta** na stranici.

```razor
@* Minimalno *@
<PageHeader Title="Korisnici" />

@* S opisom *@
<PageHeader Title="Korisnici"
            Subtitle="Pregled i upravljanje korisničkim računima" />
```

| Parametar | Tip | Obavezan | Default | Opis |
|---|---|---|---|---|
| `Title` | `string` | ✅ | — | Naslov stranice (`Typo.h4`) |
| `Subtitle` | `string?` | ❌ | `null` | Kratki opis (`Typo.body2`) |

**Pravilo:** Samo jedan `PageHeader` po stranici.

---

## `StatusBadge`

Chip za prikaz rola, statusa zapisa i tipa akcija.

```razor
<StatusBadge Text="Administrator"   Color="Color.Error" />
<StatusBadge Text="Aktivno"         Color="Color.Success" />
<StatusBadge Text="Na čekanju"      Color="Color.Warning" />
<StatusBadge Text="Finansije"       Color="Color.Info" Size="Size.Medium" />
```

| Parametar | Tip | Obavezan | Default | Opis |
|---|---|---|---|---|
| `Text` | `string` | ✅ | — | Tekst na badgeu |
| `Color` | `Color` | ❌ | `Color.Default` | MudBlazor Color enum |
| `Size` | `Size` | ❌ | `Size.Small` | MudBlazor Size enum |

**Preporučene boje za TAG:**

| Boja | Situacija |
|---|---|
| `Color.Error` | Administrator (privilegovana rola) |
| `Color.Success` | Aktivno, odobreno, verificirano |
| `Color.Warning` | Na čekanju, privremeno, u izradi |
| `Color.Info` | Ostale role (Finansije, Compliance...) |
| `Color.Secondary` | Neaktivno, arhivirano |
| `Color.Default` | Generički, bez semantike |

---

## `LoadingButton`

MudButton koji prikazuje spinner dok se async operacija izvršava.
Automatski postaje disabled dok `IsLoading = true`.

```razor
@* Osnovna upotreba *@
<LoadingButton Text="Prijava"
               IsLoading="@_isLoading"
               OnClick="@HandleLogin"
               FullWidth="true" />

@* S custom loading tekstom *@
<LoadingButton Text="Spremi"
               LoadingText="Snimanje podataka..."
               IsLoading="@_isSaving"
               OnClick="@HandleSave"
               Color="Color.Secondary" />

@* Sekundarna akcija — outlined varijanta (nema brand žute pozadine) *@
<LoadingButton Text="Otkaži"
               Variant="Variant.Outlined"
               IsLoading="@_isCancelling"
               OnClick="@HandleCancel" />
```

| Parametar | Tip | Obavezan | Default | Opis |
|---|---|---|---|---|
| `Text` | `string` | ✅ | — | Tekst dugmeta |
| `IsLoading` | `bool` | ❌ | `false` | Aktivira spinner + onemogućava klik |
| `LoadingText` | `string` | ❌ | `"Molimo sačekajte..."` | Tekst dok se učitava |
| `OnClick` | `EventCallback` | ❌ | — | Click handler |
| `Disabled` | `bool` | ❌ | `false` | Dodatno onemogućavanje |
| `FullWidth` | `bool` | ❌ | `false` | Puna širina roditelja |
| `Variant` | `Variant` | ❌ | `Variant.Filled` | MudBlazor Variant |
| `Color` | `Color` | ❌ | `Color.Primary` | MudBlazor Color |

**Pattern za korištenje u `@code` bloku:**
```csharp
private bool _isLoading;

private async Task HandleSubmit()
{
    _isLoading = true;
    try
    {
        await SomeService.DoWorkAsync();
    }
    finally
    {
        _isLoading = false; // uvijek reset, čak i ako baci iznimku
    }
}
```

---

## `ErrorAlert`

Error poruka koja se glatko pojavljuje/nestaje koristeći `MudCollapse` animaciju.

```razor
<ErrorAlert Message="@_errorMessage" />
```

| Parametar | Tip | Obavezan | Default | Opis |
|---|---|---|---|---|
| `Message` | `string?` | ❌ | `null` | `null`/`""` = skriven; tekst = vidljiv |

**Pattern za korištenje u `@code` bloku:**
```csharp
private string? _errorMessage;

private async Task HandleLogin()
{
    _errorMessage = null; // resetuj pri svakom pokušaju

    var result = await AuthService.LoginAsync(_username, _password);
    if (!result.IsSuccess)
    {
        _errorMessage = "Neispravni podaci za prijavu."; // generička poruka (sigurnost)
    }
}
```

**Zašto `MudCollapse` umjesto `@if`:**
`@if` uklanja element bez animacije → layout odjednom "skače".
`MudCollapse` animira visinu → smooth UX koji privlači pažnju bez iznenađenja.

---

## `NavItem`

Navigacijski link s ugrađenom `disabled` logikom. Enkapsulira `nav-disabled-wrapper`
pattern iz `app.css`.

```razor
@* Aktivan link *@
<NavItem Href="/"
         Label="Home"
         Icon="@Icons.Material.Filled.Home"
         ExactMatch="true" />

@* Disabled (ruta ne postoji / korisnik nema pristup) *@
<NavItem Href="/users"
         Label="Korisnici"
         Icon="@Icons.Material.Filled.ManageAccounts"
         HasAccess="false" />

@* Dinamički po roli *@
<NavItem Href="/roles"
         Label="Upravljanje rolama"
         Icon="@Icons.Material.Filled.AdminPanelSettings"
         HasAccess="@CanAccess(AppModules.Role)" />
```

| Parametar | Tip | Obavezan | Default | Opis |
|---|---|---|---|---|
| `Href` | `string` | ✅ | — | URL rute |
| `Label` | `string` | ✅ | — | Tekst linka |
| `Icon` | `string` | ✅ | — | MudBlazor icon path |
| `HasAccess` | `bool` | ❌ | `true` | `false` = disabled s tooltipom |
| `ExactMatch` | `bool` | ❌ | `false` | `true` samo za Home (`/`) |

**Role-based integracija:** `HasAccess` se vezuje na `AppModules.CanAccess(modul, role)`
u `MainLayout.razor` (role iz prijavljenog korisnika). Samo `MainLayout.razor` postavlja
vrijednost — komponenta ostaje ista.

---

## Spacing — MudBlazor utility klase vs CSS tokeni

Aplikacija koristi **dva paralelna spacing sistema**. Oba su valjana — bitno je
ne miješati ih u istoj liniji.

### MudBlazor utility klase (`Class="mb-4"`, `Class="pa-6"`, `Class="mr-2"`)

- Koriste se **DIREKTNO u Razor markupu**, za margin/padding na MudBlazor komponentama
- Numerirani od 0 do 16 — npr. `mb-4` = 16px, `pt-16` = 64px, `gap-2` = 8px
- **Kada koristiti:** brzi spacing između elemenata u Razor markupu

```razor
<MudPaper Class="pa-4 mb-6">           @* padding 16px, margin-bottom 24px *@
<MudButton Class="mr-2">Odustani       @* margin-right 8px *@
```

### CSS tokeni (`var(--space-4)`, `var(--space-component-md)`)

- Koriste se **ISKLJUČIVO u `app.css`** — unutar CSS klasa
- **Kada koristiti:** kada definišeš novu CSS klasu ili modificiraš shared komponentu

```css
.rbi-paper {
    padding: var(--space-component-lg);     /* 24px iz semantičkog tokena */
    margin-bottom: var(--space-4);          /* 16px iz primitivnog tokena */
}
```

### Zlatno pravilo

**NE pisati** `Style="margin: var(--space-4)"` na MudBlazor komponenti — koristiti `Class="mb-4"`.
**NE pisati** `.my-class { margin: 16px }` u CSS-u — koristiti `var(--space-4)`.

### Zašto dvojni sistem?

MudBlazor utility klase su brzi shorthand za spacing kompoziciju u markupu.
Tokeni su za reusable CSS klase koje treba mijenjati na jednom mjestu.

**Trade-off:** promjena CSS tokena NE propagira automatski na MudBlazor utility klase
(`mb-4` u MudBlazor nije vezan za `--space-4` u našem app.css). Ovo je dokumentirana
odluka, ne bug — usklađenost vrijednosti se održava ručno (oboje su trenutno 16px).

---

## Konvencije za nove shared komponente

1. **Bez `@page` direktive** — stranica postaje ruta, shared komponenta ne
2. **XML komentari** na svim `[Parameter]` propertyima — VS IntelliSense ih prikazuje
3. **`EditorRequired`** za obavezne parametre — kompajler upozorava ako se zaboravi
4. **`string.Empty` kao default** za string parametre (ne `null`) — izbjegava NullReferenceException
5. **Bez direktnih CSS boja u stilu** — koristiti `var(--color-*)` tokene iz `app.css`
6. **Ime fajla = ime komponente** — `PageHeader.razor` → `<PageHeader />`
