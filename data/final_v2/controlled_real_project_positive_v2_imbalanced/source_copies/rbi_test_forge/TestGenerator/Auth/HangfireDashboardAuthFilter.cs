using Hangfire.Dashboard;

namespace RBBH.TestAutomation.Api.Auth;

public sealed class HangfireDashboardAuthFilter : IDashboardAuthorizationFilter
{
    public bool Authorize(DashboardContext context)
    {
        var http = context.GetHttpContext();
        return http.User.IsInRole(AppRoles.Administrator)
            || http.User.IsInRole(AppRoles.QALead);
    }
}
