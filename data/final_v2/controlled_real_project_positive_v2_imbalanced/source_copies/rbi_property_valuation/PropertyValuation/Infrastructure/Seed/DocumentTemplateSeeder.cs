﻿using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Documents;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

[ExcludeFromCodeCoverage]
public static class DocumentTemplateSeeder
{
    private static readonly (string Code, string Name, string Category, string SourceFile, int Sort, string? Roles)[] Templates =
    [
        (TemplateCodes.Narudzbenica,     "Narudžbenica za procjenu vrijednosti imovine",       TemplateCategories.Workflow, "Narudzbenica_sablon.docx",                1, null),
        (TemplateCodes.NarudzbenicaBr,   "Narudžbenica za procjenu (sa brojem)",               TemplateCategories.Workflow, "Narudzbenica_sablon_br.docx",             2, null),
        (TemplateCodes.Izjava,           "Izjava o nepostojanju sukoba interesa",              TemplateCategories.Workflow, "Izjava_sablon.doc",                       3, null),
        (TemplateCodes.IzjavaSukob,      "Izjava (alternativna verzija)",                      TemplateCategories.Workflow, "Izjava_o_nepostojanju_sukoba_interesa.doc",4, null),
        (TemplateCodes.UrnekNekretnine1, "Urnek procjene nekretnine — Tip 1 (Stan)",           TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_1.docx",        10, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekNekretnine2, "Urnek procjene nekretnine — Tip 2 (Kuća)",           TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_2.docx",        11, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekNekretnine3, "Urnek procjene nekretnine — Tip 3 (Poslovni)",       TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_3.docx",        12, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekNekretnine4, "Urnek procjene nekretnine — Tip 4 (Zemljište)",       TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_4.docx",        13, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekNekretnine5, "Urnek procjene nekretnine — Tip 5 (Garaža)",         TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_5.docx",        14, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekNekretnine6, "Urnek procjene nekretnine — Tip 6 (Kombinovani)",     TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_6.docx",        15, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekPokretna7,   "Urnek procjene pokretne imovine — Tip 7",             TemplateCategories.Urnek,   "Urnek_procjena_pokretne_imovine_7.docx",  16, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
        (TemplateCodes.UrnekNekretnine8, "Urnek procjene nekretnine — Tip 8 (Specijalni)",      TemplateCategories.Urnek,   "Urnek_procjena_nekretnine_8.docx",        17, $"{AppRoles.Vjestak},{AppRoles.KolateralOficir},{AppRoles.KolateralAdministrator}"),
    ];

    public static async Task SeedAsync(ApplicationDbContext db, IFileStorageProvider storage, ILogger? logger)
    {
        var templateDir = FindTemplateDir();
        if (templateDir is null) { logger?.LogWarning("Template directory not found — skipping."); return; }

        foreach (var (code, name, category, sourceFile, sort, roles) in Templates)
        {
            if (await db.DocumentTemplates.AnyAsync(t => t.Code == code)) continue;

            var sourcePath = Path.Combine(templateDir, sourceFile);
            if (!File.Exists(sourcePath))
            {
                logger?.LogWarning("Template fajl {File} ne postoji — preskaćem.", sourceFile);
                continue;
            }

            var fileBytes = await File.ReadAllBytesAsync(sourcePath);
            var contentType = sourceFile.EndsWith(".docx")
                ? "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                : "application/msword";

            await using var stream = new MemoryStream(fileBytes);
            var result = await storage.SaveAsync(stream, sourceFile, $"templates/{code.ToLowerInvariant()}");
            var storagePath = result.StoragePath;

            var template = DocumentTemplate.Create(
                code, name, null, category,
                sourceFile, contentType, fileBytes.Length, storagePath,
                sort, roles);

            db.DocumentTemplates.Add(template);
            logger?.LogInformation("Template '{Code}' seedovan ({Size} bytes).", code, fileBytes.Length);
        }

        await db.SaveChangesAsync();
    }

    private static string? FindTemplateDir()
    {
        var candidates = new[]
        {
            Path.Combine(AppContext.BaseDirectory, "Templates"),
            Path.Combine(AppContext.BaseDirectory, "..", "Infrastructure", "Templates"),
            Path.Combine(Directory.GetCurrentDirectory(), "src", "Infrastructure", "Templates"),
        };
        return candidates.FirstOrDefault(Directory.Exists);
    }
}
