namespace RBBH.CollateralAppraisal.Api.Modules;

/// <summary>
/// Endpoint modul koji mapira vlastite minimal API rute.
///
/// Svaki feature (T2-T8) implementira ovaj interfejs uz svoje endpointe
/// (npr. <c>PropertyValuation/Endpoints/DocumentsEndpointModule.cs</c>).
/// <see cref="EndpointModuleExtensions.MapFeatureEndpoints"/> pronalazi sve
/// implementacije reflection-om i poziva <see cref="MapEndpoints"/> —
/// nije potrebno mijenjati centralni <c>WebApplicationExtensions.MapAllEndpoints</c>.
///
/// Implementacija mora imati public bezparametarski konstruktor.
/// Vidi docs/backend/feature-module-pattern.md.
/// </summary>
public interface IEndpointModule
{
    void MapEndpoints(IEndpointRouteBuilder app);
}
