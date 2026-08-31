using System.Diagnostics.CodeAnalysis;
using RBBH.CollateralAppraisal.Application.Documents.Dtos;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Application.Appraisers.Dtos;

/// <summary>Vještak — master-data zapis (Faza C).</summary>
[ExcludeFromCodeCoverage]
public sealed record AppraiserDto(
    int Id,
    string Name,
    string? City,
    string LegalForm,
    bool IsOnLeave,
    bool IsBlacklisted,
    bool IsActive,
    int ActiveAssignmentCount,
    string? ContactEmail,
    string? ContactPhone,
    string? Notes,
    string? SupportedPropertyTypes,
    DateTime CreatedAt,
    DateTime? UpdatedAt,
    string? SupportedCities = null,
    string ClientScope = "Sve");

[ExcludeFromCodeCoverage]
public sealed record CreateAppraiserRequest(
    string Name,
    string? City,
    string LegalForm,
    string? ContactEmail,
    string? ContactPhone,
    string? Notes,
    string? SupportedPropertyTypes = null,
    string? SupportedCities = null,
    string ClientScope = "Sve");

[ExcludeFromCodeCoverage]
public sealed record UpdateAppraiserRequest(
    string Name,
    string? City,
    string LegalForm,
    string? ContactEmail,
    string? ContactPhone,
    string? Notes,
    string? SupportedPropertyTypes = null,
    string? SupportedCities = null,
    string? ClientScope = null);

[ExcludeFromCodeCoverage]
public sealed record SetAppraiserFlagRequest(bool Value);

[ExcludeFromCodeCoverage]
public sealed record AppraiserListQuery(
    string? Search     = null,
    string? City       = null,
    bool?   OnLeave    = null,
    bool?   Blacklisted = null,
    bool?   Active     = null,
    int     Page       = 1,
    int     PageSize   = 50);

/// <summary>Rezultat odabira vještaka za narudžbu (automatski FL ili ručni PL — Faza C/D).</summary>
public sealed record AppraiserAssignmentResultDto(
    int OrderId,
    string OrderNumber,
    string Status,
    int StatusCode,
    int AppraiserId,
    string AppraiserName,
    string? AppraiserCity,
    bool NotificationSent,
    string Message);

/// <summary>Rezultat slanja narudžbe odabranom vještaku (Faza D).</summary>
public sealed record SendToAppraiserResultDto(
    int OrderId,
    string OrderNumber,
    string Status,
    int StatusCode,
    int AppraiserId,
    string AppraiserName,
    string? AppraiserEmail,
    bool NotificationSent,
    string Message);

/// <summary>Zahtjev za odbijanje narudžbe od strane vještaka.</summary>
[ExcludeFromCodeCoverage]
public sealed record RejectByAppraiserRequest(
    AppraiserDeclineReason Reason,
    string? FreeText);

/// <summary>Paket dokumenata za odabranog vještaka — lista download linkova (Faza D).</summary>
[ExcludeFromCodeCoverage]
public sealed record AppraiserPackageDto(
    int OrderId,
    string OrderNumber,
    int AppraiserId,
    string AppraiserName,
    string? AppraiserEmail,
    IReadOnlyList<DocumentDto> Documents);
