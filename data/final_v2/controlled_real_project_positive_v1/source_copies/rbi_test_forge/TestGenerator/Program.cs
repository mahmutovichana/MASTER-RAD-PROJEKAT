using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text.Json;
using System.Text.Json.Serialization;
using RBBH.TestAutomation.Api.Api;
using RBBH.TestAutomation.Api.Auth;
using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Core.Infrastructure;
using RBBH.TestAutomation.Api.IoC;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.Auth;
using RBBH.TestAutomation.Api.Services.Groups;
using RBBH.TestAutomation.Api.Services.Run;
using RBBH.TestAutomation.Api.Services.Scenarios;
using RBBH.TestAutomation.Api.Services.Schedules;
using Hangfire;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;
using Serilog;
using Serilog.Formatting.Elasticsearch;
using Microsoft.OpenApi.Models;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddProblemDetails();
builder.Services.ConfigureHttpJsonOptions(options =>
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter()));
builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-CSRF-TOKEN";
    options.Cookie.HttpOnly = true;
    options.Cookie.SameSite = SameSiteMode.Lax;
    options.Cookie.SecurePolicy = builder.Environment.IsDevelopment()
        ? CookieSecurePolicy.SameAsRequest
        : CookieSecurePolicy.Always;
});
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options => options.SwaggerDoc("v1", new OpenApiInfo
{
    Title = "RBBH Test Automation API",
    Version = "v1",
    Description = "API za scenarije, grupe, generisanje i izvršavanje automatizovanih testova."
}));

var databaseConfigured = ConnectionHelper.IsConfigured(builder.Configuration);
if (databaseConfigured)
    builder.Configuration["ConnectionStrings:Default"] =
        ConnectionHelper.BuildConnection(builder.Configuration);

builder.Host.UseSerilog(
    (ctx, lc) =>
        lc
            .Enrich.FromLogContext()
            .ReadFrom.Configuration(builder.Configuration)
            .WriteTo.Console(new ElasticsearchJsonFormatter())
);

var mockAuthRequested = builder.Configuration.GetValue<bool?>("MockAuth:Enabled");
var oidcSection = builder.Configuration.GetSection("OpenIDConnectSettings");
var oidcConfigured = !string.IsNullOrWhiteSpace(oidcSection["Authority"])
    && !string.IsNullOrWhiteSpace(oidcSection["ClientId"])
    && !string.IsNullOrWhiteSpace(oidcSection["ClientSecret"]);
var useInMemoryDatabase = builder.Environment.IsDevelopment() && !databaseConfigured;
var mockAuth = builder.Environment.IsDevelopment() && (mockAuthRequested is true || !oidcConfigured);

if (!databaseConfigured && !builder.Environment.IsDevelopment())
    throw new InvalidOperationException(
        "SQL Server nije konfigurisan. Postavite Database__ServerName i Database__Name.");

if (useInMemoryDatabase)
    Console.Error.WriteLine("WARNING: SQL Server nije konfigurisan; koristi se lokalna in-memory baza.");

if (!oidcConfigured)
{
    Console.Error.WriteLine(
        builder.Environment.IsDevelopment()
            ? "WARNING: Keycloak nije konfigurisan; koristi se lokalni mock korisnik."
            : "WARNING: Keycloak nije konfigurisan; prijava neće biti dostupna.");
}

// Sigurnosna brana — mock autentikacija nije dozvoljena u produkciji.
if (mockAuthRequested is true && builder.Environment.IsProduction())
    throw new InvalidOperationException(
        "SIGURNOST: MockAuth:Enabled=true nije dozvoljeno u Production okruženju. " +
        "Postavi env var MockAuth__Enabled=false.");

if (!mockAuth)
{
    builder
        .Services.AddAuthentication(options =>
        {
            options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
            options.DefaultAuthenticateScheme = CookieAuthenticationDefaults.AuthenticationScheme;
            options.DefaultSignInScheme = CookieAuthenticationDefaults.AuthenticationScheme;
            options.DefaultChallengeScheme = CookieAuthenticationDefaults.AuthenticationScheme;
        })
        .AddCookie(
            CookieAuthenticationDefaults.AuthenticationScheme,
            options =>
            {
                options.ExpireTimeSpan = TimeSpan.FromMinutes(30);
                options.Cookie.Path = "/";
                options.Cookie.HttpOnly = true;
                options.Cookie.SecurePolicy = builder.Environment.IsDevelopment()
                    ? CookieSecurePolicy.SameAsRequest
                    : CookieSecurePolicy.Always;
                options.Cookie.SameSite = SameSiteMode.Lax;
                options.SlidingExpiration = true;
                options.Events.OnRedirectToLogin = context =>
                {
                    if (context.Request.Path.StartsWithSegments("/api"))
                    {
                        context.Response.StatusCode = StatusCodes.Status401Unauthorized;
                        return Task.CompletedTask;
                    }
                    context.Response.Redirect(context.RedirectUri);
                    return Task.CompletedTask;
                };
            }
        )
        .AddOpenIdConnect(
            AuthOptions.OidcScheme,
            options =>
            {
                builder.Configuration.GetSection("OpenIDConnectSettings").Bind(options);
                options.RequireHttpsMetadata = !builder.Environment.IsDevelopment();
                options.SignInScheme = CookieAuthenticationDefaults.AuthenticationScheme;
                options.ResponseType = OpenIdConnectResponseType.Code;
                // response_mode=query (KC vraća GET redirectom umjesto form_post POST-a) +
                // correlation/nonce cookie SameSite=Lax. Default (form_post + SameSite=None)
                // traži HTTPS pa "Correlation failed" preko plain HTTP-a. Lax se šalje na
                // top-level GET navigaciju → radi i preko IP/HTTP (isti site) i preko
                // HTTPS subdomena (cross-site top-level GET).
                options.ResponseMode = OpenIdConnectResponseMode.Query;
                options.CorrelationCookie.SameSite = SameSiteMode.Lax;
                options.NonceCookie.SameSite = SameSiteMode.Lax;
                options.GetClaimsFromUserInfoEndpoint = true;
                options.SaveTokens = true;
                options.MapInboundClaims = false;
                options.TokenValidationParameters.NameClaimType = JwtRegisteredClaimNames.Name;
                options.TokenValidationParameters.RoleClaimType = "roles";
                options.MaxAge = TimeSpan.FromHours(8);
                options.Scope.Clear();
                options.Scope.Add("openid");
                options.Scope.Add("profile");
                options.Scope.Add("email");
                options.Scope.Add("roles");

                options.Events = new OpenIdConnectEvents
                {
                    OnTokenValidated = context =>
                    {
                        if (context.Principal?.Identity is ClaimsIdentity identity)
                        {
                            foreach (var roleClaim in identity.FindAll("roles").ToList())
                            {
                                if (!identity.HasClaim(ClaimTypes.Role, roleClaim.Value))
                                    identity.AddClaim(new Claim(ClaimTypes.Role, roleClaim.Value));
                            }
                            var realmAccess = identity.FindFirst("realm_access")?.Value;
                            if (!string.IsNullOrWhiteSpace(realmAccess))
                            {
                                try
                                {
                                    using var document = JsonDocument.Parse(realmAccess);
                                    if (document.RootElement.TryGetProperty("roles", out var roles))
                                        foreach (var role in roles.EnumerateArray().Select(x => x.GetString()).Where(x => !string.IsNullOrWhiteSpace(x)))
                                            if (!identity.HasClaim(ClaimTypes.Role, role!))
                                                identity.AddClaim(new Claim(ClaimTypes.Role, role!));
                                }
                                catch (JsonException)
                                {
                                    // Neispravan optional claim ne smije srušiti prijavu; autorizacija ostaje bez tih uloga.
                                }
                            }
                        }

                        var username = context.Principal?.FindFirst("preferred_username")?.Value
                            ?? context.Principal?.FindFirst("name")?.Value
                            ?? "unknown";
                        var ip = context.HttpContext.Connection.RemoteIpAddress?.ToString();

                        context.HttpContext.RequestServices
                            .GetRequiredService<SecurityEventLogger>()
                            .LogLoginSuccess(username, ip);

                        return Task.CompletedTask;
                    },
                    OnAuthenticationFailed = context =>
                    {
                        var logger = context.HttpContext.RequestServices
                            .GetRequiredService<ILoggerFactory>()
                            .CreateLogger("AuthDiagnostics");
                        logger.LogError(
                            context.Exception,
                            "OIDC authentication failed. Path={Path}; Error={Error}",
                            context.HttpContext.Request.Path.Value,
                            context.ProtocolMessage?.Error);

                        context.HttpContext.RequestServices
                            .GetRequiredService<SecurityEventLogger>()
                            .LogLoginFailure(
                                "unknown",
                                context.HttpContext.Connection.RemoteIpAddress?.ToString(),
                                context.Exception?.Message ?? AuditFailureReasons.InvalidCredentials);

                        return Task.CompletedTask;
                    },
                    OnRemoteFailure = context =>
                    {
                        var logger = context.HttpContext.RequestServices
                            .GetRequiredService<ILoggerFactory>()
                            .CreateLogger("AuthDiagnostics");
                        logger.LogError(
                            context.Failure,
                            "OIDC remote failure. Path={Path}; Error={Error}",
                            context.HttpContext.Request.Path.Value,
                            context.Request.Query["error"].ToString());

                        context.HttpContext.RequestServices
                            .GetRequiredService<SecurityEventLogger>()
                            .LogLoginFailure(
                                "unknown",
                                context.HttpContext.Connection.RemoteIpAddress?.ToString(),
                                context.Request.Query["error"].ToString() is { Length: > 0 } e
                                    ? e : AuditFailureReasons.InvalidCredentials);

                        // Spriječi bubble-up u generičku 500 stranicu — preusmjeri na
                        // friendly stranicu s porukom i opcijom ponovne prijave.
                        context.Response.Redirect("/greska-prijave");
                        context.HandleResponse();
                        return Task.CompletedTask;
                    },
                };
            }
        );

    builder.Services.ConfigureCookieOidcRefresh(
        CookieAuthenticationDefaults.AuthenticationScheme,
        AuthOptions.OidcScheme);
    builder.Services.AddAuthorization();

    DependencyContainer.RegisterService(builder.Services, useInMemoryDatabase);
}
else
{
    builder.Services.AddScoped<IUserContext, MockUserContext>();
    // HTTP-level auth — potrebno u .NET 8+ jer endpoint routing provjerava [Authorize]
    // na HTTP nivou, ne samo na Blazor komponentnom nivou.
    builder.Services.AddAuthentication("Mock")
        .AddScheme<AuthenticationSchemeOptions, MockHttpAuthHandler>("Mock", null);
    builder.Services.AddAuthorization();
    builder.Services.AddHttpClient("KeycloakAdmin");
    builder.Services.AddSingleton<IKeycloakAdminService, MockKeycloakAdminService>();
    builder.Services.AddSingleton<IAuditLogStore, InMemoryAuditLogStore>();
    builder.Services.AddScoped<SecurityEventLogger>();
    builder.Services.AddScoped<IdleTimeoutService>();
    builder.Services.AddHttpClient("ScenarioRunner");
    builder.Services.AddScoped<IScenarioRunner, ScenarioRunner>();
    builder.Services.AddScoped<IGroupTestExecutor, GroupTestExecutor>();
    builder.Services.AddScoped<TestRunStateService>();
    builder.Services.AddScoped<IXUnitTestRunner, XUnitTestRunner>();
    // Notifikacijski servisi i u mock modu.
    builder.Services.AddSingleton<RBBH.TestAutomation.Api.Services.Notifications.EmailSender>();
    builder.Services.AddSingleton<RBBH.TestAutomation.Api.Services.Notifications.SlackSender>();
    builder.Services.AddSingleton<RBBH.TestAutomation.Api.Services.Notifications.TeamsSender>();
    builder.Services.AddScoped<RBBH.TestAutomation.Api.Services.Notifications.INotificationService,
        RBBH.TestAutomation.Api.Services.Notifications.NotificationService>();
}

// Baza i autentifikacija su nezavisne: stvarni SQL Server se koristi čim je
// konfigurisan, a Development bez connection stringa koristi EF Core InMemory.
DependencyContainer.RegisterTestForge(builder.Services, builder.Configuration);

builder.Services.AddHttpContextAccessor();

builder.Services.AddScoped<ISifarnikService, SifarnikService>();

builder.Services.AddScoped<IScenarioImportExportService, ScenarioImportExportService>();
// US #5 — servis grupa testova (mock/real switch je u AddGroupServices, prati MockGroups:Enabled).
builder.Services.AddGroupServices(builder.Configuration);

// Generatori su stateless — nema zavisnosti na bazu ni auth, registruju se uvijek.
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Generation.RestTestGenerator>();
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Generation.BUnitTestGenerator>();
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Generation.PlaywrightE2eGenerator>();

// E2E runner — okida Playwright na GitHub Actions (workflow_dispatch) i vraća stanje.
// Stateless (samo HttpClient + config), registruje se uvijek (mock i real mod).
builder.Services.AddHttpClient("GitHubApi");
builder.Services.AddScoped<RBBH.TestAutomation.Api.Services.Run.IGitHubActionsE2eRunner,
    RBBH.TestAutomation.Api.Services.Run.GitHubActionsE2eRunner>();

// Formatteri izvještaja run-a (JUnit/TRX/HTML/JSON) — stateless, biraju se po formatu u report endpointu.
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Reporting.IRunReportFormatter, RBBH.TestAutomation.Core.Reporting.JsonReportFormatter>();
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Reporting.IRunReportFormatter, RBBH.TestAutomation.Core.Reporting.JUnitReportFormatter>();
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Reporting.IRunReportFormatter, RBBH.TestAutomation.Core.Reporting.TrxReportFormatter>();
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Reporting.IRunReportFormatter, RBBH.TestAutomation.Core.Reporting.HtmlReportFormatter>();

// TAG-37 — OpenAPI/Swagger parser (stateless) + HTTP klijent za dohvat swagger.json s URL-a.
builder.Services.AddSingleton<RBBH.TestAutomation.Core.Parsing.IOpenApiEndpointParser,
    RBBH.TestAutomation.Core.Parsing.OpenApiEndpointParser>();
builder.Services.AddHttpClient("SwaggerFetch");

// Servis scenarija — pravi EF Core kada MockAuth/MockScenarios nije aktivan.
builder.Services.AddScenarioServices(builder.Configuration);

// Hangfire rasporedi — SQL Server backend u pravom modu, in-memory mock u dev modu.
builder.Services.AddScheduleServices(builder.Configuration);

// CI/CD run servis — Singleton tracker jobova pokrenutih preko REST API-ja.
builder.Services.AddSingleton<RBBH.TestAutomation.Api.Services.Ci.ICiRunService, RBBH.TestAutomation.Api.Services.Ci.CiRunService>();

builder.Services.AddMemoryCache();

// Iza reverse proxyja (nginx, TLS terminacija): vjeruj X-Forwarded-Proto/For da app
// zna da je zahtjev stigao kao HTTPS. Bez ovoga OIDC Secure cookie-ji i redirect URI
// se grade kao http → login puca iza proxyja.
builder.Services.Configure<ForwardedHeadersOptions>(options =>
{
    options.ForwardedHeaders =
        ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
    // Proxy je u Docker mreži (promjenjiva interna IP) — ne ograničavaj na poznate proxyje.
    options.KnownIPNetworks.Clear();
    options.KnownProxies.Clear();
});

// DataProtection koristi platformsku lokaciju, osim kada deployment eksplicitno
// zada trajni direktorij. Putanja nikada nije zakucana u aplikacijskom kodu.
var dataProtection = builder.Services.AddDataProtection().SetApplicationName("RBBH.TestAutomation.Api");
var keysPath = builder.Configuration["DataProtection:KeysPath"];
if (!string.IsNullOrWhiteSpace(keysPath))
    dataProtection.PersistKeysToFileSystem(new DirectoryInfo(keysPath));

// Health checks prikazuju oba nezavisna podsistema i u fallback režimu.
var healthChecks = builder.Services.AddHealthChecks();
healthChecks.AddCheck<RBBH.TestAutomation.Api.Health.DatabaseHealthCheck>("database");
healthChecks.AddCheck<RBBH.TestAutomation.Api.Health.KeycloakHealthCheck>("keycloak");

var app = builder.Build();

// MORA biti prvi middleware — da scheme/IP budu ispravni prije auth/redirect logike.
app.UseForwardedHeaders();
app.Use(async (context, next) =>
{
    context.Response.Headers["X-Content-Type-Options"] = "nosniff";
    context.Response.Headers["X-Frame-Options"] = "DENY";
    context.Response.Headers["Referrer-Policy"] = "no-referrer";
    context.Response.Headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'";
    await next();
});

// Baza se priprema nezavisno od izabranog načina autentifikacije.
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<TestForgeDbContext>();
    if (db.Database.IsRelational() && db.Database.GetMigrations().Any())
        await db.Database.MigrateAsync();
    else
        await db.Database.EnsureCreatedAsync();
    if (app.Environment.IsDevelopment() || app.Environment.IsEnvironment("Staging"))
        await TestForgeSeed.SeedAsync(db);
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler();
    app.UseHsts();
}

if (!app.Environment.IsDevelopment())
    app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseSwagger(options => options.RouteTemplate = "openapi/{documentName}.json");
app.UseCookiePolicy(new CookiePolicyOptions { Secure = CookieSecurePolicy.SameAsRequest });

if (!mockAuth)
{
    app.UseAuthentication();
    app.UseAuthorization();

    // Dashboard mora biti NAKON UseAuthentication da bi User.IsInRole() vidio claims.
    // U Development okruženju bez Keycloaka: nema auth filtera (slobodan pristup za testiranje).
    var dashboardAuth = app.Environment.IsDevelopment()
        ? Array.Empty<Hangfire.Dashboard.IDashboardAuthorizationFilter>()
        : (Hangfire.Dashboard.IDashboardAuthorizationFilter[])[new RBBH.TestAutomation.Api.Auth.HangfireDashboardAuthFilter()];

    app.UseHangfireDashboard("/hangfire", new DashboardOptions
    {
        Authorization  = dashboardAuth,
        DashboardTitle = "Test Generator Jobs",
        AppPath        = "/rasporedi",   // "Back to site" vodi na Rasporedi stranicu
        DisplayStorageConnectionString = false,
    });

    app.MapGet(
        "/authentication/login",
        (string? returnUrl) =>
            Results.Challenge(
                new AuthenticationProperties { RedirectUri = SafeLocal(returnUrl) },
                new[] { AuthOptions.OidcScheme }
            )
    );

    app.MapGet(
        "/authentication/logout",
        (HttpContext http) =>
        {
            var username = http.User.FindFirst("preferred_username")?.Value
                ?? http.User.Identity?.Name ?? "unknown";
            http.RequestServices
                .GetRequiredService<SecurityEventLogger>()
                .LogLogout(username, http.Connection.RemoteIpAddress?.ToString());

            return Results.SignOut(
                new AuthenticationProperties { RedirectUri = "/" },
                new[] { CookieAuthenticationDefaults.AuthenticationScheme, AuthOptions.OidcScheme }
            );
        }
    );

}
else
{
    app.UseAuthentication();
    app.UseAuthorization();

    // Mock mod: dashboard s InMemory storage-om, bez auth filtera.
    app.UseHangfireDashboard("/hangfire", new DashboardOptions
    {
        Authorization  = [],
        DashboardTitle = "Test Generator Jobs (Mock)",
        AppPath        = "/rasporedi",
        DisplayStorageConnectionString = false,
    });

}

app.Use(async (context, next) =>
{
    var mutation = HttpMethods.IsPost(context.Request.Method)
        || HttpMethods.IsPut(context.Request.Method)
        || HttpMethods.IsPatch(context.Request.Method)
        || HttpMethods.IsDelete(context.Request.Method);
    if (mutation && context.Request.Path.StartsWithSegments("/api/frontend"))
    {
        var antiforgery = context.RequestServices.GetRequiredService<Microsoft.AspNetCore.Antiforgery.IAntiforgery>();
        try { await antiforgery.ValidateRequestAsync(context); }
        catch (Microsoft.AspNetCore.Antiforgery.AntiforgeryValidationException)
        {
            context.Response.StatusCode = StatusCodes.Status400BadRequest;
            await context.Response.WriteAsJsonAsync(new ProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Sigurnosna provjera zahtjeva nije uspjela.",
                Detail = "Osvježite stranicu i pokušajte ponovo."
            });
            return;
        }
    }
    await next();
});

// Health endpoint (anoniman) — 200 ako su app + baza + Keycloak zdravi, inače 503.
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");
app.MapGet("/api/security/csrf", (Microsoft.AspNetCore.Antiforgery.IAntiforgery antiforgery, HttpContext context) =>
{
    var tokens = antiforgery.GetAndStoreTokens(context);
    return Results.Ok(new { token = tokens.RequestToken });
}).RequireAuthorization();

// CI/CD REST API — pokretanje grupa/tagova i polling statusa iz pipeline-a.
app.MapCiRunEndpoints();
app.MapFrontendDataEndpoints();

// Ovaj proces je isključivo backend za novi React frontend. U lokalnom radu
// otvaranje API porta vodi developera na odgovarajući frontend umjesto na
// uklonjeni prethodni serverski interfejs.
if (app.Environment.IsDevelopment())
    app.MapGet("/", () => Results.Redirect("http://localhost:8081"));

app.Run();

static string SafeLocal(string? url) =>
    !string.IsNullOrWhiteSpace(url) && url.StartsWith('/') && !url.StartsWith("//") ? url : "/";
