using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Orders.Requests;

namespace RBBH.CollateralAppraisal.Application.Common.Validation;

/// <summary>
/// Statička klasa koja enkapsulira sva validacijska pravila za narudžbe.
/// Poziva je i FluentValidation validator (pipeline) i servis (direktni pozivi),
/// osiguravajući jedinstven skup pravila na jednom mjestu.
/// </summary>
public static class OrderRequestValidator
{
    public static void ValidateCreate(CreateOrderRequest r)
    {
        var errors = new List<ValidationFieldError>();

        errors.AddRange(OrderClientNameValidator.Validate(r.ClientName, r.ClientType, "clientName"));

        if (string.IsNullOrWhiteSpace(r.ClientType))
            errors.Add(new ValidationFieldError("clientType", ValidationErrorCodes.RequiredClientType,
                "Tip klijenta je obavezan."));

        if ((r.CollateralTypeId <= 0) && !r.CombinedCollateralTypeId.HasValue)
            errors.Add(new ValidationFieldError("collateralTypeId", ValidationErrorCodes.RequiredField,
                "Tip kolaterala je obavezan."));

        if (string.IsNullOrWhiteSpace(r.City))
            errors.Add(new ValidationFieldError("city", ValidationErrorCodes.RequiredField,
                "Grad je obavezan."));
        else if (r.City.Length > 100)
            errors.Add(new ValidationFieldError("city", ValidationErrorCodes.MaxLengthExceeded,
                "Naziv grada ne smije biti duži od 100 znakova."));

        if (string.IsNullOrWhiteSpace(r.Branch))
            errors.Add(new ValidationFieldError("branch", ValidationErrorCodes.RequiredField,
                "Poslovnica je obavezna."));
        else if (!BranchCityMap.IsValid(r.City, r.Branch))
            errors.Add(new ValidationFieldError("branch", ValidationErrorCodes.InvalidBranchForCity,
                "Odabrana poslovnica ne pripada odabranom gradu."));

        if (string.IsNullOrWhiteSpace(r.BranchAddress))
            errors.Add(new ValidationFieldError("branchAddress", ValidationErrorCodes.RequiredField,
                "Adresa poslovnice je obavezna."));

        errors.AddRange(PersonNameValidator.Validate(r.ContactName, "contactName", minLength: 2, maxLength: 200));
        errors.AddRange(PersonNameValidator.Validate(r.DeliveryContactName, "deliveryContactName", minLength: 2, maxLength: 300));
        errors.AddRange(PersonNameValidator.Validate(r.AmRecipientName, "amRecipientName", minLength: 2, maxLength: 300));
        errors.AddRange(PhoneNumberValidator.Validate(r.ContactPhone, "contactPhone"));
        errors.AddRange(EmailValidator.Validate(r.ContactEmail, "contactEmail"));
        errors.AddRange(ClientIdentifierValidator.Validate(r.ClientIdentifier, r.ClientType, "clientIdentifier"));

        if (!string.IsNullOrWhiteSpace(r.InternalNote) && r.InternalNote.Length > 500)
            errors.Add(new ValidationFieldError("internalNote", ValidationErrorCodes.MaxLengthExceeded,
                "Interna napomena ne smije biti duža od 500 znakova."));

        if (string.IsNullOrWhiteSpace(r.PropertyAddress))
            errors.Add(new ValidationFieldError("propertyAddress", ValidationErrorCodes.RequiredField,
                "Adresa nekretnine je obavezna."));
        else if (r.PropertyAddress.Length > 500)
            errors.Add(new ValidationFieldError("propertyAddress", ValidationErrorCodes.MaxLengthExceeded,
                "Adresa nekretnine ne smije biti duža od 500 znakova."));

        if (!r.RequestReceivedAt.HasValue)
            errors.Add(new ValidationFieldError("requestReceivedAt", ValidationErrorCodes.RequiredField,
                "Datum i vrijeme prijema zahtjeva od klijenta je obavezan."));
        else if (r.RequestSentAt.HasValue && r.RequestReceivedAt.Value > r.RequestSentAt.Value)
            errors.Add(new ValidationFieldError("requestReceivedAt", ValidationErrorCodes.InvalidDateRange,
                "Datum prijema zahtjeva ne smije biti nakon datuma slanja zahtjeva."));

        if (r.SquareMetersCommercial.HasValue && r.SquareMetersCommercial.Value < 0)
            errors.Add(new ValidationFieldError("squareMetersCommercial", ValidationErrorCodes.InvalidFormat,
                "Broj kvadrata poslovnog dijela ne smije biti negativan."));

        if (r.SquareMetersResidential.HasValue && r.SquareMetersResidential.Value < 0)
            errors.Add(new ValidationFieldError("squareMetersResidential", ValidationErrorCodes.InvalidFormat,
                "Broj kvadrata stambenog dijela ne smije biti negativan."));

        if (errors.Count > 0) throw new ValidationException(errors);
    }

    public static void ValidateUpdate(
        UpdateOrderRequest r,
        string? effectiveClientType,
        string? effectiveCity = null,
        string? effectiveBranch = null)
    {
        var errors = new List<ValidationFieldError>();

        if (r.ClientType != null && string.IsNullOrWhiteSpace(r.ClientType))
            errors.Add(new ValidationFieldError("clientType", ValidationErrorCodes.RequiredClientType,
                "Tip klijenta je obavezan."));

        if (r.ClientName != null)
            errors.AddRange(OrderClientNameValidator.Validate(r.ClientName, effectiveClientType, "clientName"));

        if (r.ContactName != null)
            errors.AddRange(PersonNameValidator.Validate(r.ContactName, "contactName", minLength: 2, maxLength: 200));
        if (r.DeliveryContactName != null)
            errors.AddRange(PersonNameValidator.Validate(r.DeliveryContactName, "deliveryContactName", minLength: 2, maxLength: 300));
        if (r.AmRecipientName != null)
            errors.AddRange(PersonNameValidator.Validate(r.AmRecipientName, "amRecipientName", minLength: 2, maxLength: 300));
        if (r.ContactPhone != null)
            errors.AddRange(PhoneNumberValidator.Validate(r.ContactPhone, "contactPhone"));
        if (r.ContactEmail != null)
            errors.AddRange(EmailValidator.Validate(r.ContactEmail, "contactEmail"));

        if (r.City != null)
        {
            if (string.IsNullOrWhiteSpace(r.City))
                errors.Add(new ValidationFieldError("city", ValidationErrorCodes.RequiredField, "Grad je obavezan."));
            else if (r.City.Length > 100)
                errors.Add(new ValidationFieldError("city", ValidationErrorCodes.MaxLengthExceeded,
                    "Naziv grada ne smije biti duži od 100 znakova."));
        }

        if (r.Branch != null && string.IsNullOrWhiteSpace(r.Branch))
            errors.Add(new ValidationFieldError("branch", ValidationErrorCodes.RequiredField, "Poslovnica je obavezna."));

        if ((r.City != null || r.Branch != null) && effectiveCity != null && effectiveBranch != null
            && !BranchCityMap.IsValid(effectiveCity, effectiveBranch))
            errors.Add(new ValidationFieldError("branch", ValidationErrorCodes.InvalidBranchForCity,
                "Odabrana poslovnica ne pripada odabranom gradu."));
        if (r.BranchAddress != null && string.IsNullOrWhiteSpace(r.BranchAddress))
            errors.Add(new ValidationFieldError("branchAddress", ValidationErrorCodes.RequiredField, "Adresa poslovnice je obavezna."));

        if (r.InternalNote != null && r.InternalNote.Length > 500)
            errors.Add(new ValidationFieldError("internalNote", ValidationErrorCodes.MaxLengthExceeded,
                "Interna napomena ne smije biti duža od 500 znakova."));

        if (r.PropertyAddress != null)
        {
            if (string.IsNullOrWhiteSpace(r.PropertyAddress))
                errors.Add(new ValidationFieldError("propertyAddress", ValidationErrorCodes.RequiredField,
                    "Adresa nekretnine je obavezna."));
            else if (r.PropertyAddress.Length > 500)
                errors.Add(new ValidationFieldError("propertyAddress", ValidationErrorCodes.MaxLengthExceeded,
                    "Adresa nekretnine ne smije biti duža od 500 znakova."));
        }

        if (r.RequestReceivedAt.HasValue && r.RequestSentAt.HasValue &&
            r.RequestReceivedAt.Value > r.RequestSentAt.Value)
            errors.Add(new ValidationFieldError("requestReceivedAt", ValidationErrorCodes.InvalidDateRange,
                "Datum prijema zahtjeva ne smije biti nakon datuma slanja zahtjeva."));

        if (r.SquareMetersCommercial.HasValue && r.SquareMetersCommercial.Value < 0)
            errors.Add(new ValidationFieldError("squareMetersCommercial", ValidationErrorCodes.InvalidFormat,
                "Broj kvadrata poslovnog dijela ne smije biti negativan."));
        if (r.SquareMetersResidential.HasValue && r.SquareMetersResidential.Value < 0)
            errors.Add(new ValidationFieldError("squareMetersResidential", ValidationErrorCodes.InvalidFormat,
                "Broj kvadrata stambenog dijela ne smije biti negativan."));

        if (errors.Count > 0) throw new ValidationException(errors);
    }
}
