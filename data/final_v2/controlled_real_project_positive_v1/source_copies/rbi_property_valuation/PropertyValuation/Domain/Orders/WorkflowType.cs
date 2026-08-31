namespace RBBH.CollateralAppraisal.Domain.Orders;

/// <summary>
/// Tip workflow-a narudžbe procjene — bira se eksplicitno na ulaznom ekranu
/// ("Fizička lica" / "Pravna lica", Slika 7.1) i određuje cijeli tok narudžbe:
/// routing, vidljivost statusa, dostupne akcije i lanac odgovornih rola.
///
/// FL (Slika 4):   Klijent → Prodaja → CA → Vještak → CO
/// PL (Slika 4.1): Klijent → Prodaja → CA → CO → CA → Prodaja → CA → Vještak → CO
/// </summary>
public enum WorkflowType
{
    /// <summary>Fizička lica (FL) — kraći tok bez inicijalne CO provjere pristupa.</summary>
    FizickaLica = 1,

    /// <summary>Pravna lica (PL) — duži tok sa CO provjerom pristupa i povratnom petljom CA → Prodaja → CA.</summary>
    PravnaLica  = 2
}

/// <summary>
/// Pomoćne mape između <see cref="WorkflowType"/> i postojećeg <c>ClientType</c> (FL/PL),
/// te lanac odgovornih rola koji se prikazuje na timeline-u narudžbe.
/// </summary>
public static class WorkflowTypes
{
    /// <summary>Vraća ClientType kod ("FL"/"PL") koji odgovara odabranom workflow tipu.</summary>
    public static string ToClientType(WorkflowType type) =>
        type == WorkflowType.PravnaLica ? "PL" : "FL";

    /// <summary>Izvodi <see cref="WorkflowType"/> iz ClientType koda ("FL"/"PL"). Default je FL.</summary>
    public static WorkflowType FromClientType(string? clientType) =>
        string.Equals(clientType, "PL", StringComparison.OrdinalIgnoreCase)
            ? WorkflowType.PravnaLica
            : WorkflowType.FizickaLica;

    /// <summary>Parsira kod sa ulaznog ekrana ("FL"/"PL") u <see cref="WorkflowType"/>.</summary>
    public static WorkflowType? Parse(string? code) => code?.ToUpperInvariant() switch
    {
        "FL" or "FIZICKALICA" or "FIZICKA" => WorkflowType.FizickaLica,
        "PL" or "PRAVNALICA"  or "PRAVNA"  => WorkflowType.PravnaLica,
        _ => null
    };

    /// <summary>Kratki naziv za prikaz (UI naslovi, badge).</summary>
    public static string DisplayName(WorkflowType type) =>
        type == WorkflowType.PravnaLica ? "Pravna lica" : "Fizička lica";
}
