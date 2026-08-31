namespace RBBH.CollateralAppraisal.Application.Security.DTOs;

/// <summary>
/// Request za dodjelu role korisniku.
/// Endpoint: POST /api/roles/assign
/// Policy: AppPolicies.RolesAssign
/// </summary>
public sealed record AssignRoleRequest(
    string UserId,
    string RoleName
);
