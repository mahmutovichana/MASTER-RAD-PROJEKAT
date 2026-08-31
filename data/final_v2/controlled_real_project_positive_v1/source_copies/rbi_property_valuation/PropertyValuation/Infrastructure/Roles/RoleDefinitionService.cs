using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Roles.Interfaces;
using RBBH.CollateralAppraisal.Application.Roles.Models;
using RBBH.CollateralAppraisal.Application.Roles.Requests;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Domain.Roles;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Roles;

/// <summary>
/// Upravljanje definicijama rola u SQL Server bazi + sinhronizacija s Keycloak-om.
///
/// Poslovna pravila:
/// - Sistemske role (IsSystem=true) ne mogu se mijenjati imenom ni brisati.
/// - Deaktivirana rola ne može se dodijeliti novim korisnicima.
/// - Custom rola se kreira u PG + Keycloak transakcijski (rollback ako Keycloak fail).
/// - Kada se promijene permissioni role, invalidira se IMemoryCache za tu rolu.
/// </summary>
public sealed class RoleDefinitionService : IRoleDefinitionService
{
    private readonly ApplicationDbContext _db;
    private readonly ICurrentUserService  _currentUser;
    private readonly IAuditService        _audit;
    private readonly IKeycloakRoleSyncService _keycloakSync;
    private readonly IMemoryCache _cache;
    private readonly ILogger<RoleDefinitionService> _logger;

    public RoleDefinitionService(
        ApplicationDbContext db,
        ICurrentUserService  currentUser,
        IAuditService        audit,
        IKeycloakRoleSyncService keycloakSync,
        IMemoryCache cache,
        ILogger<RoleDefinitionService> logger)
    {
        _db          = db;
        _currentUser = currentUser;
        _cache       = cache;
        _audit       = audit;
        _keycloakSync = keycloakSync;
        _logger      = logger;
    }

    public async Task<PagedResult<RoleDefinitionListItemDto>> GetAllAsync(
        RoleQueryRequest request, CancellationToken ct = default)
    {
        var query = _db.RoleDefinitions
            .AsNoTracking()
            .Include(r => r.Permissions)
            .AsQueryable();

        if (!string.IsNullOrWhiteSpace(request.Search))
        {
            var s = request.Search.Trim().ToLowerInvariant();
            query = query.Where(r =>
                r.Name.ToLower().Contains(s) ||
                r.DisplayName.ToLower().Contains(s));
        }

        if (request.IsActive.HasValue)
            query = query.Where(r => r.IsActive == request.IsActive.Value);

        var total = await query.CountAsync(ct);
        var page  = Math.Max(1, request.Page);
        var size  = Math.Clamp(request.PageSize, 1, 100);

        var rawItems = await query
            .OrderBy(r => r.IsSystem ? 0 : 1).ThenBy(r => r.Name)
            .Skip((page - 1) * size)
            .Take(size)
            .Select(r => new { r.Id, r.Name, r.DisplayName, r.Description,
                               r.IsSystem, r.IsActive, PermCount = r.Permissions.Count })
            .ToListAsync(ct);

        // Keycloak user counts — paralelno za sve role na stranici
        var userCountTasks = rawItems.Select(async r =>
        {
            try   { return await _keycloakSync.GetRoleUserCountAsync(r.Name, ct); }
            catch (Exception ex) { _logger.LogWarning(ex, "Nije moguće dohvatiti broj korisnika za rolu '{Role}' iz Keycloak-a.", r.Name); return 0; }
        });
        var userCounts = await Task.WhenAll(userCountTasks);

        var items = rawItems.Select((r, i) => new RoleDefinitionListItemDto(
            r.Id, r.Name, r.DisplayName, r.Description,
            r.IsSystem, r.IsActive,
            r.PermCount,
            userCounts[i])).ToList();

        return new PagedResult<RoleDefinitionListItemDto>
        {
            Items      = items,
            TotalCount = total,
            Page       = page,
            PageSize   = size
        };
    }

    public async Task<RoleDefinitionDto> GetByIdAsync(int id, CancellationToken ct = default)
    {
        var role = await FindOrThrowAsync(id, ct, includePermissions: true);
        return ToDto(role);
    }

    public async Task<RoleDefinitionDto> CreateAsync(CreateRoleRequest request, CancellationToken ct = default)
    {
        ValidateRoleName(request.Name);
        ValidateDisplayName(request.DisplayName);

        var duplicate = await _db.RoleDefinitions
            .AnyAsync(r => r.Name.ToLower() == request.Name.Trim().ToLower(), ct);
        if (duplicate)
            throw new ConflictException(
                $"Rola s imenom '{request.Name}' već postoji.", "ROLE_DUPLICATE_NAME");

        var role = RoleDefinition.CreateCustom(
            request.Name.Trim(), request.DisplayName.Trim(), request.Description?.Trim(),
            _currentUser.UserId);

        _db.RoleDefinitions.Add(role);
        await _db.SaveChangesAsync(ct);

        // Sinhronizacija s Keycloak-om — rollback ako ne uspije
        try
        {
            await _keycloakSync.CreateRoleAsync(role.Name, role.Description, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Keycloak sync failed za rolu {Role}. Rollback.", role.Name);
            _db.RoleDefinitions.Remove(role);
            await _db.SaveChangesAsync(ct);

            await RecordAuditAsync(AuditActions.KeycloakRoleSyncFailed, role, null, ct);
            throw new ConflictException(
                "Rola je kreirana lokalno ali nije sinhronizovana s Keycloak-om. Operacija je poništena.",
                "KEYCLOAK_SYNC_FAILED");
        }

        await RecordAuditAsync(AuditActions.RoleCreated, role,
            new { role.Name, role.DisplayName }, ct);

        return ToDto(role);
    }

    public async Task<RoleDefinitionDto> UpdateAsync(
        int id, UpdateRoleRequest request, CancellationToken ct = default)
    {
        ValidateDisplayName(request.DisplayName);

        var role = await FindOrThrowAsync(id, ct);
        var now  = DateTime.UtcNow;
        var old  = new { role.DisplayName, role.Description };

        role.Update(request.DisplayName.Trim(), request.Description?.Trim(),
            _currentUser.UserId, now);

        await _db.SaveChangesAsync(ct);
        await RecordAuditAsync(AuditActions.RoleUpdated, role,
            new { Old = old, New = new { role.DisplayName, role.Description } }, ct);

        return ToDto(role);
    }

    public async Task<RoleDefinitionDto> DeactivateAsync(int id, CancellationToken ct = default)
    {
        var role = await FindOrThrowAsync(id, ct);

        if (!role.IsActive)
            throw new ConflictException("Rola je već neaktivna.", "ROLE_ALREADY_INACTIVE");

        role.Deactivate(_currentUser.UserId, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);
        await RecordAuditAsync(AuditActions.RoleDeactivated, role, null, ct);

        return ToDto(role);
    }

    public async Task<RoleDefinitionDto> ActivateAsync(int id, CancellationToken ct = default)
    {
        var role = await FindOrThrowAsync(id, ct);

        if (role.IsActive)
            throw new ConflictException("Rola je već aktivna.", "ROLE_ALREADY_ACTIVE");

        role.Activate(_currentUser.UserId, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);
        await RecordAuditAsync(AuditActions.RoleReactivated, role, null, ct);

        return ToDto(role);
    }

    public async Task DeleteAsync(int id, CancellationToken ct = default)
    {
        var role = await FindOrThrowAsync(id, ct);

        if (role.IsSystem)
            throw new ConflictException(
                "Sistemske role se ne mogu brisati.", "ROLE_SYSTEM_DELETE_BLOCKED");

        // Provjeri da li je rola u upotrebi u Keycloak-u
        int userCount;
        try
        {
            userCount = await _keycloakSync.GetRoleUserCountAsync(role.Name, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Provjera upotrebe role {Role} nije uspjela.", role.Name);
            await RecordAuditAsync(AuditActions.RoleDeleteBlockedInUse, role,
                new { Reason = "Provjera nije uspjela (fail-safe)" }, ct);
            throw new ConflictException(
                "Provjera upotrebe role nije uspjela. Brisanje blokirano iz sigurnosnih razloga.",
                "ROLE_DELETE_BLOCKED_USAGE_CHECK_FAILED");
        }

        if (userCount > 0)
        {
            await RecordAuditAsync(AuditActions.RoleDeleteBlockedInUse, role,
                new { UserCount = userCount }, ct);
            throw new ConflictException(
                $"Rola se koristi na {userCount} korisnika i ne može se fizički obrisati. " +
                "Deaktivirajte je kako se ne bi mogla dodijeliti novim korisnicima.",
                "ROLE_DELETE_BLOCKED_IN_USE");
        }

        role.SoftDelete(_currentUser.UserId, DateTime.UtcNow);
        await _db.SaveChangesAsync(ct);

        // Pokušaj brisanja iz Keycloak-a (non-blocking)
        try
        {
            await _keycloakSync.DeleteRoleAsync(role.Name, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Rola {Role} je soft-deleted lokalno ali nije uklonjena iz Keycloaka.", role.Name);
            await RecordAuditAsync(AuditActions.KeycloakRoleSyncFailed, role, null, ct);
        }

        await RecordAuditAsync(AuditActions.RoleSoftDeleted, role, null, ct);
    }

    public async Task<RoleDefinitionDto> AddPermissionAsync(
        int roleId, int permissionId, CancellationToken ct = default)
    {
        var role = await FindOrThrowAsync(roleId, ct, includePermissions: true);

        var permission = await _db.PermissionDefinitions.FindAsync([permissionId], ct)
            ?? throw new NotFoundException(
                $"Permission s ID={permissionId} nije pronađen.", "PERMISSION_NOT_FOUND");

        if (role.Permissions.Any(p => p.PermissionDefinitionId == permissionId))
            throw new ConflictException(
                "Rola već ima ovaj permission.", "ROLE_PERMISSION_DUPLICATE");

        var rp = RolePermission.Create(roleId, permissionId, _currentUser.UserId);
        _db.RolePermissions.Add(rp);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.RolePermissionAdded, role,
            new { PermissionCode = permission.Code }, ct);

        // Invalidira cache za ovu rolu — sljedeći zahtjev učitava ažurirane permissione
        PermissionClaimsTransformation.InvalidateRoleCache(_cache, role.Name);

        return await GetByIdAsync(roleId, ct);
    }

    public async Task<RoleDefinitionDto> RemovePermissionAsync(
        int roleId, int permissionId, CancellationToken ct = default)
    {
        var role = await FindOrThrowAsync(roleId, ct, includePermissions: true);

        var rp = role.Permissions.FirstOrDefault(p => p.PermissionDefinitionId == permissionId)
            ?? throw new NotFoundException(
                "Rola nema ovaj permission.", "ROLE_PERMISSION_NOT_FOUND");

        var permission = await _db.PermissionDefinitions.FindAsync([permissionId], ct);
        _db.RolePermissions.Remove(rp);
        await _db.SaveChangesAsync(ct);

        await RecordAuditAsync(AuditActions.RolePermissionRemoved, role,
            new { PermissionCode = permission?.Code }, ct);

        // Invalidira cache — korisnici s ovom rolom gube permission pri sljedećem zahtjevu
        PermissionClaimsTransformation.InvalidateRoleCache(_cache, role.Name);

        return await GetByIdAsync(roleId, ct);
    }

    public async Task<IReadOnlyList<string>> GetPermissionCodesForRoleAsync(
        string roleName, CancellationToken ct = default)
    {
        return await _db.RoleDefinitions
            .AsNoTracking()
            .Where(r => r.Name == roleName && r.IsActive)
            .SelectMany(r => r.Permissions)
            .Select(rp => rp.PermissionDefinition.Code)
            .Distinct()
            .ToListAsync(ct);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private async Task<RoleDefinition> FindOrThrowAsync(
        int id, CancellationToken ct, bool includePermissions = false)
    {
        var query = _db.RoleDefinitions.AsQueryable();

        if (includePermissions)
            query = query.Include(r => r.Permissions)
                         .ThenInclude(p => p.PermissionDefinition);

        var role = await query.FirstOrDefaultAsync(r => r.Id == id, ct)
            ?? throw new NotFoundException($"Rola s ID={id} nije pronađena.", "ROLE_NOT_FOUND");

        return role;
    }

    private static void ValidateRoleName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("name", "REQUIRED_FIELD", "Naziv role je obavezan.")]);

        if (name.Length > 150)
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("name", "MAX_LENGTH_EXCEEDED", "Naziv role ne smije biti duži od 150 znakova.")]);

        if (name.Any(c => c == ' '))
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("name", "INVALID_FORMAT", "Naziv role ne smije sadržavati razmake. Koristite PascalCase.")]);
    }

    private static void ValidateDisplayName(string displayName)
    {
        if (string.IsNullOrWhiteSpace(displayName))
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("displayName", "REQUIRED_FIELD", "Prikazni naziv je obavezan.")]);

        if (displayName.Length > 250)
            throw new Application.Common.Exceptions.ValidationException(
                [new Application.Common.Models.ValidationFieldError("displayName", "MAX_LENGTH_EXCEEDED", "Prikazni naziv ne smije biti duži od 250 znakova.")]);
    }

    private async Task RecordAuditAsync(
        string action, RoleDefinition role, object? details, CancellationToken ct)
    {
        try
        {
            await _audit.RecordAsync(new AuditEvent
            {
                Action            = action,
                OperationType     = AuditOperationTypes.Update,
                Module            = AuditModules.Roles,
                EntityType        = nameof(RoleDefinition),
                EntityKey         = role.Id.ToString(),
                EntityDisplayName = role.DisplayName,
                NewValues         = details,
                Status            = AuditStatuses.Success,
                Severity          = AuditSeverity.Info
            }, ct);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Audit nije zapisan za rolu {Role}.", role.Name);
        }
    }

    private RoleDefinitionDto ToDto(RoleDefinition role)
    {
        var perms = role.Permissions
            .Where(p => p.PermissionDefinition is not null)
            .Select(p => new PermissionDefinitionDto(
                p.PermissionDefinition.Id,
                p.PermissionDefinition.Code,
                p.PermissionDefinition.DisplayName,
                p.PermissionDefinition.Description,
                p.PermissionDefinition.Module,
                p.PermissionDefinition.IsActive))
            .ToList();

        return new RoleDefinitionDto(
            role.Id, role.Name, role.DisplayName, role.Description,
            role.IsSystem, role.IsActive, role.DeletedAt.HasValue,
            role.CreatedAt, role.CreatedByUserId,
            role.UpdatedAt ?? role.CreatedAt, role.UpdatedByUserId,
            perms);
    }
}
