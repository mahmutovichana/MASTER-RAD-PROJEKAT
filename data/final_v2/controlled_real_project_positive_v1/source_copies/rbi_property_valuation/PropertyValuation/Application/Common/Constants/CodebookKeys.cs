namespace RBBH.CollateralAppraisal.Application.Common.Constants;

/// <summary>
/// Centralne konstante za codebook ključeve — eliminacija magic stringova.
/// Svaka referenca na codebook tip u cijeloj aplikaciji koristi ove konstante.
/// </summary>
public static class CodebookKeys
{
    public const string DocumentTypes              = "tipovi_dokumenata";
    public const string CollateralTypes            = "tipovi_kolaterala";
    public const string PropertyTypes              = "tipovi_nekretnina";
    public const string CombinedCollateralTypes    = "kombinovani_tipovi_kolaterala";
    public const string Cities                     = "gradovi";
    public const string Branches                   = "poslovnice";
    public const string DocumentationSupplementReasons = "razlozi_dopune_dokumentacije";
}

/// <summary>
/// Konstante za kodove tipova dokumenata iz šifarnika.
/// </summary>
/// <summary>
/// Konstante za kodove tipova kolaterala iz šifarnika.
/// </summary>
public static class CollateralTypeCodes
{
    public const string Apartment     = "APP";
    public const string ApartmentLegacy = "APP_STAN";

    // Kombinovani tipovi kolaterala — stan + polustrukturirani prostor
    public const string ApartmentGarage          = "APP_STAN_I_GARAZA";
    public const string ApartmentStorage         = "APP_STAN_I_OSTAVA";
    public const string ApartmentGarageStorage   = "APP_STAN_GARAZA_I_OSTAVA";
}

/// <summary>
/// Filtarski kodovi za AppraisalType query parametar (UI i API filteri).
/// Odvojeno od CollateralTypeCodes jer su ovo UI/query vrijednosti, ne DB kode.
/// </summary>
public static class AppraisalTypeFilterCodes
{
    public const string Stan              = "STAN";
    public const string StanIGaraza       = "STAN_I_GARAZA";
    public const string StanIOstava       = "STAN_I_OSTAVA";
    public const string StanGarazaIOstava = "STAN_GARAZA_I_OSTAVA";

    public static string? ToCombinedDbCode(string filterCode) => filterCode switch
    {
        StanIGaraza       => CollateralTypeCodes.ApartmentGarage,
        StanIOstava       => CollateralTypeCodes.ApartmentStorage,
        StanGarazaIOstava => CollateralTypeCodes.ApartmentGarageStorage,
        _                 => null
    };
}

public static class DocumentTypeCodes
{
    public const string FinalAppraisal = "FINALNA_PROCJENA";
    public const string ZkExtract      = "ZK";
    public const string PaymentReceipt = "UPLATNICA";
    public const string Consent        = "SAGLASNOST";
    public const string CoOpinion      = "MISLJENJE_CO";
    public const string LegalOpinion   = "MISLJENJE_PRAVNA";
}
