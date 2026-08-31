using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Roles;

/// <summary>
/// Definicija role u aplikaciji. Čuva se u SQL Server i sinhronizuje u Keycloak.
///
/// VAŽNO: Ime role mora biti jedinstveno unutar Keycloak realm-a.
/// IsSystem = true → rola ne može biti obrisana (Administrator, Unosnik, Verifikator).
/// IsActive = false → rola ne može biti dodijeljena novim korisnicima.
/// DeletedAt != null → soft delete — rola se ne prikazuje u UI-u.
/// </summary>
public sealed class RoleDefinition : BaseEntity
{
    /// <summary>Naziv role — mora odgovarati imenu u Keycloak (unique).</summary>
    public string Name { get; private set; } = null!;

    /// <summary>Prikazni naziv za UI.</summary>
    public string DisplayName { get; private set; } = null!;

    public string? Description { get; private set; }

    /// <summary>Sistemska rola — ne može se obrisati ni iz UI ni programski.</summary>
    public bool IsSystem { get; private set; }

    /// <summary>Aktivna rola se može dodijeliti korisnicima. Neaktivna ostaje na postojećim korisnicima.</summary>
    public bool IsActive { get; private set; }

    public string? CreatedByUserId { get; private set; }
    public string? UpdatedByUserId { get; private set; }

    // ── Soft delete ───────────────────────────────────────────────────────────
    public DateTime? DeletedAt { get; private set; }
    public string? DeletedByUserId { get; private set; }

    // ── Navigacija ────────────────────────────────────────────────────────────
    public ICollection<RolePermission> Permissions { get; private set; } = [];

    private RoleDefinition() { }

    public static RoleDefinition CreateSystem(string name, string displayName, string? description = null)
        => new()
        {
            Name        = name,
            DisplayName = displayName,
            Description = description,
            IsSystem    = true,
            IsActive    = true
        };

    public static RoleDefinition CreateCustom(
        string name, string displayName, string? description, string? createdByUserId)
        => new()
        {
            Name             = name,
            DisplayName      = displayName,
            Description      = description,
            IsSystem         = false,
            IsActive         = true,
            CreatedByUserId  = createdByUserId
        };

    public void Update(string displayName, string? description, string? userId, DateTime now)
    {
        DisplayName     = displayName;
        Description     = description;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    public void Deactivate(string? userId, DateTime now)
    {
        IsActive        = false;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    public void Activate(string? userId, DateTime now)
    {
        IsActive        = true;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }

    public void SoftDelete(string? userId, DateTime now)
    {
        DeletedAt       = now;
        DeletedByUserId = userId;
        UpdatedByUserId = userId;
        SetUpdatedAt(now);
    }
}
