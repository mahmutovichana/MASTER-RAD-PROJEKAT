using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;

namespace RBBH.TestAutomation.Api.Services;

/// <summary>EF Core implementacija šifrarnika; jednako radi sa SQL Server i InMemory providerom.</summary>
public sealed class SifarnikService(TestForgeDbContext db) : ISifarnikService
{
    public async Task<IReadOnlyList<SifarnikKategorijaDto>> GetKategorijeAsync(CancellationToken ct = default) =>
        await db.CodeListCategories.AsNoTracking().Where(x => x.Active).OrderBy(x => x.Name)
            .Select(x => new SifarnikKategorijaDto(x.Id, x.Name, x.Slug, x.Description, x.Active, x.CreatedAt)).ToListAsync(ct);

    public async Task<SifarnikKategorijaDto?> GetKategorijaBySlugAsync(string slug, CancellationToken ct = default) =>
        await db.CodeListCategories.AsNoTracking().Where(x => x.Slug == slug)
            .Select(x => new SifarnikKategorijaDto(x.Id, x.Name, x.Slug, x.Description, x.Active, x.CreatedAt)).SingleOrDefaultAsync(ct);

    public async Task<IReadOnlyList<SifarnikVrijednostDto>> GetVrijednostiAsync(Guid kategorijaId, bool onlyActive = false, CancellationToken ct = default) =>
        await db.CodeListValues.AsNoTracking().Where(x => x.CategoryId == kategorijaId && (!onlyActive || x.Active))
            .OrderBy(x => x.Order).ThenBy(x => x.Name).Select(ToDto).ToListAsync(ct);

    public async Task<SifarnikVrijednostDto?> GetVrijednostByIdAsync(Guid id, CancellationToken ct = default) =>
        await db.CodeListValues.AsNoTracking().Where(x => x.Id == id).Select(ToDto).SingleOrDefaultAsync(ct);

    public async Task<Guid> CreateVrijednostAsync(CreateSifarnikVrijednostRequest request, string actorId, string actorName, CancellationToken ct = default)
    {
        var name = request.Naziv.Trim();
        if (await db.CodeListValues.AnyAsync(x => x.CategoryId == request.KategorijaId && x.Name == name, ct))
            throw new InvalidOperationException($"Vrijednost \"{name}\" već postoji u ovoj kategoriji.");
        if (!await db.CodeListCategories.AnyAsync(x => x.Id == request.KategorijaId, ct))
            throw new InvalidOperationException("Kategorija šifrarnika ne postoji.");
        var entity = new CodeListValue { CategoryId = request.KategorijaId, Name = name, Code = request.Kod, Order = request.Redoslijed, Active = request.Active, CreatedBy = actorId };
        db.CodeListValues.Add(entity);
        AddAudit(entity.Id, AuditActions.Create, actorId, actorName, null, entity);
        await db.SaveChangesAsync(ct);
        return entity.Id;
    }

    public async Task UpdateVrijednostAsync(Guid id, UpdateSifarnikVrijednostRequest request, string actorId, string actorName, CancellationToken ct = default)
    {
        var entity = await db.CodeListValues.SingleOrDefaultAsync(x => x.Id == id, ct)
            ?? throw new InvalidOperationException("Vrijednost šifrarnika ne postoji.");
        var old = Snapshot(entity);
        var name = request.Naziv.Trim();
        if (await db.CodeListValues.AnyAsync(x => x.Id != id && x.CategoryId == entity.CategoryId && x.Name == name, ct))
            throw new InvalidOperationException($"Vrijednost \"{name}\" već postoji u ovoj kategoriji.");
        entity.Name = name; entity.Code = request.Kod; entity.Order = request.Redoslijed; entity.Active = request.Active;
        entity.UpdatedBy = actorId; entity.UpdatedAt = DateTime.UtcNow;
        AddAudit(id, AuditActions.Update, actorId, actorName, old, entity);
        await db.SaveChangesAsync(ct);
    }

    public async Task DeleteVrijednostAsync(Guid id, string actorId, string actorName, CancellationToken ct = default)
    {
        var entity = await db.CodeListValues.SingleOrDefaultAsync(x => x.Id == id, ct)
            ?? throw new InvalidOperationException("Vrijednost šifrarnika ne postoji.");
        AddAudit(id, AuditActions.Delete, actorId, actorName, entity, null);
        db.CodeListValues.Remove(entity);
        await db.SaveChangesAsync(ct);
    }

    // Uloge se čuvaju u Keycloaku, ne u lokalnoj bazi, pa šifrarnik nema lokalne FK upotrebe.
    public Task<int> CountUsagesAsync(Guid vrijednostId, CancellationToken ct = default) => Task.FromResult(0);
    public Task<bool> IsVrijednostInUseAsync(Guid vrijednostId, CancellationToken ct = default) => Task.FromResult(false);

    public async Task<AuditLogEntryDto?> GetLastAuditEntryAsync(string entityType, Guid entityId, CancellationToken ct = default) =>
        await db.AuditEntries.AsNoTracking().Where(x => x.EntityType == entityType && x.EntityId == entityId)
            .OrderByDescending(x => x.ChangedAt).Select(ToAuditDto).FirstOrDefaultAsync(ct);

    public async Task<IReadOnlyDictionary<Guid, AuditLogEntryDto>> GetLastAuditEntriesAsync(string entityType, IEnumerable<Guid> entityIds, CancellationToken ct = default)
    {
        var ids = entityIds.Distinct().ToArray();
        if (ids.Length == 0) return new Dictionary<Guid, AuditLogEntryDto>();
        var rows = await db.AuditEntries.AsNoTracking().Where(x => x.EntityType == entityType && x.EntityId.HasValue && ids.Contains(x.EntityId.Value))
            .OrderByDescending(x => x.ChangedAt).Select(ToAuditDto).ToListAsync(ct);
        return rows.Where(x => x.EntityId.HasValue).GroupBy(x => x.EntityId!.Value).ToDictionary(x => x.Key, x => x.First());
    }

    private void AddAudit(Guid id, string action, string actorId, string actorName, object? oldValue, object? newValue) =>
        db.AuditEntries.Add(new ApplicationAuditEntry { EntityType = AuditEntityTypes.SifarnikVrijednost, EntityId = id, Action = action, ChangedBy = actorId, ChangedByName = actorName, OldValues = Serialize(oldValue), NewValues = Serialize(newValue) });

    private static object Snapshot(CodeListValue x) => new { x.Id, x.CategoryId, x.Name, x.Code, x.Order, x.Active, x.CreatedBy, x.CreatedAt, x.UpdatedBy, x.UpdatedAt };
    private static string? Serialize(object? value) => value is null ? null : JsonSerializer.Serialize(value);
    private static readonly System.Linq.Expressions.Expression<Func<CodeListValue, SifarnikVrijednostDto>> ToDto = x => new(x.Id, x.CategoryId, x.Name, x.Code, x.Order, x.Active, x.CreatedBy, x.CreatedAt, x.UpdatedBy, x.UpdatedAt);
    private static readonly System.Linq.Expressions.Expression<Func<ApplicationAuditEntry, AuditLogEntryDto>> ToAuditDto = x => new(x.Id, x.EntityType, x.EntityId, x.Action, x.ChangedBy, x.ChangedByName, x.ChangedAt, x.OldValues, x.NewValues);
}
