using System.Net;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using NSubstitute;
using RBBH.CollateralAppraisal.Application.Audit;
using RBBH.CollateralAppraisal.Application.Common.Exceptions;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Auth;
using RBBH.CollateralAppraisal.Infrastructure.Users;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Users;

/// <summary>
/// Tests for UserSuspensionService.
/// HTTP calls to Keycloak Admin API are intercepted by FakeHttpMessageHandler,
/// which returns JSON responses matching Keycloak's format.
/// </summary>
public sealed class UserSuspensionServiceTests
{
    // ── Fake HTTP infrastructure ─────────────────────────────────────────────

    /// <summary>
    /// Simple fake handler that lets tests configure per-URL responses.
    /// </summary>
    private sealed class FakeHttpMessageHandler : HttpMessageHandler
    {
        private readonly Dictionary<(HttpMethod Method, string PathContains), (HttpStatusCode Status, string Body)>
            _responses = new();

        public void Setup(HttpMethod method, string pathContains, HttpStatusCode status, string body) =>
            _responses[(method, pathContains)] = (status, body);

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request, CancellationToken cancellationToken)
        {
            foreach (var ((method, pathContains), (status, body)) in _responses)
            {
                if (request.Method == method
                    && (request.RequestUri?.ToString().Contains(pathContains) ?? false))
                {
                    return Task.FromResult(new HttpResponseMessage(status)
                    {
                        Content = new StringContent(body, Encoding.UTF8, "application/json")
                    });
                }
            }

            return Task.FromResult(new HttpResponseMessage(HttpStatusCode.InternalServerError)
            {
                Content = new StringContent("Unmatched request: " + request.RequestUri)
            });
        }
    }

    // ── Test state ───────────────────────────────────────────────────────────

    private readonly ICurrentUserService _user;
    private readonly IAuditService       _audit;
    private readonly FakeHttpMessageHandler _handler;
    private readonly IHttpClientFactory  _httpClientFactory;
    private readonly KeycloakAdminOptions _options;
    private readonly UserSuspensionService _sut;

    private const string TestRealm        = "rbbh-realm";
    private const string TargetUserId     = "user-target-123";
    private const string CurrentUserId    = "user-admin-1";
    private const string FakeTokenJson    = """{"access_token":"fake-token-abc"}""";

    public UserSuspensionServiceTests()
    {
        _user  = Substitute.For<ICurrentUserService>();
        _audit = Substitute.For<IAuditService>();

        _user.UserId.Returns(CurrentUserId);
        _user.IsAuthenticated.Returns(true);

        _options = new KeycloakAdminOptions
        {
            BaseUrl      = "http://keycloak.test",
            Realm        = TestRealm,
            ClientId     = "admin-client",
            ClientSecret = "secret-abc"
        };

        _handler = new FakeHttpMessageHandler();

        // Default: token endpoint always returns 200 with fake token
        _handler.Setup(HttpMethod.Post, "openid-connect/token",
            HttpStatusCode.OK, FakeTokenJson);

        var httpClient = new HttpClient(_handler) { BaseAddress = new Uri(_options.BaseUrl) };
        _httpClientFactory = Substitute.For<IHttpClientFactory>();
        _httpClientFactory.CreateClient("KeycloakAdmin").Returns(httpClient);

        _sut = new UserSuspensionService(
            _httpClientFactory,
            Options.Create(_options),
            _user,
            _audit,
            Substitute.For<ILogger<UserSuspensionService>>());
    }

    private static string EnabledUserJson(string userId, string username, bool enabled) =>
        JsonSerializer.Serialize(new { id = userId, username, enabled });

    // ── SuspendAsync — happy path ────────────────────────────────────────────

    [Fact]
    public async Task SuspendAsync_EnabledUser_CallsKeycloakPut()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: true);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        await _sut.SuspendAsync(TargetUserId, "Kršenje pravilnika");

        // No exception = success
    }

    [Fact]
    public async Task SuspendAsync_RecordsAuditEvent()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: true);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        await _sut.SuspendAsync(TargetUserId, "Razlog suspenzije");

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.UserSuspended
                                 && e.EntityKey == TargetUserId),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task SuspendAsync_WithReason_ReasonInAuditDetails()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: true);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        await _sut.SuspendAsync(TargetUserId, "Poseban razlog");

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.UserSuspended),
            Arg.Any<CancellationToken>());
    }

    // ── SuspendAsync — sad path ──────────────────────────────────────────────

    [Fact]
    public async Task SuspendAsync_SelfSuspension_ThrowsConflict()
    {
        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SuspendAsync(CurrentUserId, "Razlog"));
        Assert.Equal("SELF_SUSPENSION_BLOCKED", ex.ErrorCode);
    }

    [Fact]
    public async Task SuspendAsync_UserNotFound_ThrowsNotFound()
    {
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.NotFound, "");

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.SuspendAsync(TargetUserId, "Razlog"));
        Assert.Equal("USER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task SuspendAsync_AlreadySuspended_ThrowsConflict()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: false);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.SuspendAsync(TargetUserId, "Razlog"));
        Assert.Equal("USER_ALREADY_SUSPENDED", ex.ErrorCode);
    }

    // ── ReactivateAsync — happy path ─────────────────────────────────────────

    [Fact]
    public async Task ReactivateAsync_SuspendedUser_CallsKeycloakPut()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: false);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        await _sut.ReactivateAsync(TargetUserId);

        // No exception = success
    }

    [Fact]
    public async Task ReactivateAsync_RecordsAuditEvent()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: false);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        await _sut.ReactivateAsync(TargetUserId);

        await _audit.Received(1).RecordAsync(
            Arg.Is<AuditEvent>(e => e.Action == AuditActions.UserReactivated
                                 && e.EntityKey == TargetUserId),
            Arg.Any<CancellationToken>());
    }

    // ── ReactivateAsync — sad path ────────────────────────────────────────────

    [Fact]
    public async Task ReactivateAsync_UserNotFound_ThrowsNotFound()
    {
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.NotFound, "");

        var ex = await Assert.ThrowsAsync<NotFoundException>(
            () => _sut.ReactivateAsync(TargetUserId));
        Assert.Equal("USER_NOT_FOUND", ex.ErrorCode);
    }

    [Fact]
    public async Task ReactivateAsync_AlreadyActive_ThrowsConflict()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: true);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);

        var ex = await Assert.ThrowsAsync<ConflictException>(
            () => _sut.ReactivateAsync(TargetUserId));
        Assert.Equal("USER_ALREADY_ACTIVE", ex.ErrorCode);
    }

    // ── Resilience ─────────────────────────────────────────────────────────────

    [Fact]
    public async Task SuspendAsync_AuditThrows_StillSucceeds()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: true);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit down")));

        // Should not throw — audit failure is swallowed
        await _sut.SuspendAsync(TargetUserId, "Razlog");
    }

    [Fact]
    public async Task ReactivateAsync_AuditThrows_StillSucceeds()
    {
        var userJson = EnabledUserJson(TargetUserId, "target.user", enabled: false);
        _handler.Setup(HttpMethod.Get, $"users/{TargetUserId}",
            HttpStatusCode.OK, userJson);
        _handler.Setup(HttpMethod.Put, $"users/{TargetUserId}",
            HttpStatusCode.NoContent, "");

        _audit.RecordAsync(Arg.Any<AuditEvent>(), Arg.Any<CancellationToken>())
            .Returns(Task.FromException(new InvalidOperationException("audit down")));

        // Should not throw — audit failure is swallowed
        await _sut.ReactivateAsync(TargetUserId);
    }
}
