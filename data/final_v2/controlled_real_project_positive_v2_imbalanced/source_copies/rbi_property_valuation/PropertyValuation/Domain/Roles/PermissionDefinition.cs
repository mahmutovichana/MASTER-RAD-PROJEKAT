using RBBH.CollateralAppraisal.Domain.Common;

namespace RBBH.CollateralAppraisal.Domain.Roles;

/// <summary>
/// Definicija permissiona iz Permission Catalog-a.
///
/// VAŽNO: Permissioni se NE kreiraju kroz UI.
/// Novi permission se dodaje kroz migraciju/seed (jer mora odgovarati stvarnoj backend akciji).
/// Admin samo bira iz ovog kataloga pri dodjeli permissiona roli.
/// </summary>
public sealed class PermissionDefinition : BaseEntity
{
    /// <summary>Kod permissiona — mora odgovarati konstanti u AppPermissions (npr. "users.view").</summary>
    public string Code { get; private set; } = null!;

    /// <summary>Prikazni naziv za UI.</summary>
    public string DisplayName { get; private set; } = null!;

    public string? Description { get; private set; }

    /// <summary>Modul kojemu permission pripada (Users, Roles, Records, Codebooks, Audit...).</summary>
    public string Module { get; private set; } = null!;

    public bool IsActive { get; private set; }

    // ── Navigacija ────────────────────────────────────────────────────────────
    public ICollection<RolePermission> RolePermissions { get; private set; } = [];

    private PermissionDefinition() { }

    public static PermissionDefinition Create(
        string code, string displayName, string? description, string module)
        => new()
        {
            Code        = code,
            DisplayName = displayName,
            Description = description,
            Module      = module,
            IsActive    = true
        };
}
