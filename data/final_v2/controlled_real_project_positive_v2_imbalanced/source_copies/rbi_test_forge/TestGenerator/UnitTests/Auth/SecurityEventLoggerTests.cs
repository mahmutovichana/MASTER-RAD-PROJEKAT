using RBBH.TestAutomation.Api.Services.Auth;
using Microsoft.Extensions.Logging;
using NSubstitute;

namespace UnitTests.Auth;

/// <summary>
/// Unit testovi za <see cref="SecurityEventLogger"/>.
///
/// SecurityEventLogger je dual-write: IAuditLogStore (in-memory) + ILogger (Serilog).
/// Testujemo samo store interakciju — logger je mock koji ne verifikujemo.
///
/// Pokriva TAG-2 acceptance kriterije:
///   #1 — Uspješna autentikacija / neuspješna prijava bilježe se u audit
///   #2 — Odjava se bilježi
/// </summary>
public class SecurityEventLoggerTests
{
    private static (SecurityEventLogger logger, InMemoryAuditLogStore store) CreateSut()
    {
        var store       = new InMemoryAuditLogStore();
        var mockLogger  = Substitute.For<ILogger<SecurityEventLogger>>();
        var sut         = new SecurityEventLogger(store, mockLogger);
        return (sut, store);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // LogLoginSuccess
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void LogLoginSuccess_AddsEntryToStore()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginSuccess("admin", "127.0.0.1");

        Assert.Single(store.GetRecent());
    }

    [Fact]
    public void LogLoginSuccess_EntryHasCorrectEventType()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginSuccess("admin", "127.0.0.1");

        var entry = store.GetRecent()[0];
        Assert.Equal(AuditEventTypes.LoginSuccess, entry.EventType);
    }

    [Fact]
    public void LogLoginSuccess_EntryHasCorrectUsername()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginSuccess("testkorisnik", "10.0.0.1");

        var entry = store.GetRecent()[0];
        Assert.Equal("testkorisnik", entry.Username);
    }

    [Fact]
    public void LogLoginSuccess_EntryHasNullFailureReason()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginSuccess("admin", null);

        var entry = store.GetRecent()[0];
        Assert.Null(entry.FailureReason);
    }

    [Fact]
    public void LogLoginSuccess_WhenIpIsNull_EntryStillCreated()
    {
        var (logger, store) = CreateSut();
        var ex = Record.Exception(() => logger.LogLoginSuccess("admin", null));
        Assert.Null(ex);
        Assert.Single(store.GetRecent());
    }

    [Fact]
    public void LogLoginSuccess_TimestampIsRecent()
    {
        var (logger, store) = CreateSut();
        var before = DateTime.UtcNow;
        logger.LogLoginSuccess("admin", "127.0.0.1");

        var entry = store.GetRecent()[0];
        Assert.True(entry.TimestampUtc >= before);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // LogLoginFailure — Acceptance kriterij #1
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void LogLoginFailure_AddsEntryToStore()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginFailure("hacker", "192.168.1.1", AuditFailureReasons.InvalidCredentials);

        Assert.Single(store.GetRecent());
    }

    [Fact]
    public void LogLoginFailure_EntryHasLoginFailureEventType()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginFailure("hacker", "192.168.1.1", AuditFailureReasons.InvalidCredentials);

        var entry = store.GetRecent()[0];
        Assert.Equal(AuditEventTypes.LoginFailure, entry.EventType);
    }

    [Fact]
    public void LogLoginFailure_EntryPreservesFailureReason()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginFailure("user", "1.2.3.4", AuditFailureReasons.Locked);

        var entry = store.GetRecent()[0];
        Assert.Equal(AuditFailureReasons.Locked, entry.FailureReason);
    }

    [Fact]
    public void LogLoginFailure_EntryPreservesIpAddress()
    {
        var (logger, store) = CreateSut();
        logger.LogLoginFailure("user", "10.20.30.40", AuditFailureReasons.InvalidCredentials);

        var entry = store.GetRecent()[0];
        Assert.Equal("10.20.30.40", entry.IpAddress);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // LogLogout — Acceptance kriterij #2
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void LogLogout_AddsEntryToStore()
    {
        var (logger, store) = CreateSut();
        logger.LogLogout("admin", "127.0.0.1");

        Assert.Single(store.GetRecent());
    }

    [Fact]
    public void LogLogout_EntryHasLogoutEventType()
    {
        var (logger, store) = CreateSut();
        logger.LogLogout("admin", "127.0.0.1");

        var entry = store.GetRecent()[0];
        Assert.Equal(AuditEventTypes.Logout, entry.EventType);
    }

    [Fact]
    public void LogLogout_EntryHasNullFailureReason()
    {
        var (logger, store) = CreateSut();
        logger.LogLogout("admin", "127.0.0.1");

        var entry = store.GetRecent()[0];
        Assert.Null(entry.FailureReason);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Sekvencijalni scenarij — login/fail/logout
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void MultipleEvents_AllStoredInOrder()
    {
        var (logger, store) = CreateSut();

        logger.LogLoginFailure("user", "1.1.1.1", AuditFailureReasons.InvalidCredentials);
        logger.LogLoginSuccess("user", "1.1.1.1");
        logger.LogLogout("user", "1.1.1.1");

        var entries = store.GetRecent(); // najnoviji prvi
        Assert.Equal(3, entries.Count);
        Assert.Equal(AuditEventTypes.Logout,        entries[0].EventType);
        Assert.Equal(AuditEventTypes.LoginSuccess,  entries[1].EventType);
        Assert.Equal(AuditEventTypes.LoginFailure,  entries[2].EventType);
    }

    [Fact]
    public void MultipleFailedAttempts_AllRecorded()
    {
        var (logger, store) = CreateSut();

        for (var i = 0; i < 5; i++)
            logger.LogLoginFailure($"user{i}", "1.2.3.4", AuditFailureReasons.InvalidCredentials);

        Assert.Equal(5, store.GetRecent().Count);
        Assert.All(store.GetRecent(), e =>
            Assert.Equal(AuditEventTypes.LoginFailure, e.EventType));
    }
}
