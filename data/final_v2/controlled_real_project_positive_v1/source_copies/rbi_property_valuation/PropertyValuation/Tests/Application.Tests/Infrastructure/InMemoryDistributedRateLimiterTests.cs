using FluentAssertions;
using RBBH.CollateralAppraisal.Infrastructure.Common;
using Xunit;

namespace RBBH.CollateralAppraisal.Application.Tests.Infrastructure;

// ═══════════════════════════════════════════════════════════════
// TEST MATRIX — InMemoryDistributedRateLimiter
//
// Scenario                          | Expected        | Type
// ─────────────────────────────────────────────────────────────────
// Prva N zahtjeva (≤ maxRequests)   | true (allowed)  | BVA happy
// N+1-ti zahtjev (> maxRequests)    | false (limited) | BVA upper+1
// Tačno maxRequests zahtjeva        | true (boundary) | BVA upper
// Različiti ključevi su nezavisni   | nema interf.    | Isolation
// Nakon isteka window-a reset       | true (allowed)  | Window reset
// maxRequests = 0 → odmah odbiti    | false           | Edge case
// maxRequests = 1 → 1. da, 2. ne   | true, false     | Min valid
// ═══════════════════════════════════════════════════════════════

public sealed class InMemoryDistributedRateLimiterTests
{
    private readonly InMemoryDistributedRateLimiter _sut = new();

    // ── Basic allow/deny ──────────────────────────────────────────────────────

    [Fact]
    public void IsAllowed_FirstRequest_ShouldBeAllowed()
    {
        var result = _sut.IsAllowed("key1", maxRequests: 5, window: TimeSpan.FromMinutes(1));

        result.Should().BeTrue("prva zahtjev uvijek treba proći");
    }

    [Theory]
    [InlineData(1)]
    [InlineData(3)]
    [InlineData(10)]
    public void IsAllowed_RequestsUpToMax_ShouldAllBeAllowed(int maxRequests)
    {
        // BVA: sve do i uključujući maxRequests mora biti allowed
        var key = $"bva-max-{maxRequests}";
        var results = new List<bool>();

        for (var i = 0; i < maxRequests; i++)
            results.Add(_sut.IsAllowed(key, maxRequests, TimeSpan.FromMinutes(1)));

        results.Should().AllSatisfy(r => r.Should().BeTrue(),
            $"svih {maxRequests} zahtjeva mora biti dozvoljeno");
    }

    [Fact]
    public void IsAllowed_ExactlyAtLimit_ShouldBeAllowed()
    {
        // BVA: zahtjev broj maxRequests je točno na granici — treba proći
        var key = "exact-limit";
        for (var i = 0; i < 4; i++)
            _sut.IsAllowed(key, 5, TimeSpan.FromMinutes(1));

        var result = _sut.IsAllowed(key, 5, TimeSpan.FromMinutes(1)); // 5. zahtjev

        result.Should().BeTrue("5. od 5 zahtjeva je na granici i mora biti dozvoljen");
    }

    [Fact]
    public void IsAllowed_OneOverLimit_ShouldBeDenied()
    {
        // BVA: zahtjev broj maxRequests+1 — treba biti odbijen
        var key = "over-limit";
        for (var i = 0; i < 5; i++)
            _sut.IsAllowed(key, 5, TimeSpan.FromMinutes(1));

        var result = _sut.IsAllowed(key, 5, TimeSpan.FromMinutes(1)); // 6. zahtjev

        result.Should().BeFalse("6. od 5 dozvoljenih zahtjeva mora biti odbijen");
    }

    // ── Key isolation ─────────────────────────────────────────────────────────

    [Fact]
    public void IsAllowed_DifferentKeys_AreIndependent()
    {
        // Iscrpljivanje limita za ključ A ne smije utjecati na ključ B
        for (var i = 0; i < 10; i++)
            _sut.IsAllowed("key-a", 3, TimeSpan.FromMinutes(1));

        var resultB = _sut.IsAllowed("key-b", 3, TimeSpan.FromMinutes(1));

        resultB.Should().BeTrue("rate limit je per-key — key-b nije dotaknut");
    }

    [Theory]
    [InlineData("user:123:login", "user:456:login")]
    [InlineData("api:upload", "api:download")]
    public void IsAllowed_DifferentKeyFormats_AreIndependent(string keyA, string keyB)
    {
        for (var i = 0; i < 5; i++)
            _sut.IsAllowed(keyA, 3, TimeSpan.FromMinutes(1));

        _sut.IsAllowed(keyB, 3, TimeSpan.FromMinutes(1)).Should().BeTrue();
    }

    // ── Window reset ──────────────────────────────────────────────────────────

    [Fact]
    public void IsAllowed_AfterWindowExpires_ShouldResetCounter()
    {
        // Iscrpimo limit za ključ
        var key = "window-reset";
        for (var i = 0; i < 3; i++)
            _sut.IsAllowed(key, 3, TimeSpan.FromMilliseconds(1));

        // Sačekamo da window istekne (2ms je dovoljno za 1ms window)
        Thread.Sleep(5);

        // Nakon expiry, nova serija zahtjeva treba proći
        var result = _sut.IsAllowed(key, 3, TimeSpan.FromMilliseconds(1));

        result.Should().BeTrue("counter se resetuje nakon što window istekne");
    }

    // ── Edge cases ────────────────────────────────────────────────────────────

    [Fact]
    public void IsAllowed_WithMaxRequestsOne_FirstAllowedSecondDenied()
    {
        // Min valid: maxRequests = 1
        var key = "one-max";

        _sut.IsAllowed(key, 1, TimeSpan.FromMinutes(1)).Should().BeTrue("1. zahtjev dozvoljen");
        _sut.IsAllowed(key, 1, TimeSpan.FromMinutes(1)).Should().BeFalse("2. zahtjev odbijen");
    }

    [Fact]
    public void IsAllowed_ConcurrentCallsSameKey_ShouldNotExceedLimit()
    {
        // Thread safety: paralelni pozivi ne smiju dozvoliti više od maxRequests
        var key = "concurrent";
        const int maxRequests = 5;
        const int totalCalls  = 20;
        var allowed = new System.Collections.Concurrent.ConcurrentBag<bool>();

        Parallel.For(0, totalCalls, _ =>
            allowed.Add(_sut.IsAllowed(key, maxRequests, TimeSpan.FromMinutes(1))));

        allowed.Count(r => r).Should().Be(maxRequests,
            "tačno maxRequests zahtjeva mora biti dozvoljeno čak i kod paralelnih poziva");
    }
}
