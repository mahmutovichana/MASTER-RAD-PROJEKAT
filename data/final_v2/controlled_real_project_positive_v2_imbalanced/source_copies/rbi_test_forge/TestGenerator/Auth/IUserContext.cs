namespace RBBH.TestAutomation.Api.Auth;

public interface IUserContext
{
    string UserId { get; }
    string FullName { get; }
    string Email { get; }
    string[] Roles { get; }
    bool IsAuthenticated { get; }
    string Initials { get; }
    bool HasRole(string role);
    bool HasAnyRole(params string[] roles);
    bool CanAccess(string module);
}
