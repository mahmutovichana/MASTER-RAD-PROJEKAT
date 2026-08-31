using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public sealed class DocumentTemplateEndpoints : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/templates").WithTags("Document Templates");

        group.MapGet("/", ListTemplates)
            .RequireAuthorization(AppPolicies.DocumentsView)
            .WithName("ListDocumentTemplates")
            .WithSummary("Lista svih dostupnih šablona/urneka.");

        group.MapGet("/{id:int}/download", DownloadTemplate)
            .RequireAuthorization(AppPolicies.DocumentsDownload)
            .WithName("DownloadDocumentTemplate")
            .WithSummary("Preuzimanje šablona/urneka po ID-u.");
    }

    private static async Task<IResult> ListTemplates(
        ApplicationDbContext db,
        ICurrentUserService currentUser,
        string? category,
        CancellationToken ct)
    {
        var query = db.DocumentTemplates
            .AsNoTracking()
            .Where(t => t.IsActive);

        if (!string.IsNullOrWhiteSpace(category))
            query = query.Where(t => t.Category == category);

        var templates = await query
            .OrderBy(t => t.SortOrder)
            .Select(t => new
            {
                t.Id, t.Code, t.Name, t.Description, t.Category,
                t.FileName, t.FileSize, t.SortOrder, t.AllowedRoles
            })
            .ToListAsync(ct);

        // Filtriraj po roli korisnika
        var userRoles = currentUser.Roles;
        var filtered = templates.Where(t =>
            t.AllowedRoles is null ||
            t.AllowedRoles.Split(',').Any(r => userRoles.Contains(r.Trim(), StringComparer.OrdinalIgnoreCase))
        ).ToList();

        return Results.Ok(filtered);
    }

    private static async Task<IResult> DownloadTemplate(
        int id,
        ApplicationDbContext db,
        IFileStorageProvider storage,
        ICurrentUserService currentUser,
        CancellationToken ct)
    {
        var template = await db.DocumentTemplates
            .AsNoTracking()
            .FirstOrDefaultAsync(t => t.Id == id && t.IsActive, ct);

        if (template is null)
            return Results.NotFound("Šablon nije pronađen.");

        // Provjera role pristupa
        if (template.AllowedRoles is not null)
        {
            var allowed = template.AllowedRoles.Split(',').Select(r => r.Trim());
            if (!allowed.Any(r => currentUser.Roles.Contains(r, StringComparer.OrdinalIgnoreCase)))
                return Results.Forbid();
        }

        var stream = await storage.OpenReadAsync(template.StoragePath, ct);
        return Results.File(stream, template.ContentType, template.FileName);
    }
}
