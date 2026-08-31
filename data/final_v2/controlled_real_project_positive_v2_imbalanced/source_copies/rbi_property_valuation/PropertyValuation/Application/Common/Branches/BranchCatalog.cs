namespace RBBH.CollateralAppraisal.Application.Common.Branches;

public sealed record BranchItem(
    string Code,
    string Name,
    string CityName,
    string Address);

/// <summary>
/// Jedini izvor istine za poslovnice: kod, naziv, grad i adresa.
///
/// ADR-053 fix: BranchSeeder sada derivira iz ove liste umjesto da drži
/// vlastitu kopiju. Dodavanje nove poslovnice = samo ovdje.
/// </summary>
public static class BranchCatalog
{
    public static readonly IReadOnlyList<BranchItem> All =
    [
        // ── Sarajevo ─────────────────────────────────────────────────────────
        new("POS_SARAJEVO_CENTAR",    "Poslovnica Sarajevo Centar",    "Sarajevo",      "Zmaja od Bosne 74, 71000 Sarajevo"),
        new("POS_SARAJEVO_ILIDZA",    "Poslovnica Ilidža",             "Sarajevo",      "Bosanski trg 3, 71210 Ilidža"),
        new("POS_SARAJEVO_VOGOSCA",   "Poslovnica Vogošća",            "Sarajevo",      "Jošanička 53, 71320 Vogošća"),
        new("POS_SARAJEVO_NV",        "Poslovnica Novi Grad",          "Sarajevo",      "Prvomajska 2, 71000 Sarajevo"),
        new("POS_SARAJEVO_HADZICI",   "Poslovnica Hadžići",            "Sarajevo",      "1. Hadžićkog odreda bb, 71240 Hadžići"),
        new("POS_SARAJEVO_VISNJIK",   "Poslovnica Višnjik",            "Sarajevo",      "Kolodvorska 12, 71000 Sarajevo"),
        new("POS_SARAJEVO_DOBRINJA",  "Poslovnica Dobrinja",           "Sarajevo",      "Trg ZAVNOBIH-a 25, 71000 Sarajevo"),
        new("POS_SARAJEVO_ALIPASINO", "Poslovnica Alipašino Polje",    "Sarajevo",      "Bosanska 6, 71000 Sarajevo"),

        // ── Banja Luka ───────────────────────────────────────────────────────
        new("POS_BANJA_LUKA",         "Poslovnica Banja Luka",         "Banja Luka",    "Veselina Masleše 6, 78000 Banja Luka"),
        new("POS_BANJA_LUKA_2",       "Poslovnica Banja Luka Centar",  "Banja Luka",    "Kralja Petra I Karađorđevića 97, 78000 Banja Luka"),

        // ── Tuzla ────────────────────────────────────────────────────────────
        new("POS_TUZLA",              "Poslovnica Tuzla",              "Tuzla",         "Maršala Tita 15, 75000 Tuzla"),
        new("POS_TUZLA_SJENJAK",      "Poslovnica Tuzla Sjenjak",      "Tuzla",         "Bosne Srebrene 1, 75000 Tuzla"),

        // ── Mostar ───────────────────────────────────────────────────────────
        new("POS_MOSTAR",             "Poslovnica Mostar",             "Mostar",        "Kneza Domagoja bb, 88000 Mostar"),
        new("POS_MOSTAR_RONDO",       "Poslovnica Mostar Rondo",       "Mostar",        "Maršala Tita 172, 88000 Mostar"),

        // ── Zenica ───────────────────────────────────────────────────────────
        new("POS_ZENICA",             "Poslovnica Zenica",             "Zenica",        "Masarykova 46, 72000 Zenica"),
        new("POS_ZENICA_CENTAR",      "Poslovnica Zenica Centar",      "Zenica",        "Maršala Tita 13, 72000 Zenica"),

        // ── Bijeljina ────────────────────────────────────────────────────────
        new("POS_BIJELJINA",          "Poslovnica Bijeljina",          "Bijeljina",     "Cara Lazara 10, 76300 Bijeljina"),

        // ── Trebinje ─────────────────────────────────────────────────────────
        new("POS_TREBINJE",           "Poslovnica Trebinje",           "Trebinje",      "Vojvode Stepe 4, 89101 Trebinje"),

        // ── Brčko ────────────────────────────────────────────────────────────
        new("POS_BRCKO",              "Poslovnica Brčko",              "Brčko",         "Bulevar mira 2, 76100 Brčko"),

        // ── Bihać ────────────────────────────────────────────────────────────
        new("POS_BIHAC",              "Poslovnica Bihać",              "Bihać",         "Bosanska 8, 77000 Bihać"),

        // ── Travnik ──────────────────────────────────────────────────────────
        new("POS_TRAVNIK",            "Poslovnica Travnik",            "Travnik",       "Bosanska 140, 72270 Travnik"),

        // ── Livno ────────────────────────────────────────────────────────────
        new("POS_LIVNO",              "Poslovnica Livno",              "Livno",         "Trg Kralja Tomislava bb, 80101 Livno"),

        // ── Gradačac ─────────────────────────────────────────────────────────
        new("POS_GRADACAC",           "Poslovnica Gradačac",           "Gradačac",      "H.K. Gradaščevića 54, 76250 Gradačac"),

        // ── Gračanica ────────────────────────────────────────────────────────
        new("POS_GRACANICA",          "Poslovnica Gračanica",          "Gračanica",     "Zlatnih ljiljana bb, 75320 Gračanica"),

        // ── Cazin ────────────────────────────────────────────────────────────
        new("POS_CAZIN",              "Poslovnica Cazin",              "Cazin",         "Trg Zlatnih ljiljana bb, 77220 Cazin"),

        // ── Visoko ───────────────────────────────────────────────────────────
        new("POS_VISOKO",             "Poslovnica Visoko",             "Visoko",        "Alije Izetbegovića 1, 71300 Visoko"),

        // ── Kakanj ───────────────────────────────────────────────────────────
        new("POS_KAKANJ",             "Poslovnica Kakanj",             "Kakanj",        "Alije Izetbegovića 44, 72240 Kakanj"),

        // ── Goražde ──────────────────────────────────────────────────────────
        new("POS_GORAZDE",            "Poslovnica Goražde",            "Goražde",       "Zaima Imamovića 3, 73000 Goražde"),

        // ── Široki Brijeg ─────────────────────────────────────────────────────
        new("POS_SIROKI_BRIJEG",      "Poslovnica Široki Brijeg",      "Široki Brijeg", "Fra Didaka Buntića bb, 88220 Široki Brijeg"),

        // ── Konjic ───────────────────────────────────────────────────────────
        new("POS_KONJIC",             "Poslovnica Konjic",             "Konjic",        "Maršala Tita 31, 88400 Konjic"),

        // ── Bugojno ──────────────────────────────────────────────────────────
        new("POS_BUGOJNO",            "Poslovnica Bugojno",            "Bugojno",       "Zlatnih ljiljana 2, 70230 Bugojno"),

        // ── Vitez ────────────────────────────────────────────────────────────
        new("POS_VITEZ",              "Poslovnica Vitez",              "Vitez",         "Poslovni centar 96-2, 72250 Vitez"),

        // ── Doboj ────────────────────────────────────────────────────────────
        new("POS_DOBOJ",              "Poslovnica Doboj",              "Doboj",         "Cara Dušana 2, 74000 Doboj"),

        // ── Prijedor ─────────────────────────────────────────────────────────
        new("POS_PRIJEDOR",           "Poslovnica Prijedor",           "Prijedor",      "Kralja Petra I bb, 79101 Prijedor"),

        // ── Sanski Most ──────────────────────────────────────────────────────
        new("POS_SANSKI_MOST",        "Poslovnica Sanski Most",        "Sanski Most",   "Prijedorska 3, 79260 Sanski Most"),

        // ── Velika Kladuša ───────────────────────────────────────────────────
        new("POS_VELIKA_KLADUSA",     "Poslovnica Velika Kladuša",     "Velika Kladuša","Izeta Nanića bb, 77230 Velika Kladuša"),

        // ── Lukavac ──────────────────────────────────────────────────────────
        new("POS_LUKAVAC",            "Poslovnica Lukavac",            "Lukavac",       "Trg Slobode bb, 75300 Lukavac"),

        // ── Živinice ─────────────────────────────────────────────────────────
        new("POS_ZIVINICE",           "Poslovnica Živinice",           "Živinice",      "Alije Izetbegovića bb, 75270 Živinice"),

        // ── Čapljina ─────────────────────────────────────────────────────────
        new("POS_CAPLJINA",           "Poslovnica Čapljina",           "Čapljina",      "Ante Starčevića bb, 88300 Čapljina"),

        // ── Stolac ───────────────────────────────────────────────────────────
        new("POS_STOLAC",             "Poslovnica Stolac",             "Stolac",        "Bišćevića sokak bb, 88360 Stolac"),
    ];

    public static BranchItem? GetByCode(string code) =>
        All.FirstOrDefault(b => b.Code.Equals(code, StringComparison.OrdinalIgnoreCase));

    public static bool IsValidCityBranch(string? cityName, string? branchCode)
    {
        if (string.IsNullOrWhiteSpace(cityName) || string.IsNullOrWhiteSpace(branchCode))
            return true;
        var branch = GetByCode(branchCode);
        return branch is not null &&
               branch.CityName.Equals(cityName, StringComparison.OrdinalIgnoreCase);
    }
}
