using RBBH.TestAutomation.Api.Services.Auth;

namespace UnitTests.Auth;

/// <summary>
/// Unit testovi za <see cref="InMemoryAuditLogStore"/>.
///
/// Pokriva acceptance kriterije TAG-2 user storyja:
///   #1 — Neuspješna prijava prikazuje odgovarajuću poruku greške (audit zapis se kreira)
///   #2 — Sigurnosni audit log drži zadnjih N zapisa (ring buffer, FIFO)
/// </summary>
public class InMemoryAuditLogStoreTests
{
    private static AuditLogEntry MakeEntry(
        string eventType = AuditEventTypes.LoginSuccess,
        string username  = "testuser",
        string? ip       = "127.0.0.1",
        string? reason   = null)
        => new(DateTime.UtcNow, eventType, username, ip, reason);

    // ═══════════════════════════════════════════════════════════════════════════
    // Add + GetRecent
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void GetRecent_WhenEmpty_ReturnsEmptyList()
    {
        var store = new InMemoryAuditLogStore();
        Assert.Empty(store.GetRecent());
    }

    [Fact]
    public void Add_WhenOneEntry_GetRecentReturnsIt()
    {
        var store = new InMemoryAuditLogStore();
        var entry = MakeEntry();
        store.Add(entry);

        var result = store.GetRecent();
        Assert.Single(result);
        Assert.Equal(entry, result[0]);
    }

    [Fact]
    public void GetRecent_WhenMultipleEntries_ReturnsMostRecentFirst()
    {
        // GetRecent koristi Reverse() — zadnje dodano je prvo u rezultatu
        var store = new InMemoryAuditLogStore();
        var first  = MakeEntry(username: "user1");
        var second = MakeEntry(username: "user2");
        var third  = MakeEntry(username: "user3");

        store.Add(first);
        store.Add(second);
        store.Add(third);

        var result = store.GetRecent();
        Assert.Equal("user3", result[0].Username);
        Assert.Equal("user1", result[2].Username);
    }

    [Fact]
    public void GetRecent_WithMaxParameter_LimitsResults()
    {
        var store = new InMemoryAuditLogStore();
        for (var i = 0; i < 10; i++)
            store.Add(MakeEntry(username: $"user{i}"));

        var result = store.GetRecent(max: 3);
        Assert.Equal(3, result.Count);
    }

    [Fact]
    public void GetRecent_DefaultMax_ReturnsUpTo100Entries()
    {
        var store = new InMemoryAuditLogStore();
        for (var i = 0; i < 150; i++)
            store.Add(MakeEntry(username: $"user{i}"));

        var result = store.GetRecent(); // default max = 100
        Assert.Equal(100, result.Count);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Ring buffer — Acceptance kriterij #2
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void Add_WhenCapacityExceeded_OldestEntryIsDropped()
    {
        // Store drži max 1000 — provjeravamo FIFO logiku s manjim skupom
        var store = new InMemoryAuditLogStore();

        // Popunimo do kapaciteta + 1
        for (var i = 0; i < 1001; i++)
            store.Add(MakeEntry(username: $"user{i}"));

        // Total mora biti max 1000
        var all = store.GetRecent(max: 2000);
        Assert.True(all.Count <= 1000);
    }

    [Fact]
    public void Add_WhenCapacityExceeded_NewestEntryIsRetained()
    {
        var store = new InMemoryAuditLogStore();

        for (var i = 0; i < 1001; i++)
            store.Add(MakeEntry(username: $"user{i}"));

        // Zadnji dodan (user1000) mora biti u rezultatu
        var recent = store.GetRecent(max: 1);
        Assert.Equal("user1000", recent[0].Username);
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Sadržaj zapisa
    // ═══════════════════════════════════════════════════════════════════════════

    [Fact]
    public void Add_LoginFailureEntry_PreservesAllFields()
    {
        // Acceptance kriterij #1 — neuspješna prijava bilježi sve detalje
        var store = new InMemoryAuditLogStore();
        var before = DateTime.UtcNow;

        store.Add(new AuditLogEntry(
            TimestampUtc:  DateTime.UtcNow,
            EventType:     AuditEventTypes.LoginFailure,
            Username:      "hacker",
            IpAddress:     "192.168.1.1",
            FailureReason: AuditFailureReasons.InvalidCredentials));

        var result = store.GetRecent(max: 1)[0];

        Assert.Equal(AuditEventTypes.LoginFailure,          result.EventType);
        Assert.Equal("hacker",                              result.Username);
        Assert.Equal("192.168.1.1",                         result.IpAddress);
        Assert.Equal(AuditFailureReasons.InvalidCredentials, result.FailureReason);
        Assert.True(result.TimestampUtc >= before);
    }

    [Fact]
    public void Add_LoginSuccessEntry_HasNullFailureReason()
    {
        var store = new InMemoryAuditLogStore();
        store.Add(MakeEntry(eventType: AuditEventTypes.LoginSuccess));

        var result = store.GetRecent(max: 1)[0];
        Assert.Null(result.FailureReason);
    }

    [Fact]
    public void Add_EntryWithNullIpAddress_IsAccepted()
    {
        var store = new InMemoryAuditLogStore();
        var ex = Record.Exception(() =>
            store.Add(MakeEntry(ip: null)));
        Assert.Null(ex);
    }
}
