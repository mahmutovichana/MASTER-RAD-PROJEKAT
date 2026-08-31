using System.Data;
using Microsoft.EntityFrameworkCore;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;
using RBBH.CollateralAppraisal.Infrastructure.Persistence;

namespace RBBH.CollateralAppraisal.Infrastructure.Common;

/// <summary>Distribuirani SQL Server lock preko sp_getapplock/sp_releaseapplock.</summary>
public sealed class SqlServerJobLock(ApplicationDbContext db) : IDistributedJobLock
{
    public async Task<bool> TryAcquireAsync(long lockKey, CancellationToken ct = default)
    {
        var connection = db.Database.GetDbConnection();
        if (connection.State != ConnectionState.Open)
            await db.Database.OpenConnectionAsync(ct);

        await using var command = connection.CreateCommand();
        command.CommandText = "DECLARE @result int; EXEC @result = sp_getapplock @Resource, 'Exclusive', 'Session', 0; SELECT @result;";
        var parameter = command.CreateParameter();
        parameter.ParameterName = "@Resource";
        parameter.Value = $"rbi-job-{lockKey}";
        command.Parameters.Add(parameter);
        return Convert.ToInt32(await command.ExecuteScalarAsync(ct)) >= 0;
    }

    public async Task ReleaseAsync(long lockKey, CancellationToken ct = default)
    {
        var connection = db.Database.GetDbConnection();
        if (connection.State != ConnectionState.Open) return;
        await using var command = connection.CreateCommand();
        command.CommandText = "EXEC sp_releaseapplock @Resource, 'Session';";
        var parameter = command.CreateParameter();
        parameter.ParameterName = "@Resource";
        parameter.Value = $"rbi-job-{lockKey}";
        command.Parameters.Add(parameter);
        await command.ExecuteNonQueryAsync(ct);
    }
}
