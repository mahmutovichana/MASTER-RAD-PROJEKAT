namespace E2ETests.Fixtures;

/// <summary>
/// Razrješava apsolutnu putanju za test artifakte (screenshotovi, videi).
///
/// Test proces se pokreće iz bin/{Config}/net10.0, pa relativna putanja
/// "TestResults/artifacts" završi pored DLL-a — gdje je workflow ne uploaduje.
/// Ovaj helper hoda nagore do repo root-a i sidra artifakte u
/// TestGenerator/E2ETests/TestResults/artifacts, isti folder u koji ide i .trx i koji
/// e2e.yml uploaduje kao artifakt.
/// </summary>
internal static class ArtifactPaths
{
    public static string Root { get; } = ResolveRoot();

    public static string For(string testName) => Path.Combine(Root, testName);

    private static string ResolveRoot()
    {
        var dir = AppContext.BaseDirectory;
        while (dir is not null)
        {
            var e2eProj = Path.Combine(dir, "TestGenerator", "E2ETests");
            if (Directory.Exists(e2eProj))
                return Path.Combine(e2eProj, "TestResults", "artifacts");
            dir = Path.GetDirectoryName(dir);
        }
        // Fallback: relativno na working dir ako korijen projekta nije pronađen.
        return Path.Combine("TestResults", "artifacts");
    }
}
