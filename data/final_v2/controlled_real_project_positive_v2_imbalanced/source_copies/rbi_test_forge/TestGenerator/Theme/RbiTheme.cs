using MudBlazor;

namespace RBBH.TestAutomation.Api.Theme;

/// <summary>
/// MudBlazor custom tema za Raiffeisen Bank International (RBI).
///
/// <para>
/// Vrijednosti su usklađene s CSS design tokenima u <c>wwwroot/app.css</c>.
/// Sve MudBlazor theming klase (<c>PaletteLight</c>, <c>Typography</c>,
/// <c>LayoutProperties</c>, <c>H1Typography</c>... ) su u <c>MudBlazor</c> namespace-u.
/// </para>
///
/// <para>
/// MudBlazor 8.x API napomene:
/// <list type="bullet">
///   <item><description><c>PaletteLight</c> umjesto zastarjelog <c>Palette</c> (v6/v7).</description></item>
///   <item><description><c>Shape</c> klasa ne postoji — border radius je u <c>LayoutProperties.DefaultBorderRadius</c>.</description></item>
///   <item><description>Tipografske sub-klase imaju sufiks: <c>H3Typography</c>, <c>Body1Typography</c>, <c>ButtonTypography</c> itd.</description></item>
///   <item><description><c>FontWeight</c> i <c>LineHeight</c> su <c>string</c>, ne <c>int</c>/<c>double</c>.</description></item>
/// </list>
/// </para>
/// </summary>
public static class RbiTheme
{
    public static MudTheme Create() => new()
    {
        // ─────────────────────────────────────────────────────────────────
        // PALETA — light mode
        // ─────────────────────────────────────────────────────────────────
        PaletteLight = new PaletteLight
        {
            // Brand boje
            Primary               = "#FEE600",  // RBI Yellow Primary — jedina obavezna brand boja
            PrimaryContrastText   = "#2B2D33",  // Off Black — dovoljan kontrast na žutoj (WCAG AA)
            Secondary             = "#225B45",  // RBI Green Deep — korporativni/ESG zeleni
            SecondaryContrastText = "#FFFFFF",

            // AppBar — tamna pozadina naglašava brand žutu u logou
            AppbarBackground      = "#2B2D33",  // RBI Off Black
            AppbarText            = "#FFFFFF",

            // Drawer (bočni meni)
            DrawerBackground      = "#F1EDE6",  // RBI Warm Grey
            DrawerText            = "#2B2D33",  // Off Black
            DrawerIcon            = "#2B2D33",

            // Pozadine
            Background            = "#FFFFFF",
            BackgroundGray        = "#F8F6F2",  // RBI Warm Grey 50%
            Surface               = "#FFFFFF",

            // Tekst
            TextPrimary           = "#2B2D33",  // Off Black
            TextSecondary         = "#5C5E66",  // izvedena sekundarna nijansa
            TextDisabled          = "#9EA0A6",

            // Akcije
            ActionDefault         = "#2B2D33",
            ActionDisabled        = "#9EA0A6",
            ActionDisabledBackground = "#F1EDE6",

            // Borderi i linije
            Divider               = "#DDD9D2",
            DividerLight          = "#F1EDE6",
            LinesDefault          = "#DDD9D2",
            LinesInputs           = "#B8B4AD",
            TableLines            = "#DDD9D2",

            // Status — mapirani na RBI sekundarnu paletu, ne generičke boje
            Success               = "#225B45",  // RBI Green Deep
            SuccessContrastText   = "#FFFFFF",
            Error                 = "#C65C4A",  // RBI Coral Deep (RBI nema crvenu u brand paleti)
            ErrorContrastText     = "#FFFFFF",
            Warning               = "#F9BB30",  // RBI Yellow 3 — amber ton
            WarningContrastText   = "#2B2D33",
            Info                  = "#67D0AB",  // RBI Green Midtone
            InfoContrastText      = "#2B2D33",

            // Hover i ripple — suptilniji od MudBlazor defaulta
            HoverOpacity          = 0.06,
            RippleOpacity         = 0.08,
        },

        // ─────────────────────────────────────────────────────────────────
        // TIPOGRAFIJA
        // Primarni font je Hanken Grotesk (učitan u App.razor).
        // Roboto ostaje kao fallback jer ga učitava MudBlazor.
        //
        // NAPOMENA: Vrijednosti SU DUPLICIRANE iz app.css --font-size-* /
        // --font-weight-* tokena. Razlog: MudBlazor 8.x ne čita CSS varijable;
        // theme prima string vrijednosti pri inicijalizaciji.
        // PRI PROMJENI tipografije AŽURIRATI OBJE LOKACIJE:
        //   1. app.css :root (--font-size-*, --font-weight-*, --line-height-*)
        //   2. RbiTheme.cs Typography blok (ispod)
        // FontWeight: string | LineHeight: string
        // ─────────────────────────────────────────────────────────────────
        Typography = new Typography
        {
            Default = new DefaultTypography
            {
                FontFamily    = ["Hanken Grotesk", "Roboto", "Helvetica Neue", "Arial", "sans-serif"],
                FontSize      = "0.875rem",   // 14px
                FontWeight    = "400",
                LineHeight    = "1.5",
                LetterSpacing = "normal",
            },
            H1 = new H1Typography
            {
                FontSize      = "2.25rem",    // 36px
                FontWeight    = "800",
                LineHeight    = "1.2",
                LetterSpacing = "-0.025em",
            },
            H2 = new H2Typography
            {
                FontSize      = "1.875rem",   // 30px
                FontWeight    = "800",
                LineHeight    = "1.2",
                LetterSpacing = "-0.025em",
            },
            H3 = new H3Typography
            {
                FontSize      = "1.5rem",     // 24px
                FontWeight    = "700",
                LineHeight    = "1.375",
                LetterSpacing = "-0.015em",
            },
            H4 = new H4Typography
            {
                FontSize      = "1.25rem",    // 20px
                FontWeight    = "700",
                LineHeight    = "1.375",
                LetterSpacing = "-0.015em",
            },
            H5 = new H5Typography
            {
                FontSize      = "1.125rem",   // 18px
                FontWeight    = "600",
                LineHeight    = "1.375",
            },
            H6 = new H6Typography
            {
                FontSize      = "1rem",       // 16px
                FontWeight    = "600",
                LineHeight    = "1.5",
            },
            Body1 = new Body1Typography
            {
                FontSize      = "1rem",       // 16px — naglašeni body tekst
                FontWeight    = "400",
                LineHeight    = "1.5",
                LetterSpacing = "normal",
            },
            Body2 = new Body2Typography
            {
                FontSize      = "0.875rem",   // 14px — primarni body tekst
                FontWeight    = "400",
                LineHeight    = "1.5",
            },
            Button = new ButtonTypography
            {
                FontSize      = "0.875rem",   // 14px
                FontWeight    = "500",        // Medium
                LetterSpacing = "0.05em",     // 0.75px ≈ 0.05em na 14px
                TextTransform = "none",       // RBI brand ne koristi all-caps dugmad
            },
            Caption = new CaptionTypography
            {
                FontSize      = "0.75rem",    // 12px
                FontWeight    = "400",
                LineHeight    = "1.375",
            },
            Overline = new OverlineTypography
            {
                FontSize      = "0.625rem",   // 10px
                FontWeight    = "400",
                LetterSpacing = "0.08em",
                TextTransform = "uppercase",
            },
            Subtitle1 = new Subtitle1Typography
            {
                FontSize      = "1rem",
                FontWeight    = "400",
                LineHeight    = "1.625",
            },
            Subtitle2 = new Subtitle2Typography
            {
                FontSize      = "0.875rem",
                FontWeight    = "500",
                LineHeight    = "1.375",
            },
        },

        // ─────────────────────────────────────────────────────────────────
        // LAYOUT
        // Shape klasa ne postoji u MudBlazor 8.x.
        // DefaultBorderRadius ide u LayoutProperties.
        // ─────────────────────────────────────────────────────────────────
        LayoutProperties = new LayoutProperties
        {
            DefaultBorderRadius = "6px",   // --radius-md iz app.css design tokena
            DrawerWidthLeft     = "240px",
            DrawerMiniWidthLeft = "56px",
            DrawerWidthRight    = "240px",
            AppbarHeight        = "64px",
        },
    };
}
