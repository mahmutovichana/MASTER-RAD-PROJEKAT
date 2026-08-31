using Xunit;

namespace RBBH.CollateralAppraisal.E2E.Tests.Infrastructure;

/// <summary>
/// Serijska kolekcija — svi E2E testovi dijele jedan PlaywrightFixture.
/// Testovi se ne izvršavaju paralelno jer mijenjaju zajednički state (DB, Keycloak).
/// </summary>
[CollectionDefinition("E2E")]
public sealed class E2ECollectionDefinition : ICollectionFixture<PlaywrightFixture> { }
