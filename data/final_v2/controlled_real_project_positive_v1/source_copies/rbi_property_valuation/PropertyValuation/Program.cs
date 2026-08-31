using RBBH.CollateralAppraisal.Api.Extensions;
using RBBH.CollateralAppraisal.Infrastructure.Auth;

var builder = WebApplication.CreateBuilder(args);

// Lokalni override kredencijala — učitava se NAKON appsettings.Development.json.
// Fajl appsettings.Development.Local.json je gitignored i sadrži stvarne lozinke/secret-e.
// Kopiraj PropertyValuation/appsettings.Development.Local.json.example i popuni.
builder.Configuration
    .AddJsonFile("appsettings.Development.Local.json", optional: true, reloadOnChange: false);

builder.Services.AddApiServices(builder.Configuration);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddOpenApi();

var app = builder.Build();

var authentication = app.Services.GetRequiredService<AuthenticationStartupStatus>();
if (!authentication.KeycloakEnabled)
    app.Logger.LogWarning("{AuthenticationStatus}", authentication.Message);

await app.ApplyMigrationsAsync();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.ConfigurePipeline();

app.Run();

public partial class Program { }
