using RBBH.CollateralAppraisal.Api.Modules;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Application.Notifications;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

/// <summary>
/// Inbox in-app notifikacija prijavljenog korisnika.
/// Proof-of-concept za <see cref="IEndpointModule"/> auto-discovery —
/// vidi docs/backend/feature-module-pattern.md.
/// </summary>
public sealed class NotificationsEndpointModule : IEndpointModule
{
    public void MapEndpoints(IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/notifications").WithTags("Notifications");

        group.MapGet("/mine", GetMine)
             .RequireAuthorization(AppPolicies.NotificationsView)
             .WithName("GetMyNotifications")
             .WithSummary("Paginirani inbox in-app notifikacija prijavljenog korisnika.");

        group.MapGet("/unread-count", GetUnreadCount)
             .RequireAuthorization(AppPolicies.NotificationsView)
             .WithName("GetUnreadNotificationCount")
             .WithSummary("Broj nepročitanih notifikacija — za bell ikonu.");

        group.MapPost("/{id:int}/read", MarkRead)
             .RequireAuthorization(AppPolicies.NotificationsView)
             .WithName("MarkNotificationRead")
             .WithSummary("Označava notifikaciju kao pročitanu.");
    }

    private static async Task<IResult> GetMine(
        ICurrentUserService  currentUser,
        INotificationService notifications,
        CancellationToken    ct,
        int  page       = 1,
        int  pageSize   = 20,
        bool unreadOnly = false)
    {
        if (currentUser.UserId is null)
            return Results.Unauthorized();

        var result = await notifications.GetInboxAsync(currentUser.UserId, page, pageSize, unreadOnly, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetUnreadCount(
        ICurrentUserService  currentUser,
        INotificationService notifications,
        CancellationToken    ct)
    {
        if (currentUser.UserId is null)
            return Results.Unauthorized();

        var count = await notifications.GetUnreadCountAsync(currentUser.UserId, ct);
        return Results.Ok(new { count });
    }

    private static async Task<IResult> MarkRead(
        int id,
        ICurrentUserService  currentUser,
        INotificationService notifications,
        CancellationToken    ct)
    {
        if (currentUser.UserId is null)
            return Results.Unauthorized();

        var found = await notifications.MarkReadAsync(id, currentUser.UserId, ct);
        return found ? Results.NoContent() : Results.NotFound();
    }
}
