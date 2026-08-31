namespace RBBH.CollateralAppraisal.Application.Security.DTOs;

/// <summary>
/// Request za uklanjanje role korisniku.
/// Endpoint: POST /api/roles/remove
/// Policy: AppPolicies.RolesRemove
/// </summary>
public sealed record RemoveRoleRequest(
    string UserId,
    string RoleName
);
