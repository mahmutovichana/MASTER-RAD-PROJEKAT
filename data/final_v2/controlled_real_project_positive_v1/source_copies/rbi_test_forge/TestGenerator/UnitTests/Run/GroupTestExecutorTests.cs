using RBBH.TestAutomation.Api.DTO;
using RBBH.TestAutomation.Api.Services;
using RBBH.TestAutomation.Api.Services.Run;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using NSubstitute;
using RBBH.TestAutomation.Core.Domain;
using RBBH.TestAutomation.Core.Infrastructure;
using RBBH.TestAutomation.Core.Repositories;

namespace UnitTests.Run;

public class GroupTestExecutorTests
{
    [Fact]
    public async Task ExecuteGroupAsync_StopsOnFirstFailure_WhenOptionIsEnabled()
    {
        var groupId = Guid.NewGuid();
        var first = Guid.NewGuid();
        var second = Guid.NewGuid();
        var executor = CreateExecutor(
            groupId,
            [first, second],
            id => Result(id, id == first ? ScenarioRunStatus.Failed : ScenarioRunStatus.Passed));

        var progress = await executor.ExecuteGroupAsync(groupId, new RunOptions(StopOnFirstFailure: true));

        Assert.Equal(1, progress.Completed);
        Assert.Equal(1, progress.Failed);
        Assert.Single(progress.Results);
    }

    [Fact]
    public async Task ExecuteGroupAsync_PersistsProgressAfterEachScenario()
    {
        var groupId = Guid.NewGuid();
        var ids = new[] { Guid.NewGuid(), Guid.NewGuid() };
        await using var db = CreateDb();
        db.Groups.Add(new TestGroup { Id = groupId, Naziv = "Smoke" });
        await db.SaveChangesAsync();

        var services = new ServiceCollection()
            .AddScoped<IRunRepository>(_ => new RunRepository(db))
            .BuildServiceProvider();

        var groupSvc = GroupService(groupId, ids);
        var scenarioSvc = ScenarioService(ids);
        var runner = Substitute.For<IScenarioRunner>();
        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(ci => Result(ci.Arg<ScenarioDto>().Id, ScenarioRunStatus.Passed));

        var executor = new GroupTestExecutor(
            groupSvc,
            scenarioSvc,
            runner,
            services,
            NullLogger<GroupTestExecutor>.Instance);

        var progressEvents = new List<GroupRunProgress>();
        executor.ProgressChanged += progressEvents.Add;

        var progress = await executor.ExecuteGroupAsync(groupId, new RunOptions());
        var run = await db.RunResults.SingleAsync();

        Assert.Equal(2, progress.Passed);
        Assert.Equal(3, progressEvents.Count);
        Assert.Equal(2, run.TotalCount);
        Assert.Equal(2, run.PassedCount);
        Assert.Equal(0, run.FailedCount);
        Assert.Contains("Request", run.DetailsJson);
        Assert.NotNull(run.CompletedAt);
    }

    [Fact]
    public async Task ExecuteGroupAsync_WhenParallel_HonorsMaxParallelThreads()
    {
        var groupId = Guid.NewGuid();
        var ids = Enumerable.Range(0, 5).Select(_ => Guid.NewGuid()).ToList();
        var scenarioSvc = ScenarioService(ids);
        var runner = Substitute.For<IScenarioRunner>();
        var running = 0;
        var maxRunning = 0;

        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(async ci =>
            {
                var current = Interlocked.Increment(ref running);
                maxRunning = Math.Max(maxRunning, current);
                await Task.Delay(50, ci.Arg<CancellationToken>());
                Interlocked.Decrement(ref running);
                return Result(ci.Arg<ScenarioDto>().Id, ScenarioRunStatus.Passed);
            });

        var executor = new GroupTestExecutor(
            GroupService(groupId, ids),
            scenarioSvc,
            runner,
            new ServiceCollection().BuildServiceProvider(),
            NullLogger<GroupTestExecutor>.Instance);

        var progress = await executor.ExecuteGroupAsync(
            groupId,
            new RunOptions(RunInParallel: true, MaxParallelThreads: 2));

        Assert.Equal(5, progress.Passed);
        Assert.True(maxRunning <= 2, $"Expected max concurrency <= 2, got {maxRunning}.");
        Assert.True(progress.ThroughputPerSecond > 0);
    }

    [Fact]
    public async Task ExecuteGroupAsync_WhenParallel_FlushesBatchBeforeSequentialScenario()
    {
        var groupId = Guid.NewGuid();
        var first = Guid.NewGuid();
        var sequential = Guid.NewGuid();
        var items = new[]
        {
            new ScenarioListItemDto(first, groupId, "Parallel first", "REST", 0),
            new ScenarioListItemDto(sequential, groupId, "Sequential dependency", "REST", 1)
            {
                RunSequentially = true,
            },
        };
        var scenarioSvc = ScenarioService(items.Select(i => i.Id).ToList());
        var runner = Substitute.For<IScenarioRunner>();
        var finishedFirst = false;
        var sequentialStartedAfterFirstFinished = false;

        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(async ci =>
            {
                var id = ci.Arg<ScenarioDto>().Id;
                if (id == first)
                {
                    await Task.Delay(50, ci.Arg<CancellationToken>());
                    finishedFirst = true;
                }
                else if (id == sequential)
                {
                    sequentialStartedAfterFirstFinished = finishedFirst;
                }

                return Result(id, ScenarioRunStatus.Passed);
            });

        var executor = new GroupTestExecutor(
            GroupService(groupId, items),
            scenarioSvc,
            runner,
            new ServiceCollection().BuildServiceProvider(),
            NullLogger<GroupTestExecutor>.Instance);

        await executor.ExecuteGroupAsync(groupId, new RunOptions(RunInParallel: true, MaxParallelThreads: 4));

        Assert.True(sequentialStartedAfterFirstFinished);
    }

    private static GroupTestExecutor CreateExecutor(
        Guid groupId,
        IReadOnlyList<Guid> scenarioIds,
        Func<Guid, ScenarioRunResult> resultFactory)
    {
        var groupSvc = GroupService(groupId, scenarioIds);
        var scenarioSvc = ScenarioService(scenarioIds);
        var runner = Substitute.For<IScenarioRunner>();
        runner.RunAsync(Arg.Any<ScenarioDto>(), Arg.Any<RunConfigDto>(), Arg.Any<CancellationToken>())
            .Returns(ci => resultFactory(ci.Arg<ScenarioDto>().Id));

        return new GroupTestExecutor(
            groupSvc,
            scenarioSvc,
            runner,
            new ServiceCollection().BuildServiceProvider(),
            NullLogger<GroupTestExecutor>.Instance);
    }

    private static IGroupService GroupService(Guid groupId, IReadOnlyList<Guid> scenarioIds)
    {
        return GroupService(
            groupId,
            scenarioIds.Select((id, index) => new ScenarioListItemDto(id, groupId, $"Scenario {index}", "REST", index)).ToList());
    }

    private static IGroupService GroupService(Guid groupId, IReadOnlyList<ScenarioListItemDto> items)
    {
        var groupSvc = Substitute.For<IGroupService>();
        groupSvc.GetScenariosAsync(groupId, Arg.Any<CancellationToken>())
            .Returns(items.ToList());
        return groupSvc;
    }

    private static IScenarioService ScenarioService(IReadOnlyList<Guid> scenarioIds)
    {
        var scenarioSvc = Substitute.For<IScenarioService>();
        scenarioSvc.GetRunConfigAsync(Arg.Any<CancellationToken>())
            .Returns(new RunConfigDto([]));

        foreach (var id in scenarioIds)
        {
            scenarioSvc.GetByIdAsync(id, Arg.Any<CancellationToken>())
                .Returns(new ScenarioDto(id, null, $"Scenario {id:N}", null, TipScenarija.Rest, null, null, null, null, DateTime.UtcNow, null, null));
        }

        return scenarioSvc;
    }

    private static ScenarioRunResult Result(Guid id, ScenarioRunStatus status) =>
        new(id, $"Scenario {id:N}", status, 200, 200, 10, status == ScenarioRunStatus.Failed ? "fail" : null, "Request", "Response");

    private static TestForgeDbContext CreateDb()
    {
        var options = new DbContextOptionsBuilder<TestForgeDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;

        return new TestForgeDbContext(options);
    }
}
