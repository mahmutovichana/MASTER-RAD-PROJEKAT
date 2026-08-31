namespace RBBH.CollateralAppraisal.Application.Security;

/// <summary>
/// Centralne konstante za role aplikacije.
///
/// PRAVILO: Nikad ne pisati hardkodirane stringove za role direktno po endpointima.
/// Uvijek koristiti ove konstante.
///
/// Kako dodati novu rolu:
/// 1. Dodaj konstantu ovdje.
/// 2. Dodaj permissions za novu rolu u <see cref="RolePermissionMatrix"/>.
/// 3. Dokumentuj rolu u docs/backend/role-permission-rules.md.
/// 4. Rola mora biti kreirana u Keycloak realm-u.
/// </summary>
public static class AppRoles
{
    public const string Administrator = "Administrator";
    public const string Unosnik       = "Unosnik";
    public const string Verifikator   = "Verifikator";

    // ── Segment/kućica Prodaja (narudžbe procjene — US 92/93/94) ──────────────
    // AM, SM i UB su tri ODVOJENE Keycloak/aplikativne role. Korisnik se NIKAD
    // ne prijavljuje kao generička rola "Prodaja" — uvijek kao AM, SM ili UB.
    // Sve tri pripadaju zajedničkom poslovnom segmentu "Prodaja" (vidi
    // <see cref="ProdajaSegment"/>) i imaju identičan skup permission-a
    // (vidi RolePermissionMatrix) — razlika je samo u "ko je inicirao narudžbu".

    /// <summary>Account Manager — inicira narudžbu procjene u segmentu Prodaja.</summary>
    public const string AM = "AM";

    /// <summary>Sales Manager — inicira narudžbu procjene u segmentu Prodaja.</summary>
    public const string SM = "SM";

    /// <summary>Universal Banker — inicira narudžbu procjene u segmentu Prodaja.</summary>
    public const string UB = "UB";

    /// <summary>
    /// Naziv poslovnog segmenta/kućice kojem AM, SM i UB pripadaju.
    /// NIJE Keycloak rola i NIKO se ne prijavljuje pod ovim imenom — koristi se
    /// isključivo za grupisanje/labeling (UI naslovi, audit, notifikacije).
    /// </summary>
    public const string ProdajaSegment = "Prodaja";

    /// <summary>Kolateral administrator (CA) — vodi narudžbu, dokumentaciju, vještaka, fakturu.</summary>
    public const string KolateralAdministrator = "KolateralAdministrator";

    /// <summary>Kolateral oficir (CO) — provjera pristupa, odobrenje procjene, mišljenje.</summary>
    public const string KolateralOficir        = "KolateralOficir";

    /// <summary>Vještak (eksterni) — radi procjenu, uploaduje finalnu procjenu.</summary>
    public const string Vjestak                = "Vjestak";

    /// <summary>Pravna služba — daje pravno mišljenje (US 94).</summary>
    public const string PravnaSluzba           = "PravnaSluzba";

    /// <summary>Protokol — upload i obrada fakture (5. kućica).</summary>
    public const string Protokol               = "Protokol";

    /// <summary>Likvidatura / Računovodstvo — evidentira plaćanje fakture (US-F3).</summary>
    public const string Likvidatura            = "Likvidatura";

    /// <summary>Specijalni računi — prima notifikaciju o fakturi za PL (US-F2).</summary>
    public const string SpecijalniRacuni       = "SpecijalniRacuni";

    /// <summary>Računovodstvo — prima notifikaciju o fakturi za PL i evidentira plaćanje (US-F2/F3).</summary>
    public const string Racunovodstvo          = "Racunovodstvo";

    /// <summary>Sve role segmenta Prodaja — AM, SM, UB. Sve tri imaju identičan permission set.</summary>
    public static readonly string[] SalesRoles = [AM, SM, UB];

    /// <summary>Vraća true ako je data rola jedna od AM/SM/UB (segment Prodaja).</summary>
    public static bool IsSalesRole(string? role) =>
        role is not null && SalesRoles.Contains(role, StringComparer.OrdinalIgnoreCase);

    /// <summary>
    /// Role koje vide sve narudžbe (ne samo vlastite).
    /// Prodajne role (AM/SM/UB) vide isključivo vlastite narudžbe — one nisu ovdje.
    /// Svaka nova rola kojoj treba pristup cijelom redu narudžbi mora se dodati OVDJE.
    /// </summary>
    public static readonly IReadOnlySet<string> OrderViewerRoles = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
    {
        Administrator,
        KolateralAdministrator,
        KolateralOficir,
        Vjestak,
        PravnaSluzba,
        Protokol
    };

    /// <summary>
    /// Sve aktivno podržane role. Unosnik i Verifikator su namjerno izostavljeni —
    /// Records modul još nije implementiran (Jul 2026). Dodati kad se Records modul završi.
    /// </summary>
    public static readonly IReadOnlyList<string> All =
    [
        Administrator,
        AM,
        SM,
        UB,
        KolateralAdministrator,
        KolateralOficir,
        Vjestak,
        PravnaSluzba,
        Protokol,
        Likvidatura,
        SpecijalniRacuni,
        Racunovodstvo
    ];
}
