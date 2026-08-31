using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Domain.Audit;
using RBBH.CollateralAppraisal.Infrastructure.Audit;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure.Audit;

public sealed class AuditServiceTests
{
    private readonly ICurrentUserService  _currentUser;
    private readonly IHttpContextAccessor _httpContextAccessor;
    private readonly IAuditValueSanitizer _sanitizer;
    private readonly IAuditLogQueue       _queue;

    public AuditServiceTests()
    {
        _currentUser         = Substitute.For<ICurrentUserService>();
        _httpContextAccessor = Substitute.For<IHttpContextAccessor>();
        _sanitizer           = Substitute.For<IAuditValueSanitizer>();
        _queue               = Substitute.For<IAuditLogQueue>();

        _currentUser.UserId.Returns("user-1");
        _currentUser.Username.Returns("ivan");
        _currentUser.Email.Returns("ivan@test.ba");
        _currentUser.Role.Returns("AM");
    }

    private AuditService CreateSut(params IAuditSink[] sinks) =>
        new(sinks, _queue, _sanitizer, _currentUser, _httpContextAccessor, Substitute.For<ILogger<AuditService>>());

    private static AuditEvent MakeEvent(
        string? correlationId = null,
        object? oldValues = null,
        object? newValues = null,
        IReadOnlyList<string>? changedFields = null) => new()
    {
        Action        = "ORDER_CREATED",
        OperationType = "Create",
        Module        = "Orders",
        EntityType    = "AppraisalOrder",
        EntityKey     = "123",
        Status        = "Success",
        Severity      = "Info",
        OldValues     = oldValues,
        NewValues     = newValues,
        ChangedFields = changedFields,
        CorrelationId = correlationId,
    };

    // AuditService gradi log sinhrono i stavlja ga u red (IAuditLogQueue); stvarni upis u
    // sinkove se dešava asinhrono u pozadini. Zato hvatamo log iz queue.EnqueueAsync, ne iz sinka.
    private IAuditSink CreateCapturingSink(out Func<AuditLog?> getCaptured)
    {
        AuditLog? captured = null;
        _queue.EnqueueAsync(Arg.Do<AuditLog>(l => captured = l), Arg.Any<CancellationToken>())
            .Returns(ValueTask.CompletedTask);
        getCaptured = () => captured;
        return Substitute.For<IAuditSink>();
    }

    [Fact]
    public async Task RecordAsync_ValidEvent_EnqueuesLog()
    {
        var sut = CreateSut();

        await sut.RecordAsync(MakeEvent());

        await _queue.Received(1).EnqueueAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task RecordAsync_NoCurrentUser_DefaultsActorToSystem()
    {
        _currentUser.UserId.Returns((string?)null);
        _currentUser.Username.Returns((string?)null);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        Assert.Equal("system", getCaptured()!.ActorUserId);
        Assert.Equal("system", getCaptured()!.ActorUsername);
    }

    [Fact]
    public async Task RecordAsync_CurrentUserSet_PopulatesActorFields()
    {
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        var log = getCaptured()!;
        Assert.Equal("user-1", log.ActorUserId);
        Assert.Equal("ivan", log.ActorUsername);
        Assert.Equal("ivan@test.ba", log.ActorEmail);
        Assert.Equal("AM", log.ActorRole);
        Assert.Equal("ORDER_CREATED", log.Action);
        Assert.Equal("AppraisalOrder", log.EntityType);
    }

    [Fact]
    public async Task RecordAsync_QueueEnqueueThrows_FallsBackToSinksAndDoesNotPropagate()
    {
        // Kad enqueue padne, AuditService se vraća na direktan upis kroz sinkove (sigurnosna mreža);
        // greška jednog sinka ne smije spriječiti ostale niti se propagirati pozivaocu.
        _queue.EnqueueAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>())
            .Returns(ValueTask.FromException(new InvalidOperationException("queue down")));
        var sink1 = Substitute.For<IAuditSink>();
        sink1.WriteAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("db down")));
        var sink2 = Substitute.For<IAuditSink>();
        var sut = CreateSut(sink1, sink2);

        await sut.RecordAsync(MakeEvent());

        await sink1.Received(1).WriteAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>());
        await sink2.Received(1).WriteAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task RecordAsync_BuildAuditLogThrows_DoesNotEnqueueOrCallSinkOrThrow()
    {
        _sanitizer.Sanitize(Arg.Any<object?>())
            .Returns(_ => throw new InvalidOperationException("sanitize failed"));
        var sink = Substitute.For<IAuditSink>();
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent(oldValues: new { foo = "bar" }));

        await _queue.DidNotReceive().EnqueueAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>());
        await sink.DidNotReceive().WriteAsync(Arg.Any<AuditLog>(), Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task RecordAsync_EventCorrelationIdSet_UsesEventValue()
    {
        _httpContextAccessor.HttpContext.Returns((HttpContext?)null);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent(correlationId: "evt-corr"));

        Assert.Equal("evt-corr", getCaptured()!.CorrelationId);
    }

    [Fact]
    public async Task RecordAsync_NoHttpContextNoEventCorrelationId_RequestMetadataIsNull()
    {
        _httpContextAccessor.HttpContext.Returns((HttpContext?)null);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        var log = getCaptured()!;
        Assert.Null(log.CorrelationId);
        Assert.Null(log.IpAddress);
        Assert.Null(log.RequestPath);
    }

    [Fact]
    public async Task RecordAsync_HttpContextHasCorrelationIdItem_UsesHttpContextValue()
    {
        var httpContext = new DefaultHttpContext();
        httpContext.Items[HttpHeaders.CorrelationId] = "http-corr";
        _httpContextAccessor.HttpContext.Returns(httpContext);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        Assert.Equal("http-corr", getCaptured()!.CorrelationId);
    }

    [Fact]
    public async Task RecordAsync_HttpContextWithXForwardedFor_UsesFirstForwardedIp()
    {
        var httpContext = new DefaultHttpContext();
        httpContext.Request.Headers["X-Forwarded-For"] = "1.2.3.4, 5.6.7.8";
        _httpContextAccessor.HttpContext.Returns(httpContext);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        Assert.Equal("1.2.3.4", getCaptured()!.IpAddress);
    }

    [Fact]
    public async Task RecordAsync_HttpContextWithoutForwardedHeader_UsesConnectionRemoteIp()
    {
        var httpContext = new DefaultHttpContext();
        httpContext.Connection.RemoteIpAddress = IPAddress.Parse("10.0.0.5");
        _httpContextAccessor.HttpContext.Returns(httpContext);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        Assert.Equal("10.0.0.5", getCaptured()!.IpAddress);
    }

    [Fact]
    public async Task RecordAsync_HttpContextPresent_PopulatesRequestMetadata()
    {
        var httpContext = new DefaultHttpContext();
        httpContext.Request.Path = "/api/orders";
        httpContext.Request.Method = "POST";
        httpContext.Request.Headers["User-Agent"] = "TestAgent/1.0";
        _httpContextAccessor.HttpContext.Returns(httpContext);
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        var log = getCaptured()!;
        Assert.Equal("/api/orders", log.RequestPath);
        Assert.Equal("POST", log.HttpMethod);
        Assert.Equal("TestAgent/1.0", log.UserAgent);
    }

    [Fact]
    public async Task RecordAsync_ChangedFieldsProvided_SerializesToJsonArray()
    {
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent(changedFields: new[] { "Status", "AssignedAgent" }));

        Assert.Equal("[\"Status\",\"AssignedAgent\"]", getCaptured()!.ChangedFieldsJson);
    }

    [Fact]
    public async Task RecordAsync_ChangedFieldsNull_ChangedFieldsJsonIsNull()
    {
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent());

        Assert.Null(getCaptured()!.ChangedFieldsJson);
    }

    [Fact]
    public async Task RecordAsync_OldAndNewValuesProvided_PassesThroughSanitizer()
    {
        _sanitizer.Sanitize(Arg.Any<object?>())
            .Returns(ci => ci.Arg<object?>() is null ? null : "sanitized-json");
        var sink = CreateCapturingSink(out var getCaptured);
        var sut = CreateSut(sink);

        await sut.RecordAsync(MakeEvent(
            oldValues: new { status = "Draft" },
            newValues: new { status = "Submitted" }));

        var log = getCaptured()!;
        Assert.Equal("sanitized-json", log.OldValuesJson);
        Assert.Equal("sanitized-json", log.NewValuesJson);
    }
}
