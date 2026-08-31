using MediatR;
using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Security;
using RBBH.CollateralAppraisal.Application.WorkflowTask.Commands;
using RBBH.CollateralAppraisal.Application.WorkflowTask.Queries;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class WorkflowTaskEndpoints
{
    public static IEndpointRouteBuilder MapWorkflowTaskEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/tasks").WithTags("Tasks");

        group.MapGet("/my", GetMyTasks)
             .RequireAuthorization(AppPolicies.OrdersViewOwn)
             .WithName("GetMyTasks")
             .WithSummary("Taskovi dodijeljeni trenutnom korisniku ili njegovoj roli.");

        group.MapPost("/{id:int}/accept", AcceptTask)
             .RequireAuthorization(AppPolicies.OrdersAccept)
             .WithName("AcceptTask")
             .WithSummary("Prihvatanje taska — zaključava task za tog korisnika.");

        group.MapPost("/{id:int}/complete", CompleteTask)
             .RequireAuthorization(AppPolicies.OrdersAccept)
             .WithName("CompleteTask")
             .WithSummary("Završetak taska.");

        return app;
    }

    private static async Task<IResult> GetMyTasks(
        IMediator mediator,
        int page     = 1,
        int pageSize = 20,
        CancellationToken ct = default)
    {
        var result = await mediator.Send(new GetMyTasksQuery(page, pageSize), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> AcceptTask(
        int id,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new AcceptTaskCommand(id), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> CompleteTask(
        int id,
        [FromBody] CompleteTaskRequest? request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new CompleteTaskCommand(id, request?.Comment), ct);
        return Results.Ok(result);
    }
}

public sealed record CompleteTaskRequest(string? Comment);
