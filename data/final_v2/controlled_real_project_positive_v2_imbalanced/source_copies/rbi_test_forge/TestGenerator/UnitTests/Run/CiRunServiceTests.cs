using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.Ci;
using RBBH.TestAutomation.Api.Services.Run;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using NSubstitute;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Repositories;
using Xunit;

namespace UnitTests.Run;

/// <summary>
/// Unit testovi za <see cref="CiRunService"/> — pokretanje grupa, agregacija statusa,
/// lista palih testova i validacija taga. Servisi su substituirani (NSubstitute),
/// a CiRunService dobija pravi <see cref="IServiceScopeFactory"/> iz mini-kontejnera.
/// </summary>
public class CiRunServiceTests
{
    private static ScenarioDto Scenario(Guid id, string naziv) =>
        new(id, Guid.NewGuid(), naziv, null, TipScenarija.Rest, null, null, null,
            null, DateTime.UtcNow, null, null);

    private static ScenarioRunResult Result(Guid id, string naziv, ScenarioRunStatus status) =>
        new(id, naziv, status, 200, 200, 5, status == ScenarioRunStatus.Failed ? "pao" : null, null, null);

    private static (CiRunService Ci, IGroupService Groups, IScenarioService Scenarios, IScenarioRunner Runner)
        Build()
    {
        var groups    = Substitute.For<IGroupService>();
        var scenarios = Substitute.For<IScenarioService>();
        var runner    = Substitute.For<IScenarioRunner>();

        scenarios.GetRunConfigAsync(Arg.Any<CancellationToken>())
            .Returns(new RunConfigDto([]));

        var services = new ServiceCollection();
        services.AddScoped(_ => groups);
        services.AddScoped(_ => scenarios);
        services.AddScoped(_ => runner);
        var provider = services.BuildServiceProvider();

        var ci = new CiRunService(
            provider.GetRequiredService<IServiceScopeFactory>(),
            NullLogger<CiRunService>.Instance);

        return (ci, groups, scenarios, runner);
    }

    [Fact]
    public async Task GrupaSaSvimProlazima_VracaPassed()
    {
        var (ci, groups, scenarios, runner) = Build();
        var groupId = Guid.NewGuid();
        var s1 = Guid.NewGuid();
        var s2 = Guid.NewGuid();

        groups.GetScenariosAsync(groupId, Arg.Any<CancellationToken>())
            .Returns(new List<ScenarioListItemDto>
            {
                new(s1, groupId, "Test 1", "Rest", 0),
                new(s2, groupId, "Test 2", "Rest", 1),
            });
        scenarios.GetByIdAsync(s1, Arg.Any<CancellationToken>()).Returns(Scenario(s1, "Test 1"));
        scenarios.GetByIdAsync(s2, Arg.Any<CancellationToken>()).Returns(Scenario(s2, "Test 2"));
        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(ci2 => Result(((ScenarioDto)ci2[0]).Id, ((ScenarioDto)ci2[0]).Naziv, ScenarioRunStatus.Passed));

        var jobId = ci.StartGroupRun(groupId);
        var snap = await ci.WaitForCompletionAsync(jobId, TimeSpan.FromSeconds(10));

        Assert.NotNull(snap);
        Assert.Equal(CiJobStatus.Passed, snap!.Status);
        Assert.Equal(2, snap.Total);
        Assert.Equal(2, snap.Completed);
        Assert.Equal(2, snap.Passed);
        Assert.Equal(0, snap.Failed);
        Assert.Equal(100, snap.PassRate);
        Assert.Empty(snap.FailedTests);
    }

    [Fact]
    public async Task GrupaSaPadom_VracaFailed_IListaPalih()
    {
        var (ci, groups, scenarios, runner) = Build();
        var groupId = Guid.NewGuid();
        var s1 = Guid.NewGuid();
        var s2 = Guid.NewGuid();

        groups.GetScenariosAsync(groupId, Arg.Any<CancellationToken>())
            .Returns(new List<ScenarioListItemDto>
            {
                new(s1, groupId, "Prolazi", "Rest", 0),
                new(s2, groupId, "Pada", "Rest", 1),
            });
        scenarios.GetByIdAsync(s1, Arg.Any<CancellationToken>()).Returns(Scenario(s1, "Prolazi"));
        scenarios.GetByIdAsync(s2, Arg.Any<CancellationToken>()).Returns(Scenario(s2, "Pada"));
        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(call =>
            {
                var dto = (ScenarioDto)call[0];
                var status = dto.Naziv == "Pada" ? ScenarioRunStatus.Failed : ScenarioRunStatus.Passed;
                return Result(dto.Id, dto.Naziv, status);
            });

        var jobId = ci.StartGroupRun(groupId);
        var snap = await ci.WaitForCompletionAsync(jobId, TimeSpan.FromSeconds(10));

        Assert.NotNull(snap);
        Assert.Equal(CiJobStatus.Failed, snap!.Status);
        Assert.Equal(1, snap.Passed);
        Assert.Equal(1, snap.Failed);
        Assert.Equal(50, snap.PassRate);
        Assert.Contains("Pada", snap.FailedTests);
    }

    [Fact]
    public async Task Snapshot_NosiPerTestRezultate_ZaIzvjestaje()
    {
        var (ci, groups, scenarios, runner) = Build();
        var groupId = Guid.NewGuid();
        var s1 = Guid.NewGuid();
        var s2 = Guid.NewGuid();

        groups.GetScenariosAsync(groupId, Arg.Any<CancellationToken>())
            .Returns(new List<ScenarioListItemDto>
            {
                new(s1, groupId, "Prolazi", "Rest", 0),
                new(s2, groupId, "Pada", "Rest", 1),
            });
        scenarios.GetByIdAsync(s1, Arg.Any<CancellationToken>()).Returns(Scenario(s1, "Prolazi"));
        scenarios.GetByIdAsync(s2, Arg.Any<CancellationToken>()).Returns(Scenario(s2, "Pada"));
        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(call =>
            {
                var dto = (ScenarioDto)call[0];
                var status = dto.Naziv == "Pada" ? ScenarioRunStatus.Failed : ScenarioRunStatus.Passed;
                return Result(dto.Id, dto.Naziv, status);
            });

        var jobId = ci.StartGroupRun(groupId);
        var snap = await ci.WaitForCompletionAsync(jobId, TimeSpan.FromSeconds(10));

        Assert.NotNull(snap);
        Assert.Equal(2, snap!.Results.Count);
        Assert.Contains(snap.Results, r => r.Name == "Prolazi" && r.Status == ScenarioRunStatus.Passed);
        Assert.Contains(snap.Results, r => r.Name == "Pada"
            && r.Status == ScenarioRunStatus.Failed && r.FailReason == "pao");
    }

    [Fact]
    public async Task CiRun_PersistiraRunResultSaDetailsJson()
    {
        var groups    = Substitute.For<IGroupService>();
        var scenarios = Substitute.For<IScenarioService>();
        var runner    = Substitute.For<IScenarioRunner>();
        var repo      = Substitute.For<IRunRepository>();

        scenarios.GetRunConfigAsync(Arg.Any<CancellationToken>()).Returns(new RunConfigDto([]));

        var groupId = Guid.NewGuid();
        var s1 = Guid.NewGuid();
        groups.GetScenariosAsync(groupId, Arg.Any<CancellationToken>())
            .Returns(new List<ScenarioListItemDto> { new(s1, groupId, "Health check", "Rest", 0) });
        scenarios.GetByIdAsync(s1, Arg.Any<CancellationToken>()).Returns(Scenario(s1, "Health check"));
        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(ci => Result(((ScenarioDto)ci[0]).Id, ((ScenarioDto)ci[0]).Naziv, ScenarioRunStatus.Passed));

        var services = new ServiceCollection();
        services.AddScoped(_ => groups);
        services.AddScoped(_ => scenarios);
        services.AddScoped(_ => runner);
        services.AddScoped(_ => repo);
        var provider = services.BuildServiceProvider();

        var ci = new CiRunService(
            provider.GetRequiredService<IServiceScopeFactory>(),
            NullLogger<CiRunService>.Instance);

        var jobId = ci.StartGroupRun(groupId);
        await ci.WaitForCompletionAsync(jobId, TimeSpan.FromSeconds(10));

        // Run se persistira s per-test DetailsJson (preživljava restart) i popunjenim brojačima.
        await repo.Received(1).AddAsync(
            Arg.Is<RunResult>(r =>
                r.DetailsJson != null &&
                r.DetailsJson.Contains("Health check") &&
                r.TotalCount == 1 &&
                r.PassedCount == 1),
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public void NevalidanTag_VracaNull()
    {
        var (ci, _, _, _) = Build();
        Assert.Null(ci.StartTagRun("NepostojeciTag"));
    }

    [Fact]
    public void ValidanTag_VracaJobId()
    {
        var (ci, groups, _, _) = Build();
        groups.GetGroupsTreeAsync(Arg.Any<CancellationToken>())
            .Returns(new List<GroupTreeNodeDto>());

        Assert.NotNull(ci.StartTagRun("smoke"));   // case-insensitive
    }

    [Fact]
    public void NepoznatJob_GetStatus_VracaNull()
    {
        var (ci, _, _, _) = Build();
        Assert.Null(ci.GetStatus(Guid.NewGuid()));
    }
}
