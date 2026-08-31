using RBBH.TestAutomation.Api.DTO;

namespace UnitTests.Sifarnici;

/// <summary>
/// Testovi za DTO konstante šifarnika.
///
/// Svrha: "lock" na string vrijednosti koje idu direktno u SQL Server bazu
/// (audit_log.action, audit_log.entity_type). Ako neko promijeni konstantu,
/// baza prestaje pravilno upisivati zapise — test odmah pukne i upozori.
/// </summary>
public class SifarnikDtoTests
{
    // ── AuditActions ──────────────────────────────────────────────────────────
    // Moraju odgovarati CHECK constraint-u u init.sql:
    //   CHECK (action IN ('CREATE', 'UPDATE', 'DELETE'))

    [Fact]
    public void AuditActions_Create_MatchesDatabaseConstraint()
    {
        Assert.Equal("CREATE", AuditActions.Create);
    }

    [Fact]
    public void AuditActions_Update_MatchesDatabaseConstraint()
    {
        Assert.Equal("UPDATE", AuditActions.Update);
    }

    [Fact]
    public void AuditActions_Delete_MatchesDatabaseConstraint()
    {
        Assert.Equal("DELETE", AuditActions.Delete);
    }

    [Fact]
    public void AuditActions_AllValuesAreUpperCase()
    {
        Assert.Equal(AuditActions.Create, AuditActions.Create.ToUpperInvariant());
        Assert.Equal(AuditActions.Update, AuditActions.Update.ToUpperInvariant());
        Assert.Equal(AuditActions.Delete, AuditActions.Delete.ToUpperInvariant());
    }

    [Fact]
    public void AuditActions_AllValuesAreDistinct()
    {
        var values = new[] { AuditActions.Create, AuditActions.Update, AuditActions.Delete };
        Assert.Equal(values.Length, values.Distinct().Count());
    }

    // ── AuditEntityTypes ──────────────────────────────────────────────────────
    // Moraju odgovarati string vrijednostima koje se čuvaju u audit_log.entity_type.

    [Fact]
    public void AuditEntityTypes_SifarnikVrijednost_IsCorrectString()
    {
        Assert.Equal("sifarnik_vrijednost", AuditEntityTypes.SifarnikVrijednost);
    }

    [Fact]
    public void AuditEntityTypes_SifarnikKategorija_IsCorrectString()
    {
        Assert.Equal("sifarnik_kategorija", AuditEntityTypes.SifarnikKategorija);
    }

    [Fact]
    public void AuditEntityTypes_RoleAssignment_IsCorrectString()
    {
        Assert.Equal("role_assignment", AuditEntityTypes.RoleAssignment);
    }

    [Fact]
    public void AuditEntityTypes_AllValuesAreLowerCase()
    {
        Assert.Equal(AuditEntityTypes.SifarnikVrijednost,
            AuditEntityTypes.SifarnikVrijednost.ToLowerInvariant());
        Assert.Equal(AuditEntityTypes.SifarnikKategorija,
            AuditEntityTypes.SifarnikKategorija.ToLowerInvariant());
        Assert.Equal(AuditEntityTypes.RoleAssignment,
            AuditEntityTypes.RoleAssignment.ToLowerInvariant());
    }

    [Fact]
    public void AuditEntityTypes_AllValuesAreDistinct()
    {
        var values = new[]
        {
            AuditEntityTypes.SifarnikVrijednost,
            AuditEntityTypes.SifarnikKategorija,
            AuditEntityTypes.RoleAssignment,
        };
        Assert.Equal(values.Length, values.Distinct().Count());
    }
}
