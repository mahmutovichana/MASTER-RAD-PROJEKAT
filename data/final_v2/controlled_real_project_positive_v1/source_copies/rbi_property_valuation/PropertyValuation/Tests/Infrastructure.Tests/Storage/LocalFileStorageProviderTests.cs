using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using RBBH.CollateralAppraisal.Infrastructure.Storage;
using Xunit;

namespace RBBH.CollateralAppraisal.Infrastructure.Tests.Storage;

public sealed class LocalFileStorageProviderTests : IDisposable
{
    private readonly string _root;
    private readonly LocalFileStorageProvider _provider;

    public LocalFileStorageProviderTests()
    {
        _root = Directory.CreateTempSubdirectory("collateral-storage-tests-").FullName;
        _provider = new LocalFileStorageProvider(
            Options.Create(new FileStorageOptions { RootPath = _root }),
            new FakeHostEnvironment(_root));
    }

    public void Dispose() => Directory.Delete(_root, recursive: true);

    [Fact]
    public async Task SaveAsync_StoresFileUnderSubPathWithGeneratedName()
    {
        var content = new MemoryStream([1, 2, 3, 4, 5]);

        var result = await _provider.SaveAsync(content, "ugovor.pdf", "appraisal-orders/123");

        Assert.StartsWith("appraisal-orders/123/", result.StoragePath);
        Assert.EndsWith(".pdf", result.StoragePath);
        Assert.Equal(5, result.FileSize);
        Assert.True(File.Exists(Path.Combine(_root, result.StoragePath.Replace('/', Path.DirectorySeparatorChar))));
    }

    [Fact]
    public async Task SaveAsync_WithoutExtension_OmitsExtension()
    {
        var content = new MemoryStream([1]);

        var result = await _provider.SaveAsync(content, "bezekstenzije", "docs");

        Assert.DoesNotContain('.', Path.GetFileName(result.StoragePath));
    }

    [Theory]
    [InlineData("../escape")]
    [InlineData("docs/../../escape")]
    [InlineData("docs/..")]
    public async Task SaveAsync_WithPathTraversalSubPath_Throws(string subPath)
    {
        await Assert.ThrowsAsync<ArgumentException>(
            () => _provider.SaveAsync(new MemoryStream([1]), "f.pdf", subPath));
    }

    [Fact]
    public async Task SaveAsync_WithEmptySubPath_Throws()
    {
        await Assert.ThrowsAsync<ArgumentException>(
            () => _provider.SaveAsync(new MemoryStream([1]), "f.pdf", "  "));
    }

    [Fact]
    public async Task OpenReadAsync_ReturnsSavedContent()
    {
        byte[] original = [10, 20, 30, 40];
        var saved = await _provider.SaveAsync(new MemoryStream(original), "data.bin", "docs");

        await using var stream = await _provider.OpenReadAsync(saved.StoragePath);
        using var reader = new MemoryStream();
        await stream.CopyToAsync(reader);

        Assert.Equal(original, reader.ToArray());
    }

    [Fact]
    public async Task OpenReadAsync_WhenFileMissing_ThrowsFileNotFound()
    {
        await Assert.ThrowsAsync<FileNotFoundException>(
            () => _provider.OpenReadAsync("docs/nepostojeci.pdf"));
    }

    [Theory]
    [InlineData("../outside.txt")]
    [InlineData("docs/../../outside.txt")]
    public async Task OpenReadAsync_WithPathOutsideRoot_Throws(string storagePath)
    {
        await Assert.ThrowsAsync<ArgumentException>(() => _provider.OpenReadAsync(storagePath));
    }

    [Fact]
    public async Task ExistsAsync_ReflectsFilePresence()
    {
        var saved = await _provider.SaveAsync(new MemoryStream([1]), "f.pdf", "docs");

        Assert.True(await _provider.ExistsAsync(saved.StoragePath));
        Assert.False(await _provider.ExistsAsync("docs/nepostojeci.pdf"));
    }

    [Fact]
    public async Task DeleteAsync_RemovesFile_AndIsIdempotent()
    {
        var saved = await _provider.SaveAsync(new MemoryStream([1]), "f.pdf", "docs");

        await _provider.DeleteAsync(saved.StoragePath);
        Assert.False(await _provider.ExistsAsync(saved.StoragePath));

        // Brisanje nepostojećeg fajla ne smije baciti grešku.
        await _provider.DeleteAsync(saved.StoragePath);
    }

    private sealed class FakeHostEnvironment(string contentRootPath) : IHostEnvironment
    {
        public string ApplicationName { get; set; } = "RBBH.CollateralAppraisal.Infrastructure.Tests";
        public IFileProvider ContentRootFileProvider { get; set; } = new NullFileProvider();
        public string ContentRootPath { get; set; } = contentRootPath;
        public string EnvironmentName { get; set; } = "Test";
    }
}
