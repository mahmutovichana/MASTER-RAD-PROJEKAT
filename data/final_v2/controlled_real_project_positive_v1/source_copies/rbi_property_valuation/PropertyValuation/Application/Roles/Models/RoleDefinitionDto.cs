namespace RBBH.CollateralAppraisal.Application.Roles.Models;

public sealed record RoleDefinitionDto(
    int      Id,
    string   Name,
    string   DisplayName,
    string?  Description,
    bool     IsSystem,
    bool     IsActive,
    bool     IsDeleted,
    DateTime CreatedAt,
    string?  CreatedByUserId,
    DateTime UpdatedAt,
    string?  UpdatedByUserId,
    IReadOnlyList<PermissionDefinitionDto> Permissions);

public sealed record RoleDefinitionListItemDto(
    int     Id,
    string  Name,
    string  DisplayName,
    string? Description,
    bool    IsSystem,
    bool    IsActive,
    int     PermissionCount,
    int     UserCount);

public sealed record PermissionDefinitionDto(
    int     Id,
    string  Code,
    string  DisplayName,
    string? Description,
    string  Module,
    bool    IsActive);

public sealed record AuditLogDto(
    long     Id,
    DateTime TimestampUtc,
    string?  ActorUserId,
    string?  ActorUsername,
    string?  ActorEmail,
    string?  ActorFullName,
    string?  ActorRole,
    string?  ActiveRole,
    string   Action,
    string   OperationType,
    string   Module,
    string?  EntityType,
    string?  EntityKey,
    string?  EntityDisplayName,
    string?  OldValuesJson,
    string?  NewValuesJson,
    string?  ChangedFieldsJson,
    string   Status,
    string   Severity,
    string?  Reason,
    string?  CorrelationId,
    string?  RequestPath,
    string?  IpAddress,
    string?  UserAgent);
