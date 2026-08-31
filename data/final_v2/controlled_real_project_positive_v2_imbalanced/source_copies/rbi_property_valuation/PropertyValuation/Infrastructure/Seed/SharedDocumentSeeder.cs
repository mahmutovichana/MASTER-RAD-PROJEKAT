using System.Text;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Documents;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

/// <summary>
/// Idempotentno popunjava SharedDocuments referentnim dokumentima za demo/produkciju:
/// cjenovnik procjena i liste potrebne dokumentacije po tipu kolaterala.
/// Pokrece se na svim okruzenjima (za razliku od AppraisalOrderSeeder koji radi samo Dev/Staging).
/// </summary>
public static class SharedDocumentSeeder
{
    public static async Task SeedAsync(
        ApplicationDbContext db,
        IFileStorageProvider fileStorage,
        ILogger? logger = null,
        CancellationToken ct = default)
    {
        var anyExists = await db.SharedDocuments
            .IgnoreQueryFilters()
            .AnyAsync(ct);

        if (anyExists)
        {
            logger?.LogInformation("SharedDocumentSeeder: dijeljeni dokumenti vec postoje, preskacemi.");
            return;
        }

        var documents = new[]
        {
            (
                Title:    "Cjenovnik procjena nekretnina 2026",
                Category: SharedDocumentCategories.Cjenovnik,
                FileName: "Cjenovnik_procjena_nekretnina_2026.pdf",
                Pages:    BuildCjenovnikPages()
            ),
            (
                Title:    "Lista dokumentacije - Fizicka lica (Nekretnine)",
                Category: SharedDocumentCategories.Dokumentacija,
                FileName: "Lista_dokumentacije_FL_nekretnine.pdf",
                Pages:    BuildListaFlPages()
            ),
            (
                Title:    "Lista dokumentacije - Pravna lica (Nekretnine)",
                Category: SharedDocumentCategories.Dokumentacija,
                FileName: "Lista_dokumentacije_PL_nekretnine.pdf",
                Pages:    BuildListaPlPages()
            ),
            (
                Title:    "Lista dokumentacije - Pokretna imovina",
                Category: SharedDocumentCategories.Dokumentacija,
                FileName: "Lista_dokumentacije_pokretna_imovina.pdf",
                Pages:    BuildListaPokretnaPages()
            ),
        };

        foreach (var (title, category, fileName, pages) in documents)
        {
            var pdfBytes = BuildPdf(pages);
            await using var stream = new MemoryStream(pdfBytes);

            var stored = await fileStorage.SaveAsync(stream, fileName, "shared-documents", ct);

            var doc = SharedDocument.Create(
                title:            title,
                category:         category,
                fileName:         Path.GetFileName(stored.StoragePath),
                originalFileName: fileName,
                contentType:      "application/pdf",
                fileSize:         stored.FileSize,
                storagePath:      stored.StoragePath,
                uploadedByUserId: "system-seed");

            db.SharedDocuments.Add(doc);
            logger?.LogInformation("SharedDocumentSeeder: seedovan '{Title}'.", title);
        }

        await db.SaveChangesAsync(ct);
    }

    // ── Per-document content ─────────────────────────────────────────────────

    private static string[] BuildCjenovnikPages() =>
    [
        BuildPage(
            header: "CJENOVNIK PROCJENA NEKRETNINA 2026",
            subtitle: "RBBHBank - Kolateral menadžment",
            lines:
            [
                "",
                "STANDARDNI TIPOVI PROCJENE                               CIJENA (KM)",
                "─────────────────────────────────────────────────────────────────────",
                "Stan / Apartman  (do 100 m2)                               250,00 KM",
                "Stan / Apartman  (100 - 200 m2)                            320,00 KM",
                "Kuca  (do 200 m2)                                          300,00 KM",
                "Kuca  (200 - 400 m2)                                       400,00 KM",
                "Kuca  (preko 400 m2)                                       500,00 KM",
                "Garaza / parking mjesta                                    150,00 KM",
                "Poslovni prostor  (do 200 m2)                              350,00 KM",
                "Poslovni prostor  (200 - 500 m2)                           500,00 KM",
                "Poslovni prostor  (preko 500 m2)                           700,00 KM",
                "Industrijski objekat / skladiste                           600,00 KM",
                "Zemljiste - gradjevinsko  (do 1.000 m2)                    200,00 KM",
                "Zemljiste - gradjevinsko  (1.000 - 5.000 m2)               300,00 KM",
                "Zemljiste - gradjevinsko  (preko 5.000 m2)                 450,00 KM",
                "Zemljiste - poljoprivredno                                 180,00 KM",
                "",
                "POKRETNA IMOVINA                                          CIJENA (KM)",
                "─────────────────────────────────────────────────────────────────────",
                "Putnicko vozilo                                            100,00 KM",
                "Teretno vozilo / kamion                                    200,00 KM",
                "Radna masina / gradevinska oprema                          250,00 KM",
                "Plovilo                                                    300,00 KM",
                "Oprema / postrojenje                                       200,00 KM",
                "",
                "NAPOMENE:",
                "─────────────────────────────────────────────────────────────────────",
                "  * Cijene su u KM i bez PDV-a.",
                "  * Hitni nalozi (rok isporuke < 3 dana): uvecanje od 50%.",
                "  * Terenski troskovi (udaljenost > 50 km): po dogovoru.",
                "  * Kompleksni objekti: individualna procjena.",
            ]
        )
    ];

    private static string[] BuildListaFlPages() =>
    [
        BuildPage(
            header: "LISTA DOKUMENTACIJE - FIZICKA LICA",
            subtitle: "Procjena nekretnina i pokretne imovine",
            lines:
            [
                "",
                "A) STAN / APARTMAN",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / putne isprave vlasnika",
                "  [ ]  Izvadak iz zemljišne knjige (ZK) - ne stariji od 6 mj.",
                "  [ ]  Posjedovni list - ne stariji od 6 mj.",
                "  [ ]  Osnov sticanja (kupoprodajni ugovor / rjesenje o",
                "       nasljedivanju / darovni ugovor)",
                "  [ ]  Tlocrt stana (skica - ako ne postoji u ZK dokumentaciji)",
                "  [ ]  Urbanisticka saglasnost / odobrenje za izgradnju",
                "  [ ]  Upotrebna dozvola (ako je dostupna)",
                "",
                "B) KUCA",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / putne isprave vlasnika",
                "  [ ]  ZK izvadak - ne stariji od 6 mj.",
                "  [ ]  Posjedovni list - ne stariji od 6 mj.",
                "  [ ]  Osnov sticanja",
                "  [ ]  Projektna dokumentacija (tlocrt, presjek)",
                "  [ ]  Odobrenje za gradnju",
                "  [ ]  Upotrebna dozvola",
                "  [ ]  ZK izvadak za zemljiste ispod kuce",
                "",
                "C) POSLOVNI PROSTOR / GARAZA",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / putne isprave vlasnika",
                "  [ ]  ZK izvadak - ne stariji od 6 mj.",
                "  [ ]  Posjedovni list - ne stariji od 6 mj.",
                "  [ ]  Osnov sticanja",
                "  [ ]  Tlocrt / skica prostora",
                "",
                "D) VOZILO",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte vlasnika",
                "  [ ]  Saobracajna dozvola",
                "  [ ]  Polica osiguranja (opcija)",
            ]
        )
    ];

    private static string[] BuildListaPlPages() =>
    [
        BuildPage(
            header: "LISTA DOKUMENTACIJE - PRAVNA LICA",
            subtitle: "Procjena nekretnina i pokretne imovine",
            lines:
            [
                "",
                "A) DOKUMENTI PRAVNOG SUBJEKTA",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Izvod iz sudskog registra (ne stariji od 3 mj.)",
                "  [ ]  ID broj / porezni identifikacijski broj",
                "  [ ]  Podaci o ovlastenom licu za zastupanje",
                "  [ ]  Kopija licne karte zastupnika",
                "",
                "B) STAN / APARTMAN / GARAZA (u vlasnistvu pravnog lica)",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  ZK izvadak - ne stariji od 6 mj.",
                "  [ ]  Posjedovni list - ne stariji od 6 mj.",
                "  [ ]  Osnov sticanja (ugovor / rjesenje)",
                "  [ ]  Tlocrt / skica prostora",
                "  [ ]  Odobrenje za izgradnju / upotrebna dozvola",
                "",
                "C) POSLOVNI PROSTOR / INDUSTRIJSKI OBJEKAT",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  ZK izvadak - ne stariji od 6 mj.",
                "  [ ]  Posjedovni list - ne stariji od 6 mj.",
                "  [ ]  Osnov sticanja",
                "  [ ]  Projektna dokumentacija (glavni projekt, tlocrti, presjeci)",
                "  [ ]  Odobrenje za izgradnju",
                "  [ ]  Upotrebna dozvola",
                "  [ ]  ZK izvadak za zemljiste (ako je odvojen od objekta)",
                "",
                "D) ZEMLJISTE",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  ZK izvadak - ne stariji od 6 mj.",
                "  [ ]  Posjedovni list - ne stariji od 6 mj.",
                "  [ ]  Urbanisticka saglasnost / lokacijska informacija",
                "  [ ]  Osnov sticanja",
                "",
                "E) OPREMA / POSTROJENJE",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Faktura / racun o kupovini",
                "  [ ]  Servisna knjiga / dokumentacija",
                "  [ ]  Polica osiguranja (opcija)",
                "",
                "NAPOMENE:",
                "  * Sva dokumenta dostavljati u PDF formatu.",
                "  * Originali na uvid po zahtjevu vjestaka.",
            ]
        )
    ];

    private static string[] BuildListaPokretnaPages() =>
    [
        BuildPage(
            header: "LISTA DOKUMENTACIJE - POKRETNA IMOVINA",
            subtitle: "Procjena vozila, plovila, opreme i postrojenja",
            lines:
            [
                "",
                "A) PUTNICKO VOZILO",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / ID vlasnika",
                "  [ ]  Saobracajna dozvola",
                "  [ ]  Ugovor o kupoprodaji (ako je kupljeno)",
                "  [ ]  Polica kasko osiguranja (opcija)",
                "  [ ]  Servisna knjiga",
                "",
                "B) TERETNO VOZILO / KAMION / BUS",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / ID vlasnika",
                "  [ ]  Saobracajna dozvola",
                "  [ ]  Tehnicka dokumentacija vozila",
                "  [ ]  Ugovor o kupoprodaji",
                "  [ ]  Servisna knjiga",
                "",
                "C) RADNA MASINA / GRADJEVINSKA OPREMA",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / ID vlasnika",
                "  [ ]  Faktura / racun o kupovini",
                "  [ ]  Tehnicki list / specifikacija",
                "  [ ]  Servisna dokumentacija",
                "  [ ]  Polica osiguranja (opcija)",
                "",
                "D) PLOVILO",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Kopija licne karte / ID vlasnika",
                "  [ ]  Brodska knjiga / dozvola",
                "  [ ]  Faktura / racun o kupovini",
                "  [ ]  Tehnicka dokumentacija",
                "",
                "E) OPREMA / POSTROJENJE",
                "─────────────────────────────────────────────────────────────────────",
                "  [ ]  Faktura / racun o kupovini",
                "  [ ]  Tehnicki list / katalog",
                "  [ ]  Servisna knjiga / garancija",
                "  [ ]  Polica osiguranja (opcija)",
                "",
                "NAPOMENE:",
                "  * Vlasnik ili ovlastena osoba obavezna biti prisutna pri pregledu.",
                "  * Sva dokumenta dostavljati u PDF formatu.",
            ]
        )
    ];

    // ── Raw PDF builder ──────────────────────────────────────────────────────

    private static string BuildPage(string header, string subtitle, string[] lines)
    {
        var sb = new StringBuilder();
        sb.AppendLine($"HEADER:{header}");
        sb.AppendLine($"SUBTITLE:{subtitle}");
        foreach (var line in lines)
            sb.AppendLine(line);
        return sb.ToString();
    }

    private static byte[] BuildPdf(string[] pages)
    {
        // Build raw PDF with one page per entry.
        // Uses Helvetica (built-in Type1, ASCII-safe).
        var pageContents  = new List<string>();
        var pageObjNums   = new List<int>();
        var contentObjNums = new List<int>();

        // Object numbering: 1=catalog, 2=pages, then pairs (page, content) per page
        int nextObj = 3;
        foreach (var pageText in pages)
        {
            pageObjNums.Add(nextObj++);
            contentObjNums.Add(nextObj++);
        }

        var sb = new StringBuilder();
        var offsets = new List<long>();

        sb.Append("%PDF-1.4\n");

        // Obj 1: Catalog
        offsets.Add(sb.Length);
        var kidsRef = string.Join(" ", pageObjNums.Select(n => $"{n} 0 R"));
        sb.Append($"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n");

        // Obj 2: Pages
        offsets.Add(sb.Length);
        sb.Append($"2 0 obj\n<< /Type /Pages /Kids [{kidsRef}] /Count {pages.Length} >>\nendobj\n");

        // Per-page objects
        for (int i = 0; i < pages.Length; i++)
        {
            var pageObj    = pageObjNums[i];
            var contentObj = contentObjNums[i];

            // Page object
            while (offsets.Count < pageObj - 1) offsets.Add(0);
            offsets.Add(sb.Length);
            sb.Append($"{pageObj} 0 obj\n");
            sb.Append($"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n");
            sb.Append($"   /Resources << /Font << /F1 {nextObj} 0 R /F2 {nextObj + 1} 0 R >> >>\n");
            sb.Append($"   /Contents {contentObj} 0 R >>\n");
            sb.Append($"endobj\n");

            // Content stream
            var stream = BuildPageStream(pages[i]);
            var streamBytes = Encoding.ASCII.GetBytes(stream);
            offsets.Add(sb.Length);
            sb.Append($"{contentObj} 0 obj\n<< /Length {streamBytes.Length} >>\nstream\n");
            sb.Append(stream);
            sb.Append($"\nendstream\nendobj\n");
        }

        // Font objects (shared, referenced by last page's fontObj numbers — simplify: add after pages)
        int fontRegularObj = nextObj;
        int fontBoldObj    = nextObj + 1;

        offsets.Add(sb.Length);
        sb.Append($"{fontRegularObj} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n");
        offsets.Add(sb.Length);
        sb.Append($"{fontBoldObj} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n");

        // Cross-reference table
        var xrefOffset = sb.Length;
        int totalObjs = fontBoldObj + 1;
        sb.Append($"xref\n0 {totalObjs}\n");
        sb.Append("0000000000 65535 f \n");
        foreach (var off in offsets)
            sb.Append($"{off:D10} 00000 n \n");

        sb.Append($"trailer\n<< /Size {totalObjs} /Root 1 0 R >>\n");
        sb.Append($"startxref\n{xrefOffset}\n%%EOF");

        return Encoding.ASCII.GetBytes(sb.ToString());
    }

    private static string BuildPageStream(string pageText)
    {
        var stream = new StringBuilder();
        float y = 750f;

        var allLines = pageText.Split('\n');

        foreach (var raw in allLines)
        {
            var line = raw.TrimEnd();

            if (line.StartsWith("HEADER:"))
            {
                var text = EscapePdf(line["HEADER:".Length..]);
                stream.AppendLine($"BT /F2 16 Tf 50 {y:F1} Td ({text}) Tj ET");
                y -= 22;
                // Underline
                stream.AppendLine($"0.2 w 50 {y + 2:F1} m 562 {y + 2:F1} l S");
                y -= 6;
                continue;
            }

            if (line.StartsWith("SUBTITLE:"))
            {
                var text = EscapePdf(line["SUBTITLE:".Length..]);
                stream.AppendLine($"BT /F1 11 Tf 50 {y:F1} Td ({text}) Tj ET");
                y -= 22;
                continue;
            }

            if (string.IsNullOrWhiteSpace(line))
            {
                y -= 8;
                continue;
            }

            // Section headers (all caps, short, starts with A) B) etc. or ─)
            if (line.StartsWith("─") || (line.Length > 2 && line[1] == ')'))
            {
                if (line.StartsWith("─"))
                {
                    // Horizontal rule as PDF line
                    stream.AppendLine($"0.5 w 50 {y:F1} m 562 {y:F1} l S");
                    y -= 10;
                }
                else
                {
                    var text = EscapePdf(line);
                    stream.AppendLine($"BT /F2 10 Tf 50 {y:F1} Td ({text}) Tj ET");
                    y -= 14;
                }
                continue;
            }

            // NAPOMENE / all-caps section title
            if (line == line.ToUpper() && line.Trim().Length > 3 && !line.Contains("[") && !line.Contains("*") && !line.Contains("─"))
            {
                var text = EscapePdf(line);
                stream.AppendLine($"BT /F2 10 Tf 50 {y:F1} Td ({text}) Tj ET");
                y -= 14;
                continue;
            }

            // Normal line
            {
                var text = EscapePdf(line);
                stream.AppendLine($"BT /F1 9 Tf 50 {y:F1} Td ({text}) Tj ET");
                y -= 13;
            }
        }

        return stream.ToString();
    }

    private static string EscapePdf(string text)
    {
        // Strip Bosnian diacritics to stay ASCII-safe with built-in Helvetica
        text = text
            .Replace("č", "c").Replace("Č", "C")
            .Replace("ć", "c").Replace("Ć", "C")
            .Replace("š", "s").Replace("Š", "S")
            .Replace("ž", "z").Replace("Ž", "Z")
            .Replace("đ", "dj").Replace("Đ", "Dj")
            .Replace("(", "\\(").Replace(")", "\\)")
            .Replace("\\", "\\\\");
        return text;
    }
}
