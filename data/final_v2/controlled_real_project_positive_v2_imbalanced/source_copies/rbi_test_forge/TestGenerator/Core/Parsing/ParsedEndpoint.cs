namespace RBBH.TestAutomation.Core.Parsing;

/// <summary>
/// Jedan HTTP endpoint izveden iz OpenAPI/Swagger spec-a — spreman da se mapira u
/// <c>TestScenario</c> (REST) i proslijedi generatoru testova.
/// </summary>
/// <param name="HttpMethod">HTTP metoda velikim slovima: GET, POST, PUT, DELETE, PATCH...</param>
/// <param name="Route">Ruta endpointa, npr. <c>/api/transactions/{id}</c>.</param>
/// <param name="Controller">Kontroler/tag grupa (Swashbuckle koristi ime kontrolera kao tag).</param>
/// <param name="OperationId">operationId iz spec-a (ako postoji).</param>
/// <param name="Summary">Kratki opis operacije (summary ili operationId).</param>
/// <param name="Parameters">Path/query/header parametri.</param>
/// <param name="RequestBodyJsonSample">Generisan primjer JSON tijela (null ako endpoint nema body).</param>
/// <param name="SuccessStatus">Prvi 2xx status iz responses (fallback 200) — happy-path očekivanje.</param>
/// <param name="ResponseStatuses">Svi deklarisani numerički status kodovi.</param>
/// <param name="AuthSchemes">Čitljivi nazivi sigurnosnih shema koje endpoint zahtijeva (npr. "JWT Bearer").</param>
public sealed record ParsedEndpoint(
    string HttpMethod,
    string Route,
    string Controller,
    string? OperationId,
    string? Summary,
    IReadOnlyList<ParsedParameter> Parameters,
    string? RequestBodyJsonSample,
    int SuccessStatus,
    IReadOnlyList<int> ResponseStatuses,
    IReadOnlyList<string> AuthSchemes)
{
    /// <summary>True ako endpoint zahtijeva autentikaciju (ima bar jednu sigurnosnu shemu).</summary>
    public bool RequiresAuth => AuthSchemes.Count > 0;
}
