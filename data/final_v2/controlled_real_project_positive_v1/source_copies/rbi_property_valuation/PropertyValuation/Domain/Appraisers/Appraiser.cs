using RBBH.CollateralAppraisal.Domain.Common;
using RBBH.CollateralAppraisal.Domain.Orders;

namespace RBBH.CollateralAppraisal.Domain.Appraisers;

/// <summary>
/// Vještak (procjenitelj nekretnina) — master-data entitet koji administrira CA.
/// Vještak nema korisnički nalog/login; komunikacija ide preko kontakt podataka (US-93 Faza C/D).
///
/// NAPOMENA o imenovanju: <see cref="AppraiserLegalForm"/> (Individual/Firm) je drugačija osa
/// od <c>AppraisalOrder.ClientType</c> "FL/PL" (klijent banke) — ne mješati.
/// </summary>
public sealed class Appraiser : BaseEntity
{
    public string Name { get; private set; } = null!;
    public string? City { get; private set; }
    public AppraiserLegalForm LegalForm { get; private set; }

    /// <summary>
    /// Koju vrstu klijenata banke vještak smije procjenjivati (FL/PL/oboje).
    /// Određuje da li mu CA smije dodijeliti narudžbu — PL vještak ne dobija FL i obrnuto.
    /// </summary>
    public AppraiserClientScope ClientScope { get; private set; }

    /// <summary>
    /// Tipovi nekretnina koje vještak pokriva (kodovi iz šifarnika tipovi_nekretnina,
    /// npr. "STAN,KUCA,POSLOVNI_PROSTOR"). Null = pokriva sve tipove.
    /// </summary>
    public string? SupportedPropertyTypes { get; private set; }

    /// <summary>
    /// Gradovi u kojima vještak može raditi procjene (npr. "SARAJEVO,MOSTAR,TUZLA").
    /// Null = pokriva sve gradove. Spec prilog 4: šifarnik vještaka — vještaci prema gradu.
    /// </summary>
    public string? SupportedCities { get; private set; }

    public bool IsOnLeave { get; private set; }
    public bool IsBlacklisted { get; private set; }
    public string? ContactEmail { get; private set; }
    public string? ContactPhone { get; private set; }
    public string? Notes { get; private set; }
    public bool IsActive { get; private set; }

    private Appraiser() { }

    public static Appraiser Create(
        string name,
        string? city,
        AppraiserLegalForm legalForm,
        string? contactEmail,
        string? contactPhone,
        string? notes,
        AppraiserClientScope clientScope = AppraiserClientScope.Sve,
        string? supportedPropertyTypes = null,
        string? supportedCities = null)
    {
        return new Appraiser
        {
            Name                   = name,
            City                   = city,
            LegalForm              = legalForm,
            ClientScope            = clientScope,
            SupportedPropertyTypes = supportedPropertyTypes,
            SupportedCities        = supportedCities,
            ContactEmail           = contactEmail,
            ContactPhone           = contactPhone,
            Notes                  = notes,
            IsActive               = true
        };
    }

    public void UpdateDetails(
        string name,
        string? city,
        AppraiserLegalForm legalForm,
        string? contactEmail,
        string? contactPhone,
        string? notes,
        DateTime now,
        AppraiserClientScope? clientScope = null,
        string? supportedPropertyTypes = null,
        string? supportedCities = null)
    {
        Name                   = name;
        City                   = city;
        LegalForm              = legalForm;
        if (clientScope.HasValue) ClientScope = clientScope.Value;
        SupportedPropertyTypes = supportedPropertyTypes;
        SupportedCities        = supportedCities;
        ContactEmail           = contactEmail;
        ContactPhone           = contactPhone;
        Notes                  = notes;
        SetUpdatedAt(now);
    }

    /// <summary>Vraća true ako vještak smije procjenjivati datu vrstu klijenta (FL/PL).</summary>
    public bool CanHandle(WorkflowType? workflowType)
    {
        if (ClientScope == AppraiserClientScope.Sve) return true;
        return workflowType == RBBH.CollateralAppraisal.Domain.Orders.WorkflowType.PravnaLica
            ? ClientScope == AppraiserClientScope.PravnaLica
            : ClientScope == AppraiserClientScope.FizickaLica;
    }

    /// <summary>Vraća true ako vještak pokriva dati grad (null SupportedCities = pokriva sve, fallback na City).</summary>
    public bool CanHandleCity(string? city)
    {
        if (string.IsNullOrWhiteSpace(city)) return true;
        if (!string.IsNullOrWhiteSpace(SupportedCities))
        {
            return SupportedCities
                .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                .Contains(city, StringComparer.OrdinalIgnoreCase);
        }
        return string.IsNullOrWhiteSpace(City) || string.Equals(City, city, StringComparison.OrdinalIgnoreCase);
    }

    /// <summary>Vraća true ako vještak pokriva dati tip nekretnine (null = pokriva sve).</summary>
    public bool CanHandlePropertyType(string? propertyTypeCode)
    {
        if (string.IsNullOrWhiteSpace(SupportedPropertyTypes)) return true;
        if (string.IsNullOrWhiteSpace(propertyTypeCode)) return true;
        return SupportedPropertyTypes
            .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Contains(propertyTypeCode, StringComparer.OrdinalIgnoreCase);
    }

    public void SetOnLeave(bool value, DateTime now)
    {
        IsOnLeave = value;
        SetUpdatedAt(now);
    }

    public void SetBlacklisted(bool value, DateTime now)
    {
        IsBlacklisted = value;
        SetUpdatedAt(now);
    }

    public void Deactivate(DateTime now)
    {
        IsActive = false;
        SetUpdatedAt(now);
    }
}

/// <summary>Pravna forma vještaka — utiče na limit aktivnih dodjela (Individual&lt;2, Firm&lt;5).</summary>
public enum AppraiserLegalForm
{
    Individual = 0,
    Firm       = 1
}

/// <summary>Vrsta klijenata banke koje vještak smije procjenjivati.</summary>
public enum AppraiserClientScope
{
    /// <summary>Smije procjenjivati i fizička i pravna lica.</summary>
    Sve         = 0,
    /// <summary>Samo fizička lica (FL).</summary>
    FizickaLica = 1,
    /// <summary>Samo pravna lica (PL).</summary>
    PravnaLica  = 2
}
