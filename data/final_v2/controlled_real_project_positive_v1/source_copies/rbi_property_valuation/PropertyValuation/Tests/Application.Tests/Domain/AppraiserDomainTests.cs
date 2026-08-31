using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Domain.Orders;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Domain;

public sealed class AppraiserDomainTests
{
    // ── CanHandleCity (existing) ─────────────────────────────────────────────

    [Fact]
    public void CanHandleCity_NullSupportedCities_MatchesByPrimaryCity()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Individual, null, null, null);

        Assert.True(a.CanHandleCity("Sarajevo"));
        Assert.True(a.CanHandleCity("SARAJEVO"));
        Assert.False(a.CanHandleCity("Mostar"));
    }

    [Fact]
    public void CanHandleCity_WithSupportedCities_MatchesAnyListedCity()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Firm, null, null, null,
            supportedCities: "Sarajevo,Mostar,Tuzla");

        Assert.True(a.CanHandleCity("Sarajevo"));
        Assert.True(a.CanHandleCity("mostar"));
        Assert.True(a.CanHandleCity("TUZLA"));
        Assert.False(a.CanHandleCity("Banja Luka"));
    }

    [Fact]
    public void CanHandleCity_NullCity_ReturnsTrue()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Individual, null, null, null);

        Assert.True(a.CanHandleCity(null));
        Assert.True(a.CanHandleCity(""));
    }

    [Fact]
    public void CanHandleCity_NoPrimaryAndNoSupportedCities_ReturnsTrue()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);

        Assert.True(a.CanHandleCity("Sarajevo"));
    }

    [Fact]
    public void Create_WithSupportedCities_StoresValue()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Firm, null, null, null,
            supportedCities: "Sarajevo,Banja Luka");

        Assert.Equal("Sarajevo,Banja Luka", a.SupportedCities);
    }

    [Fact]
    public void CanHandleCity_WhitespaceOnlyCity_ReturnsTrue()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Individual, null, null, null);
        Assert.True(a.CanHandleCity("   "));
    }

    [Fact]
    public void CanHandleCity_SupportedCitiesWithSpaces_TrimsAndMatches()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Individual, null, null, null,
            supportedCities: " Sarajevo , Mostar , Tuzla ");

        Assert.True(a.CanHandleCity("Sarajevo"));
        Assert.True(a.CanHandleCity("Mostar"));
        Assert.True(a.CanHandleCity("Tuzla"));
    }

    // ── Create ───────────────────────────────────────────────────────────────

    [Fact]
    public void Create_AllFields_SetsAllProperties()
    {
        var a = Appraiser.Create(
            name: "Marko Markovic",
            city: "Mostar",
            legalForm: AppraiserLegalForm.Firm,
            contactEmail: "marko@test.com",
            contactPhone: "+38761111222",
            notes: "Biljeska",
            clientScope: AppraiserClientScope.PravnaLica,
            supportedPropertyTypes: "STAN,KUCA",
            supportedCities: "Mostar,Sarajevo");

        Assert.Equal("Marko Markovic", a.Name);
        Assert.Equal("Mostar", a.City);
        Assert.Equal(AppraiserLegalForm.Firm, a.LegalForm);
        Assert.Equal("marko@test.com", a.ContactEmail);
        Assert.Equal("+38761111222", a.ContactPhone);
        Assert.Equal("Biljeska", a.Notes);
        Assert.Equal(AppraiserClientScope.PravnaLica, a.ClientScope);
        Assert.Equal("STAN,KUCA", a.SupportedPropertyTypes);
        Assert.Equal("Mostar,Sarajevo", a.SupportedCities);
        Assert.True(a.IsActive);
        Assert.False(a.IsOnLeave);
        Assert.False(a.IsBlacklisted);
    }

    [Fact]
    public void Create_MinimalFields_DefaultsClientScopeToSve()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);

        Assert.Equal(AppraiserClientScope.Sve, a.ClientScope);
        Assert.Null(a.SupportedPropertyTypes);
        Assert.Null(a.SupportedCities);
        Assert.Null(a.City);
        Assert.Null(a.ContactEmail);
        Assert.Null(a.ContactPhone);
        Assert.Null(a.Notes);
        Assert.True(a.IsActive);
    }

    // ── UpdateDetails ────────────────────────────────────────────────────────

    [Fact]
    public void UpdateDetails_ChangesAllFields()
    {
        var a = Appraiser.Create("Old", "Sarajevo", AppraiserLegalForm.Individual, "old@test.com", "111", "old notes");
        var now = new DateTime(2026, 6, 1, 12, 0, 0, DateTimeKind.Utc);

        a.UpdateDetails(
            name: "New Name",
            city: "Tuzla",
            legalForm: AppraiserLegalForm.Firm,
            contactEmail: "new@test.com",
            contactPhone: "222",
            notes: "new notes",
            now: now,
            clientScope: AppraiserClientScope.FizickaLica,
            supportedPropertyTypes: "POSLOVNI_PROSTOR",
            supportedCities: "Tuzla,Zenica");

        Assert.Equal("New Name", a.Name);
        Assert.Equal("Tuzla", a.City);
        Assert.Equal(AppraiserLegalForm.Firm, a.LegalForm);
        Assert.Equal("new@test.com", a.ContactEmail);
        Assert.Equal("222", a.ContactPhone);
        Assert.Equal("new notes", a.Notes);
        Assert.Equal(AppraiserClientScope.FizickaLica, a.ClientScope);
        Assert.Equal("POSLOVNI_PROSTOR", a.SupportedPropertyTypes);
        Assert.Equal("Tuzla,Zenica", a.SupportedCities);
        Assert.Equal(now, a.UpdatedAt);
    }

    [Fact]
    public void UpdateDetails_NullClientScope_KeepsExistingScope()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.PravnaLica);
        var now = DateTime.UtcNow;

        a.UpdateDetails("Updated", null, AppraiserLegalForm.Individual, null, null, null, now,
            clientScope: null);

        Assert.Equal(AppraiserClientScope.PravnaLica, a.ClientScope);
    }

    [Fact]
    public void UpdateDetails_ExplicitClientScope_OverridesExisting()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.PravnaLica);
        var now = DateTime.UtcNow;

        a.UpdateDetails("Updated", null, AppraiserLegalForm.Individual, null, null, null, now,
            clientScope: AppraiserClientScope.FizickaLica);

        Assert.Equal(AppraiserClientScope.FizickaLica, a.ClientScope);
    }

    [Fact]
    public void UpdateDetails_ClearsOptionalFieldsToNull()
    {
        var a = Appraiser.Create("Test", "Sarajevo", AppraiserLegalForm.Individual,
            "email@test.com", "+387", "notes",
            supportedPropertyTypes: "STAN",
            supportedCities: "Sarajevo");
        var now = DateTime.UtcNow;

        a.UpdateDetails("Test", null, AppraiserLegalForm.Individual, null, null, null, now,
            supportedPropertyTypes: null,
            supportedCities: null);

        Assert.Null(a.City);
        Assert.Null(a.ContactEmail);
        Assert.Null(a.ContactPhone);
        Assert.Null(a.Notes);
        Assert.Null(a.SupportedPropertyTypes);
        Assert.Null(a.SupportedCities);
    }

    // ── CanHandle (WorkflowType) ─────────────────────────────────────────────

    [Fact]
    public void CanHandle_ScopeIsSve_ReturnsTrueForAll()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.Sve);

        Assert.True(a.CanHandle(WorkflowType.FizickaLica));
        Assert.True(a.CanHandle(WorkflowType.PravnaLica));
        Assert.True(a.CanHandle(null));
    }

    [Fact]
    public void CanHandle_ScopeIsFizickaLica_OnlyMatchesFL()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.FizickaLica);

        Assert.True(a.CanHandle(WorkflowType.FizickaLica));
        Assert.False(a.CanHandle(WorkflowType.PravnaLica));
    }

    [Fact]
    public void CanHandle_ScopeIsPravnaLica_OnlyMatchesPL()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.PravnaLica);

        Assert.False(a.CanHandle(WorkflowType.FizickaLica));
        Assert.True(a.CanHandle(WorkflowType.PravnaLica));
    }

    [Fact]
    public void CanHandle_ScopeIsFizickaLica_NullWorkflow_ReturnsTrue()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.FizickaLica);

        Assert.True(a.CanHandle(null));
    }

    [Fact]
    public void CanHandle_ScopeIsPravnaLica_NullWorkflow_ReturnsFalse()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            clientScope: AppraiserClientScope.PravnaLica);

        Assert.False(a.CanHandle(null));
    }

    // ── CanHandlePropertyType ────────────────────────────────────────────────

    [Fact]
    public void CanHandlePropertyType_NullSupportedTypes_ReturnsTrue()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);

        Assert.True(a.CanHandlePropertyType("STAN"));
        Assert.True(a.CanHandlePropertyType(null));
        Assert.True(a.CanHandlePropertyType(""));
    }

    [Fact]
    public void CanHandlePropertyType_WithSupportedTypes_MatchesListed()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            supportedPropertyTypes: "STAN,KUCA,POSLOVNI_PROSTOR");

        Assert.True(a.CanHandlePropertyType("STAN"));
        Assert.True(a.CanHandlePropertyType("stan"));
        Assert.True(a.CanHandlePropertyType("KUCA"));
        Assert.True(a.CanHandlePropertyType("POSLOVNI_PROSTOR"));
        Assert.False(a.CanHandlePropertyType("GARAZA"));
    }

    [Fact]
    public void CanHandlePropertyType_WithSupportedTypes_NullCodeReturnsTrue()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            supportedPropertyTypes: "STAN");

        Assert.True(a.CanHandlePropertyType(null));
        Assert.True(a.CanHandlePropertyType(""));
        Assert.True(a.CanHandlePropertyType("  "));
    }

    [Fact]
    public void CanHandlePropertyType_SupportedTypesWithSpaces_TrimsAndMatches()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null,
            supportedPropertyTypes: " STAN , KUCA ");

        Assert.True(a.CanHandlePropertyType("STAN"));
        Assert.True(a.CanHandlePropertyType("KUCA"));
    }

    // ── SetOnLeave ───────────────────────────────────────────────────────────

    [Fact]
    public void SetOnLeave_True_SetsIsOnLeaveAndUpdatedAt()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);
        var now = new DateTime(2026, 7, 1, 10, 0, 0, DateTimeKind.Utc);

        a.SetOnLeave(true, now);

        Assert.True(a.IsOnLeave);
        Assert.Equal(now, a.UpdatedAt);
    }

    [Fact]
    public void SetOnLeave_False_ClearsIsOnLeave()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);
        var now = DateTime.UtcNow;
        a.SetOnLeave(true, now);

        var later = now.AddHours(1);
        a.SetOnLeave(false, later);

        Assert.False(a.IsOnLeave);
        Assert.Equal(later, a.UpdatedAt);
    }

    // ── SetBlacklisted ───────────────────────────────────────────────────────

    [Fact]
    public void SetBlacklisted_True_SetsIsBlacklistedAndUpdatedAt()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);
        var now = new DateTime(2026, 7, 1, 10, 0, 0, DateTimeKind.Utc);

        a.SetBlacklisted(true, now);

        Assert.True(a.IsBlacklisted);
        Assert.Equal(now, a.UpdatedAt);
    }

    [Fact]
    public void SetBlacklisted_False_ClearsIsBlacklisted()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);
        var now = DateTime.UtcNow;
        a.SetBlacklisted(true, now);

        var later = now.AddHours(1);
        a.SetBlacklisted(false, later);

        Assert.False(a.IsBlacklisted);
        Assert.Equal(later, a.UpdatedAt);
    }

    // ── Deactivate ───────────────────────────────────────────────────────────

    [Fact]
    public void Deactivate_SetsIsActiveFalseAndUpdatedAt()
    {
        var a = Appraiser.Create("Test", null, AppraiserLegalForm.Individual, null, null, null);
        Assert.True(a.IsActive);

        var now = new DateTime(2026, 7, 1, 10, 0, 0, DateTimeKind.Utc);
        a.Deactivate(now);

        Assert.False(a.IsActive);
        Assert.Equal(now, a.UpdatedAt);
    }

    // ── Enum values ──────────────────────────────────────────────────────────

    [Fact]
    public void AppraiserLegalForm_HasExpectedValues()
    {
        Assert.Equal(0, (int)AppraiserLegalForm.Individual);
        Assert.Equal(1, (int)AppraiserLegalForm.Firm);
    }

    [Fact]
    public void AppraiserClientScope_HasExpectedValues()
    {
        Assert.Equal(0, (int)AppraiserClientScope.Sve);
        Assert.Equal(1, (int)AppraiserClientScope.FizickaLica);
        Assert.Equal(2, (int)AppraiserClientScope.PravnaLica);
    }
}
