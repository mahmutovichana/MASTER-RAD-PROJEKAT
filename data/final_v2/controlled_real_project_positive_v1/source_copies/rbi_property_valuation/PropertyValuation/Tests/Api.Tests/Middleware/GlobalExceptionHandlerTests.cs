using FluentAssertions;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Api.Middleware;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Models;
using RBBH.CollateralAppraisal.Application.Common.Validation;
using RBBH.CollateralAppraisal.Domain.Orders;
using System.Text.Json;
using Xunit;

namespace RBBH.CollateralAppraisal.Api.Tests.Middleware;

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — GlobalExceptionHandler
//
// Exception type                 | HTTP | title             | Audit | Type
// ─────────────────────────────────────────────────────────────────────────────
// NotFoundException              | 404  | "Not Found"       | Ne    | Happy path
// ConflictException              | 409  | "Conflict"        | Ne    | Happy path
// InvalidStateTransitionException| 409  | "Invalid State"   | Ne    | State
// ForbiddenException             | 403  | "Forbidden"       | Da    | Security + audit
// ValidationException FieldErrors| 400  | "Validation.."    | Ne    | Validation
// ValidationException Errors dict| 400  | "Validation.."    | Ne    | Validation (legacy)
// BadHttpRequestException        | 400  | "Bad Request"     | Ne    | Protocol
// Unknown Exception              | 500  | "Internal.."      | Ne    | Error
// OperationCanceledException     | -    | (swallowed)       | Ne    | Edge case
// errorCode propagation          | any  | extensions set    | Ne    | Observability
// correlationId propagation      | any  | extensions set    | Ne    | Observability
// Audit failure → response ok    | 403  | still sent        | Fail  | Resilience
// ═══════════════════════════════════════════════════════════════

public sealed class GlobalExceptionHandlerTests
{
    private readonly ILogger<GlobalExceptionHandler> _logger
        = Substitute.For<ILogger<GlobalExceptionHandler>>();
    private readonly IAuditService _audit
        = Substitute.For<IAuditService>();

    private GlobalExceptionHandler BuildSut()
    {
        var services = new ServiceCollection();
        services.AddSingleton(_audit);
        var sp     = services.BuildServiceProvider();
        var factory = new DefaultServiceScopeFactory(sp);
        return new GlobalExceptionHandler(_logger, factory);
    }

    private static DefaultHttpContext BuildHttpContext(string correlationId = "test-corr-id")
    {
        var ctx = new DefaultHttpContext
        {
            Response = { Body = new System.IO.MemoryStream() }
        };
        ctx.Items[HttpHeaders.CorrelationId] = correlationId;
        ctx.Request.Path = "/api/test";
        return ctx;
    }

    private static async Task<ProblemDetails?> ReadResponseAsync(HttpContext ctx)
    {
        ctx.Response.Body.Seek(0, System.IO.SeekOrigin.Begin);
        return await JsonSerializer.DeserializeAsync<ProblemDetails>(
            ctx.Response.Body,
            new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
    }

    // ── Status code mapping ───────────────────────────────────────────────────

    [Fact]
    public async Task Handle_NotFoundException_ShouldReturn404()
    {
        var ctx = BuildHttpContext();
        var ex  = new NotFoundException("Narudžba nije pronađena.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(404);
        var pd = await ReadResponseAsync(ctx);
        pd!.Title.Should().Be("Not Found");
        pd.Detail.Should().Be("Narudžba nije pronađena.");
    }

    [Fact]
    public async Task Handle_ConflictException_ShouldReturn409()
    {
        var ctx = BuildHttpContext();
        var ex  = new ConflictException("Vještak je već odabran.", "APPRAISER_ALREADY_SELECTED");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(409);
        var pd = await ReadResponseAsync(ctx);
        pd!.Title.Should().Be("Conflict");
    }

    [Fact]
    public async Task Handle_InvalidStateTransitionException_ShouldReturn409()
    {
        var ctx = BuildHttpContext();
        var ex  = new InvalidStateTransitionException(
            AppraisalOrderStatus.Draft,
            AppraisalOrderStatus.Completed);

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(409);
        var pd = await ReadResponseAsync(ctx);
        pd!.Title.Should().Be("Invalid State");
    }

    [Fact]
    public async Task Handle_ForbiddenException_ShouldReturn403()
    {
        var ctx = BuildHttpContext();
        var ex  = new ForbiddenException("Nemate ovlaštenja.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(403);
        var pd = await ReadResponseAsync(ctx);
        pd!.Title.Should().Be("Forbidden");
    }

    [Fact]
    public async Task Handle_ValidationExceptionWithFieldErrors_ShouldReturn400WithFieldErrors()
    {
        var ctx = BuildHttpContext();
        var errors = new List<ValidationFieldError>
        {
            new("clientName", ValidationErrorCodes.RequiredField, "Ime je obavezno."),
            new("city",       ValidationErrorCodes.RequiredField, "Grad je obavezan.")
        };
        var ex = new ValidationException(errors);

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(400);
        var pd = await ReadResponseAsync(ctx);
        pd!.Title.Should().Be("Validation Error");
        pd.Extensions.Should().ContainKey("fieldErrors");
    }

    [Fact]
    public async Task Handle_ValidationExceptionWithLegacyErrors_ShouldReturn400WithErrors()
    {
        var ctx = BuildHttpContext();
        var ex  = new ValidationException(new Dictionary<string, string[]>
        {
            { "clientName", new[] { "Ime je obavezno." } }
        });

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(400);
        var pd = await ReadResponseAsync(ctx);
        pd!.Extensions.Should().ContainKey("errors");
    }

    [Fact]
    public async Task Handle_BadHttpRequestException_ShouldReturnBadRequestStatusCode()
    {
        var ctx = BuildHttpContext();
        var ex  = new BadHttpRequestException("Neispravan JSON.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(400);
    }

    [Fact]
    public async Task Handle_UnhandledException_ShouldReturn500()
    {
        var ctx = BuildHttpContext();
        var ex  = new InvalidOperationException("Neočekivano.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(500);
        var pd = await ReadResponseAsync(ctx);
        pd!.Title.Should().Be("Internal Server Error");
    }

    // ── OperationCanceledException — edge case ────────────────────────────────

    [Fact]
    public async Task Handle_OperationCanceledWithAbortedRequest_ShouldSwallowAndReturnTrue()
    {
        var cts = new CancellationTokenSource();
        cts.Cancel();
        var ctx = BuildHttpContext();
        // Simuliramo prekinuti zahtjev
        ctx.RequestAborted = cts.Token;
        var ex = new OperationCanceledException(cts.Token);

        var handled = await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        handled.Should().BeTrue("OperationCanceledException od prekinutog zahtjeva se guta");
        ctx.Response.StatusCode.Should().Be(200, "nije upisivan response kod za canceliran zahtjev");
    }

    // ── errorCode u extensions ────────────────────────────────────────────────

    [Fact]
    public async Task Handle_ConflictExceptionWithErrorCode_ShouldIncludeErrorCodeInExtensions()
    {
        var ctx = BuildHttpContext();
        var ex  = new ConflictException("Pogrešan status.", "ORDER_NOT_WITH_APPRAISER");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        var pd = await ReadResponseAsync(ctx);
        pd!.Extensions.Should().ContainKey("errorCode");
        pd.Extensions["errorCode"]!.ToString().Should().Contain("ORDER_NOT_WITH_APPRAISER");
    }

    [Fact]
    public async Task Handle_ExceptionWithoutErrorCode_ShouldNotIncludeErrorCodeInExtensions()
    {
        // NotFoundException bez koda → bez errorCode u extensionima
        var ctx = BuildHttpContext();
        var ex  = new NotFoundException("Nešto nije pronađeno.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        var pd = await ReadResponseAsync(ctx);
        pd!.Extensions.Should().NotContainKey("errorCode");
    }

    // ── correlationId propagacija ─────────────────────────────────────────────

    [Fact]
    public async Task Handle_AnyException_ShouldIncludeCorrelationIdInExtensions()
    {
        var ctx = BuildHttpContext("my-corr-123");
        var ex  = new NotFoundException("Test.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        var pd = await ReadResponseAsync(ctx);
        pd!.Extensions.Should().ContainKey("correlationId");
        pd.Extensions["correlationId"]!.ToString().Should().Contain("my-corr-123");
    }

    // ── audit side-effect za 403 ─────────────────────────────────────────────

    [Fact]
    public async Task Handle_ForbiddenException_ShouldCallAuditServiceOnce()
    {
        var ctx = BuildHttpContext();
        var ex  = new ForbiddenException("Zabranjen pristup.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e =>
                e.Status   == AuditStatuses.Forbidden &&
                e.Severity == AuditSeverity.Security &&
                e.Reason   == "Zabranjen pristup."),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task Handle_NotFoundException_ShouldNotCallAudit()
    {
        // Audit se zove SAMO za 403, ne za ostale exception tipove
        var ctx = BuildHttpContext();
        var ex  = new NotFoundException("Nije pronađeno.");

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        await _audit.DidNotReceive().RecordAsync(
            Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>());
    }

    // ── Resilience: audit neuspjeh ne blokira response ────────────────────────

    [Fact]
    public async Task Handle_WhenAuditServiceFails_ShouldStillReturn403()
    {
        _audit.When(x => x.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>()))
              .Do(_ => throw new InvalidOperationException("Audit DB nedostupan"));

        var ctx = BuildHttpContext();
        var ex  = new ForbiddenException("Zabranjen.");

        // Ne smije propagirati iznimku iz audit servisa
        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        ctx.Response.StatusCode.Should().Be(403,
            "audit neuspjeh ne smije blokirati HTTP odgovor korisniku");
    }

    // ── Return value ──────────────────────────────────────────────────────────

    [Theory]
    [InlineData(typeof(NotFoundException))]
    [InlineData(typeof(ConflictException))]
    [InlineData(typeof(ForbiddenException))]
    [InlineData(typeof(InvalidOperationException))]
    public async Task Handle_AnyHandledException_ShouldReturnTrue(Type exceptionType)
    {
        var ctx = BuildHttpContext();
        var ex  = exceptionType == typeof(NotFoundException)
            ? (Exception)new NotFoundException("x")
            : exceptionType == typeof(ConflictException)
            ? new ConflictException("x", "C")
            : exceptionType == typeof(ForbiddenException)
            ? new ForbiddenException("x")
            : new InvalidOperationException("x");

        var result = await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        result.Should().BeTrue("handler uvijek preuzima iznimku i vraća true");
    }

    // ── RFC 7231 type URIs ────────────────────────────────────────────────────

    [Theory]
    [InlineData(404, "https://tools.ietf.org/html/rfc7231#section-6.5.4")]
    [InlineData(409, "https://tools.ietf.org/html/rfc7231#section-6.5.8")]
    [InlineData(403, "https://tools.ietf.org/html/rfc7231#section-6.5.3")]
    public async Task Handle_Exception_ShouldIncludeCorrectRFC7231TypeUri(int statusCode, string expectedUri)
    {
        var ctx = BuildHttpContext();
        Exception ex = statusCode switch
        {
            404 => new NotFoundException("x"),
            409 => new ConflictException("x", "C"),
            403 => new ForbiddenException("x"),
            _   => new Exception("x")
        };

        await BuildSut().TryHandleAsync(ctx, ex, CancellationToken.None);

        var pd = await ReadResponseAsync(ctx);
        pd!.Type.Should().Be(expectedUri, $"RFC 7231 URI za {statusCode} mora biti ispravan");
    }
}

/// <summary>Minimal implementation of IServiceScopeFactory for tests.</summary>
file sealed class DefaultServiceScopeFactory : IServiceScopeFactory
{
    private readonly IServiceProvider _sp;
    public DefaultServiceScopeFactory(IServiceProvider sp) => _sp = sp;
    public IServiceScope CreateScope() => new DefaultServiceScope(_sp);
}

file sealed class DefaultServiceScope : IServiceScope
{
    public IServiceProvider ServiceProvider { get; }
    public DefaultServiceScope(IServiceProvider sp) => ServiceProvider = sp;
    public void Dispose() { }
}
