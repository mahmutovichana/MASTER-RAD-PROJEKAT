namespace RBBH.CollateralAppraisal.Application.Roles.Requests;

public sealed record CreateRoleRequest(
    string  Name,
    string  DisplayName,
    string? Description);

public sealed record UpdateRoleRequest(
    string  DisplayName,
    string? Description);

public sealed record AddPermissionToRoleRequest(int PermissionDefinitionId);

public sealed record RoleQueryRequest(
    string? Search   = null,
    bool?   IsActive = null,
    int     Page     = 1,
    int     PageSize = 20);

public sealed record AuditQueryRequest(
    string? ActorUserId    = null,
    string? ActorUsername  = null,
    /// <summary>Filtrira po ActiveRole (rola pod kojom je akcija izvršena), fallback ActorRole.</summary>
    string? ActorRole      = null,
    string? Module         = null,
    string? Action         = null,
    string? EntityType     = null,
    string? EntityKey      = null,
    string? Status         = null,
    string? Severity       = null,
    string? Search         = null,
    DateTime? From         = null,
    DateTime? To           = null,
    int     Page           = 1,
    int     PageSize       = 50);
