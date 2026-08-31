using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Common.Branches;
using RBBH.CollateralAppraisal.Domain.Branches;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;
using System.Diagnostics.CodeAnalysis;

namespace RBBH.CollateralAppraisal.Infrastructure.Seed;

/// <summary>
/// Seeder koji derivira podatke isključivo iz <see cref="BranchCatalog"/> —
/// eliminacija dual-source problema (ADR-053 fix).
/// BranchCatalog je jedini source of truth; seeder je derivat, ne duplikat.
/// Dodavanje nove poslovnice: samo ažurirati BranchCatalog.All.
/// </summary>
[ExcludeFromCodeCoverage]
public static class BranchSeeder
{
    public static async Task SeedAsync(ApplicationDbContext db)
    {
        var byCity = BranchCatalog.All
            .GroupBy(b => b.CityName, StringComparer.OrdinalIgnoreCase);

        foreach (var cityGroup in byCity)
        {
            var city = await db.Cities
                .FirstOrDefaultAsync(c => c.Name == cityGroup.Key);

            if (city is null)
            {
                city = City.Create(cityGroup.Key);
                db.Cities.Add(city);
                await db.SaveChangesAsync();
            }

            foreach (var branchItem in cityGroup)
            {
                var exists = await db.Branches
                    .AnyAsync(x => x.Code == branchItem.Code);

                if (!exists)
                {
                    db.Branches.Add(
                        Branch.Create(branchItem.Code, branchItem.Name, branchItem.Address, city.Id));
                }
            }
        }

        await db.SaveChangesAsync();
    }
}
