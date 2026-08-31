using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Domain.Appraisers;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

/// <summary>
/// Idempotentno puni tabelu vještaka testnim podacima za demo.
/// Pokreće se na svim okruženjima ako tabela prazna.
/// </summary>
public static class AppraiserSeeder
{
    public static async Task SeedAsync(
        ApplicationDbContext db,
        ILogger? logger = null,
        CancellationToken ct = default)
    {
        var anyExists = await db.Appraisers.IgnoreQueryFilters().AnyAsync(ct);
        if (anyExists)
        {
            logger?.LogInformation("AppraiserSeeder: vještaci već postoje, preskačem.");
            return;
        }

        var appraisers = new[]
        {
            Appraiser.Create(
                name:                   "Mirza Hodžić",
                city:                   "Sarajevo",
                legalForm:              AppraiserLegalForm.Individual,
                contactEmail:           "mirza.hodzic@procjene.ba",
                contactPhone:           "+387 61 111 222",
                notes:                  null,
                clientScope:            AppraiserClientScope.Sve,
                supportedPropertyTypes: null,
                supportedCities:        "Sarajevo,Ilidža,Hadžići"),

            Appraiser.Create(
                name:                   "Amra Softić",
                city:                   "Sarajevo",
                legalForm:              AppraiserLegalForm.Individual,
                contactEmail:           "amra.softic@procjene.ba",
                contactPhone:           "+387 62 333 444",
                notes:                  null,
                clientScope:            AppraiserClientScope.FizickaLica,
                supportedPropertyTypes: "STAN,KUCA",
                supportedCities:        "Sarajevo,Vogošća,Ilijaš"),

            Appraiser.Create(
                name:                   "Procjene d.o.o.",
                city:                   "Mostar",
                legalForm:              AppraiserLegalForm.Firm,
                contactEmail:           "info@procjene-mostar.ba",
                contactPhone:           "+387 36 555 666",
                notes:                  "Specijalizovani za poslovne prostore i industrijske objekte.",
                clientScope:            AppraiserClientScope.PravnaLica,
                supportedPropertyTypes: "POSLOVNI_PROSTOR,INDUSTRIJSKI_OBJEKAT",
                supportedCities:        "Mostar,Čapljina,Stolac"),

            Appraiser.Create(
                name:                   "Kenan Čović",
                city:                   "Tuzla",
                legalForm:              AppraiserLegalForm.Individual,
                contactEmail:           "kenan.covic@procjene.ba",
                contactPhone:           "+387 61 777 888",
                notes:                  null,
                clientScope:            AppraiserClientScope.Sve,
                supportedPropertyTypes: null,
                supportedCities:        "Tuzla,Živinice,Lukavac"),

            Appraiser.Create(
                name:                   "Lejla Mušanović",
                city:                   "Banja Luka",
                legalForm:              AppraiserLegalForm.Individual,
                contactEmail:           "lejla.musanovic@procjene.ba",
                contactPhone:           "+387 65 999 000",
                notes:                  null,
                clientScope:            AppraiserClientScope.FizickaLica,
                supportedPropertyTypes: "STAN,KUCA,GARAZA",
                supportedCities:        "Banja Luka,Laktaši,Gradiška"),

            Appraiser.Create(
                name:                   "Nekretnine Ekspert d.o.o.",
                city:                   "Sarajevo",
                legalForm:              AppraiserLegalForm.Firm,
                contactEmail:           "ekspert@nekretnine.ba",
                contactPhone:           "+387 33 444 555",
                notes:                  "Ovlašteni procjenitelji za sve tipove nekretnina.",
                clientScope:            AppraiserClientScope.Sve,
                supportedPropertyTypes: null,
                supportedCities:        null),
        };

        db.Appraisers.AddRange(appraisers);
        await db.SaveChangesAsync(ct);

        logger?.LogInformation("AppraiserSeeder: dodano {Count} vještaka.", appraisers.Length);
    }
}
