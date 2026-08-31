namespace E2ETests.Fixtures;

[CollectionDefinition("E2E")]
public class E2ECollection : ICollectionFixture<AppFixture>, ICollectionFixture<PlaywrightFixture>;
