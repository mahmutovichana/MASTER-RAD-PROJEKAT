namespace RBBH.CollateralAppraisal.Application.Users.Models;

/// <summary>
/// Odgovor /api/me endpointaa — sve što frontend treba za inicijalizaciju sesije.
/// </summary>
public record MeDto(
    string?               UserId,
    string?               Username,
    string?               DisplayName,
    string?               Email,
    IReadOnlyList<string> Roles,
    IReadOnlyList<string> Permissions,
    string?               DefaultRoute,
    IReadOnlyList<string> AvailableModules,
    string                UserStatus       // "Active", "Suspended", "NoRole", "UnknownRole"
);
