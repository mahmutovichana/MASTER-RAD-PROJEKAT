namespace RBBH.CollateralAppraisal.Domain.Roles;

/// <summary>Join tabela između RoleDefinition i PermissionDefinition.</summary>
public sealed class RolePermission
{
    public int RoleDefinitionId { get; private set; }
    public int PermissionDefinitionId { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public string? CreatedByUserId { get; private set; }

    // ── Navigacija ────────────────────────────────────────────────────────────
    public RoleDefinition RoleDefinition { get; private set; } = null!;
    public PermissionDefinition PermissionDefinition { get; private set; } = null!;

    private RolePermission() { }

    public static RolePermission Create(int roleId, int permissionId, string? userId, DateTime? now = null)
        => new()
        {
            RoleDefinitionId       = roleId,
            PermissionDefinitionId = permissionId,
            CreatedAt              = now ?? DateTime.UtcNow,
            CreatedByUserId        = userId
        };
}
