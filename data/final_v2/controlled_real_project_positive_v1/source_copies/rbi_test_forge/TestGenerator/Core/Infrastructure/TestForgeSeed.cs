using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Domain.Enums;

namespace RBBH.TestAutomation.Core.Infrastructure;

/// <summary>
/// Idempotentan seed — provjerava po nazivu grupe i nazivu scenarija.
/// Siguran za visekratno pokretanje bez -v. Ne brise postojece podatke.
/// </summary>
public static class TestForgeSeed
{
    public static async Task SeedAsync(TestForgeDbContext db, CancellationToken ct = default)
    {
        var groupIds = await SeedGroupsAsync(db, ct);
        await SeedScenariosAsync(db, groupIds, ct);
        await SeedOperationalDataAsync(db, groupIds, ct);
        await SeedCodeListsAsync(db, ct);
    }

    private static async Task SeedCodeListsAsync(TestForgeDbContext db, CancellationToken ct)
    {
        var definitions = new (string Name, string Slug, string Description, string[] Values)[]
        {
            ("Vrste scenarija", "scenario-types", "Podržane vrste automatizovanih testova.", ["REST", "UI", "Blazor/bUnit"]),
            ("HTTP metode", "http-methods", "Metode dostupne REST scenarijima.", ["GET", "POST", "PUT", "PATCH", "DELETE"]),
            ("Vrste grupa", "group-tags", "Namjena grupe testova.", ["Smoke", "Regression", "Full"]),
            ("Statusi izvršavanja", "run-states", "Mogući ishodi izvršavanja.", ["Queued", "Running", "Passed", "Failed", "Cancelled"]),
            ("Vremenske zone", "timezones", "Vremenske zone rasporeda.", ["Europe/Sarajevo", "UTC"]),
        };

        foreach (var definition in definitions)
        {
            var category = await db.CodeListCategories.Include(x => x.Values)
                .SingleOrDefaultAsync(x => x.Slug == definition.Slug, ct);
            if (category is null)
            {
                category = new CodeListCategory { Name = definition.Name, Slug = definition.Slug, Description = definition.Description };
                db.CodeListCategories.Add(category);
            }
            for (var index = 0; index < definition.Values.Length; index++)
            {
                var value = definition.Values[index];
                if (!category.Values.Any(x => x.Name == value))
                    category.Values.Add(new CodeListValue { Name = value, Code = value.ToUpperInvariant().Replace('/', '_'), Order = index, CreatedBy = "seed" });
            }
        }
        await db.SaveChangesAsync(ct);
    }

    private static async Task SeedOperationalDataAsync(
        TestForgeDbContext db,
        (Guid Smoke, Guid Regression, Guid Full) groupIds,
        CancellationToken ct)
    {
        if (!await db.Schedules.AnyAsync(ct))
        {
            db.Schedules.AddRange(
                new ScheduleConfig { GroupId = groupIds.Smoke, CronExpression = "0 8 * * 1-5", IsActive = true, Timezone = "Europe/Sarajevo" },
                new ScheduleConfig { GroupId = groupIds.Regression, CronExpression = "0 20 * * 5", IsActive = true, Timezone = "Europe/Sarajevo" });
        }

        if (!await db.RunResults.AnyAsync(ct))
        {
            db.RunResults.AddRange(
                new RunResult { GroupId = groupIds.Smoke, State = RunState.Passed, TotalCount = 2, PassedCount = 2, PassRate = 100, Duration = TimeSpan.FromSeconds(4), CompletedAt = DateTime.UtcNow.AddMinutes(-15) },
                new RunResult { GroupId = groupIds.Regression, State = RunState.Failed, TotalCount = 3, PassedCount = 2, FailedCount = 1, PassRate = 66.67, Duration = TimeSpan.FromSeconds(11), StartedAt = DateTime.UtcNow.AddHours(-2), CompletedAt = DateTime.UtcNow.AddHours(-2).AddSeconds(11) });
        }

        if (!await db.ApiKeys.AnyAsync(ct))
        {
            db.ApiKeys.Add(new ApiKey
            {
                Name = "Lokalni CI primjer",
                Prefix = "local_ci",
                KeyHash = "development-seed-not-a-real-secret",
                CreatedBy = "seed",
                ExpiresAt = DateTime.UtcNow.AddMonths(3)
            });
        }

        await db.SaveChangesAsync(ct);
    }

    // Vraca (smokeId, regressionId, fullId) — bilo da su upravo kreirane ili vec postoje
    private static async Task<(Guid Smoke, Guid Regression, Guid Full)> SeedGroupsAsync(
        TestForgeDbContext db, CancellationToken ct)
    {
        var existing = await db.Groups
            .Where(g => g.Naziv == "Smoke Tests" || g.Naziv == "Regression Suite" || g.Naziv == "Full Suite")
            .Select(g => new { g.Id, g.Naziv })
            .ToListAsync(ct);

        Guid smokeId      = existing.FirstOrDefault(g => g.Naziv == "Smoke Tests")?.Id      ?? Guid.Empty;
        Guid regressionId = existing.FirstOrDefault(g => g.Naziv == "Regression Suite")?.Id ?? Guid.Empty;
        Guid fullId       = existing.FirstOrDefault(g => g.Naziv == "Full Suite")?.Id        ?? Guid.Empty;

        var toAdd = new List<TestGroup>();

        if (smokeId == Guid.Empty)
        {
            smokeId = Guid.NewGuid();
            toAdd.Add(new TestGroup
            {
                Id = smokeId, Naziv = "Smoke Tests", Tag = TestTag.Smoke,
                Opis = "Brza provjera da sistem radi", Boja = "#4CAF50", Prioritet = 100,
                KreiranOd = "seed", KreiranAt = DateTime.UtcNow
            });
        }

        if (regressionId == Guid.Empty)
        {
            regressionId = Guid.NewGuid();
            toAdd.Add(new TestGroup
            {
                Id = regressionId, Naziv = "Regression Suite", Tag = TestTag.Regression,
                Opis = "Provjera da izmjene nisu pokvarile postojece funkcionalnosti", Boja = "#2196F3", Prioritet = 80,
                KreiranOd = "seed", KreiranAt = DateTime.UtcNow
            });
        }

        if (fullId == Guid.Empty)
        {
            fullId = Guid.NewGuid();
            toAdd.Add(new TestGroup
            {
                Id = fullId, Naziv = "Full Suite", Tag = TestTag.Full,
                Opis = "Kompletna test suita — svi testovi", Boja = "#9C27B0", Prioritet = 60,
                KreiranOd = "seed", KreiranAt = DateTime.UtcNow
            });
        }

        if (toAdd.Count > 0)
        {
            db.Groups.AddRange(toAdd);
            await db.SaveChangesAsync(ct);
        }

        return (smokeId, regressionId, fullId);
    }

    private static async Task SeedScenariosAsync(
        TestForgeDbContext db,
        (Guid Smoke, Guid Regression, Guid Full) groupIds,
        CancellationToken ct)
    {
        // HttpMetoda enum: Get=0, Post=1, Put=2, Patch=3, Delete=4
        var seedNazivi = new[]
        {
            "Dohvati objavu (GET /posts/1)",
            "Lista svih objava (GET /posts)",
            "Kreiraj objavu (POST /posts)",
            "Dohvati korisnika (GET /users/1)",
            "Lista zadataka korisnika (GET /users/1/todos)",
            "Azuriraj objavu (PUT /posts/1)",
            "Obrisi objavu (DELETE /posts/1)",
            "Komentari objave (GET /posts/1/comments)",
        };

        var existingNazivi = await db.Scenarios
            .Where(s => seedNazivi.Contains(s.Naziv))
            .Select(s => s.Naziv)
            .ToListAsync(ct);

        var toAdd = new List<TestScenario>();

        void TryAdd(string naziv, Guid groupId, int red, string tip, string target, string act)
        {
            if (!existingNazivi.Contains(naziv))
                toAdd.Add(new TestScenario
                {
                    GroupId = groupId, Redoslijed = red, Naziv = naziv,
                    Tip = tip, Target = target, KreiranOd = "seed", KreiranAt = DateTime.UtcNow,
                    Act = act
                });
        }

        TryAdd("Dohvati objavu (GET /posts/1)", groupIds.Smoke, 0, "Rest",
            "https://jsonplaceholder.typicode.com/posts/1",
            """{"Metoda":0,"Url":"https://jsonplaceholder.typicode.com/posts/1","Headeri":[],"RequestBody":null,"OcekivaniStatus":200,"ResponseAsserti":[{"JsonPutanja":"$.id","OcekivanaVrijednost":"1"},{"JsonPutanja":"$.userId","OcekivanaVrijednost":"1"}]}""");

        TryAdd("Lista svih objava (GET /posts)", groupIds.Smoke, 1, "Rest",
            "https://jsonplaceholder.typicode.com/posts",
            """{"Metoda":0,"Url":"https://jsonplaceholder.typicode.com/posts","Headeri":[],"RequestBody":null,"OcekivaniStatus":200,"ResponseAsserti":[{"JsonPutanja":"$[0].id","OcekivanaVrijednost":"1"},{"JsonPutanja":"$[0].userId","OcekivanaVrijednost":"1"}]}""");

        TryAdd("Kreiraj objavu (POST /posts)", groupIds.Regression, 0, "Rest",
            "https://jsonplaceholder.typicode.com/posts",
            """{"Metoda":1,"Url":"https://jsonplaceholder.typicode.com/posts","Headeri":[{"Kljuc":"Content-Type","Vrijednost":"application/json"}],"RequestBody":"{\"title\":\"Test objava\",\"body\":\"Automatski generisan REST scenarij\",\"userId\":1}","OcekivaniStatus":201,"ResponseAsserti":[{"JsonPutanja":"$.id","OcekivanaVrijednost":"101"},{"JsonPutanja":"$.title","OcekivanaVrijednost":"Test objava"}]}""");

        TryAdd("Dohvati korisnika (GET /users/1)", groupIds.Regression, 1, "Rest",
            "https://jsonplaceholder.typicode.com/users/1",
            """{"Metoda":0,"Url":"https://jsonplaceholder.typicode.com/users/1","Headeri":[],"RequestBody":null,"OcekivaniStatus":200,"ResponseAsserti":[{"JsonPutanja":"$.id","OcekivanaVrijednost":"1"},{"JsonPutanja":"$.username","OcekivanaVrijednost":"Bret"},{"JsonPutanja":"$.email","OcekivanaVrijednost":"Sincere@april.biz"}]}""");

        TryAdd("Lista zadataka korisnika (GET /users/1/todos)", groupIds.Regression, 2, "Rest",
            "https://jsonplaceholder.typicode.com/users/1/todos",
            """{"Metoda":0,"Url":"https://jsonplaceholder.typicode.com/users/1/todos","Headeri":[],"RequestBody":null,"OcekivaniStatus":200,"ResponseAsserti":[{"JsonPutanja":"$[0].userId","OcekivanaVrijednost":"1"},{"JsonPutanja":"$[0].id","OcekivanaVrijednost":"1"}]}""");

        TryAdd("Azuriraj objavu (PUT /posts/1)", groupIds.Full, 0, "Rest",
            "https://jsonplaceholder.typicode.com/posts/1",
            """{"Metoda":2,"Url":"https://jsonplaceholder.typicode.com/posts/1","Headeri":[{"Kljuc":"Content-Type","Vrijednost":"application/json"}],"RequestBody":"{\"id\":1,\"title\":\"Azuriran naslov\",\"body\":\"Azurirani sadrzaj\",\"userId\":1}","OcekivaniStatus":200,"ResponseAsserti":[{"JsonPutanja":"$.id","OcekivanaVrijednost":"1"},{"JsonPutanja":"$.title","OcekivanaVrijednost":"Azuriran naslov"}]}""");

        TryAdd("Obrisi objavu (DELETE /posts/1)", groupIds.Full, 1, "Rest",
            "https://jsonplaceholder.typicode.com/posts/1",
            """{"Metoda":4,"Url":"https://jsonplaceholder.typicode.com/posts/1","Headeri":[],"RequestBody":null,"OcekivaniStatus":200,"ResponseAsserti":[]}""");

        TryAdd("Komentari objave (GET /posts/1/comments)", groupIds.Full, 2, "Rest",
            "https://jsonplaceholder.typicode.com/posts/1/comments",
            """{"Metoda":0,"Url":"https://jsonplaceholder.typicode.com/posts/1/comments","Headeri":[],"RequestBody":null,"OcekivaniStatus":200,"ResponseAsserti":[{"JsonPutanja":"$[0].postId","OcekivanaVrijednost":"1"},{"JsonPutanja":"$[0].id","OcekivanaVrijednost":"1"}]}""");

        if (toAdd.Count > 0)
        {
            db.Scenarios.AddRange(toAdd);
            await db.SaveChangesAsync(ct);
        }
    }
}
