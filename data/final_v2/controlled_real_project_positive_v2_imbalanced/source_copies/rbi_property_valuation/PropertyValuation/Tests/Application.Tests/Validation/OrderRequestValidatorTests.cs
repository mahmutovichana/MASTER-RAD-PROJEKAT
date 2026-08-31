using FluentAssertions;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Validation;

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — OrderRequestValidator.ValidateCreate
//
// Polja koja se testiraju:
//   clientName, clientType, collateralTypeId/combined, city (BVA 100),
//   branch/city map, branchAddress, contactName, contactPhone,
//   contactEmail, clientIdentifier (JMBG FL/PL), internalNote (BVA 500),
//   propertyAddress (BVA 500), requestReceivedAt/requestSentAt
//
// Konvencija: svaki test provjerava JEDAN aspekt validacije (Equivalence Partitioning)
// ═══════════════════════════════════════════════════════════════

public sealed class OrderRequestValidatorTests
{
    // ── Test Data Builder helper ──────────────────────────────────────────────
    // Vraća validne default vrijednosti za sve obavezne parametre.
    // Pozivač overriduje samo polje koje testira.

    // requestReceivedAt je OBAVEZNO polje — zadani datum osigurava da ostali testovi
    // ne padaju zbog tog polja dok testiraju nešto drugo.
    private static readonly DateTime DefaultReceivedAt =
        new(2026, 1, 15, 10, 0, 0, DateTimeKind.Utc);

    private static CreateOrderRequest Valid(
        string  clientName         = "Amina Aminovic",
        string? clientType         = "FL",
        string? clientIdentifier   = "0101985100129",
        int     collateralTypeId   = 1,
        int?    combined           = null,
        string  city               = "Sarajevo",
        string  branch             = "POS_SARAJEVO_CENTAR",
        string? branchAddress      = "Zmaja od Bosne 74",
        string  contactName        = "Amar Kontakt",
        string  contactPhone       = "061123456",
        string? contactEmail       = "amar@test.ba",
        string? internalNote       = null,
        string  deliveryContact    = "Dostava Dostavlja",
        string  amRecipient        = "AM Primalac",
        string? propertyAddress    = "Obala 1, Sarajevo",
        DateTime? receivedAt       = null,
        DateTime? sentAt           = null)
    {
        return new CreateOrderRequest(
            clientName, clientType, clientIdentifier,
            collateralTypeId, combined,
            city, propertyAddress, branch, branchAddress,
            contactName, contactPhone, contactEmail,
            internalNote, deliveryContact, amRecipient,
            // requestReceivedAt je obavezan — ako nije eksplicitno null, koristimo default
            receivedAt ?? DefaultReceivedAt,
            sentAt);
    }

    private static void ShouldThrow(CreateOrderRequest r, string field, string? code = null)
    {
        var ex = Assert.Throws<RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException>(
            () => OrderRequestValidator.ValidateCreate(r));
        ex.FieldErrors.Should().Contain(e => e.Field == field,
            $"Expected field '{field}' to have a validation error");
        if (code is not null)
            ex.FieldErrors.Should().Contain(e => e.Field == field && e.Code == code,
                $"Expected field '{field}' with code '{code}'");
    }

    private static void ShouldPass(CreateOrderRequest r)
    {
        try
        {
            OrderRequestValidator.ValidateCreate(r);
        }
        catch (RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException ex)
        {
            var details = string.Join("; ",
                ex.FieldErrors.Select(e => $"{e.Field}[{e.Code}]"));
            Assert.Fail($"Expected no validation errors but got: {details}");
        }
    }

    // ── Happy path ────────────────────────────────────────────────────────────

    [Fact]
    public void ValidateCreate_WithAllValidFieldsFL_ShouldPass()
    {
        ShouldPass(Valid());
    }

    [Fact]
    public void ValidateCreate_WithAllValidFieldsPL_ShouldPass()
    {
        // PL: clientIdentifier = tax number (13 cifara)
        ShouldPass(Valid(clientType: "PL", clientIdentifier: "0101985100129"));
    }

    [Fact]
    public void ValidateCreate_WithCombinedCollateral_ShouldPass()
    {
        ShouldPass(Valid(collateralTypeId: 1, combined: 2));
    }

    // ── clientName ────────────────────────────────────────────────────────────

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void ValidateCreate_WithEmptyClientName_ShouldFailRequired(string? name)
    {
        ShouldThrow(Valid(clientName: name!), "clientName", ValidationErrorCodes.RequiredField);
    }

    [Theory]
    [InlineData("Samir Samarovic")]
    [InlineData("Sacir Cengic")]
    [InlineData("Ana-Marija Petrovic")]   // crtica dozvoljena
    [InlineData("X Y")]                   // min 2 znaka s razmakom
    public void ValidateCreate_WithValidClientName_ShouldPass(string name)
    {
        ShouldPass(Valid(clientName: name));
    }

    [Fact]
    public void ValidateCreate_WithClientNameContainingApostrophe_ShouldFailInvalidChars()
    {
        // PersonNameValidator dozvoljava samo slova, razmake i crtice
        // Apostrof (') nije dozvoljeni znak — dokumentovan ponašaj
        ShouldThrow(Valid(clientName: "O'Brien Test"), "clientName");
    }

    // ── clientType ────────────────────────────────────────────────────────────

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("  ")]
    public void ValidateCreate_WithEmptyClientType_ShouldFailRequired(string? type)
    {
        ShouldThrow(Valid(clientType: type), "clientType", ValidationErrorCodes.RequiredClientType);
    }

    [Theory]
    [InlineData("FL")]
    [InlineData("PL")]
    public void ValidateCreate_WithValidClientType_ShouldPass(string type)
    {
        ShouldPass(Valid(clientType: type));
    }

    // ── collateralTypeId + combined ───────────────────────────────────────────

    [Fact]
    public void ValidateCreate_WithNoCollateral_ShouldFailRequired()
    {
        // Ni collateralTypeId ni combined nisu postavljeni
        ShouldThrow(Valid(collateralTypeId: 0, combined: null), "collateralTypeId");
    }

    [Fact]
    public void ValidateCreate_WithOnlyCombinedCollateral_ShouldPass()
    {
        // Ako collateralTypeId=0 ali combined postoji → ok
        ShouldPass(Valid(collateralTypeId: 0, combined: 5));
    }

    [Fact]
    public void ValidateCreate_WithCollateralTypeId1_ShouldPass()
    {
        ShouldPass(Valid(collateralTypeId: 1));
    }

    // ── city — BVA ────────────────────────────────────────────────────────────

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    public void ValidateCreate_WithEmptyCity_ShouldFailRequired(string? city)
    {
        ShouldThrow(Valid(city: city!), "city", ValidationErrorCodes.RequiredField);
    }

    [Fact]
    public void ValidateCreate_WithCityLengthBelowMax_ShouldNotFailLength()
    {
        // BVA: bilo koji grad iz kataloga (Sarajevo = 8 znakova) je << 100.
        // Test osigurava da validni kratki grad ne dobija MaxLengthExceeded grešku.
        // Napomena: test s 100-char gradom nije moguć jer nijedan branch u katalogu
        // ne odgovara 100-char gradu (branch-city constraint bi pao).
        ShouldPass(Valid(city: "Sarajevo", branch: "POS_SARAJEVO_CENTAR"));
    }

    [Fact]
    public void ValidateCreate_WithCity101Chars_ShouldFailMaxLength()
    {
        // BVA: upper boundary + 1
        ShouldThrow(Valid(city: new string('a', 101)), "city", ValidationErrorCodes.MaxLengthExceeded);
    }

    // ── branch / city map ─────────────────────────────────────────────────────

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    public void ValidateCreate_WithEmptyBranch_ShouldFailRequired(string? branch)
    {
        ShouldThrow(Valid(branch: branch!), "branch", ValidationErrorCodes.RequiredField);
    }

    [Fact]
    public void ValidateCreate_WithBranchNotMatchingCity_ShouldFailBranchCityMap()
    {
        // POS_BANJA_LUKA ne pripada Sarajevu
        ShouldThrow(
            Valid(city: "Sarajevo", branch: "POS_BANJA_LUKA"),
            "branch",
            ValidationErrorCodes.InvalidBranchForCity);
    }

    [Fact]
    public void ValidateCreate_WithBranchMatchingCity_ShouldPass()
    {
        ShouldPass(Valid(city: "Sarajevo", branch: "POS_SARAJEVO_CENTAR"));
    }

    [Theory]
    [InlineData("Sarajevo",   "POS_SARAJEVO_CENTAR")]
    [InlineData("Banja Luka", "POS_BANJA_LUKA")]
    [InlineData("Tuzla",      "POS_TUZLA")]
    [InlineData("Mostar",     "POS_MOSTAR")]
    public void ValidateCreate_WithBranchMatchingCity_ShouldPass_MultiCity(string city, string branch)
    {
        ShouldPass(Valid(city: city, branch: branch));
    }

    // ── contactPhone ──────────────────────────────────────────────────────────

    [Theory]
    [InlineData("abc")]
    [InlineData("123")]
    [InlineData("")]
    public void ValidateCreate_WithInvalidPhone_ShouldFailPhone(string phone)
    {
        ShouldThrow(Valid(contactPhone: phone), "contactPhone");
    }

    [Theory]
    [InlineData("061123456")]          // 0 + 8 cifara
    [InlineData("+38761123456")]        // +387 + 8 cifara
    [InlineData("063-123-456")]         // crtice — normalise
    [InlineData("062 111 222")]         // razmaci — normalise
    public void ValidateCreate_WithValidPhone_ShouldPass(string phone)
    {
        ShouldPass(Valid(contactPhone: phone));
    }

    // ── contactEmail ──────────────────────────────────────────────────────────

    [Theory]
    [InlineData("notanemail")]
    [InlineData("missing@")]
    [InlineData("@nodomain")]
    public void ValidateCreate_WithInvalidEmail_ShouldFailEmail(string email)
    {
        ShouldThrow(Valid(contactEmail: email), "contactEmail");
    }

    [Theory]
    [InlineData(null)]
    [InlineData("valid@example.com")]
    [InlineData("user.name+tag@subdomain.example.ba")]
    public void ValidateCreate_WithValidOrNullEmail_ShouldPass(string? email)
    {
        ShouldPass(Valid(contactEmail: email));
    }

    // ── clientIdentifier (JMBG) — FL ─────────────────────────────────────────

    [Theory]
    [InlineData("123")]           // prekratak
    [InlineData("01019851001294")] // predugačak (14)
    [InlineData("abcdefghijklm")] // slova
    public void ValidateCreate_WithInvalidJmbgFL_ShouldFailIdentifier(string identifier)
    {
        ShouldThrow(Valid(clientType: "FL", clientIdentifier: identifier), "clientIdentifier");
    }

    [Fact]
    public void ValidateCreate_WithValid13DigitJmbgFL_ShouldPass()
    {
        ShouldPass(Valid(clientType: "FL", clientIdentifier: "0101985100129"));
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    public void ValidateCreate_WithEmptyJmbgFL_ShouldFailRequired(string? id)
    {
        ShouldThrow(Valid(clientType: "FL", clientIdentifier: id), "clientIdentifier");
    }

    // ── internalNote — BVA 500 ────────────────────────────────────────────────

    [Fact]
    public void ValidateCreate_WithInternalNote500Chars_ShouldPass()
    {
        ShouldPass(Valid(internalNote: new string('x', 500)));
    }

    [Fact]
    public void ValidateCreate_WithInternalNote501Chars_ShouldFailMaxLength()
    {
        ShouldThrow(Valid(internalNote: new string('x', 501)),
            "internalNote", ValidationErrorCodes.MaxLengthExceeded);
    }

    [Fact]
    public void ValidateCreate_WithNullInternalNote_ShouldPass()
    {
        ShouldPass(Valid(internalNote: null));
    }

    // ── propertyAddress — BVA 500 ─────────────────────────────────────────────

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    public void ValidateCreate_WithEmptyPropertyAddress_ShouldFailRequired(string? addr)
    {
        ShouldThrow(Valid(propertyAddress: addr), "propertyAddress");
    }

    [Fact]
    public void ValidateCreate_WithPropertyAddress500Chars_ShouldPass()
    {
        ShouldPass(Valid(propertyAddress: new string('A', 500)));
    }

    [Fact]
    public void ValidateCreate_WithPropertyAddress501Chars_ShouldFailMaxLength()
    {
        ShouldThrow(Valid(propertyAddress: new string('A', 501)),
            "propertyAddress", ValidationErrorCodes.MaxLengthExceeded);
    }

    // ── requestReceivedAt / requestSentAt — date range ────────────────────────

    [Fact]
    public void ValidateCreate_WithReceivedAfterSent_ShouldFailDateRange()
    {
        var sent     = new DateTime(2026, 1, 1, 12, 0, 0, DateTimeKind.Utc);
        var received = sent.AddDays(1); // received AFTER sent — invalid

        ShouldThrow(
            Valid(receivedAt: received, sentAt: sent),
            "requestReceivedAt",
            ValidationErrorCodes.InvalidDateRange);
    }

    [Fact]
    public void ValidateCreate_WithReceivedBeforeSent_ShouldPass()
    {
        var received = new DateTime(2026, 1, 1, 12, 0, 0, DateTimeKind.Utc);
        var sent     = received.AddDays(1);

        ShouldPass(Valid(receivedAt: received, sentAt: sent));
    }

    [Fact]
    public void ValidateCreate_WithReceivedEqualsTo_ShouldPass()
    {
        // Boundary: received == sent je dozvoljeno
        var dt = new DateTime(2026, 1, 15, 10, 0, 0, DateTimeKind.Utc);
        ShouldPass(Valid(receivedAt: dt, sentAt: dt));
    }

    [Fact]
    public void ValidateCreate_WithNullReceivedAt_ShouldFailRequired()
    {
        // requestReceivedAt je OBAVEZNO polje (explicit null test)
        var r = new CreateOrderRequest(
            "Amina", "FL", "0101985100129",
            1, null, "Sarajevo", "Obala 1", "POS_SARAJEVO_CENTAR", "Adresa",
            "Kontakt", "061123456", null, null, "Dostava", "AM",
            null, null); // receivedAt = null → greška

        ShouldThrow(r, "requestReceivedAt", ValidationErrorCodes.RequiredField);
    }
}

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — OrderRequestValidator.ValidateUpdate
//
// ValidateUpdate je partial update — null znači "ne mijenjaj".
// Scenariji:
//  All null fields (no-op update)       → No errors
//  ClientType explicit empty string     → Required error
//  City = 101 chars                     → MaxLength error
//  City = ""                            → Required error
//  Branch = "" (explicit)               → Required error
//  BranchAddress = "" (explicit)        → Required error
//  InternalNote = 501 chars             → MaxLength error
//  PropertyAddress = ""                 → Required error
//  SquareMetersCommercial < 0           → Invalid format
//  SquareMetersResidential < 0          → Invalid format
//  SquareMetersCommercial = 0           → No errors (zero dozvoljeno)
//  Invalid date range                   → Invalid date range
//  effectiveCity/Branch mismatch        → Branch-city error
// ═══════════════════════════════════════════════════════════════

public sealed class OrderRequestValidatorUpdateTests
{
    // Helper: UpdateOrderRequest s all-null poljem (no-op)
    private static UpdateOrderRequest Null() =>
        new(null, null, null, null, null, null, null, null, null,
            null, null, null, null);

    private static void ShouldPassUpdate(UpdateOrderRequest r,
        string? effectiveClientType = "FL",
        string? effectiveCity = null,
        string? effectiveBranch = null)
    {
        try
        {
            OrderRequestValidator.ValidateUpdate(r, effectiveClientType, effectiveCity, effectiveBranch);
        }
        catch (RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException ex)
        {
            var details = string.Join("; ", ex.FieldErrors.Select(e => $"{e.Field}[{e.Code}]"));
            Assert.Fail($"Expected no update validation errors but got: {details}");
        }
    }

    private static void ShouldThrowUpdate(UpdateOrderRequest r,
        string field, string? code = null,
        string? effectiveClientType = "FL",
        string? effectiveCity = null,
        string? effectiveBranch = null)
    {
        var ex = Assert.Throws<RBBH.CollateralAppraisal.Application.Common.Exceptions.ValidationException>(
            () => OrderRequestValidator.ValidateUpdate(r, effectiveClientType, effectiveCity, effectiveBranch));
        ex.FieldErrors.Should().Contain(e => e.Field == field,
            $"Expected field '{field}' to have an error");
        if (code is not null)
            ex.FieldErrors.Should().Contain(e => e.Field == field && e.Code == code,
                $"Expected field '{field}' with code '{code}'");
    }

    // ── Happy path: null polja (partial update bez izmjena) ───────────────────

    [Fact]
    public void ValidateUpdate_WithAllNullFields_ShouldPass()
    {
        // Null = "ne mijenjaj ovo polje" — nema grešaka
        ShouldPassUpdate(Null());
    }

    [Fact]
    public void ValidateUpdate_WithValidPartialFields_ShouldPass()
    {
        var r = Null() with { ContactPhone = "061123456", ContactEmail = "novi@test.ba" };
        ShouldPassUpdate(r);
    }

    // ── clientType — explicit empty ───────────────────────────────────────────

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    public void ValidateUpdate_WithExplicitEmptyClientType_ShouldFailRequired(string emptyType)
    {
        // Null = ne mijenjaj; explicit empty = greška
        var r = Null() with { ClientType = emptyType };
        ShouldThrowUpdate(r, "clientType", ValidationErrorCodes.RequiredClientType);
    }

    [Fact]
    public void ValidateUpdate_WithNullClientType_ShouldPass()
    {
        ShouldPassUpdate(Null() with { ClientType = null });
    }

    // ── city — BVA ───────────────────────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithEmptyCity_ShouldFailRequired()
    {
        ShouldThrowUpdate(Null() with { City = "" }, "city", ValidationErrorCodes.RequiredField);
    }

    [Fact]
    public void ValidateUpdate_WithCity101Chars_ShouldFailMaxLength()
    {
        ShouldThrowUpdate(Null() with { City = new string('a', 101) },
            "city", ValidationErrorCodes.MaxLengthExceeded);
    }

    [Fact]
    public void ValidateUpdate_WithCity100Chars_ShouldPass()
    {
        // BVA: upper boundary — city 100 chars bez branch-city provjere
        ShouldPassUpdate(Null() with { City = new string('a', 100) });
    }

    // ── branch — explicit empty ───────────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithExplicitEmptyBranch_ShouldFailRequired()
    {
        ShouldThrowUpdate(Null() with { Branch = "" }, "branch", ValidationErrorCodes.RequiredField);
    }

    [Fact]
    public void ValidateUpdate_WithNullBranch_ShouldPass()
    {
        ShouldPassUpdate(Null() with { Branch = null });
    }

    // ── branch-city mismatch kada je effectiveCity i Branch dostupan ──────────

    [Fact]
    public void ValidateUpdate_WithBranchCityMismatch_WhenEffectiveValuesProvided_ShouldFail()
    {
        // effectiveCity = "Sarajevo", branch je POS_BANJA_LUKA → mismatch
        var r = Null() with { Branch = "POS_BANJA_LUKA" };
        ShouldThrowUpdate(r, "branch", ValidationErrorCodes.InvalidBranchForCity,
            effectiveCity: "Sarajevo", effectiveBranch: "POS_BANJA_LUKA");
    }

    [Fact]
    public void ValidateUpdate_WithBranchCityMatch_ShouldPass()
    {
        var r = Null() with { Branch = "POS_SARAJEVO_CENTAR" };
        ShouldPassUpdate(r, effectiveCity: "Sarajevo", effectiveBranch: "POS_SARAJEVO_CENTAR");
    }

    [Fact]
    public void ValidateUpdate_WithoutEffectiveValues_SkipsBranchCityCheck()
    {
        // Ako effectiveCity/Branch nisu proslijeđeni, provjera se preskače
        var r = Null() with { Branch = "POS_BANJA_LUKA" };
        ShouldPassUpdate(r, effectiveCity: null, effectiveBranch: null);
    }

    // ── branchAddress — explicit empty ────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithExplicitEmptyBranchAddress_ShouldFailRequired()
    {
        ShouldThrowUpdate(Null() with { BranchAddress = "" },
            "branchAddress", ValidationErrorCodes.RequiredField);
    }

    // ── internalNote — BVA 500 ────────────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithInternalNote500Chars_ShouldPass()
    {
        ShouldPassUpdate(Null() with { InternalNote = new string('x', 500) });
    }

    [Fact]
    public void ValidateUpdate_WithInternalNote501Chars_ShouldFailMaxLength()
    {
        ShouldThrowUpdate(Null() with { InternalNote = new string('x', 501) },
            "internalNote", ValidationErrorCodes.MaxLengthExceeded);
    }

    // ── propertyAddress ───────────────────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithExplicitEmptyPropertyAddress_ShouldFailRequired()
    {
        ShouldThrowUpdate(Null() with { PropertyAddress = "" },
            "propertyAddress", ValidationErrorCodes.RequiredField);
    }

    [Fact]
    public void ValidateUpdate_WithPropertyAddress500Chars_ShouldPass()
    {
        ShouldPassUpdate(Null() with { PropertyAddress = new string('A', 500) });
    }

    // ── squareMeters — negative values ────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithNegativeSquareMetersCommercial_ShouldFail()
    {
        ShouldThrowUpdate(Null() with { SquareMetersCommercial = -1m },
            "squareMetersCommercial", ValidationErrorCodes.InvalidFormat);
    }

    [Fact]
    public void ValidateUpdate_WithNegativeSquareMetersResidential_ShouldFail()
    {
        ShouldThrowUpdate(Null() with { SquareMetersResidential = -0.01m },
            "squareMetersResidential", ValidationErrorCodes.InvalidFormat);
    }

    [Fact]
    public void ValidateUpdate_WithZeroSquareMeters_ShouldPass()
    {
        // BVA: nula je dozvoljena (0 m² = polje je poznato ali prazno)
        ShouldPassUpdate(Null() with { SquareMetersCommercial = 0m, SquareMetersResidential = 0m });
    }

    [Fact]
    public void ValidateUpdate_WithPositiveSquareMeters_ShouldPass()
    {
        ShouldPassUpdate(Null() with { SquareMetersCommercial = 150.5m, SquareMetersResidential = 80m });
    }

    // ── date range ────────────────────────────────────────────────────────────

    [Fact]
    public void ValidateUpdate_WithReceivedAfterSent_ShouldFailDateRange()
    {
        var sent     = new DateTime(2026, 1, 1, 10, 0, 0, DateTimeKind.Utc);
        var received = sent.AddDays(1);
        ShouldThrowUpdate(Null() with { RequestReceivedAt = received, RequestSentAt = sent },
            "requestReceivedAt", ValidationErrorCodes.InvalidDateRange);
    }

    [Fact]
    public void ValidateUpdate_WithOnlyReceivedAt_ShouldPass()
    {
        // Samo receivedAt bez sentAt → ne može biti range greška
        ShouldPassUpdate(Null() with
        {
            RequestReceivedAt = new DateTime(2026, 1, 1, 10, 0, 0, DateTimeKind.Utc)
        });
    }
}
