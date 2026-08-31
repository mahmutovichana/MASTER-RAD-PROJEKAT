namespace RBBH.CollateralAppraisal.Application.Security.Interfaces;

/// <summary>
/// Izračunava permission-e trenutnog korisnika na osnovu njegovih rola.
/// Podržava korisnike sa više rola — permission-e se sabiraju.
/// </summary>
public interface IUserPermissionService
{
    /// <summary>
    /// Vraća true ako trenutni korisnik ima datu permission.
    /// </summary>
    bool CurrentUserHasPermission(string permission);
}
