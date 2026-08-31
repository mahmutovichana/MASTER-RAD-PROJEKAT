using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Application.Common.Interfaces;

namespace RBBH.CollateralAppraisal.Infrastructure.Storage;

/// <summary>
/// Skladišti fajlove na lokalnom disku ispod <see cref="FileStorageOptions.RootPath"/>.
/// Relativne putanje koje vraća/prima provider su uvijek relativne na korijenski direktorij
/// i koriste '/' kao separator (čuvaju se u <c>Document.StoragePath</c>).
///
/// Sigurnost: svaka putanja se rješava kroz <see cref="ResolveFullPath"/> koji garantuje
/// da rezultat ostaje unutar korijenskog direktorija (zaštita od path traversal-a).
/// </summary>
public sealed class LocalFileStorageProvider : IFileStorageProvider
{
    private readonly string _rootPath;
    private readonly long   _maxFileSizeBytes;

    public LocalFileStorageProvider(IOptions<FileStorageOptions> options, IHostEnvironment environment)
    {
        var configuredPath = options.Value.RootPath;
        _rootPath = Path.IsPathRooted(configuredPath)
            ? configuredPath
            : Path.Combine(environment.ContentRootPath, configuredPath);
        _maxFileSizeBytes = options.Value.MaxFileSizeBytes;

        Directory.CreateDirectory(_rootPath);
    }

    public async Task<FileStorageResult> SaveAsync(
        Stream content,
        string originalFileName,
        string subPath,
        CancellationToken ct = default)
    {
        if (_maxFileSizeBytes > 0 && content.CanSeek && content.Length > _maxFileSizeBytes)
            throw new InvalidOperationException(
                $"Fajl prelazi maksimalnu dozvoljenu veličinu od {_maxFileSizeBytes / (1024 * 1024)} MB.");

        var safeSubPath = SanitizeSubPath(subPath);

        var extension = Path.GetExtension(originalFileName);
        if (extension.Length is 0 or > 20)
            extension = string.Empty;

        var relativePath = $"{safeSubPath}/{Guid.NewGuid():N}{extension}";
        var fullPath     = ResolveFullPath(relativePath);

        Directory.CreateDirectory(Path.GetDirectoryName(fullPath)!);

        await using (var fileStream = new FileStream(fullPath, FileMode.CreateNew, FileAccess.Write))
        {
            await content.CopyToAsync(fileStream, ct);
        }

        return new FileStorageResult(relativePath, new FileInfo(fullPath).Length);
    }

    public Task<Stream> OpenReadAsync(string storagePath, CancellationToken ct = default)
    {
        var fullPath = ResolveFullPath(storagePath);
        if (!File.Exists(fullPath))
            throw new FileNotFoundException("Fajl nije pronađen u skladištu.", storagePath);

        return Task.FromResult<Stream>(new FileStream(fullPath, FileMode.Open, FileAccess.Read, FileShare.Read));
    }

    public Task DeleteAsync(string storagePath, CancellationToken ct = default)
    {
        var fullPath = ResolveFullPath(storagePath);
        if (File.Exists(fullPath))
            File.Delete(fullPath);

        return Task.CompletedTask;
    }

    public Task<bool> ExistsAsync(string storagePath, CancellationToken ct = default) =>
        Task.FromResult(File.Exists(ResolveFullPath(storagePath)));

    /// <summary>Odbacuje "." i ".." segmente i normalizuje separatore na '/'.</summary>
    private static string SanitizeSubPath(string subPath)
    {
        if (string.IsNullOrWhiteSpace(subPath))
            throw new ArgumentException("subPath ne smije biti prazan.", nameof(subPath));

        var segments = subPath.Split(['/', '\\'], StringSplitOptions.RemoveEmptyEntries);
        foreach (var segment in segments)
        {
            if (segment is "." or "..")
                throw new ArgumentException($"Nevažeći segment putanje: '{segment}'.", nameof(subPath));
        }

        return string.Join('/', segments);
    }

    /// <summary>Mapira relativnu putanju na fizičku lokaciju i osigurava da ostaje unutar korijena.</summary>
    private string ResolveFullPath(string relativePath)
    {
        var fullPath = Path.GetFullPath(Path.Combine(_rootPath, relativePath));

        var normalizedRoot = Path.GetFullPath(_rootPath);
        if (!normalizedRoot.EndsWith(Path.DirectorySeparatorChar))
            normalizedRoot += Path.DirectorySeparatorChar;

        if (!fullPath.StartsWith(normalizedRoot, StringComparison.Ordinal))
            throw new ArgumentException("Putanja izvan dozvoljenog skladišta.", nameof(relativePath));

        return fullPath;
    }
}
