using RBBH.TestAutomation.Api.Auth;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.ApiKeys;
using RBBH.TestAutomation.Api.Services.Auth;
using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Api.Services.Schedules;
using RBBH.TestAutomation.Core.Generation;
using RBBH.TestAutomation.Core.Parsing;
using System.Text.Json;

namespace RBBH.TestAutomation.Api.Api;

/// <summary>Stabilni HTTP ugovor React klijenta nad postojećim poslovnim servisima.</summary>
public static class FrontendDataEndpoints
{
    public static IEndpointRouteBuilder MapFrontendDataEndpoints(this IEndpointRouteBuilder app)
    {
        var api = app.MapGroup("/api/frontend").RequireAuthorization().WithTags("Frontend");
        MapProfile(api); MapGroups(api); MapScenarios(api); MapSchedules(api);
        MapHistory(api); MapApiKeys(api); MapUsers(api); MapCodeLists(api);
        MapAudit(api); MapGenerator(api);
        return app;
    }

    private static void MapProfile(RouteGroupBuilder api) => api.MapGet("/profile", (IUserContext user) => Results.Ok(new
    {
        user.UserId, user.FullName, user.Email, user.Initials, user.Roles, user.IsAuthenticated,
        Modules = new
        {
            Groups = user.CanAccess(AppModules.Grupe), Scenarios = user.CanAccess(AppModules.TestScenarios),
            Generator = user.CanAccess(AppModules.TestGenerator), ApiImport = user.CanAccess(AppModules.ApiImport),
            Users = user.CanAccess(AppModules.Korisnici), CodeLists = user.CanAccess(AppModules.Sifarnici),
            Audit = user.CanAccess(AppModules.AuditLog), ApiKeys = user.CanAccess(AppModules.ApiKeys)
        }
    }));

    private static void MapGroups(RouteGroupBuilder api)
    {
        var routes = api.MapGroup("/groups");
        routes.MapGet("/", async (IGroupService service, CancellationToken ct) => Results.Ok(await service.GetGroupsTreeAsync(ct)));
        routes.MapGet("/{id:guid}", async (Guid id, IGroupService service, CancellationToken ct) =>
            await service.GetByIdAsync(id, ct) is { } value ? Results.Ok(value) : Results.NotFound());
        routes.MapPost("/", async (CreateGroupRequest request, IGroupService service, IUserContext user, CancellationToken ct) =>
        {
            var errors = ValidateGroup(request.Naziv, request.Prioritet);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            var id = await service.CreateAsync(request, user.UserId, user.FullName, ct);
            return Results.Created($"/api/frontend/groups/{id}", new { id });
        });
        routes.MapPut("/{id:guid}", async (Guid id, UpdateGroupRequest request, IGroupService service, IUserContext user, CancellationToken ct) =>
        {
            var errors = ValidateGroup(request.Naziv, request.Prioritet);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            await service.UpdateAsync(id, request, user.UserId, user.FullName, ct);
            return Results.NoContent();
        });
        routes.MapDelete("/{id:guid}", async (Guid id, IGroupService service, IUserContext user, CancellationToken ct) =>
        { await service.DeleteAsync(id, user.UserId, user.FullName, ct); return Results.NoContent(); });
        routes.MapPost("/{id:guid}/run", async (Guid id, IGroupTestExecutor runner, CancellationToken ct) =>
            Results.Ok(await runner.ExecuteGroupAsync(id, new RunOptions(), ct)));
    }

    private static void MapScenarios(RouteGroupBuilder api)
    {
        var routes = api.MapGroup("/scenarios");
        routes.MapGet("/", async (IScenarioService service, CancellationToken ct) => Results.Ok(await service.GetAllAsync(ct)));
        routes.MapGet("/{id:guid}", async (Guid id, IScenarioService service, CancellationToken ct) =>
            await service.GetByIdAsync(id, ct) is { } value ? Results.Ok(value) : Results.NotFound());
        routes.MapPost("/", async (CreateScenarioRequest request, IScenarioService service, IGroupService groups, IUserContext user, CancellationToken ct) =>
        {
            var errors = ValidateScenario(request.GroupId, request.Naziv, request.Opis, request.Tip, request.Rest, request.Ui, request.Blazor);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            if (request.GroupId is not { } groupId || await groups.GetByIdAsync(groupId, ct) is null)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["groupId"] = ["Odabrana grupa testova ne postoji."] });
            var id = await service.CreateAsync(request, user.UserId, user.FullName, ct);
            return Results.Created($"/api/frontend/scenarios/{id}", new { id });
        });
        routes.MapPut("/{id:guid}", async (Guid id, UpdateScenarioRequest request, IScenarioService service, IGroupService groups, IUserContext user, CancellationToken ct) =>
        {
            var errors = ValidateScenario(request.GroupId, request.Naziv, request.Opis, request.Tip, request.Rest, request.Ui, request.Blazor);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            if (request.GroupId is not { } groupId || await groups.GetByIdAsync(groupId, ct) is null)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["groupId"] = ["Odabrana grupa testova ne postoji."] });
            await service.UpdateAsync(id, request, user.UserId, user.FullName, ct);
            return Results.NoContent();
        });
        routes.MapDelete("/{id:guid}", async (Guid id, IScenarioService service, IUserContext user, CancellationToken ct) =>
        { await service.DeleteAsync(id, user.UserId, user.FullName, ct); return Results.NoContent(); });
        routes.MapPost("/{id:guid}/clone", async (Guid id, IScenarioService service, IUserContext user, CancellationToken ct) =>
            Results.Ok(await service.CloneAsync(id, user.UserId, user.FullName, ct)));
        routes.MapPost("/{id:guid}/run", async (Guid id, IScenarioRunner runner, IScenarioService scenarios, CancellationToken ct) =>
        {
            var scenario = await scenarios.GetByIdAsync(id, ct);
            return scenario is null
                ? Results.NotFound()
                : Results.Ok(await runner.RunAsync(scenario, await scenarios.GetRunConfigAsync(ct), ct));
        });
    }

    private static void MapSchedules(RouteGroupBuilder api)
    {
        var routes = api.MapGroup("/schedules");
        routes.MapGet("/", async (IScheduleService service, CancellationToken ct) => Results.Ok(await service.GetAllAsync(ct)));
        routes.MapPost("/", async (CreateScheduleRequest request, IScheduleService service, IGroupService groups, CancellationToken ct) =>
        {
            var errors = ValidateSchedule(request.CronExpression, request.Timezone, request.GroupId);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            if (await groups.GetByIdAsync(request.GroupId, ct) is null)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["groupId"] = ["Odabrana grupa testova ne postoji."] });
            var id = await service.CreateAsync(request, ct);
            return Results.Created($"/api/frontend/schedules/{id}", new { id });
        });
        routes.MapPut("/{id:guid}", async (Guid id, UpdateScheduleRequest request, IScheduleService service, CancellationToken ct) =>
        {
            var errors = ValidateSchedule(request.CronExpression, request.Timezone);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            await service.UpdateAsync(id, request, ct);
            return Results.NoContent();
        });
        routes.MapDelete("/{id:guid}", async (Guid id, IScheduleService service, CancellationToken ct) =>
        { await service.DeleteAsync(id, ct); return Results.NoContent(); });
        routes.MapPost("/{id:guid}/run", async (Guid id, IScheduleService service, CancellationToken ct) =>
        { await service.TriggerNowAsync(id, ct); return Results.Accepted(); });
    }

    private static void MapHistory(RouteGroupBuilder api)
    {
        api.MapGet("/history", async (IRunHistoryService service, CancellationToken ct) =>
            Results.Ok(await service.GetHistoryAsync(new RunHistoryFilter(), ct)));
        api.MapGet("/history/dashboard", async (IRunHistoryService service, CancellationToken ct) => Results.Ok(await service.GetDashboardAsync(ct)));
        api.MapGet("/history/trend", async (int? days, IRunHistoryService service, CancellationToken ct) =>
            Results.Ok(await service.GetTrendAsync(Math.Clamp(days ?? 30, 1, 365), ct)));
    }

    private static void MapApiKeys(RouteGroupBuilder api)
    {
        var routes = api.MapGroup("/api-keys");
        routes.MapGet("/", async (IApiKeyService service, CancellationToken ct) => Results.Ok(await service.GetAllAsync(ct)));
        routes.MapPost("/", async (ApiKeyCreateRequest request, IApiKeyService service, IUserContext user, CancellationToken ct) =>
        {
            if (string.IsNullOrWhiteSpace(request.Name))
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["name"] = ["Naziv ključa je obavezan."] });
            if (request.Name.Trim().Length > 120)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["name"] = ["Naziv ključa može imati najviše 120 znakova."] });
            if (request.ExpiresAt is { } expiresAt && expiresAt <= DateTime.UtcNow)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["expiresAt"] = ["Datum isteka mora biti u budućnosti."] });
            var result = await service.GenerateAsync(request.Name.Trim(), request.ExpiresAt, user.UserId, ct);
            return Results.Created($"/api/frontend/api-keys/{result.Key.Id}", new { result.Key, result.RawKey });
        });
        routes.MapDelete("/{id:guid}", async (Guid id, IApiKeyService service, CancellationToken ct) =>
        { await service.RevokeAsync(id, ct); return Results.NoContent(); });
    }

    private static void MapUsers(RouteGroupBuilder api)
    {
        var routes = api.MapGroup("/users");
        routes.MapGet("/", async (IKeycloakAdminService service, CancellationToken ct) => Results.Ok(await service.GetUsersWithRolesAsync(ct)));
        routes.MapGet("/roles", () => Results.Ok(AppRoles.All));
        routes.MapPut("/{userId}/roles", async (string userId, UpdateRolesRequest request, IKeycloakAdminService service, CancellationToken ct) =>
        {
            var requested = (request.Roles ?? []).Where(role => !string.IsNullOrWhiteSpace(role)).Distinct(StringComparer.OrdinalIgnoreCase).ToArray();
            if (requested.Any(role => !AppRoles.All.Contains(role, StringComparer.OrdinalIgnoreCase)))
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["roles"] = ["Zahtjev sadrži nepoznatu ulogu."] });
            var current = (await service.GetUsersWithRolesAsync(ct)).FirstOrDefault(x => x.User.Id == userId);
            if (current is null) return Results.NotFound();
            foreach (var role in current.Roles.Except(requested, StringComparer.OrdinalIgnoreCase)) await service.RemoveRoleAsync(userId, role, ct);
            foreach (var role in requested.Except(current.Roles, StringComparer.OrdinalIgnoreCase)) await service.AssignRoleAsync(userId, role, ct);
            return Results.NoContent();
        });
    }

    private static void MapCodeLists(RouteGroupBuilder api)
    {
        var routes = api.MapGroup("/code-lists");
        routes.MapGet("/", async (ISifarnikService service, CancellationToken ct) => Results.Ok(await service.GetKategorijeAsync(ct)));
        routes.MapGet("/{categoryId:guid}/values", async (Guid categoryId, ISifarnikService service, CancellationToken ct) =>
            Results.Ok(await service.GetVrijednostiAsync(categoryId, false, ct)));
        routes.MapPost("/{categoryId:guid}/values", async (Guid categoryId, CodeValueRequest request, ISifarnikService service, IUserContext user, CancellationToken ct) =>
        {
            var errors = ValidateCodeValue(request);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            var id = await service.CreateVrijednostAsync(new(categoryId, request.Name.Trim(), request.Code?.Trim(), request.Order, request.Active), user.UserId, user.FullName, ct);
            return Results.Created($"/api/frontend/code-lists/{categoryId}/values/{id}", new { id });
        });
        routes.MapPut("/{categoryId:guid}/values/{id:guid}", async (Guid categoryId, Guid id, CodeValueRequest request, ISifarnikService service, IUserContext user, CancellationToken ct) =>
        {
            var errors = ValidateCodeValue(request);
            if (errors.Count > 0) return Results.ValidationProblem(errors);
            _ = categoryId;
            await service.UpdateVrijednostAsync(id, new(request.Name.Trim(), request.Code?.Trim(), request.Order, request.Active), user.UserId, user.FullName, ct);
            return Results.NoContent();
        });
        routes.MapDelete("/{categoryId:guid}/values/{id:guid}", async (Guid categoryId, Guid id, ISifarnikService service, IUserContext user, CancellationToken ct) =>
        {
            _ = categoryId;
            if (await service.IsVrijednostInUseAsync(id, ct)) return Results.Conflict(new { message = "Vrijednost je u upotrebi i ne može se obrisati." });
            await service.DeleteVrijednostAsync(id, user.UserId, user.FullName, ct); return Results.NoContent();
        });
    }

    private static void MapAudit(RouteGroupBuilder api) => api.MapGet("/audit", (int? limit, IAuditLogStore store) =>
        Results.Ok(store.GetRecent(Math.Clamp(limit ?? 100, 1, 500))));

    private static void MapGenerator(RouteGroupBuilder api)
    {
        api.MapPost("/generator/rest", (RestEndpointSpec request, RestTestGenerator generator) =>
        {
            var errors = ValidateRestGenerator(request);
            return errors.Count > 0 ? Results.ValidationProblem(errors) : Results.Ok(generator.Generate(request));
        });
        api.MapPost("/generator/component/analyze", (ComponentAnalysisRequest request) =>
        {
            if (request.Files.Count == 0)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["files"] = ["Odaberite najmanje jedan .razor ili .razor.cs fajl."] });
            if (request.Files.Count > 250 || request.Files.Sum(file => file.Content.Length) > 5_000_000)
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["files"] = ["Projekt može sadržavati najviše 250 fajlova i 5 MB teksta."] });
            var files = request.Files
                .Where(file => file.RelativePath.EndsWith(".razor", StringComparison.OrdinalIgnoreCase) || file.RelativePath.EndsWith(".razor.cs", StringComparison.OrdinalIgnoreCase))
                .Select(file => new BlazorRazorFile(file.RelativePath, file.Content))
                .ToArray();
            return Results.Ok(BlazorProjectAnalyzer.Analyze(files));
        });
        api.MapPost("/generator/component", (ComponentGenerationRequest request, BUnitTestGenerator bunit, PlaywrightE2eGenerator playwright) =>
        {
            if (string.IsNullOrWhiteSpace(request.Spec.ComponentName))
                return Results.ValidationProblem(new Dictionary<string, string[]> { ["componentName"] = ["Naziv komponente je obavezan."] });
            return request.Framework.ToLowerInvariant() switch
            {
                "bunit" => Results.Ok(bunit.Generate(request.Spec)),
                "playwright" => Results.Ok(playwright.Generate(request.Spec)),
                _ => Results.ValidationProblem(new Dictionary<string, string[]> { ["framework"] = ["Podržani generatori su bUnit i Playwright."] })
            };
        });
        api.MapPost("/api-import/parse", (OpenApiContentRequest request, IOpenApiEndpointParser parser) =>
        {
            if (string.IsNullOrWhiteSpace(request.Content))
                return Results.BadRequest(new { message = "OpenAPI dokument je prazan." });
            if (request.Content.Length > 5_000_000) return Results.BadRequest(new { message = "OpenAPI dokument ne smije biti veći od 5 MB." });
            var parsed = parser.Parse(request.Content);
            return parsed.Success ? Results.Ok(parsed) : Results.BadRequest(new { message = parsed.Error });
        });
    }

    private static Dictionary<string, string[]> ValidateGroup(string name, int priority)
    {
        var errors = new Dictionary<string, string[]>();
        if (string.IsNullOrWhiteSpace(name)) errors["name"] = ["Naziv grupe je obavezan."];
        else if (name.Trim().Length > 200) errors["name"] = ["Naziv može imati najviše 200 znakova."];
        if (priority is < 0 or > 1000) errors["priority"] = ["Prioritet mora biti između 0 i 1000."];
        return errors;
    }

    private static Dictionary<string, string[]> ValidateScenario(Guid? groupId, string name, string? description, TipScenarija type, RestScenarioDto? rest, UiScenarioDto? ui, BlazorScenarioDto? blazor)
    {
        var errors = new Dictionary<string, string[]>();
        if (groupId is null || groupId == Guid.Empty) errors["groupId"] = ["Scenarij mora biti dodijeljen grupi testova."];
        if (string.IsNullOrWhiteSpace(name)) errors["name"] = ["Naziv scenarija je obavezan."];
        else if (name.Trim().Length > 200) errors["name"] = ["Naziv scenarija može imati najviše 200 znakova."];
        if (description?.Length > 1000) errors["description"] = ["Opis može imati najviše 1000 znakova."];
        if (type == TipScenarija.Rest && rest is null) errors["rest"] = ["REST konfiguracija je obavezna."];
        if (type == TipScenarija.Ui && ui is null) errors["ui"] = ["UI koraci su obavezni."];
        if (type == TipScenarija.Blazor && blazor is null) errors["blazor"] = ["Sadržaj komponente je obavezan."];
        if (rest is { OcekivaniStatus: < 100 or > 599 }) errors["expectedStatus"] = ["HTTP status mora biti između 100 i 599."];
        if (rest is not null)
        {
            if (!IsEndpointUrl(rest.Url)) errors["url"] = ["Unesite ispravan HTTP(S) URL ili adresu koja počinje sa {{baseUrl}}."];
            if (!string.IsNullOrWhiteSpace(rest.RequestBody) && !IsJson(rest.RequestBody)) errors["requestBody"] = ["Tijelo zahtjeva mora biti ispravan JSON."];
            if (rest.Headeri.Any(header => string.IsNullOrWhiteSpace(header.Kljuc))) errors["headers"] = ["Svaki HTTP header mora imati naziv."];
            if (rest.ResponseAsserti.Any(assertion => string.IsNullOrWhiteSpace(assertion.JsonPutanja))) errors["assertions"] = ["Svaka provjera odgovora mora imati JSON putanju."];
        }
        if (ui is not null)
        {
            if (!IsEndpointUrl(ui.UrlStranice)) errors["pageUrl"] = ["Unesite ispravan URL stranice ili adresu koja počinje sa {{baseUrl}}."];
            if (ui.Koraci.Count == 0) errors["steps"] = ["Dodajte najmanje jedan UI korak."];
        }
        if (blazor is not null && (string.IsNullOrWhiteSpace(blazor.ComponentName) || string.IsNullOrWhiteSpace(blazor.RazorContent)))
            errors["blazor"] = ["Naziv komponente i Razor sadržaj su obavezni."];
        return errors;
    }

    private static bool IsEndpointUrl(string? value)
    {
        if (string.IsNullOrWhiteSpace(value)) return false;
        if (value.StartsWith("{{baseUrl}}", StringComparison.Ordinal)) return value.Length > "{{baseUrl}}".Length;
        return Uri.TryCreate(value, UriKind.Absolute, out var uri) && (uri.Scheme == Uri.UriSchemeHttp || uri.Scheme == Uri.UriSchemeHttps);
    }

    private static bool IsJson(string value)
    {
        try { using var _ = JsonDocument.Parse(value); return true; }
        catch (JsonException) { return false; }
    }

    private static Dictionary<string, string[]> ValidateSchedule(string cronExpression, string timezone, Guid? groupId = null)
    {
        var errors = new Dictionary<string, string[]>();
        if (!CronUtil.IsValid(cronExpression))
            errors["cronExpression"] = ["Unesite ispravan Cron izraz sa pet polja, npr. 0 8 * * 1-5."];
        if (string.IsNullOrWhiteSpace(timezone))
            errors["timezone"] = ["Vremenska zona je obavezna."];
        else
        {
            try { _ = TimeZoneInfo.FindSystemTimeZoneById(timezone.Trim()); }
            catch (TimeZoneNotFoundException) { errors["timezone"] = ["Odabrana vremenska zona nije podržana."]; }
            catch (InvalidTimeZoneException) { errors["timezone"] = ["Odabrana vremenska zona nije ispravna."]; }
        }
        if (groupId == Guid.Empty)
            errors["groupId"] = ["Odaberite grupu testova."];
        return errors;
    }

    private static Dictionary<string, string[]> ValidateCodeValue(CodeValueRequest request)
    {
        var errors = new Dictionary<string, string[]>();
        if (string.IsNullOrWhiteSpace(request.Name))
            errors["name"] = ["Naziv je obavezan."];
        else if (request.Name.Trim().Length > 200)
            errors["name"] = ["Naziv može imati najviše 200 znakova."];
        if (request.Code?.Trim().Length > 100)
            errors["code"] = ["Šifra može imati najviše 100 znakova."];
        if (request.Order is < 0 or > 10000)
            errors["order"] = ["Redoslijed mora biti između 0 i 10000."];
        return errors;
    }

    private static Dictionary<string, string[]> ValidateRestGenerator(RestEndpointSpec request)
    {
        var errors = new Dictionary<string, string[]>();
        if (string.IsNullOrWhiteSpace(request.ClassName) || !System.Text.RegularExpressions.Regex.IsMatch(request.ClassName, "^[A-Za-z_][A-Za-z0-9_]*$"))
            errors["className"] = ["Naziv test klase mora biti ispravan C# identifikator."];
        if (!new[] { "GET", "POST", "PUT", "PATCH", "DELETE" }.Contains(request.HttpMethod, StringComparer.OrdinalIgnoreCase))
            errors["httpMethod"] = ["Odaberite podržanu HTTP metodu."];
        if (string.IsNullOrWhiteSpace(request.RoutePath) || !request.RoutePath.StartsWith('/'))
            errors["routePath"] = ["Ruta mora počinjati znakom /."];
        if (request.ExpectedStatus is < 100 or > 599)
            errors["expectedStatus"] = ["HTTP status mora biti između 100 i 599."];
        if (!string.IsNullOrWhiteSpace(request.RequestBodyJson) && !IsJson(request.RequestBodyJson))
            errors["requestBodyJson"] = ["Tijelo zahtjeva mora biti ispravan JSON."];
        return errors;
    }

    private sealed record ApiKeyCreateRequest(string Name, DateTime? ExpiresAt);
    private sealed record UpdateRolesRequest(IReadOnlyList<string> Roles);
    private sealed record CodeValueRequest(string Name, string? Code, int Order, bool Active = true);
    private sealed record OpenApiContentRequest(string Content);
    private sealed record ComponentFileRequest(string RelativePath, string Content);
    private sealed record ComponentAnalysisRequest(IReadOnlyList<ComponentFileRequest> Files);
    private sealed record ComponentGenerationRequest(string Framework, BlazorComponentSpec Spec);
}
