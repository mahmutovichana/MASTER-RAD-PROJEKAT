using MediatR;
using Microsoft.AspNetCore.Mvc;
using RBBH.CollateralAppraisal.Application.Orders.Requests;
using RBBH.CollateralAppraisal.Application.Orders.Commands;
using RBBH.CollateralAppraisal.Application.Orders.Queries;
using RBBH.CollateralAppraisal.Application.Security;

namespace RBBH.CollateralAppraisal.Api.Endpoints;

public static class OrderEndpoints
{
    public static IEndpointRouteBuilder MapOrderEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders").WithTags("Orders");

        group.MapPost("/", Create)
             .RequireAuthorization(AppPolicies.OrdersCreate)
             .WithName("CreateOrder")
             .WithSummary("Inicira novu narudžbu procjene (Draft).");

        group.MapPost("/draft", CreateDraft)
             .RequireAuthorization(AppPolicies.OrdersCreate)
             .WithName("CreateOrderDraft")
             .WithSummary("Kreira prazan nacrt narudžbe za autosave.");

        group.MapGet("/", GetList)
             .RequireAuthorization(AppPolicies.OrdersViewOwn)
             .WithName("GetOrderList")
             .WithSummary("Lista narudžbi — prodaja vidi vlastite, CA/Admin vide sve.");

        group.MapGet("/summary", GetSummary)
             .RequireAuthorization(AppPolicies.OrdersViewOwn)
             .WithName("GetOrderSummary")
             .WithSummary("Sažetak broja narudžbi po statusu za KPI kartice.");

        group.MapGet("/{id:int}", GetById)
             .RequireAuthorization(AppPolicies.OrdersViewOwn)
             .WithName("GetOrderById")
             .WithSummary("Detalji narudžbe.");

        group.MapPut("/{id:int}", UpdateDraft)
             .RequireAuthorization(AppPolicies.OrdersUpdateDraft)
             .WithName("UpdateOrderDraft")
             .WithSummary("Ažurira narudžbu u statusu Draft.");

        group.MapPost("/{id:int}/submit", Submit)
             .RequireAuthorization(AppPolicies.OrdersSubmit)
             .WithName("SubmitOrder")
             .WithSummary("Podnosi narudžbu CA-u. Transakcijski: protokol + task + notifikacija.");

        group.MapDelete("/{id:int}", Cancel)
             .RequireAuthorization(AppPolicies.OrdersCancel)
             .WithName("CancelOrder")
             .WithSummary("Otkazuje narudžbu u statusu Draft (soft delete).");

        group.MapGet("/{id:int}/appraisal-status", GetAppraisalStatus)
             .RequireAuthorization(AppPolicies.OrdersViewOwn)
             .WithName("GetAppraisalStatus")
             .WithSummary("DIO_1 — 'U kojem je statusu izrada procjene': vraća status i ključne datume vještaka.");

        return app;
    }

    private static async Task<IResult> Create(
        [FromBody] CreateOrderRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new CreateOrderCommand(request), ct);
        return Results.Created($"/api/orders/{result.Id}", result);
    }

    private static async Task<IResult> CreateDraft(
        [FromQuery] string? tip,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new CreateDraftOrderCommand(tip), ct);
        return Results.Created($"/api/orders/{result.Id}", result);
    }

    private static async Task<IResult> GetList(
        [AsParameters] OrderListRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetOrdersListQuery(request), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetSummary(
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetOrderSummaryQuery(), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetById(
        int id,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new GetOrderByIdQuery(id), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> UpdateDraft(
        int id,
        [FromBody] UpdateOrderRequest request,
        IMediator mediator,
        CancellationToken ct,
        [FromQuery] bool autosave = false)
    {
        var result = await mediator.Send(new UpdateDraftOrderCommand(id, request, autosave), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Submit(
        int id,
        IMediator mediator,
        CancellationToken ct)
    {
        var result = await mediator.Send(new SubmitOrderCommand(id), ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> Cancel(
        int id,
        IMediator mediator,
        CancellationToken ct)
    {
        await mediator.Send(new CancelOrderCommand(id), ct);
        return Results.NoContent();
    }

    private static async Task<IResult> GetAppraisalStatus(
        int id,
        IMediator mediator,
        CancellationToken ct)
    {
        var order = await mediator.Send(new GetOrderByIdQuery(id), ct);
        return Results.Ok(new
        {
            order.Id,
            order.OrderNumber,
            order.Status,
            order.Title,
            order.CreatedAt,
            order.SubmittedAt,
            DaysElapsed = order.SubmittedAt.HasValue
                ? (int)(DateTime.UtcNow - order.SubmittedAt.Value).TotalDays
                : (int?)null
        });
    }
}
